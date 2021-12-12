import numpy as np

from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.point import Point


class Container:
    def __init__(self, container_params: ContainerParameters) -> None:
        self._space = np.zeros((container_params.length, container_params.width, container_params.height))
        self._lifting_capacity = container_params.lifting_capacity

        self._start_point = Point(0, 0, 0)
        self._last_point = None

        self._point_to_shipment = {}

    def load(self, shipment: ShipmentParameters) -> bool:
        pass

    def unload(self) -> None:
        pass

    def _fits(self, point: Point, shipment: ShipmentParameters) -> bool:
        x = point.x
        y = point.y
        z = point.z

        x_upper = x + shipment.length
        y_upper = y + shipment.width
        z_upper = z + shipment.height

        x_shape = self._space.shape[0]
        y_shape = self._space.shape[1]
        z_shape = self._space.shape[2]

        if x_upper > x_shape or y_upper > y_shape or z_upper > z_shape:
            return False

        return self._space[x:x_upper, y:y_upper, z:z_upper] == 0
