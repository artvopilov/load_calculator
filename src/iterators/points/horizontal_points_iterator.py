from typing import Tuple

from src.loading.point import Point
from src.iterators.points.points_iterator import PointsIterator


class HorizontalPointsIterator(PointsIterator):
    def _get_point_order_key(self, point: Point) -> Tuple:
        return point.z, point.x, point.y
