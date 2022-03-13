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
        if not self._volume_fits(point, shipment_params):
            return False
        if not self._weight_fits(shipment_params.weight):
            return False
        return True

    def _volume_fits(self, point: Point, shipment_params: ShipmentParameters) -> bool:
        max_points = self._loadable_point_to_max_points[point]
        for max_point in max_points:
            v = VolumeParameters.from_points(point, max_point)
            if v.length < shipment_params.length:
                continue
            if v.width < shipment_params.width:
                continue
            if v.height < shipment_params.height:
                continue
            return True
        return False

    def _weight_fits(self, weight: int) -> bool:
        total_weight = sum([shipment.weight for shipment in self._id_to_shipment.values()])
        total_weight += weight
        return total_weight <= self.lifting_capacity

    def _update_loadable_points(self, loading_p: Point, shipment: Shipment) -> None:
        loading_max_p = self._compute_max_point(loading_p, shipment.parameters)

        # insert point above
        if shipment.can_stack:
            new_point = loading_p.with_z(loading_max_p.z + 1)
            new_max_point = loading_max_p.with_z(self.height - 1)
            self._loadable_point_to_max_points[new_point].add(new_max_point)

        bottom_points, top_points = self._select_points_for_update(loading_p, loading_max_p)

        self._update_bottom_points(loading_p, loading_max_p, bottom_points)
        self._update_top_points(loading_p, loading_max_p, top_points)

    def _select_points_for_update(self, loading_p: Point, loading_max_p: Point) -> Tuple:
        bottom_points, top_points = [], []
        for p in self._loadable_point_to_max_points.keys():
            # bottom points which should be cropped
            if p.z == loading_p.z and p.x <= loading_max_p.x and p.y <= loading_max_p.y:
                bottom_points.append(p)
            # top points
            elif p.z == loading_max_p.z + 1 and p.x <= loading_max_p.x + 1 and p.y <= loading_max_p.y + 1:
                # should be used for extension or can be extended
                top_points.append(p)
        return bottom_points, top_points

    def _update_bottom_points(self, loading_p: Point, loading_max_p: Point, points: List[Point]) -> None:
        for p in points:
            # remove point and iterate max points
            for max_p in self._loadable_point_to_max_points.pop(p):
                # should not be cropped
                if max_p.x < loading_p.x or max_p.y < loading_p.y:
                    self._loadable_point_to_max_points[p].add(max_p)
                elif p.x >= loading_p.x and p.y >= loading_p.y:
                    self._update_inside_bottom_point(p, max_p, loading_max_p)
                else:
                    self._update_outside_bottom_point(p, max_p, loading_p, loading_max_p)

    def _update_inside_bottom_point(self, p: Point, max_p: Point, loading_max_p: Point) -> None:
        # move point out of borders along x
        if max_p.x > loading_max_p.x:
            new_p_x = p.with_x(loading_max_p.x + 1)
            self._loadable_point_to_max_points[new_p_x].add(max_p)
        # move point out of borders along y
        if max_p.y > loading_max_p.y:
            new_p_y = p.with_y(loading_max_p.y + 1)
            self._loadable_point_to_max_points[new_p_y].add(max_p)

    def _update_outside_bottom_point(self, p: Point, max_p: Point, loading_p: Point, loading_max_p: Point) -> None:
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

    def _update_top_points(self, loading_p: Point, loading_max_p: Point, points: List[Point]) -> None:
        extension_points = defaultdict(set)
        extension_points[loading_p.with_z(loading_max_p.z + 1)].add(loading_max_p.with_z(self.height - 1))

        # extend width up
        cur_extension_points = defaultdict(set)
        points_for_delete = defaultdict(set)
        for p in points:
            for max_p in self._loadable_point_to_max_points[p]:
                # try to use points for extension
                for extension_p in extension_points.keys():
                    for extension_max_p in extension_points[extension_p]:
                        if max_p.x >= extension_p.x and p.x <= extension_max_p.x and max_p.y + 1 == extension_p.y:
                            new_p = p.with_x(max(p.x, extension_p.x))
                            new_max_p = extension_max_p.with_x(min(max_p.x, extension_max_p.x))
                            cur_extension_points[new_p].add(new_max_p)
                            if p.x >= extension_p.x and max_p.x <= extension_max_p.x:
                                points_for_delete[p].add(max_p)

        for cur_extension_p, cur_extension_max_points in cur_extension_points.items():
            extension_points[cur_extension_p] |= cur_extension_max_points
        for point_for_delete, max_points_for_delete in points_for_delete.items():
            self._loadable_point_to_max_points[point_for_delete] -= max_points_for_delete

        # extend length up
        cur_extension_points.clear()
        points_for_delete.clear()
        for p in points:
            for max_p in self._loadable_point_to_max_points[p]:
                # try to use points for extension
                for extension_p in extension_points.keys():
                    for extension_max_p in extension_points[extension_p]:
                        if max_p.y >= extension_p.y and p.y <= extension_max_p.y and max_p.x + 1 == extension_p.x:
                            new_p = p.with_y(max(p.y, extension_p.y))
                            new_max_p = max_p.with_x(extension_max_p.x).with_y(min(max_p.y, extension_max_p.y))
                            cur_extension_points[new_p].add(new_max_p)
                            if p.y >= extension_p.y and max_p.y <= extension_max_p.y:
                                points_for_delete[p].add(max_p)

        for cur_extension_p, cur_extension_max_points in cur_extension_points.items():
            extension_points[cur_extension_p] |= cur_extension_max_points
        for point_for_delete, max_points_for_delete in points_for_delete.items():
            self._loadable_point_to_max_points[point_for_delete] -= max_points_for_delete

        # extend width down
        cur_extension_points.clear()
        points_for_delete.clear()
        for p in points:
            for max_p in self._loadable_point_to_max_points[p]:
                # try to use points for extension
                for extension_p in extension_points.keys():
                    for extension_max_p in extension_points[extension_p]:
                        if max_p.x >= extension_p.x and p.x <= extension_max_p.x and p.y == extension_max_p.y + 1:
                            new_p = extension_p.with_x(max(p.x, extension_p.x))
                            new_max_p = max_p.with_x(min(max_p.x, extension_max_p.x))
                            cur_extension_points[new_p].add(new_max_p)
                            if p.x >= extension_p.x and max_p.x <= extension_max_p.x:
                                points_for_delete[p].add(max_p)

        for cur_extension_p, cur_extension_max_points in cur_extension_points.items():
            extension_points[cur_extension_p] |= cur_extension_max_points
        for point_for_delete, max_points_for_delete in points_for_delete.items():
            self._loadable_point_to_max_points[point_for_delete] -= max_points_for_delete

        # extend length down
        cur_extension_points.clear()
        points_for_delete.clear()
        for p in points:
            for max_p in self._loadable_point_to_max_points[p]:
                # try to use points for extension
                for extension_p in extension_points.keys():
                    for extension_max_p in extension_points[extension_p]:
                        if max_p.y >= extension_p.y and p.y <= extension_max_p.y and p.x == extension_max_p.x + 1:
                            new_p = extension_p.with_x(max(p.x, extension_p.x))
                            new_max_p = max_p.with_x(min(max_p.x, extension_max_p.x))
                            cur_extension_points[new_p].add(new_max_p)
                            if p.y >= extension_p.y and max_p.y <= extension_max_p.y:
                                points_for_delete[p].add(max_p)

        for cur_extension_p, cur_extension_max_points in cur_extension_points.items():
            extension_points[cur_extension_p] |= cur_extension_max_points
        for point_for_delete, max_points_for_delete in points_for_delete.items():
            self._loadable_point_to_max_points[point_for_delete] -= max_points_for_delete

        for extension_p, extension_max_points in extension_points.items():
            self._loadable_point_to_max_points[extension_p] |= extension_max_points


    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.length - 1,
            point.y + volume_parameters.width - 1,
            point.z + volume_parameters.height - 1)
