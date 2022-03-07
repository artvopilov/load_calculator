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

    _loadable_point_to_volumes: DefaultDict[Point, Set[VolumeParameters]]

    _id_to_min_point: Dict[int, Point]
    _id_to_shipment: Dict[int, Shipment]
    _shipment_id_order: List[int]

    def __init__(self, parameters: ContainerParameters, id_: int):
        Item.__init__(self, id_)
        VolumeItem.__init__(self, parameters)

        self._parameters = parameters

        self._loadable_point_to_volumes = defaultdict(set)
        self._loadable_point_to_volumes[Point(0, 0, 0)].add(parameters)

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
    def loadable_point_to_volumes(self) -> DefaultDict[Point, Set[VolumeParameters]]:
        return self._loadable_point_to_volumes

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
        point_volumes = self._loadable_point_to_volumes[point]
        for v in point_volumes:
            if v.length < shipment_params.length:
                return False
            if v.width < shipment_params.width:
                return False
            if v.height < shipment_params.height:
                return False
        if not self._weight_fits(shipment_params.weight):
            return False
        return True

    def _update_loadable_points(self, point: Point, shipment: Shipment) -> None:
        max_point = self._compute_max_point(point, shipment.parameters)

        # insert point above
        if shipment.can_stack:
            new_point = point.with_z(max_point.z + 1)
            new_point_volume = shipment.parameters.with_height(self.height - new_point.z)
            self._loadable_point_to_volumes[new_point].add(new_point_volume)

        points_for_update = self._select_points_for_update(point, max_point)
        inside_bottom_points, outside_bottom_points, border_top_points, out_border_top_points = points_for_update

        self._update_inside_points(max_point, inside_bottom_points)
        self._update_outside_points(point, max_point, outside_bottom_points)
        # TODO: update top points!!!

    def _select_points_for_update(self, point: Point, max_point: Point) -> Tuple:
        inside_bottom_points, outside_bottom_points = [], []
        border_top_points, out_border_top_points = [], []
        for p in self._loadable_point_to_volumes.keys():
            if p.z == point.z:
                if p.x > max_point.x or p.y > max_point.y:
                    continue
                if p.x >= point.x and p.y >= point.y:
                    inside_bottom_points.append(p)
                else:
                    outside_bottom_points.append(p)
            elif p.z == max_point.z:
                if p.x > max_point.x + 1 or p.y > max_point.y + 1:
                    continue
                if p.x == max_point.x + 1 or p.y == max_point.y + 1:
                    border_top_points.append(p)
                else:
                    out_border_top_points.append(p)
        return inside_bottom_points, outside_bottom_points, border_top_points, out_border_top_points

    def _update_inside_points(self, max_point: Point, points: List[Point]) -> None:
        for p in points:
            # remove inside point
            p_volumes = self._loadable_point_to_volumes.pop(p)
            # move out of borders
            new_p_x = p.with_x(max_point.x + 1)
            new_p_y = p.with_y(max_point.y + 1)
            for v in p_volumes:
                max_p = self._compute_max_point(p, v)
                # check if it is enough place
                left_length = max_p.x - max_point.x
                left_width = max_p.y - max_point.y
                if left_length > 0:
                    self._loadable_point_to_volumes[new_p_x].add(v.with_length(left_length))
                if left_width > 0:
                    self._loadable_point_to_volumes[new_p_y].add(v.with_width(left_width))

    def _update_outside_points(self, point: Point, max_point: Point, outside_points: List[Point]) -> None:
        for p in outside_points:
            # remove point
            p_volumes = self._loadable_point_to_volumes.pop(p)
            for v in p_volumes:
                max_p = self._compute_max_point(p, v)
                # leave the point if it cannot be updated
                if max_p.x < point.x or max_p.y < point.y:
                    self._loadable_point_to_volumes[p].add(v)
                    continue
                # length should be cropped
                p_x_diff = point.x - p.x
                if p_x_diff > 0:
                    self._loadable_point_to_volumes[p].add(v.with_length(p_x_diff))
                # when length is split by new shipment
                max_p_x_diff = max_p.x - max_point.x
                if max_p_x_diff > 0:
                    new_p_x = p.with_x(max_point.x + 1)
                    self._loadable_point_to_volumes[new_p_x].add(v.with_length(max_p_x_diff))
                # width should be cropped
                p_y_diff = point.y - p.y
                if p_y_diff > 0:
                    self._loadable_point_to_volumes[p].add(v.with_width(p_y_diff))
                # when width is split by new shipment
                max_p_y_diff = max_p.y - max_point.y
                if max_p_y_diff > 0:
                    new_p_y = p.with_y(max_point.y + 1)
                    self._loadable_point_to_volumes[new_p_y].add(v.with_width(max_p_y_diff))

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
