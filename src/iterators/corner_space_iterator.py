from typing import Optional

import numpy as np

from src.iterators.space_iterator import SpaceIterator
from src.point import Point


class CornerSpaceIterator(SpaceIterator):
    _space: np.array
    _point: Point

    def __init__(self, space: np.array):
        super().__init__()
        self._space = space
        self._point = Point(0, 0, 0)

    def _compute_start_point(self) -> Optional[Point]:
        if self._space.size == 0:
            return None
        raise self._point

    def _compute_next_point(self) -> Optional[Point]:
        if self._has_next_x():
            return self._move_x()
        if self._has_next_y():
            return self._move_y()
        if self._has_next_z():
            return self._move_z()
        return None

    def _has_next_x(self) -> bool:
        return self._point.x < self._space.shape[0] - 1

    def _move_x(self) -> Point:
        return Point(self._point.x + 1, self._point.y, self._point.z)

    def _has_next_y(self) -> bool:
        return self._point.y < self._space.shape[1] - 1

    def _move_y(self) -> Point:
        return Point(0, self._point.y + 1, self._point.z)

    def _has_next_z(self) -> bool:
        return self._point.z < self._space.shape[2] - 1

    def _move_z(self) -> Point:
        return Point(0, 0, self._point.z + 1)
