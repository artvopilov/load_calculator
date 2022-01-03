import numpy as np
from typing import Optional

from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.pallet_parameters import PalletParameters
from src.point import Point
from src.container.iterator.corner_container_iterator import CornerContainerIterator


class Container:
    def __init__(self, container_parameters: ContainerParameters, pallet_parameters: PalletParameters):
        self._space = np.zeros((container_parameters.length, container_parameters.width, container_parameters.height))
        self._lifting_capacity = container_parameters.lifting_capacity

        self._pallet_parameters = pallet_parameters

        self._point_to_shipment = {}

    def __str__(self):
        return '\n'.join(f'point: {p}, shipment: {s}' for p, s in self._point_to_shipment.items())

    def try_load(self, shipment: ShipmentParameters) -> bool:
        loading_point = self._find_loading_point(shipment)
        print(f'loading point: {loading_point}')
        if loading_point is None:
            return False

        self._load(loading_point, shipment)
        return True

    def unload(self) -> None:
        self._space.fill(0)
        self._point_to_shipment = {}

    def _load(self, point: Point, shipment: ShipmentParameters) -> None:
        x_upper = point.x + shipment.length
        y_upper = point.y + shipment.width
        z_upper = point.z + shipment.height

        self._space[point.x:x_upper, point.y:y_upper, point.z:z_upper] = 1
        self._point_to_shipment[point] = shipment

    def _find_loading_point(self, shipment: ShipmentParameters) -> Optional[Point]:
        if not self._is_shipment_holdable_by_container(shipment.weight):
            return None

        for point in CornerContainerIterator(self._space):
            if self._is_pallet_point(point):
                continue

            if self._point_fits(point, shipment):
                return point

        return None

    def _is_shipment_holdable_by_container(self, shipment_weight: int) -> bool:
        total_weight = sum([s.weight for s in self._point_to_shipment.values()])
        if total_weight + shipment_weight > self._lifting_capacity:
            return False
        return True

    def _is_pallet_point(self, point: Point):
        if not self._pallet_parameters:
            return False

        return point.z <= self._pallet_parameters.height

    def _point_fits(self, point: Point, shipment: ShipmentParameters) -> bool:
        max_point = Point(point.x + shipment.length - 1,
                          point.y + shipment.width - 1,
                          point.z + shipment.height - 1)

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

        surface = self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z - 1]
        return (surface != 0).all()

    def _is_shipment_holdable_by_pallet(self, shipment_weight: int) -> bool:
        return True

    def _is_sub_space_empty(self, min_point: Point, max_point: Point) -> bool:
        sub_space = self._space[min_point.x:max_point.x + 1, min_point.y:max_point.y + 1, min_point.z:max_point.z + 1]
        return (sub_space == 0).all()
