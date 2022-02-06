from typing import Dict, Tuple, List

import numpy as np

from src.items.lifting_item import LiftingItem
from src.items.shipment import Shipment
from src.items.volume_item import VolumeItem
from src.iterators.corner_ground_free_space_iterator import CornerGroundFreeSpaceIterator
from src.iterators.space_iterator import SpaceIterator
from src.parameters.container_parameters import ContainerParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(VolumeItem, LiftingItem):
    _id_: int
    _parameters: ContainerParameters

    _space: np.array

    _id_to_min_point: Dict[int, Point]
    _id_to_shipment: Dict[int, Shipment]
    _shipment_id_order: List[int]

    def __init__(self, parameters: ContainerParameters, id_: int):
        self._id_ = id_
        self._parameters = parameters

        self._space = np.zeros((parameters.length, parameters.width, parameters.height), dtype=np.int32)

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
    def id_to_min_point(self):
        return self._id_to_min_point

    @property
    def id_to_shipment(self):
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

    def load(self, shipment: Shipment) -> bool:
        for point in self._get_space_iterator():
            max_point = self._compute_max_point(point, shipment.parameters)
            if not self._volume_fits(point, max_point):
                continue
            if not self._surface_fits(point, max_point):
                continue
            if not self._weight_fits(shipment.weight):
                continue
            self._load(point, max_point, shipment)
            return True
        return False

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_min_point = {}
        self._id_to_shipment = {}
        self._shipment_id_order = []

    def _get_space_iterator(self) -> SpaceIterator:
        return CornerGroundFreeSpaceIterator(self._space)

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.length - 1,
            point.y + volume_parameters.width - 1,
            point.z + volume_parameters.height - 1)

    def _volume_fits(self, point: Point, max_point: Point) -> bool:
        if not (self._is_inside_container(point) and self._is_inside_container(max_point)):
            return False
        return self._is_sub_space_empty(point, max_point)

    def _is_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._space.shape[0] \
               and 0 <= point.y < self._space.shape[1] \
               and 0 <= point.z < self._space.shape[2]

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._get_sub_space(min_point, max_point)
        return (sub_space == 0).all()

    def _surface_fits(self, point: Point, max_point: Point) -> bool:
        if point.z == 0:
            return True
        surface = self._get_sub_space(point.with_height(point.z - 1), max_point.with_height(point.z - 1))
        if not self._is_surface_steady(surface):
            return False
        return self._can_stack_on_surface(surface)

    @staticmethod
    def _is_surface_steady(surface: np.array) -> bool:
        return np.all(surface != 0)

    def _can_stack_on_surface(self, surface: np.array) -> bool:
        shipments = [self._id_to_shipment[id_] for id_ in np.unique(surface)]
        return np.all([shipment.can_stack for shipment in shipments])

    def _weight_fits(self, weight: int):
        total_weight = sum([shipment.weight for shipment in self._id_to_shipment.values()])
        total_weight += weight
        return total_weight <= self.lifting_capacity

    def _get_sub_space(self, min_point: Point, max_point: Point) -> np.array:
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]

    def _load(self, point: Point, max_point: Point, shipment: Shipment) -> None:
        self._load_into_space(point, max_point, shipment.id)
        self._id_to_shipment[shipment.id] = shipment
        self._shipment_id_order.append(shipment.id)

    def _load_into_space(self, point: Point, max_point: Point, id_: int) -> None:
        self._space[point.x:max_point.x + 1, point.y:max_point.y + 1, point.z:max_point.z + 1] = id_
        self._id_to_min_point[id_] = point
