from typing import Optional

import numpy as np

from src.iterators.space_iterator import SpaceIterator
from src.point import Point


class CornerSpaceIterator(SpaceIterator):
    _space: np.array
    _x: int
    _y: int
    _z: int

    def __init__(self, space: np.array, start_point: Point = Point(0, 0, 0)) -> None:
        super().__init__()
        self._space = space
        self._x = start_point.x
        self._y = start_point.y
        self._z = start_point.z

    def _compute_start_point(self) -> Optional[Point]:
        if self._space.size == 0:
            return None
        return Point(self._x, self._y, self._z)

    def _compute_next_empty_point(self) -> Optional[Point]:
        while self._compute_next_point():
            if not self._space[self._x, self._y, self._z]:
                return Point(self._x, self._y, self._z)
        return None

    def _compute_next_point(self) -> bool:
        if self._has_next_z():
            self._z += 1
            return True
        if self._has_next_x():
            self._z = 0
            self._x += 1
            return True
        if self._has_next_y():
            self._z = 0
            self._x = 0
            self._y += 1
            return True
        return False

    def _has_next_z(self) -> bool:
        return self._z < self._space.shape[2] - 1

    def _has_next_x(self) -> bool:
        return self._x < self._space.shape[0] - 1

    def _has_next_y(self) -> bool:
        return self._y < self._space.shape[1] - 1
