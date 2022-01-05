import numpy as np

from src.iterators.area_iterator import AreaIterator
from src.point import Point


START_POINT = Point(0, 0, 0)


class CornerSurfaceIterator(AreaIterator):
    def __init__(self, space: np.array):
        super().__init__(space, START_POINT)

    def _compute_next_point(self) -> Point:
        if self._current_point.x < self._space.shape[0] - 1:
            return self._move_x()

        if self._current_point.y < self._space.shape[1] - 1:
            return self._move_y()

        raise StopIteration

    def _move_x(self) -> Point:
        return Point(self._current_point.x + 1, self._current_point.y, self._current_point.z)

    def _move_y(self) -> Point:
        return Point(0, self._current_point.y + 1, self._current_point.z)
