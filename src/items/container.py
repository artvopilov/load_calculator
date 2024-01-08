from typing import Dict, Tuple, List

from src.items.shipment import Shipment
from src.items.util_items.item import Item
from src.items.util_items.name_item import NameItem
from src.items.util_items.volume_item import VolumeItem
from src.loading.point.point import Point
from src.loading.point.places_manager import PlacesManager
from src.loading.point.points_update_info_resolver import PointsUpdateInfoResolver
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.statistics.container_statistics import ContainerStatistics


class Container(Item[ContainerParameters], VolumeItem, NameItem):
    _parameters: ContainerParameters
    _points_manager: PlacesManager
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
        self._points_manager = PlacesManager(parameters, PointsUpdateInfoResolver())
        self._id_to_min_point_shifted = {}
        self._min_point_to_id = {}
        self._id_to_shipment = {}
        self._loading_order = []
        self._container_statistics = ContainerStatistics()

    @property
    def parameters(self) -> ContainerParameters:
        return self._parameters

    @property
    def loadable_points(self) -> List[Point]:
        return self._points_manager.get_opening_points()

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

    @property
    def container_statistics(self) -> ContainerStatistics:
        return self._container_statistics

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
               f'lifting_capacity={self.parameters.lifting_capacity}' \
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
        self._points_manager.reset()
        self._id_to_min_point_shifted = {}
        self._min_point_to_id = {}
        self._id_to_shipment = {}
        self._loading_order = []
        self._container_statistics.reset()

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

    def _volume_fits(self, point: Point, shipment_params: ShipmentParameters) -> bool:
        max_points = self._points_manager.get_closing_points(point)
        for max_point in max_points:
            v = VolumeParameters.from_points(point, max_point)
            # if max_point == Point(5894, 1203, 2392) or point == Point(2561, 1203, 0):
            # if point == Point(2561, 1203, 0):
            #     logger.debug(f'Loading point: {point}')
            #     logger.debug(f'Available max point: {max_point}')
            #     logger.debug(f'Available volume: {v}')
            #     for p in self.min_point_to_id.keys():
            #         if p.y == 1204:
            #             logger.debug(f'Loaded points with 1204 y: {p}')
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
        loading_max_p = self._compute_max_point(loading_p, shipment.parameters)
        self._points_manager.update(loading_p, loading_max_p, shipment.can_stack)

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.get_loading_length() - 1,
            point.y + volume_parameters.get_loading_width() - 1,
            point.z + volume_parameters.height - 1)
