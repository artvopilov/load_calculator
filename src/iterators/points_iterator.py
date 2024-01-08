from abc import abstractmethod, ABC
from typing import Optional, List, Tuple, Iterable

from src.iterators.space_iterator import SpaceIterator
from src.loading.point.point import Point


class PointsIterator(SpaceIterator, ABC):
    _points: List[Point]
    _i: int

    def __init__(self, points: Iterable[Point]) -> None:
        super().__init__()
        self._points = sorted(points, key=lambda p: self._get_point_order_key(p))
        self._i = 0

    def _compute_start_point(self) -> Optional[Point]:
        return self._points[self._i]

    def _compute_next_empty_point(self) -> Optional[Point]:
        self._i += 1
        if self._i < len(self._points):
            return self._points[self._i]
        return None

    @abstractmethod
    def _get_point_order_key(self, point: Point) -> Tuple:
        pass
