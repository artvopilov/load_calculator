from abc import ABC, abstractmethod
from typing import Optional

from src.point import Point


class SpaceIterator(ABC):
    _current_point: Optional[Point]

    def __init__(self):
        self._current_point = None

    def __iter__(self):
        return self

    def __next__(self) -> Point:
        if not self._current_point:
            self._current_point = self._compute_start_point()
        else:
            self._current_point = self._compute_next_point()
        return self._current_point

    @abstractmethod
    def _compute_start_point(self) -> Point:
        pass

    @abstractmethod
    def _compute_next_point(self) -> Point:
        pass
