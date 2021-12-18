class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self._x = x
        self._y = y
        self._z = z

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
