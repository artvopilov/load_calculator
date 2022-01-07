import numpy as np

from src.iterators.corner_space_iterator import CornerSpaceIterator


class CornerSpaceMaxHeightIterator(CornerSpaceIterator):
    _max_height: int

    def __init__(self, space: np.array, max_height: int) -> None:
        super().__init__(space)
        self._max_height = max_height

    def _has_next_z(self) -> bool:
        return super()._has_next_z() and self._current_point.z <= self._max_height


