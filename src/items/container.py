from collections import defaultdict
from typing import Dict, Tuple, List, Optional, Set, DefaultDict

from src.items.shipment import Shipment
from src.items.util_items.item import Item
from src.items.util_items.volume_item import VolumeItem
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(Item[ContainerParameters], VolumeItem):
    _parameters: ContainerParameters

    _loadable_point_to_max_points: DefaultDict[Point, Set[Point]]

    _id_to_min_point: Dict[int, Point]
    _id_to_shipment: Dict[int, Shipment]
    _shipment_id_order: List[int]

    def __init__(self, parameters: ContainerParameters, id_: int):
        Item.__init__(self, id_)
        VolumeItem.__init__(self, parameters)

        self._parameters = parameters

        loadable_point = Point(0, 0, 0)
        loadable_max_point = Point(parameters.length - 1, parameters.width - 1, parameters.height - 1)
        self._loadable_point_to_max_points = defaultdict(set)
        self._loadable_point_to_max_points[loadable_point].add(loadable_max_point)

        self._id_to_shipment = {}
        self._id_to_min_point = {}
        self._shipment_id_order = []

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    @property
    def parameters(self) -> ContainerParameters:
        return self._parameters

    @property
    def loadable_point_to_max_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._loadable_point_to_max_points

    @property
    def id_to_min_point(self) -> Dict[int, Point]:
        return self._id_to_min_point

    @property
    def id_to_shipment(self) -> Dict[int, Shipment]:
        return self._id_to_shipment

    @property
    def shipment_id_order(self) -> List[int]:
        return self._shipment_id_order

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.lifting_capacity

    def __str__(self) -> str:
        return f'Container: (' \
               f'id={self.id}; ' \
               f'length={self.length}; ' \
               f'width={self.width}; ' \
               f'height={self.height}; ' \
               f'lifting_capacity={self.length}' \
               f')'

    def load(self, point: Point, shipment: Shipment) -> None:
        self._update_loadable_points(point, shipment)
        self._id_to_min_point[shipment.id] = point
        self._id_to_shipment[shipment.id] = shipment
        self._shipment_id_order.append(shipment.id)

    def get_last_loaded_shipment(self) -> Optional[Shipment]:
        if not self._shipment_id_order:
            return None
        last_shipment_id = self._shipment_id_order[-1]
        return self._id_to_shipment[last_shipment_id]

    def get_point_above_shipment(self, shipment: Shipment) -> Point:
        shipment_point = self._id_to_min_point[shipment.id]
        return shipment_point.with_z(shipment_point.z + shipment.height)

    def can_load_into_point(self, point: Point, shipment_params: ShipmentParameters) -> bool:
        max_points = self._loadable_point_to_max_points[point]
        for max_point in max_points:
            v = VolumeParameters.from_points(point, max_point)
            if v.length < shipment_params.length:
                return False
            if v.width < shipment_params.width:
                return False
            if v.height < shipment_params.height:
                return False
        if not self._weight_fits(shipment_params.weight):
            return False
        return True

    def _update_loadable_points(self, loading_p: Point, shipment: Shipment) -> None:
        loading_max_p = self._compute_max_point(loading_p, shipment.parameters)

        # insert point above
        if shipment.can_stack:
            new_point = loading_p.with_z(loading_max_p.z + 1)
            new_point_volume = shipment.parameters.with_height(self.height - new_point.z)
            new_max_point = self._compute_max_point(new_point, new_point_volume)
            self._loadable_point_to_max_points[new_point].add(new_max_point)

        points_for_update = self._select_points_for_update(loading_p, loading_max_p)
        inside_bottom_points, outside_bottom_points, border_top_points, out_border_top_points = points_for_update

        self._update_inside_points(loading_max_p, inside_bottom_points)
        self._update_outside_points(loading_p, loading_max_p, outside_bottom_points)
        # TODO: update top points!!!

    def _select_points_for_update(self, loading_p: Point, loading_max_p: Point) -> Tuple:
        inside_bottom_points, outside_bottom_points = [], []
        border_top_points, out_border_top_points = [], []
        for p in self._loadable_point_to_max_points.keys():
            # bottom points which should be cropped
            if p.z == loading_p.z and p.x <= loading_max_p.x and p.y <= loading_max_p.y:
                # should be moved out and cropped if possible
                if p.x >= loading_p.x and p.y >= loading_p.y:
                    inside_bottom_points.append(p)
                # should be cropped
                else:
                    outside_bottom_points.append(p)
            # top points
            elif p.z == loading_max_p.z + 1:
                # can not be used for extension
                if p.x > loading_max_p.x + 1 or p.y > loading_max_p.y + 1:
                    continue
                # should be used for extension
                if p.x == loading_max_p.x + 1 or p.y == loading_max_p.y + 1:
                    border_top_points.append(p)
                # should be extended
                else:
                    out_border_top_points.append(p)
        return inside_bottom_points, outside_bottom_points, border_top_points, out_border_top_points

    def _update_inside_points(self, loading_max_p: Point, points: List[Point]) -> None:
        for p in points:
            # move point out of borders
            new_p_x = p.with_x(loading_max_p.x + 1)
            new_p_y = p.with_y(loading_max_p.y + 1)
            # remove point and iterate max points
            for max_p in self._loadable_point_to_max_points.pop(p):
                if max_p.x > loading_max_p.x:
                    self._loadable_point_to_max_points[new_p_x].add(max_p)
                if max_p.y > loading_max_p.y:
                    self._loadable_point_to_max_points[new_p_y].add(max_p)

    def _update_outside_points(self, loading_p: Point, loading_max_p: Point, points: List[Point]) -> None:
        for p in points:
            # remove point and iterate max points
            for max_p in self._loadable_point_to_max_points.pop(p):
                # should not be cropped
                if max_p.x < loading_p.x or max_p.y < loading_p.y:
                    self._loadable_point_to_max_points[p].add(max_p)
                    continue
                # length should be cropped
                if loading_p.x > p.x:
                    self._loadable_point_to_max_points[p].add(max_p.with_x(loading_p.x - 1))
                # when length is split by new shipment
                if max_p.x > loading_max_p.x:
                    new_p_x = p.with_x(loading_max_p.x + 1)
                    self._loadable_point_to_max_points[new_p_x].add(max_p)
                # width should be cropped
                if loading_p.y > p.y:
                    self._loadable_point_to_max_points[p].add(max_p.with_y(loading_p.y - 1))
                # when width is split by new shipment
                if max_p.y > loading_max_p.y:
                    new_p_y = p.with_y(loading_max_p.y + 1)
                    self._loadable_point_to_max_points[new_p_y].add(max_p)

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.length - 1,
            point.y + volume_parameters.width - 1,
            point.z + volume_parameters.height - 1)

    def _weight_fits(self, weight: int):
        total_weight = sum([shipment.weight for shipment in self._id_to_shipment.values()])
        total_weight += weight
        return total_weight <= self.lifting_capacity
