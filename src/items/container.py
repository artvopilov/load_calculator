from collections import defaultdict
from typing import Dict, Tuple, List, Set, DefaultDict, Callable

from src.items.shipment import Shipment
from src.items.util_items.item import Item
from src.items.util_items.name_item import NameItem
from src.items.util_items.volume_item import VolumeItem
from src.loading.coordinate import Coordinate
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.loading.point import Point
from src.statistics.container_statistics import ContainerStatistics


class Container(Item[ContainerParameters], VolumeItem, NameItem):
    _parameters: ContainerParameters
    _loadable_point_to_max_points: DefaultDict[Point, Set[Point]]
    _id_to_min_point_shifted: Dict[int, Point]
    _min_point_to_id: Dict[Point, int]
    _id_to_shipment: Dict[int, Shipment]
    _loading_order: List[int]
    _container_statistics: ContainerStatistics

    def __init__(self, parameters: ContainerParameters, id_: int):
        Item.__init__(self, id_)
        VolumeItem.__init__(self, parameters)
        NameItem.__init__(self, parameters)
        self._parameters = parameters
        self._loadable_point_to_max_points = defaultdict(set)
        self._id_to_min_point_shifted = {}
        self._min_point_to_id = {}
        self._id_to_shipment = {}
        self._loading_order = []
        self._container_statistics = ContainerStatistics()
        self._insert_first_loadable_point()

    @property
    def parameters(self) -> ContainerParameters:
        return self._parameters

    @property
    def loadable_point_to_max_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._loadable_point_to_max_points

    @property
    def id_to_min_point_shifted(self) -> Dict[int, Point]:
        return self._id_to_min_point_shifted

    @property
    def min_point_to_id(self) -> Dict[Point, int]:
        return self._min_point_to_id

    @property
    def id_to_shipment(self) -> Dict[int, Shipment]:
        return self._id_to_shipment

    @property
    def loading_order(self) -> List[int]:
        return self._loading_order

    def _key(self) -> Tuple:
        return self.id, self._parameters.length, self._parameters.width, \
               self._parameters.height, self._parameters.lifting_capacity

    def __str__(self) -> str:
        return f'Container: (' \
               f'id={self.id}; ' \
               f'name={self.name}; ' \
               f'length={self.length}; ' \
               f'width={self.width}; ' \
               f'height={self.height}; ' \
               f'lifting_capacity={self.length}' \
               f')'

    def load(self, point: Point, shipment: Shipment) -> None:
        self._update_loadable_points(point, shipment)

        x = int(point.x + shipment.parameters.get_length_diff() / 2)
        y = int(point.y + shipment.parameters.get_width_diff() / 2)
        self._id_to_min_point_shifted[shipment.id] = Point(x, y, point.z)

        self._min_point_to_id[point] = shipment.id
        self._id_to_shipment[shipment.id] = shipment
        self._loading_order.append(shipment.id)
        self._container_statistics.update(point, shipment.parameters)

    def unload(self) -> None:
        self._loadable_point_to_max_points = defaultdict(set)
        self._id_to_min_point_shifted = {}
        self._min_point_to_id = {}
        self._id_to_shipment = {}
        self._loading_order = []
        self._container_statistics = ContainerStatistics()
        self._insert_first_loadable_point()

    def can_load_into_point(self, point: Point, shipment_params: ShipmentParameters) -> bool:
        if not self._volume_fits(point, shipment_params):
            return False
        if not self._weight_fits(shipment_params.weight):
            return False
        return True

    def get_loaded_volume(self) -> float:
        return self._container_statistics.loaded_volume

    def build_response(self) -> Dict:
        response = self.parameters.build_response()
        volume = self.parameters.compute_volume()
        response['loaded_volume_share'] = self._container_statistics.loaded_volume / volume
        response['ldm'] = self._container_statistics.ldm
        return response

    def _insert_first_loadable_point(self) -> None:
        loadable_point = Point(0, 0, 0)
        loadable_max_point = Point(self._parameters.length - 1, self._parameters.width - 1, self._parameters.height - 1)
        self._loadable_point_to_max_points[loadable_point].add(loadable_max_point)

    def _volume_fits(self, point: Point, shipment_params: ShipmentParameters) -> bool:
        max_points = self._loadable_point_to_max_points[point]
        for max_point in max_points:
            v = VolumeParameters.from_points(point, max_point)
            if v.length < shipment_params.get_loading_length():
                continue
            if v.width < shipment_params.get_loading_width():
                continue
            if v.height < shipment_params.height:
                continue
            return True
        return False

    def _weight_fits(self, weight: int) -> bool:
        total_weight = sum([shipment.weight for shipment in self._id_to_shipment.values()])
        total_weight += weight
        return total_weight <= self._parameters.lifting_capacity

    def _update_loadable_points(self, loading_p: Point, shipment: Shipment) -> None:
        if loading_p.x == 8332:
            print('Loadind p 8332')
        loading_max_p = self._compute_max_point(loading_p, shipment.parameters)
        bottom_points, top_points = self._select_points_for_update(loading_p, loading_max_p)
        self._update_bottom_points(loading_p, loading_max_p, bottom_points)
        if shipment.can_stack:
            self._update_top_points(loading_p, loading_max_p, top_points)

    def _select_points_for_update(self, loading_p: Point, loading_max_p: Point) -> Tuple:
        bottom_points, top_points = [], []
        for p in self._loadable_point_to_max_points.keys():
            # bottom points which should be cropped or moved outside
            if p.z == loading_p.z and p.x <= loading_max_p.x and p.y <= loading_max_p.y:
                bottom_points.append(p)
            # top points which should be used for extension or can be extended
            elif p.z == loading_max_p.z + 1 and p.x <= loading_max_p.x + 1 and p.y <= loading_max_p.y + 1:
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
        # insert point above
        new_point = loading_p.with_z(loading_max_p.z + 1)
        new_max_point = loading_max_p.with_z(self.height - 1)
        # self._loadable_point_to_max_points[new_point].add(new_max_point)

        extension_points = defaultdict(set)
        extension_points[new_point].add(new_max_point)

        self._extend(points, extension_points, Coordinate.X, Coordinate.Y, self._point_is_extendable_up)

        self._extend(points, extension_points, Coordinate.Y, Coordinate.X, self._point_is_extendable_up)

        self._extend(points, extension_points, Coordinate.X, Coordinate.Y, self._point_is_extendable_down)

        self._extend(points, extension_points, Coordinate.Y, Coordinate.X, self._point_is_extendable_down)

        for extension_p, extension_max_points in extension_points.items():
            self._loadable_point_to_max_points[extension_p] |= extension_max_points

    def _extend(
            self,
            points: List[Point],
            extension_points: DefaultDict[Point, Set[Point]],
            c_clip: Coordinate,
            c_extension: Coordinate,
            point_is_extendable: Callable[[Point, Point, Coordinate], bool]
    ) -> None:
        cur_extension_points = defaultdict(set)
        cur_points_for_delete = defaultdict(set)
        for p in points:
            for max_p in self._loadable_point_to_max_points[p]:
                # try to use points for extension
                for extension_p in extension_points.keys():
                    for extension_max_p in extension_points[extension_p]:
                        if self._point_is_clipped(p, max_p, extension_p, extension_max_p, c_clip) \
                                and point_is_extendable(max_p, extension_p, c_extension):
                            new_p = p.with_coordinate(
                                max(p.get_coordinate(c_clip), extension_p.get_coordinate(c_clip)), c_clip)
                            new_max_p = extension_max_p.with_coordinate(
                                min(max_p.get_coordinate(c_clip), extension_max_p.get_coordinate(c_clip)), c_clip)
                            cur_extension_points[new_p].add(new_max_p)
                            if p.get_coordinate(c_clip) >= extension_p.get_coordinate(c_clip) \
                                    and max_p.get_coordinate(c_clip) <= extension_max_p.get_coordinate(c_clip):
                                cur_points_for_delete[p].add(max_p)
                            if extension_p.get_coordinate(c_clip) >= p.get_coordinate(c_clip) \
                                    and extension_max_p.get_coordinate(c_clip) <= max_p.get_coordinate(c_clip):
                                cur_points_for_delete[extension_p].add(extension_max_p)
        self._process_cur_extension_points(extension_points, cur_extension_points, cur_points_for_delete)

    def _process_cur_extension_points(
            self,
            extension_points: DefaultDict[Point, Set[Point]],
            cur_extension_points: DefaultDict[Point, Set[Point]],
            cur_points_for_delete: DefaultDict[Point, Set[Point]]
    ) -> None:
        for cur_extension_p, cur_extension_max_points in cur_extension_points.items():
            extension_points[cur_extension_p] |= cur_extension_max_points
        for point_for_delete, max_points_for_delete in cur_points_for_delete.items():
            self._loadable_point_to_max_points[point_for_delete] -= max_points_for_delete
            extension_points[point_for_delete] -= max_points_for_delete

    @staticmethod
    def _point_is_clipped(
            p: Point,
            max_p: Point,
            extension_p: Point,
            extension_max_p: Point,
            c: Coordinate
    ) -> bool:
        return max_p.get_coordinate(c) >= extension_p.get_coordinate(c) \
               and p.get_coordinate(c) <= extension_max_p.get_coordinate(c)

    @staticmethod
    def _point_is_extendable_up(max_p: Point, extension_p: Point, c_extension: Coordinate) -> bool:
        return max_p.get_coordinate(c_extension) + 1 == extension_p.get_coordinate(c_extension)

    @staticmethod
    def _point_is_extendable_down(p: Point, extension_max_p: Point, c_extension: Coordinate) -> bool:
        return p.get_coordinate(c_extension) == extension_max_p.get_coordinate(c_extension) + 1

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.get_loading_length() - 1,
            point.y + volume_parameters.get_loading_width() - 1,
            point.z + volume_parameters.height - 1)
