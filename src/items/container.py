from typing import Dict, Tuple, List

import numpy as np

from src.items.lifting_item import LiftingItem
from src.items.pallet import Pallet
from src.items.shipment import Shipment
from src.items.volume_item import VolumeItem
from src.iterators.corner_ground_free_space_iterator import CornerGroundFreeSpaceIterator
from src.iterators.space_iterator import SpaceIterator
from src.parameters.container_parameters import ContainerParameters
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(VolumeItem, LiftingItem):
    _id_: int
    _parameters: ContainerParameters

    _space: np.array

    _id_to_pallet: Dict[int, Pallet]
    _id_to_shipment: Dict[int, Shipment]
    _shipment_id_order: List[int]

    _id_to_min_point: Dict[int, Point]

    _pallet_id_to_loaded_weight: Dict[int, float]

    def __init__(self, parameters: ContainerParameters, id_: int):
        self._id_ = id_
        self._parameters = parameters
        self._space = np.zeros((parameters.length, parameters.width, parameters.height), dtype=np.int32)

        self._id_to_pallet = {}
        self._id_to_shipment = {}
        self._shipment_id_order = []

        self._id_to_min_point = {}

        self._pallet_id_to_loaded_weight = {}

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
    def id_to_pallet(self):
        return self._id_to_pallet

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

    def load_pallet_if_fits(self, pallet: Pallet) -> bool:
        for point in self._get_floor_iterator():
            max_point = self._compute_max_point(point, pallet.parameters)
            if self._volume_fits(point, max_point):
                self._load_pallet(point, max_point, pallet)
                return True
        return False

    def load_shipment_if_fits(self, shipment: Shipment) -> bool:
        for point in self._get_space_iterator():
            max_point = self._compute_max_point(point, shipment.parameters)
            if not self._volume_fits(point, max_point):
                continue
            pallet_id_to_loading_weight = self._compute_pallet_id_to_loading_weight(point, max_point, shipment.weight)
            if not self._weight_fits(pallet_id_to_loading_weight):
                continue

            self._load_shipment(point, max_point, shipment, pallet_id_to_loading_weight)
            return True

        return False

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_shipment = {}
        self._id_to_pallet = {}

    def unload_empty_pallets(self) -> None:
        pallets = list(self._id_to_pallet.values())
        for pallet in pallets:
            if self._pallet_id_to_loaded_weight[pallet.id] == 0:
                min_point = self._id_to_min_point[pallet.id]
                max_point = self._compute_max_point(min_point, pallet.parameters)

                pallet_space = self._get_sub_space(min_point, max_point)
                pallet_space.fill(0)

                self.id_to_pallet.pop(pallet.id)
                self.id_to_min_point.pop(pallet.id)
                self._pallet_id_to_loaded_weight.pop(pallet.id)

    def compute_max_pallets_count(self, pallet_parameters: PalletParameters) -> int:
        max_volume_count = self._compute_max_volume_count(pallet_parameters, pallet_parameters.height)
        max_weight_count = self._compute_max_weight_count(pallet_parameters.weight)
        return min(max_volume_count, max_weight_count)

    def _compute_max_volume_count(self, volume_parameters: VolumeParameters, max_height: int) -> int:
        max_count_x = self.length // volume_parameters.length
        max_count_y = self.width // volume_parameters.width
        max_count_z = min(self.height, max_height) // volume_parameters.height
        return max_count_x * max_count_y * max_count_z

    def _compute_max_weight_count(self, weight: int) -> int:
        return self.lifting_capacity // weight

    def _get_floor_iterator(self) -> SpaceIterator:
        return CornerGroundFreeSpaceIterator(self._space[:, :, :1])

    def _get_space_iterator(self) -> SpaceIterator:
        return CornerGroundFreeSpaceIterator(self._space)

    def _compute_pallet_id_to_loading_weight(self, min_point: Point, max_point: Point, weight: int) -> Dict[int, float]:
        floor_surface = self._get_sub_space(min_point.with_height(0), max_point.with_height(1))
        pallet_ids, pallet_areas = np.unique(floor_surface, return_counts=True)

        pallet_id_to_loading_weight = {}
        for id_, area in zip(pallet_ids, pallet_areas):
            if id_ not in self._id_to_pallet:
                continue
            weight_part = area / floor_surface.size
            pallet_id_to_loading_weight[id_] = weight_part * weight
        return pallet_id_to_loading_weight

    def _weight_fits(self, pallet_id_to_loading_weight: Dict[int, float]):
        if not self._weight_fits_container(pallet_id_to_loading_weight):
            return False
        return self._weight_fits_pallet(pallet_id_to_loading_weight)

    def _weight_fits_container(self, pallet_id_to_loading_weight: Dict[int, float]) -> bool:
        total_weight = 0
        for pallet_id, pallet_loaded_weight in self._pallet_id_to_loaded_weight.items():
            pallet_loading_weight = pallet_id_to_loading_weight.get(pallet_id, 0)
            if pallet_loaded_weight + pallet_loaded_weight >= 0:
                pallet = self._id_to_pallet[pallet_id]
                total_weight += pallet.weight + pallet_loaded_weight + pallet_loading_weight

        return total_weight <= self.lifting_capacity

    def _weight_fits_pallet(self, pallet_id_to_loading_weight: Dict[int, float]) -> bool:
        for id_, pallet_loading_weight in pallet_id_to_loading_weight.items():
            pallet = self._id_to_pallet[id_]
            pallet_loaded_weight = self._pallet_id_to_loaded_weight[pallet.id]
            if pallet_loading_weight + pallet_loaded_weight > pallet.lifting_capacity:
                return False
        return True

    def _volume_fits(self, point: Point, max_point: Point) -> bool:
        if not (self._is_inside_container(point) and self._is_inside_container(max_point)):
            return False
        if not self._is_surface_under_steady(point, max_point):
            return False
        return self._is_sub_space_empty(point, max_point)

    def _load_pallet(self, point: Point, max_point: Point, pallet: Pallet) -> None:
        self._load_into_space(point, max_point, pallet.id)
        self._id_to_pallet[pallet.id] = pallet
        self._pallet_id_to_loaded_weight[pallet.id] = 0

    def _load_shipment(
            self,
            point: Point,
            max_point: Point,
            shipment: Shipment,
            pallet_id_to_loading_weight: Dict[int, float]
    ) -> None:
        self._load_into_space(point, max_point, shipment.id)
        self._id_to_shipment[shipment.id] = shipment
        self._shipment_id_order.append(shipment.id)
        for id_, weight in pallet_id_to_loading_weight.items():
            self._pallet_id_to_loaded_weight[id_] += weight

    def _load_into_space(self, point: Point, max_point: Point, id_: int) -> None:
        self._space[point.x:max_point.x + 1, point.y:max_point.y + 1, point.z:max_point.z + 1] = id_
        self._id_to_min_point[id_] = point

    def _is_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._space.shape[0] \
               and 0 <= point.y < self._space.shape[1] \
               and 0 <= point.z < self._space.shape[2]

    def _is_surface_under_steady(self, min_point: Point, max_point: Point) -> bool:
        if min_point.z == 0:
            return True

        surface = self._get_sub_space(min_point.with_height(min_point.z - 1), max_point.with_height(min_point.z - 1))
        return (surface != 0).all()

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._get_sub_space(min_point, max_point)
        return (sub_space == 0).all()

    def _get_sub_space(self, min_point: Point, max_point: Point) -> np.array:
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]

    @staticmethod
    def _compute_max_point(point: Point, volume_parameters: VolumeParameters) -> Point:
        return Point(
            point.x + volume_parameters.length - 1,
            point.y + volume_parameters.width - 1,
            point.z + volume_parameters.height - 1)
