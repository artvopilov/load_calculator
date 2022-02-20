import numpy as np

from src.iterators.free_space.corner_free_space_iterator import CornerFreeSpaceIterator


class CornerHeightFreeSpaceIterator(CornerFreeSpaceIterator):
    def _get_point_order(self) -> np.array:
        return np.lexsort((
            self._point_indices[:, 2],
            self._point_indices[:, 0],
            self._point_indices[:, 1]))
