import numpy as np

from src.iterator.space_iterator import SpaceIterator
from src.point import Point


START_POINT = Point(0, 0, 0)


class CornerSpaceIterator(SpaceIterator):
    def __init__(self, space: np.array):
        super().__init__(space, START_POINT)

    def _compute_next_point(self) -> Point:
        if self._current_point.x < self._space.shape[0] - 1:
            return self._move_x()

        if self._current_point.y < self._space.shape[1] - 1:
            return self._move_y()

        if self._current_point.z < self._space.shape[2] - 1:
            return self._move_z()

        raise StopIteration

    def _move_x(self) -> Point:
        return Point(self._current_point.x + 1, self._current_point.y, self._current_point.z)

    def _move_y(self) -> Point:
        return Point(0, self._current_point.y + 1, self._current_point.z)

    def _move_z(self) -> Point:
        return Point(0, 0, self._current_point.z + 1)
