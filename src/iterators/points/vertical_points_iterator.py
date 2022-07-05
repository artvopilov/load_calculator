from typing import Tuple

from src.loading.point import Point
from src.iterators.points.points_iterator import PointsIterator


class VerticalPointsIterator(PointsIterator):
    def _get_point_order_key(self, point: Point) -> Tuple:
        return point.x, point.y, point.z
