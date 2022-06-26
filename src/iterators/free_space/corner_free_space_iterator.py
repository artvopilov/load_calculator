from abc import abstractmethod
from typing import Optional

import numpy as np

from src.iterators.space_iterator import SpaceIterator
from src.loading.point import Point


class CornerFreeSpaceIterator(SpaceIterator):
    _point_indices: np.array
    _point_order: np.array
    _order_index: int

    def __init__(self, space: np.array):
        super().__init__()
        self._point_indices = np.argwhere(space == 0)
        self._point_order = self._get_point_order()
        self._order_index = -1

    @abstractmethod
    def _get_point_order(self) -> np.array:
        pass

    def _compute_start_point(self) -> Optional[Point]:
        return self._compute_next_empty_point()

    def _compute_next_empty_point(self) -> Optional[Point]:
        if self._has_next():
            return self._move()
        return None

    def _has_next(self) -> bool:
        return self._order_index < len(self._point_indices) - 1

    def _move(self) -> Point:
        self._order_index += 1
        point_index = self._point_indices[self._point_order[self._order_index]]
        return Point(point_index[0], point_index[1], point_index[2])
