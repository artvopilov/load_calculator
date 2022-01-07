import numpy as np

from src.iterators.corner_free_space_iterator import CornerFreeSpaceIterator


class CornerFreeSpaceMaxHeightIterator(CornerFreeSpaceIterator):
    _max_height: int

    def __init__(self, space: np.array, max_height: int):
        super().__init__(space)
        self._max_height = max_height

    def _has_next(self) -> bool:
        return super()._has_next() and self._points[self._current_point_ind + 1].z <= self._max_height



