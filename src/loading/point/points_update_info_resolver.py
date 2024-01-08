from collections import defaultdict
from typing import DefaultDict, Set

from src.loading.point.point import Point
from src.loading.point.points_update_info import PointsUpdateInfo


class PointsUpdateInfoResolver:
    def resolve(
            self,
            points: DefaultDict[Point, Set[Point]],
            used_opening_p: Point,
            used_closing_p: Point
    ) -> PointsUpdateInfo:
        """
        Bottom slots can be cropped with new shipment. Bottom border slots can grab cropped slots.
        Top slots can be extended with new area on top of new shipment.
        Other slots are not affected since shipment can be placed only on top of another shipment or ground
        and there are no slots hanging in between.
        """

        bottom_points = defaultdict(set)
        bottom_border_points = defaultdict(set)
        top_border_points = defaultdict(set)

        for opening_p, closing_ps in points.items():
            if not self._opening_point_meets_update(opening_p, used_opening_p, used_closing_p):
                continue
            for closing_p in closing_ps:
                if not self._closing_point_meets_update(closing_p, used_opening_p):
                    continue

                if opening_p.z == used_opening_p.z:
                    if self._is_border_point(opening_p, closing_p, used_opening_p, used_closing_p):
                        bottom_border_points[opening_p].add(closing_p)
                    else:
                        bottom_points[opening_p].add(closing_p)
                else:
                    top_border_points[opening_p].add(closing_p)

        return PointsUpdateInfo(bottom_points, bottom_border_points, top_border_points)

    @staticmethod
    def _opening_point_meets_update(opening_p: Point, used_opening_p: Point, used_closing_p: Point) -> bool:
        if opening_p.z != used_opening_p.z and opening_p.z != used_closing_p.z + 1:
            return False
        if opening_p.x > used_closing_p.x + 1 or opening_p.y > used_closing_p.y + 1:
            return False
        return True

    @staticmethod
    def _closing_point_meets_update(closing_p: Point, used_opening_p: Point) -> bool:
        return closing_p.x >= used_opening_p.x - 1 and closing_p.y >= used_opening_p.y - 1

    @staticmethod
    def _is_border_point(opening_p: Point, closing_p: Point, used_opening_p: Point, used_closing_p: Point) -> bool:
        return (opening_p.x == used_closing_p.x + 1
                or opening_p.y == used_closing_p.y + 1
                or closing_p.x == used_opening_p.x - 1
                or closing_p.y == used_opening_p.y - 1)
