import numpy as np
from abc import ABC, abstractmethod

from src.point import Point


class AreaIterator(ABC):
    _space: np.array
    _current_point: Point

    def __init__(self, space: np.array, start_point: Point):
        self._space = space
        self._current_point = start_point

    def __iter__(self):
        return self

    def __next__(self) -> Point:
        self._current_point = self._compute_next_point()
        return self._current_point

    @abstractmethod
    def _compute_next_point(self) -> Point:
        pass
