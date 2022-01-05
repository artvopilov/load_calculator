import numpy as np

from src.iterators.corner_surface_iterator import CornerSurfaceIterator
from src.point import Point


class CornerSpaceIterator(CornerSurfaceIterator):
    def __init__(self, space: np.array):
        super().__init__(space)

    def _compute_next_point(self) -> Point:
        if self._current_point.x < self._space.shape[0] - 1:
            return self._move_x()

        if self._current_point.y < self._space.shape[1] - 1:
            return self._move_y()

        if self._current_point.z < self._space.shape[2] - 1:
            return self._move_z()

        raise StopIteration

    def _move_z(self) -> Point:
        return Point(0, 0, self._current_point.z + 1)
