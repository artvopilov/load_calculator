from dataclasses import dataclass
from typing import Set, DefaultDict

from src.loading.point.point import Point


@dataclass
class PointsUpdateInfo:
    bottom_points: DefaultDict[Point, Set[Point]]
    bottom_border_points: DefaultDict[Point, Set[Point]]
    top_border_points: DefaultDict[Point, Set[Point]]
