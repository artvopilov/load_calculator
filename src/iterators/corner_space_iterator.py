import numpy as np

from src.iterators.space_iterator import SpaceIterator
from src.point import Point

START_POINT = Point(0, 0, 0)


class CornerSpaceIterator(SpaceIterator):
    _space: np.array

    def __init__(self, space: np.array):
        self._space = space

    def _compute_start_point(self) -> Point:
        if self._space.size != 0:
            return START_POINT
        raise StopIteration

    def _compute_next_point(self) -> Point:
        if self._has_next_x():
            return self._move_x()
        if self._has_next_y():
            return self._move_y()
        if self._has_next_z():
            return self._move_z()
        raise StopIteration

    def _has_next_x(self) -> bool:
        return self._current_point.x < self._space.shape[0] - 1

    def _move_x(self) -> Point:
        return Point(self._current_point.x + 1, self._current_point.y, self._current_point.z)

    def _has_next_y(self) -> bool:
        return self._current_point.y < self._space.shape[1] - 1

    def _move_y(self) -> Point:
        return Point(0, self._current_point.y + 1, self._current_point.z)

    def _has_next_z(self) -> bool:
        return self._current_point.z < self._space.shape[2] - 1

    def _move_z(self) -> Point:
        return Point(0, 0, self._current_point.z + 1)
