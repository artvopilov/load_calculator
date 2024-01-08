from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Set, List, Tuple, Optional

from src.loading.point.point import Point
from src.loading.point.points_update_info_resolver import PointsUpdateInfoResolver
from src.parameters.util_parameters.volume_parameters import VolumeParameters


@dataclass
class PlacesManager:
    _params: VolumeParameters
    _points_update_info_resolver: PointsUpdateInfoResolver
    _places: DefaultDict[Point, Set[Point]] = field(init=False, default_factory=lambda: defaultdict(set))

    def __post_init__(self):
        self.reset()

    @property
    def places(self) -> DefaultDict[Point, Set[Point]]:
        return self._places

    def reset(self) -> None:
        opening_point = Point(0, 0, 0)
        closing_point = Point(self._params.length - 1, self._params.width - 1, self._params.height - 1)
        self._places.clear()
        self._places[opening_point].add(closing_point)

    def get_opening_points(self) -> List[Point]:
        return list(self._places.keys())

    def get_closing_points(self, point: Point) -> Set[Point]:
        return self._places[point]

    def update(self, used_opening_p: Point, used_closing_p: Point, with_top_places: bool) -> None:
        points_update_info = self._points_update_info_resolver.resolve(self._places, used_opening_p, used_closing_p)

        self._update_bottom_places(
            used_opening_p,
            used_closing_p,
            points_update_info.bottom_points,
            points_update_info.bottom_border_points
        )

        if with_top_places:
            self._update_top_places(used_opening_p, used_closing_p, points_update_info.top_border_points)

        for opening_p in self.get_opening_points():
            if len(self._places[opening_p]) == 0:
                self._places.pop(opening_p)

    def _update_bottom_places(
            self,
            used_opening_p: Point,
            used_closing_p: Point,
            places: DefaultDict[Point, Set[Point]],
            border_places: DefaultDict[Point, Set[Point]]
    ) -> None:
        for opening_p, closing_ps in places.items():
            for closing_p in closing_ps:
                self._places[opening_p].remove(closing_p)
                if opening_p.x < used_opening_p.x:
                    new_closing_p = closing_p.with_x(used_opening_p.x - 1)
                    self._insert_bottom_place(opening_p, new_closing_p, border_places)
                if closing_p.x > used_closing_p.x:
                    new_opening_p = opening_p.with_x(used_closing_p.x + 1)
                    self._insert_bottom_place(new_opening_p, closing_p, border_places)
                if opening_p.y < used_opening_p.y:
                    new_closing_p = closing_p.with_y(used_opening_p.y - 1)
                    self._insert_bottom_place(opening_p, new_closing_p, border_places)
                if closing_p.y > used_closing_p.y:
                    new_opening_p = opening_p.with_y(used_closing_p.y + 1)
                    self._insert_bottom_place(new_opening_p, closing_p, border_places)

    def _insert_bottom_place(
            self,
            new_opening_p: Point,
            new_closing_p: Point,
            border_places: DefaultDict[Point, Set[Point]]
    ) -> None:
        border_places_to_remove = defaultdict(set)
        for border_opening_p, border_closing_ps in border_places.items():
            for border_closing_p in border_closing_ps:
                if self._place_is_inside(new_opening_p, new_closing_p, border_opening_p, border_closing_p):
                    return
                elif self._place_is_inside(border_opening_p, border_closing_p, new_opening_p, new_closing_p):
                    border_places_to_remove[border_opening_p].add(border_closing_p)

        for border_opening_p, border_closing_ps in border_places_to_remove.items():
            border_places[border_opening_p] -= border_closing_ps
            self._places[border_opening_p] -= border_closing_ps

        border_places[new_opening_p].add(new_closing_p)
        self._places[new_opening_p].add(new_closing_p)

    def _update_top_places(
            self,
            used_opening_p: Point,
            used_closing_p: Point,
            border_places: DefaultDict[Point, Set[Point]]
    ) -> None:
        new_opening_p = used_opening_p.with_z(used_closing_p.z + 1)
        new_closing_p = used_closing_p.with_z(self._params.height - 1)
        extension_places = defaultdict(set)
        extension_places[new_opening_p].add(new_closing_p)

        for border_opening_p, border_closing_ps in border_places.items():
            for border_closing_p in border_closing_ps:
                extension_places = self._extend_places(border_opening_p, border_closing_p, extension_places)

        for border_opening_p, border_closing_ps in border_places.items():
            for border_closing_p in border_closing_ps:
                if self._should_remove_place(border_opening_p, border_closing_p, extension_places):
                    self._places[border_opening_p].remove(border_closing_p)

        self._save_places(extension_places)

    def _extend_places(
            self,
            border_opening_p: Point,
            border_closing_p: Point,
            extension_places: DefaultDict[Point, Set[Point]]
    ) -> DefaultDict[Point, Set[Point]]:
        extended_places = defaultdict(set)
        for ext_opening_p, ext_closing_ps in extension_places.items():
            for ext_closing_p in ext_closing_ps:
                extended_place = self._extend_place(border_opening_p, border_closing_p, ext_opening_p, ext_closing_p)
                if extended_place is None:
                    extended_places[ext_opening_p].add(ext_closing_p)
                    continue

                new_opening_p, new_closing_p = extended_place
                extended_places[new_opening_p].add(new_closing_p)
                if not self._place_is_inside(ext_opening_p, ext_closing_p, new_opening_p, new_closing_p):
                    extended_places[ext_opening_p].add(ext_closing_p)
        return extended_places

    @staticmethod
    def _extend_place(
            border_opening_p: Point,
            border_closing_p: Point,
            opening_p: Point,
            closing_p: Point,
    ) -> Optional[Tuple[Point, Point]]:
        if border_closing_p.x + 1 == opening_p.x:
            new_opening_p = border_opening_p.with_y(max(border_opening_p.y, opening_p.y))
            new_closing_p = closing_p.with_y(min(border_closing_p.y, closing_p.y))
            return new_opening_p, new_closing_p
        elif border_closing_p.y + 1 == opening_p.y:
            new_opening_p = border_opening_p.with_x(max(border_opening_p.x, opening_p.x))
            new_closing_p = closing_p.with_x(min(border_closing_p.x, closing_p.x))
            return new_opening_p, new_closing_p
        elif border_opening_p.x - 1 == closing_p.x:
            new_opening_p = opening_p.with_y(max(border_opening_p.y, opening_p.y))
            new_closing_p = border_closing_p.with_y(min(border_closing_p.y, closing_p.y))
            return new_opening_p, new_closing_p
        elif border_opening_p.y == closing_p.y + 1:
            new_opening_p = opening_p.with_x(max(border_opening_p.x, opening_p.x))
            new_closing_p = border_closing_p.with_x(min(border_closing_p.x, closing_p.x))
            return new_opening_p, new_closing_p
        else:
            return None

    def _should_remove_place(
            self,
            border_opening_p: Point,
            border_closing_p: Point,
            places: DefaultDict[Point, Set[Point]]
    ) -> bool:
        for ext_opening_p, ext_closing_ps in places.items():
            for ext_closing_p in ext_closing_ps:
                if self._place_is_inside(border_opening_p, border_closing_p, ext_opening_p, ext_closing_p):
                    return True
        return False

    def _save_places(self, places: DefaultDict[Point, Set[Point]]) -> None:
        for opening_p, closing_ps in places.items():
            for closing_p in closing_ps:
                self._places[opening_p].add(closing_p)

    @staticmethod
    def _place_is_inside(p: Point, max_p: Point, other_p: Point, other_max_p: Point) -> bool:
        return p.x >= other_p.x and p.y >= other_p.y and max_p.x <= other_max_p.x and max_p.y <= other_max_p.y
