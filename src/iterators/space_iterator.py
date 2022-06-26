from abc import ABC, abstractmethod
from typing import Optional

from src.loading.point import Point


class SpaceIterator(ABC):
    _is_start_point: bool

    def __init__(self):
        self._is_start_point = True

    def __iter__(self):
        return self

    def __next__(self) -> Point:
        # start_time = datetime.now()

        current_point = self._compute_start_point() if self._is_start_point else self._compute_next_empty_point()
        self._is_start_point = False

        # end_time = datetime.now()
        # print(f"Point was generated in {end_time - start_time} ms")

        if not current_point:
            raise StopIteration
        return current_point

    @abstractmethod
    def _compute_start_point(self) -> Optional[Point]:
        pass

    @abstractmethod
    def _compute_next_empty_point(self) -> Optional[Point]:
        pass
