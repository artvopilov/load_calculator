from typing import Dict, Tuple

import numpy as np

from src.items.pallet import Pallet
from src.items.shipment import Shipment
from src.items.volume_item import VolumeItem
from src.parameters.container_parameters import ContainerParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point
from src.iterators.corner_space_iterator import CornerSpaceIterator
from src.iterators.corner_surface_iterator import CornerSurfaceIterator


class Container(VolumeItem):
    _parameters: ContainerParameters
    _space: np.array
    _id_to_shipment: Dict[int, Shipment]
    _id_to_pallet: Dict[int, Pallet]

    def __init__(self, parameters: ContainerParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters
        self._space = np.zeros((parameters.length, parameters.width, parameters.height))
        self._id_to_shipment = {}
        self._id_to_pallet = {}

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
        if not self._weight_fits(pallet.weight):
            return False

        for point in self._get_surface_iterator():
            if self._volume_fits(point, pallet):
                self._load_pallet(point, pallet)
                return True

        return False

    def load_shipment_if_fits(self, shipment: Shipment) -> bool:
        pass

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_shipment = {}
        self._id_to_pallet = {}

    def _get_surface_iterator(self) -> CornerSurfaceIterator:
        return CornerSurfaceIterator(self._space)

    def _get_space_iterator(self) -> CornerSpaceIterator:
        return CornerSpaceIterator(self._space)

    def _weight_fits(self, weight: int) -> bool:
        return self._get_loaded_weight() + weight <= self.lifting_capacity

    def _volume_fits(self, point: Point, item: VolumeItem) -> bool:
        max_point = Point(point.x + item.length - 1, point.y + item.width - 1, point.z + item.height - 1)

        if not (self._is_inside_container(point) and self._is_inside_container(point)):
            return False
        if not self._is_surface_steady(point, max_point):
            return False
        return self._is_sub_space_empty(point, max_point)

    def _load_pallet(self, point: Point, pallet: Pallet) -> None:
        self._load_into_space(point, pallet)
        self._id_to_pallet[pallet.id] = pallet

    def _load_shipment(self, point: Point, shipment: Shipment) -> None:
        self._load_into_space(point, shipment)
        self._id_to_shipment[shipment.id] = shipment

    def _load_into_space(self, point: Point, item: VolumeItem) -> None:
        x_upper = point.x + item.length
        y_upper = point.y + item.width
        z_upper = point.z + item.height
        self._space[point.x:x_upper, point.y:y_upper, point.z:z_upper] = item.id

    def _get_loaded_weight(self):
        loaded_shipment_weight = sum([s.weight for s in self._id_to_shipment.values()])
        loaded_pallet_weight = sum([p.weight for p in self._id_to_pallet.values()])
        return loaded_pallet_weight + loaded_shipment_weight

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
