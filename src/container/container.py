import numpy as np
from typing import Optional

from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.point import Point
from src.container.iterator.corner_container_iterator import CornerContainerIterator


class Container:
    def __init__(self, container_params: ContainerParameters):
        self._space = np.zeros((container_params.length, container_params.width, container_params.height))
        self._lifting_capacity = container_params.lifting_capacity

        self._point_to_shipment = {}

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
        total_weight = sum([s.weight for s in self._point_to_shipment.values()])
        if total_weight + shipment.weight > self._lifting_capacity:
            return None

        for point in CornerContainerIterator(self._space):
            if self._point_fits(point, shipment):
                return point

        return None

    def _point_fits(self, point: Point, shipment: ShipmentParameters) -> bool:
        x_upper = point.x + shipment.length
        y_upper = point.y + shipment.width
        z_upper = point.z + shipment.height

        if x_upper > self._space.shape[0] \
                or y_upper > self._space.shape[1] \
                or z_upper > self._space.shape[2]:
            return False

        return (self._space[point.x:x_upper, point.y:y_upper, point.z:z_upper] == 0).all()

    def __str__(self):
        return '\n'.join(f'point: {p}, shipment: {s}' for p, s in self._point_to_shipment.items())
