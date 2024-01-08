from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Set, List

from src.loading.point.point import Point
from src.loading.point.points_update_info_resolver import PointsUpdateInfoResolver
from src.parameters.util_parameters.volume_parameters import VolumeParameters


@dataclass
class PointsManager:
    _params: VolumeParameters
    _points_update_info_resolver: PointsUpdateInfoResolver
    _points: DefaultDict[Point, Set[Point]] = field(init=False, default_factory=lambda: defaultdict(set))

    def __post_init__(self):
        self.reset()

    @property
    def points(self) -> DefaultDict[Point, Set[Point]]:
        return self._points

    def reset(self) -> None:
        opening_point = Point(0, 0, 0)
        closing_point = Point(self._params.length - 1, self._params.width - 1, self._params.height - 1)
        self._points.clear()
        self._points[opening_point].add(closing_point)

    def get_opening_points(self) -> List[Point]:
        return list(self._points.keys())

    def get_closing_points(self, point: Point) -> Set[Point]:
        return self._points[point]

    def update(self, used_opening_p: Point, used_closing_p: Point, with_top_points: bool) -> None:
        points_update_info = self._points_update_info_resolver.resolve(self._points, used_opening_p, used_closing_p)

        self._update_bottom_points(
            used_opening_p,
            used_closing_p,
            points_update_info.bottom_points,
            points_update_info.bottom_border_points
        )

        if with_top_points:
            self._update_top_points(used_opening_p, used_closing_p, points_update_info.top_border_points)

    def _update_bottom_points(
            self,
            used_opening_p: Point,
            used_closing_p: Point,
            points: DefaultDict[Point, Set[Point]],
            border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        for opening_p, closing_ps in points.items():
            for closing_p in closing_ps:
                self._points[opening_p].remove(closing_p)
                if opening_p.x < used_opening_p.x:
                    new_closing_p = closing_p.with_x(used_opening_p.x - 1)
                    self._insert_bottom_point(opening_p, new_closing_p, border_points)
                if closing_p.x > used_closing_p.x:
                    new_opening_p = opening_p.with_x(used_closing_p.x + 1)
                    self._insert_bottom_point(new_opening_p, closing_p, border_points)
                if opening_p.y < used_opening_p.y:
                    new_closing_p = closing_p.with_y(used_opening_p.y - 1)
                    self._insert_bottom_point(opening_p, new_closing_p, border_points)
                if closing_p.y > used_closing_p.y:
                    new_opening_p = opening_p.with_y(used_closing_p.y + 1)
                    self._insert_bottom_point(new_opening_p, closing_p, border_points)

    def _insert_bottom_point(
            self,
            new_opening_p: Point,
            new_closing_p: Point,
            border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        border_points_to_remove = defaultdict(set)
        for border_opening_p, border_closing_ps in border_points.items():
            for border_closing_p in border_closing_ps:
                if self._point_is_inside(new_opening_p, new_closing_p, border_opening_p, border_closing_p):
                    return
                elif self._point_is_inside(border_opening_p, border_closing_p, new_opening_p, new_closing_p):
                    border_points_to_remove[border_opening_p].add(border_closing_p)

        for border_opening_p, border_closing_ps in border_points_to_remove.items():
            border_points[border_opening_p] -= border_closing_ps
            self._points[border_opening_p] -= border_closing_ps

        border_points[new_opening_p].add(new_closing_p)
        self._points[new_opening_p].add(new_closing_p)

    def _update_top_points(
            self,
            used_opening_p: Point,
            used_closing_p: Point,
            border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        new_opening_p = used_opening_p.with_z(used_closing_p.z + 1)
        new_closing_p = used_closing_p.with_z(self._params.height - 1)
        extension_points = defaultdict(set)
        extension_points[new_opening_p].add(new_closing_p)

        for border_opening_p, border_closing_ps in border_points.items():
            for border_closing_p in border_closing_ps:
                extension_points = self._extend_top_border_point(border_opening_p, border_closing_p, extension_points)

        self._save_extension_points(extension_points)
        self._remove_extra_border_points(border_points, extension_points)

    def _extend_top_border_point(
            self,
            border_opening_p: Point,
            border_closing_p: Point,
            extension_points: DefaultDict[Point, Set[Point]]
    ) -> DefaultDict[Point, Set[Point]]:
        new_extension_points = defaultdict(set)
        for ext_opening_p, ext_closing_ps in extension_points.items():
            for ext_closing_p in ext_closing_ps:
                new_extension_points[ext_opening_p].add(ext_closing_p)

                if border_closing_p.x + 1 == ext_opening_p.x:
                    new_opening_p = border_opening_p.with_y(max(border_opening_p.y, ext_opening_p.y))
                    new_closing_p = border_closing_p.with_y(min(border_closing_p.y, ext_closing_p.y))
                elif border_closing_p.y + 1 == ext_opening_p.y:
                    new_opening_p = border_opening_p.with_x(max(border_opening_p.x, ext_opening_p.x))
                    new_closing_p = border_closing_p.with_x(min(border_closing_p.x, ext_closing_p.x))
                elif border_opening_p.x - 1 == ext_closing_p.x:
                    new_opening_p = ext_opening_p.with_y(max(border_opening_p.y, ext_opening_p.y))
                    new_closing_p = border_closing_p.with_y(min(border_closing_p.y, ext_closing_p.y))
                elif border_opening_p.y == ext_closing_p.y + 1:
                    new_opening_p = ext_opening_p.with_x(max(border_opening_p.x, ext_opening_p.x))
                    new_closing_p = border_closing_p.with_x(min(border_closing_p.x, ext_closing_p.x))
                else:
                    continue

                new_extension_points[new_opening_p].add(new_closing_p)
                if self._point_is_inside(ext_opening_p, ext_closing_p, new_opening_p, new_closing_p):
                    new_extension_points[ext_opening_p].remove(ext_closing_p)
        return new_extension_points

    def _save_extension_points(self, extension_points: DefaultDict[Point, Set[Point]]) -> None:
        for ext_opening_p, ext_closing_ps in extension_points.items():
            for ext_closing_p in ext_closing_ps:
                self._points[ext_opening_p].add(ext_closing_p)

    def _remove_extra_border_points(
            self,
            border_points: DefaultDict[Point, Set[Point]],
            extension_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        for border_opening_p, border_closing_ps in border_points.items():
            for border_closing_p in border_closing_ps:
                for ext_opening_p, ext_closing_ps in extension_points.items():
                    for ext_closing_p in ext_closing_ps:
                        if self._point_is_inside(border_opening_p, border_closing_p, ext_opening_p, ext_closing_p):
                            self._points[border_opening_p].remove(border_closing_p)

    @staticmethod
    def _point_is_inside(p: Point, max_p: Point, other_p: Point, other_max_p: Point) -> bool:
        return p.x >= other_p.x and p.y >= other_p.y and max_p.x <= other_max_p.x and max_p.y <= other_max_p.y
