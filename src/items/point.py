from typing import Dict


class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self._x = x
        self._y = y
        self._z = z

    def with_x(self, x: int) -> 'Point':
        return Point(x, self.y, self.z)

    def with_y(self, y: int) -> 'Point':
        return Point(self.x, y, self.z)

    def with_z(self, z: int) -> 'Point':
        return Point(self.x, self.y, z)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.x == other.x \
                   and self.y == other.y \
                   and self.z == other.z

        return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return f'Point: ({self.x}, {self.y}, {self.z})'

    def build_response(self, shipment_params_id: int) -> Dict:
        return {'x': self.x, 'y': self.y, 'z': self.z, 'cargo_id': shipment_params_id}