from typing import List

import numpy as np

from src.iterators.space_iterator import SpaceIterator
from src.point import Point

START_POINT_IND = 0


class CornerFreeSpaceIterator(SpaceIterator):
    _points: List[Point]
    _current_point_ind: int

    def __init__(self, space: np.array):
        super().__init__()
        zero_space = np.argwhere(space == 0)
        sorted_zero_space = np.lexsort((zero_space[:, 2], zero_space[:, 1], zero_space[:, 0]))

        self._points = []
        for p_i in sorted_zero_space:
            p = zero_space[p_i]
            self._points.append(Point(p[0], p[1], p[2]))

    def _compute_start_point(self) -> Point:
        if len(self._points) != 0:
            self._current_point_ind = START_POINT_IND
            return self._points[self._current_point_ind]
        raise StopIteration

    def _compute_next_point(self) -> Point:
        if self._has_next():
            return self._move()
        raise StopIteration

    def _has_next(self) -> bool:
        return self._current_point_ind < len(self._points) - 1

    def _move(self) -> Point:
        self._current_point_ind += 1
        return self._points[self._current_point_ind]
