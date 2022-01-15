from typing import Dict, Tuple

import numpy as np

from src.items.pallet import Pallet
from src.items.shipment import Shipment
from src.items.volume_item import VolumeItem
from src.iterators.corner_free_space_iterator import CornerFreeSpaceIterator
from src.iterators.corner_free_space_max_height_iterator import CornerFreeSpaceMaxHeightIterator
from src.parameters.container_parameters import ContainerParameters
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(VolumeItem):
    _parameters: ContainerParameters
    _space: np.array

    _id_to_shipment: Dict[int, Shipment]
    _id_to_pallet: Dict[int, Pallet]

    _id_to_min_point: Dict[int, Point]

    _pallet_id_to_loaded_weight: Dict[int, float]

    def __init__(self, parameters: ContainerParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters
        self._space = np.zeros((parameters.length, parameters.width, parameters.height))

        self._id_to_shipment = {}
        self._id_to_pallet = {}

        self._id_to_min_point = {}

        self._pallet_id_to_loaded_weight = {}

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.lifting_capacity

    def _get_parameters(self) -> VolumeParameters:
        return self._parameters

    def __str__(self) -> str:
        return f'Container: ({self._key()})'

    def load_pallet_if_fits(self, pallet: Pallet) -> bool:
        if not self._weight_fits_container(pallet.weight):
            return False

        for point in self._get_floor_iterator():
            max_point = self._compute_max_point(point, pallet)
            if self._volume_fits(point, max_point):
                self._load_pallet(point, max_point, pallet)
                return True

        return False

    def load_shipment_if_fits(self, shipment: Shipment) -> bool:
        if not self._weight_fits_container(shipment.weight):
            return False

        for point in self._get_space_iterator():
            max_point = self._compute_max_point(point, shipment)
            if not self._volume_fits(point, max_point):
                continue
            pallet_id_to_loading_weight = self._compute_pallet_id_to_loading_weight(point, max_point, shipment.weight)
            if not self.weight_fits_pallet(pallet_id_to_loading_weight):
                continue

            self._load_shipment(point, max_point, shipment, pallet_id_to_loading_weight)
            return True

        return False

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_shipment = {}
        self._id_to_pallet = {}

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

    def _get_floor_iterator(self) -> CornerFreeSpaceMaxHeightIterator:
        return CornerFreeSpaceMaxHeightIterator(self._space, 0)

    def _get_space_iterator(self) -> CornerFreeSpaceIterator:
        return CornerFreeSpaceIterator(self._space)

    def _weight_fits_container(self, weight: int) -> bool:
        return self._compute_loaded_weight() + weight <= self.lifting_capacity

    def _volume_fits(self, point: Point, max_point: Point) -> bool:
        if not (self._is_inside_container(point) and self._is_inside_container(max_point)):
            return False
        if not self._is_surface_under_steady(point, max_point):
            return False
        return self._is_sub_space_empty(point, max_point)

    def weight_fits_pallet(self, pallet_id_to_loading_weight: Dict[int, float]) -> bool:
        for id_ in pallet_id_to_loading_weight.keys():
            pallet = self._id_to_pallet[id_]
            loading_weight = pallet_id_to_loading_weight[pallet.id]
            loaded_weight = self._pallet_id_to_loaded_weight[pallet.id]
            if pallet.lifting_capacity < loading_weight + loaded_weight:
                return False

        return True

    def _load_pallet(self, point: Point, max_point: Point, pallet: Pallet) -> None:
        self._load_into_space(point, max_point, pallet.id)
        self._id_to_pallet[pallet.id] = pallet

    def _load_shipment(
            self,
            point: Point,
            max_point: Point,
            shipment: Shipment,
            pallet_id_to_loading_weight: Dict[int, float]
    ) -> None:
        self._load_into_space(point, max_point, shipment.id)
        self._id_to_shipment[shipment.id] = shipment
        for id_, weight in pallet_id_to_loading_weight.items():
            self._pallet_id_to_loaded_weight[id_] += weight

    def _load_into_space(self, point: Point, max_point: Point, item_id: int) -> None:
        self._space[point.x:max_point.x + 1, point.y:max_point.y + 1, point.z:max_point.z + 1] = item_id
        self._id_to_min_point[item_id] = point

    def _compute_loaded_weight(self):
        loaded_shipment_weight = sum([s.weight for s in self._id_to_shipment.values()])
        loaded_pallet_weight = sum([p.weight for p in self._id_to_pallet.values()])
        return loaded_pallet_weight + loaded_shipment_weight

    def _compute_pallet_id_to_loaded_weight(self) -> Dict[int, float]:
        pallet_id_to_loaded_weight = {}
        for pallet in self._id_to_pallet.values():
            load_space = self._compute_pallet_load_space(pallet)
            loaded_weight = self._compute_space_loaded_weight(load_space)
            pallet_id_to_loaded_weight[pallet.id] = loaded_weight
        return pallet_id_to_loaded_weight

    def _compute_pallet_load_space(self, pallet: Pallet) -> np.array:
        min_point = self._id_to_min_point[pallet.id]
        max_point = self._compute_max_point(min_point, pallet)
        return self._get_sub_space(min_point.with_height(max_point.z + 1), max_point.with_height(self.height))

    def _compute_space_loaded_weight(self, load_space: np.array) -> float:
        shipment_ids, shipment_volume = np.unique(load_space, return_counts=True)
        total_weight = 0
        for id_, volume in zip(shipment_ids, shipment_volume):
            if id_ not in self._id_to_shipment:
                continue
            total_weight += self._id_to_shipment[id_].compute_part_weight(volume)
        return total_weight

    def _compute_pallet_id_to_loading_weight(self, min_point: Point, max_point: Point, weight: int) -> Dict[int, float]:
        floor_surface = self._get_sub_space(min_point.with_height(0), max_point.with_height(1))
        pallet_ids, pallet_areas = np.unique(floor_surface, return_counts=True)

        pallet_id_to_loading_weight = {}
        for id_, area in zip(pallet_ids, pallet_areas):
            if id_ not in self._id_to_pallet:
                continue
            weight_part = area / floor_surface.size()
            pallet_id_to_loading_weight[id_] = weight_part * weight
        return pallet_id_to_loading_weight

    def _is_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._space.shape[0] \
               and 0 <= point.y < self._space.shape[1] \
               and 0 <= point.z < self._space.shape[2]

    def _is_surface_under_steady(self, min_point: Point, max_point: Point) -> bool:
        if min_point.z == 0:
            return True

        surface = self._get_sub_space(min_point.with_height(min_point.z - 1), max_point.with_height(min_point.z))
        return (surface != 0).all()

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._get_sub_space(min_point, max_point)
        return (sub_space == 0).all()

    def _get_sub_space(self, min_point: Point, max_point: Point):
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]

    @staticmethod
    def _compute_max_point(point: Point, item: VolumeItem) -> Point:
        return Point(point.x + item.length - 1, point.y + item.width - 1, point.z + item.height - 1)
