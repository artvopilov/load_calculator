from typing import Dict, Tuple

import numpy as np

from src.items.pallet import Pallet
from src.items.shipment import Shipment
from src.items.volume_item import VolumeItem
from src.iterators.corner_free_space_iterator import CornerFreeSpaceIterator
from src.iterators.corner_free_space_max_height_iterator import CornerFreeSpaceMaxHeightIterator
from src.parameters.container_parameters import ContainerParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point


class Container(VolumeItem):
    _parameters: ContainerParameters
    _space: np.array

    _id_to_shipment: Dict[int, Shipment]
    _id_to_pallet: Dict[int, Pallet]

    _id_to_min_point: Dict[int, Point]
    _id_to_max_point: Dict[int, Point]

    def __init__(self, parameters: ContainerParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters
        self._space = np.zeros((parameters.length, parameters.width, parameters.height))

        self._id_to_shipment = {}
        self._id_to_pallet = {}

        self._id_to_min_point = {}
        self._id_to_max_point = {}

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
            if self._volume_fits(point, max_point):
                self._load_shipment(point, max_point, shipment)
                return True

        return False

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_shipment = {}
        self._id_to_pallet = {}

    def _get_floor_iterator(self) -> CornerFreeSpaceMaxHeightIterator:
        return CornerFreeSpaceMaxHeightIterator(self._space, 0)

    def _get_space_iterator(self) -> CornerFreeSpaceIterator:
        return CornerFreeSpaceIterator(self._space)

    def _weight_fits_container(self, weight: int) -> bool:
        return self._get_loaded_weight() + weight <= self.lifting_capacity

    def _volume_fits(self, point: Point, max_point: Point) -> bool:
        if not (self._is_inside_container(point) and self._is_inside_container(max_point)):
            return False
        if not self._is_surface_steady(point, max_point):
            return False
        return self._is_sub_space_empty(point, max_point)

    def weight_fits_pallet(self, point: Point, max_point: Point, weight: int) -> bool:
        pass

    def _load_pallet(self, point: Point, max_point: Point, pallet: Pallet) -> None:
        self._load_into_space(point, max_point, pallet.id)
        self._id_to_pallet[pallet.id] = pallet

    def _load_shipment(self, point: Point, max_point: Point, shipment: Shipment) -> None:
        self._load_into_space(point, max_point, shipment.id)
        self._id_to_shipment[shipment.id] = shipment

    def _load_into_space(self, point: Point, max_point: Point, item_id: int) -> None:
        self._space[point.x:max_point.x + 1, point.y:max_point.y + 1, point.z:max_point.z + 1] = item_id
        self._id_to_min_point[item_id] = point
        self._id_to_max_point[item_id] = max_point

    def _get_loaded_weight(self):
        loaded_shipment_weight = sum([s.weight for s in self._id_to_shipment.values()])
        loaded_pallet_weight = sum([p.weight for p in self._id_to_pallet.values()])
        return loaded_pallet_weight + loaded_shipment_weight

    def _get_pallet_id_to_loaded_weight(self) -> Dict[int, int]:
        pallet_ids = list(self._id_to_pallet.keys())
        for pallet_id in pallet_ids:
            min_point = self._id_to_min_point[pallet_id]
            max_point = self._id_to_max_point[pallet_id]
            pallet_shipment_space = self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, max_point.z + 1:]

    def _is_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._space.shape[0] \
               and 0 <= point.y < self._space.shape[1] \
               and 0 <= point.z < self._space.shape[2]

    def _is_surface_steady(self, min_point: Point, max_point: Point) -> bool:
        if min_point.z == 0:
            return True

        surface = self._get_surface_under(min_point, max_point)
        return (surface != 0).all()

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._get_sub_space(min_point, max_point)
        return (sub_space == 0).all()

    def _get_surface_under(self, min_point: Point, max_point: Point) -> np.array:
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z - 1]

    def _get_sub_space(self, min_point: Point, max_point: Point) -> np.array:
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]

    @staticmethod
    def _compute_max_point(point: Point, item: VolumeItem) -> Point:
        return Point(point.x + item.length - 1, point.y + item.width - 1, point.z + item.height - 1)
