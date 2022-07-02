from collections import defaultdict
from typing import DefaultDict, Set

from src.loading.point import Point


class PointsForUpdate:
    _bottom_border_points: DefaultDict[Point, Set[Point]]
    _bottom_inner_points: DefaultDict[Point, Set[Point]]
    _top_border_points: DefaultDict[Point, Set[Point]]

    def __init__(self) -> None:
        self._bottom_border_points = defaultdict(set)
        self._bottom_inner_points = defaultdict(set)
        self._top_border_points = defaultdict(set)

    @property
    def bottom_border_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._bottom_border_points

    @property
    def bottom_inner_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._bottom_inner_points

    @property
    def top_border_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._top_border_points

    def add_point(self, p: Point, max_p: Point, loading_p: Point, loading_max_p: Point) -> None:
        if p.z == loading_p.z:
            self._add_bottom_point(p, max_p, loading_p, loading_max_p)
        else:
            self._top_border_points[p].add(max_p)

    def _add_bottom_point(self, p: Point, max_p: Point, loading_p: Point, loading_max_p: Point) -> None:
        if self._is_border_point(p, max_p, loading_p, loading_max_p):
            self._bottom_border_points[p].add(max_p)
        else:
            self._bottom_inner_points[p].add(max_p)

    @staticmethod
    def _is_border_point(p: Point, max_p: Point, loading_p: Point, loading_max_p: Point) -> bool:
        return p.x == loading_max_p.x + 1 \
               or p.y == loading_max_p.y + 1 \
               or max_p.x + 1 == loading_p.x \
               or max_p.y + 1 == loading_p.y
