from typing import Optional, Dict, Tuple

import numpy as np

from src.iterator.corner_space_iterator import CornerSpaceIterator
from src.pallet import Pallet
from src.parameters.container_parameters import ContainerParameters
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point
from src.shipment import Shipment
from src.volume_item import VolumeItem


class Container(VolumeItem):
    _parameters: ContainerParameters
    _space: np.array
    _lifting_capacity: int
    _id_to_shipment: Dict[int, Shipment]
    _id_to_pallet: Dict[int, Pallet]

    def __init__(self, parameters: ContainerParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters
        self._space = np.zeros((parameters.length, parameters.width, parameters.height))
        self._lifting_capacity = parameters.lifting_capacity
        self._id_to_shipment = {}

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.lifting_capacity

    def _get_parameters(self) -> VolumeParameters:
        return self._parameters

    def __str__(self) -> str:
        return f'Container: ({self._key()})'

    def try_load_pallet(self, pallet: Pallet) -> bool:
        pallet_surface = self._space[:, :, :1]


    def try_load_shipment(self, shipment: Shipment) -> bool:
        loading_point = self._find_loading_point(shipment)
        print(f'Container loading point: {loading_point}')
        if loading_point is None:
            return False

        self._load(loading_point, shipment)
        return True

    def unload(self) -> None:
        self._space.fill(0)
        self._id_to_shipment = {}

    def _find_loading_point(self, shipment: Shipment) -> Optional[Point]:
        if not self._is_holdable(shipment.weight):
            return None

        for point in CornerSpaceIterator(self._space):
            if self._point_fits(point, shipment):
                return point

        return None

    def _load(self, point: Point, shipment: Shipment) -> None:
        x_upper = point.x + shipment.length
        y_upper = point.y + shipment.width
        z_upper = point.z + shipment.height

        self._space[point.x:x_upper, point.y:y_upper, point.z:z_upper] = shipment.id
        self._id_to_shipment[shipment.id] = shipment

    def _is_holdable(self, item_weight: int) -> bool:
        loaded_shipment_weight = sum([s.weight for s in self._id_to_shipment.values()])
        loaded_pallet_weight = sum([p.weight for p in self._id_to_pallet.values()])
        if loaded_shipment_weight + loaded_pallet_weight + item_weight > self._lifting_capacity:
            return False
        return True

    def _get_space_iterator(self):
        pass

    def _point_fits(self, point: Point, item: VolumeItem) -> bool:
        max_point = Point(point.x + item.length - 1, point.y + item.width - 1, point.z + item.height - 1)

        if not self._is_shipment_inside_container(point, max_point):
            return False

        if not self._is_surface_steady(point, max_point):
            return False

        return self._is_sub_space_empty(point, max_point)

    def _is_shipment_inside_container(self, min_point: Point, max_point: Point) -> bool:
        return self._is_point_inside_container(min_point) and self._is_point_inside_container(max_point)

    def _is_point_inside_container(self, point: Point) -> bool:
        return 0 <= point.x < self._space.shape[0] \
               and 0 <= point.y < self._space.shape[1] \
               and 0 <= point.z < self._space.shape[2]

    def _is_surface_steady(self, min_point: Point, max_point: Point) -> bool:
        if min_point.z == 0:
            return True

        surface = self._get_surface_under_shipment(min_point, max_point)
        return (surface != 0).all()

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]
        return (sub_space == 0).all()

    def _get_surface_under_shipment(self, min_point: Point, max_point: Point) -> np.array:
        return self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z - 1]
