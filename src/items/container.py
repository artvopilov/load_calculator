from typing import Dict, Tuple, List, Optional, Set

import numpy as np

from src.items.shipment import Shipment
from src.items.util_items.volume_item import VolumeItem
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(VolumeItem):
    _id_: int
    _parameters: ContainerParameters

    _top_shipment_ids: np.array

    _id_to_min_point: Dict[int, Point]
    _id_to_shipment: Dict[int, Shipment]
    _shipment_id_order: List[int]

    def __init__(self, parameters: ContainerParameters, id_: int):
        self._id_ = id_
        self._parameters = parameters

        self._top_shipment_ids = np.zeros((parameters.length, parameters.width), dtype=np.int32)

        self._id_to_shipment = {}
        self._id_to_min_point = {}
        self._shipment_id_order = []

    @property
    def id(self) -> int:
        return self._id_

    @property
    def length(self) -> int:
        return self._parameters.length

    @property
    def width(self) -> int:
        return self._parameters.width

    @property
    def height(self) -> int:
        return self._parameters.height

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    @property
    def parameters(self) -> ContainerParameters:
        return self._parameters

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
        max_point = self._compute_max_point(point, shipment.parameters)
        self._load_into_space(point, max_point, shipment.id)
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

    def can_load_into_point(self, shipment_params: ShipmentParameters, point: Point):
        max_point = self._compute_max_point(point, shipment_params)
        if not self._volume_fits(point, max_point):
            return False
        if not self._surface_fits(point, max_point):
            return False
        if not self._weight_fits(shipment_params.weight):
            return False
        return True

    def compute_top_point(self, x: int, y: int) -> Point:
        shipment_id = self._top_shipment_ids[x, y]
        height = self._get_height(shipment_id)
        return Point(x, y, height)

    def unload(self) -> None:
        self._top_shipment_ids.fill(0)
        self._id_to_min_point = {}
        self._id_to_shipment = {}
        self._shipment_id_order = []

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.length - 1,
            point.y + volume_parameters.width - 1,
            point.z + volume_parameters.height - 1)

    def _load_into_space(self, point: Point, max_point: Point, id_: int) -> None:
        self._top_shipment_ids[point.x:max_point.x + 1, point.y:max_point.y + 1] = id_
        self._id_to_min_point[id_] = point

    def _volume_fits(self, point: Point, max_point: Point) -> bool:
        if not (self._is_inside_container(point) and self._is_inside_container(max_point)):
            return False
        return self._is_sub_space_empty(point, max_point)

    def _is_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._parameters.length \
               and 0 <= point.y < self._parameters.width \
               and 0 <= point.z < self._parameters.height

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        area_heights = self._get_area_heights(min_point, max_point)
        return np.all(np.array(list(area_heights)) <= min_point.z)

    def _surface_fits(self, point: Point, max_point: Point) -> bool:
        if point.z == 0:
            return True
        area_heights = self._get_area_heights(point, max_point)
        if not np.all(np.array(list(area_heights)) == point.z):
            return False
        area_top_shipments = self._get_area_top_shipments(point, max_point)
        return np.all([s.can_stack for s in area_top_shipments])

    def _get_area_heights(self, point: Point, max_point: Point) -> Set[int]:
        shipment_ids = np.unique(self._top_shipment_ids[point.x:max_point.x + 1, point.y:max_point.y + 1])
        shipment_heights = set([self._get_height(id_) for id_ in shipment_ids])
        return shipment_heights

    def _get_height(self, id_: int) -> int:
        if id_ not in self._id_to_shipment:
            return 0
        shipment = self._id_to_shipment[id_]
        return self._id_to_min_point[shipment.id].z + shipment.height

    def _get_area_top_shipments(self, point: Point, max_point: Point) -> List[Shipment]:
        shipment_ids = np.unique(self._top_shipment_ids[point.x:max_point.x + 1, point.y:max_point.y + 1])
        shipments = []
        for id_ in shipment_ids:
            if id_ in self._id_to_shipment:
                shipments.append(self._id_to_shipment[id_])
        return shipments

    def _weight_fits(self, weight: int):
        total_weight = sum([shipment.weight for shipment in self._id_to_shipment.values()])
        total_weight += weight
        return total_weight <= self.lifting_capacity
