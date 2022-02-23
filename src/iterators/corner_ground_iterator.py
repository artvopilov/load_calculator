from typing import Optional

from src.items.container import Container
from src.iterators.space_iterator import SpaceIterator
from src.point import Point


class CornerGroundIterator(SpaceIterator):
    _container: Container
    _x: int
    _y: int

    def __init__(self, container: Container) -> None:
        super().__init__()
        self._container = container
        self._x = 0
        self._y = 0

    def _compute_start_point(self) -> Optional[Point]:
        return self._container.compute_top_point(self._x, self._y)

    def _compute_next_empty_point(self) -> Optional[Point]:
        if self._compute_next_point():
            return self._container.compute_top_point(self._x, self._y)
        return None

    def _compute_next_point(self) -> bool:
        if self._has_next_x():
            self._x += 1
            return True
        if self._has_next_y():
            self._x = 0
            self._y += 1
            return True
        return False

    def _has_next_x(self) -> bool:
        return self._x < self._container.length - 1

    def _has_next_y(self) -> bool:
        return self._y < self._container.width - 1
