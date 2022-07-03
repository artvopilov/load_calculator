from collections import defaultdict
from typing import Tuple, DefaultDict, Set, Optional

from src.loading.coordinate import Coordinate
from src.loading.direction import Direction
from src.loading.point import Point
from src.loading.points_for_update import PointsForUpdate
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class LoadablePointsManager:
    _loadable_point_to_max_points: DefaultDict[Point, Set[Point]]
    _params: VolumeParameters

    def __init__(self, params: VolumeParameters) -> None:
        self._loadable_point_to_max_points = defaultdict(set)
        self._params = params
        self.reset()

    @property
    def loadable_point_to_max_points(self) -> DefaultDict[Point, Set[Point]]:
        return self._loadable_point_to_max_points

    def reset(self) -> None:
        self._loadable_point_to_max_points.clear()
        loadable_point = Point(0, 0, 0)
        loadable_max_point = Point(self._params.length - 1, self._params.width - 1, self._params.height - 1)
        self._loadable_point_to_max_points[loadable_point].add(loadable_max_point)

    def get_max_points(self, point: Point) -> Set[Point]:
        return self._loadable_point_to_max_points[point]

    def update_points(self, loading_p: Point, loading_max_p: Point, update_top_points: bool) -> None:
        points_for_update = self._select_points_for_update(loading_p, loading_max_p)
        self._update_bottom_points(
            loading_p,
            loading_max_p,
            points_for_update.bottom_inner_points,
            points_for_update.bottom_border_points)
        if update_top_points:
            self._update_top_points(loading_p, loading_max_p, points_for_update.top_border_points)

    def _select_points_for_update(self, loading_p: Point, loading_max_p: Point) -> PointsForUpdate:
        points_for_update = PointsForUpdate()
        for p, max_points in self._loadable_point_to_max_points.items():
            if not self._point_meets_update(p, loading_p, loading_max_p):
                continue
            for max_p in max_points:
                if not self._max_point_meets_update(max_p, loading_p):
                    continue
                points_for_update.add_point(p, max_p, loading_p, loading_max_p)
        return points_for_update

    def _update_bottom_points(
            self,
            loading_p: Point,
            loading_max_p: Point,
            inner_points: DefaultDict[Point, Set[Point]],
            border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        for inner_p, inner_max_points in inner_points.items():
            for inner_max_p in inner_max_points:
                self._update_inner_bottom_point(loading_p, loading_max_p, inner_p, inner_max_p, border_points)

    def _update_inner_bottom_point(
            self,
            loading_p: Point,
            loading_max_p: Point,
            inner_p: Point,
            inner_max_p: Point,
            border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        self._loadable_point_to_max_points[inner_p].remove(inner_max_p)

        if inner_p.x < loading_p.x:
            new_max_p = inner_max_p.with_x(loading_p.x - 1)
            self.try_insert_bottom_point(inner_p, new_max_p, border_points, Coordinate.X, Coordinate.Y)
        if inner_max_p.x > loading_max_p.x:
            new_p = inner_p.with_x(loading_max_p.x + 1)
            self.try_insert_bottom_point(new_p, inner_max_p, border_points, Coordinate.X, Coordinate.Y)
        if loading_p.y > inner_p.y:
            new_max_p = inner_max_p.with_y(loading_p.y - 1)
            self.try_insert_bottom_point(inner_p, new_max_p, border_points, Coordinate.Y, Coordinate.X)
        if inner_max_p.y > loading_max_p.y:
            new_p = inner_p.with_y(loading_max_p.y + 1)
            self.try_insert_bottom_point(new_p, inner_max_p, border_points, Coordinate.Y, Coordinate.X)

    def try_insert_bottom_point(
            self,
            p: Point,
            max_p: Point,
            border_points: DefaultDict[Point, Set[Point]],
            c_clip: Coordinate,
            c_consume: Coordinate
    ) -> None:
        border_points_for_remove = defaultdict(set)
        for border_p, border_max_points in border_points.items():
            for border_max_p in border_max_points:
                if border_p.get_coordinate(c_clip) != p.get_coordinate(c_clip) \
                        or border_max_p.get_coordinate(c_clip) != max_p.get_coordinate(c_clip):
                    continue
                if border_p.get_coordinate(c_consume) <= p.get_coordinate(c_consume) \
                        and border_max_p.get_coordinate(c_consume) >= max_p.get_coordinate(c_consume):
                    return
                elif border_p.get_coordinate(c_consume) >= p.get_coordinate(c_consume) \
                        and border_max_p.get_coordinate(c_consume) <= max_p.get_coordinate(c_consume):
                    border_points_for_remove[border_p].add(border_max_p)
        self._insert_bottom_point(p, max_p, border_points, border_points_for_remove)

    def _insert_bottom_point(
            self,
            p: Point,
            max_p: Point,
            border_points: DefaultDict[Point, Set[Point]],
            border_points_for_remove: DefaultDict[Point, Set[Point]]
    ) -> None:
        border_points[p].add(max_p)
        self._loadable_point_to_max_points[p].add(max_p)
        for border_p, border_max_points in border_points_for_remove.items():
            border_points[border_p] -= border_max_points
            self._loadable_point_to_max_points[border_p] -= border_max_points

    def _update_top_points(
            self,
            loading_p: Point,
            loading_max_p: Point,
            top_border_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        new_point = loading_p.with_z(loading_max_p.z + 1)
        new_max_point = loading_max_p.with_z(self._params.height - 1)

        extension_points = defaultdict(set)
        extension_points[new_point].add(new_max_point)

        self._extend_top_border_points(top_border_points, extension_points)

        self._remove_extra_top_border_points(top_border_points, extension_points)

        self._save_extension_points(extension_points)

    def _extend_top_border_points(
            self,
            top_border_points: DefaultDict[Point, Set[Point]],
            extension_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        for border_p, border_max_points in top_border_points.items():
            for border_max_p in border_max_points:
                extension_points_for_add = defaultdict(set)
                extension_points_for_remove = defaultdict(set)

                for extension_p, extension_max_points in extension_points.items():
                    for extension_max_p in extension_max_points:
                        new_points = self._try_extend_top_point(border_p, border_max_p, extension_p, extension_max_p)
                        if new_points is not None:
                            new_p, new_max_p = new_points
                            extension_points_for_add[new_p].add(new_max_p)
                            if self._point_is_inside(extension_p, extension_max_p, new_p, new_max_p):
                                extension_points_for_remove[extension_p].add(extension_max_p)

                for p, max_points in extension_points_for_add.items():
                    extension_points[p] |= max_points
                for p, max_points in extension_points_for_remove.items():
                    extension_points[p] -= max_points

    def _remove_extra_top_border_points(
            self,
            top_border_points: DefaultDict[Point, Set[Point]],
            extension_points: DefaultDict[Point, Set[Point]]
    ) -> None:
        for border_p, border_max_points in top_border_points.items():
            for border_max_p in border_max_points:
                if self._should_remove_top_border_point(border_p, border_max_p, extension_points):
                    self._loadable_point_to_max_points[border_p].remove(border_max_p)

    def _save_extension_points(self, extension_points: DefaultDict[Point, Set[Point]]) -> None:
        for extension_p, extension_max_points in extension_points.items():
            for extension_max_p in extension_max_points:
                self._loadable_point_to_max_points[extension_p].add(extension_max_p)

    def _try_extend_top_point(
            self,
            border_p: Point,
            border_max_p: Point,
            extension_p: Point,
            extension_max_p: Point
    ) -> Optional[Tuple[Point, Point]]:
        if self._is_extendable_up(border_max_p, extension_p, Coordinate.X):
            return self._extend_top_point(border_p, border_max_p, extension_p, extension_max_p, Coordinate.Y, Direction.UP)
        elif self._is_extendable_up(border_max_p, extension_p, Coordinate.Y):
            return self._extend_top_point(border_p, border_max_p, extension_p, extension_max_p, Coordinate.X, Direction.UP)
        elif self._is_extendable_down(border_p, extension_max_p, Coordinate.X):
            return self._extend_top_point(border_p, border_max_p, extension_p, extension_max_p, Coordinate.Y, Direction.DOWN)
        elif self._is_extendable_down(border_p, extension_max_p, Coordinate.Y):
            return self._extend_top_point(border_p, border_max_p, extension_p, extension_max_p, Coordinate.X, Direction.DOWN)

    def _extend_top_point(
            self,
            p: Point,
            max_p: Point,
            extension_p: Point,
            extension_max_p: Point,
            c: Coordinate,
            d: Direction
    ) -> Tuple[Point, Point]:
        if d == Direction.UP:
            return self._create_up_points(p, max_p, extension_p, extension_max_p, c)
        else:
            return self._create_down_points(p, max_p, extension_p, extension_max_p, c)

    def _should_remove_top_border_point(
            self,
            border_p: Point,
            border_max_p: Point,
            extension_points: DefaultDict[Point, Set[Point]]
    ) -> bool:
        for extension_p, extension_max_points in extension_points.items():
            for extension_max_p in extension_max_points:
                if self._point_is_inside(border_p, border_max_p, extension_p, extension_max_p):
                    return True
        return False

    @staticmethod
    def _point_is_inside(p: Point, max_p: Point, new_p: Point, new_max_p: Point) -> bool:
        return p.x >= new_p.x and p.y >= new_p.y and max_p.x <= new_max_p.x and max_p.y <= new_max_p.y

    @staticmethod
    def _is_extendable_up(max_p: Point, extension_p: Point, c: Coordinate) -> bool:
        return max_p.get_coordinate(c) + 1 == extension_p.get_coordinate(c)

    @staticmethod
    def _is_extendable_down(p: Point, extension_max_p: Point, c: Coordinate) -> bool:
        return p.get_coordinate(c) == extension_max_p.get_coordinate(c) + 1

    @staticmethod
    def _create_up_points(
            p: Point,
            max_p: Point,
            extension_p: Point,
            extension_max_p: Point,
            c: Coordinate
    ) -> Tuple[Point, Point]:
        new_p = p.with_coordinate(c, max(p.get_coordinate(c), extension_p.get_coordinate(c)))
        new_max_p = extension_max_p.with_coordinate(c, min(max_p.get_coordinate(c), extension_max_p.get_coordinate(c)))
        return new_p, new_max_p

    @staticmethod
    def _create_down_points(
            p: Point,
            max_p: Point,
            extension_p: Point,
            extension_max_p: Point,
            c: Coordinate
    ) -> Tuple[Point, Point]:
        new_p = extension_p.with_coordinate(c, max(p.get_coordinate(c), extension_p.get_coordinate(c)))
        new_max_p = max_p.with_coordinate(c, min(max_p.get_coordinate(c), extension_max_p.get_coordinate(c)))
        return new_p, new_max_p

    @staticmethod
    def _point_meets_update(p: Point, loading_p: Point, loading_max_p: Point) -> bool:
        if p.z != loading_p.z and p.z != loading_max_p.z + 1:
            return False
        if p.x > loading_max_p.x + 1 or p.y > loading_max_p.y + 1:
            return False
        return True

    @staticmethod
    def _max_point_meets_update(max_p: Point, loading_p: Point) -> bool:
        return max_p.x + 1 >= loading_p.x or max_p.y + 1 >= loading_p.y

