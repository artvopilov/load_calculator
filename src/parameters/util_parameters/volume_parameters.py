import math
from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters
from src.items.point import Point


class VolumeParameters(Parameters):
    DEFAULT_EXTENSION: float = 0.0

    _length: int
    _width: int
    _height: int
    _extension: float

    def __init__(self, length: int, width: int, height: int, extension: float) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._extension = extension

    @staticmethod
    def from_points(point: Point, max_point: Point) -> 'VolumeParameters':
        return VolumeParameters(max_point.x - point.x + 1, max_point.y - point.y + 1, max_point.z - point.z + 1, 0)

    def with_length(self, length: int) -> 'VolumeParameters':
        return VolumeParameters(length, self.width, self.height, self.extension)

    def with_width(self, width: int) -> 'VolumeParameters':
        return VolumeParameters(self.length, width, self.height, self.extension)

    def with_height(self, height: int) -> 'VolumeParameters':
        return VolumeParameters(self.length, self.width, height, self.extension)

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def extension(self) -> float:
        return self._extension

    def get_extended_length(self) -> int:
        extended_area = self.compute_extended_area()
        area_extension = extended_area / self.compute_area()
        return int(self.length * math.sqrt(area_extension))

    def get_extended_width(self) -> int:
        extended_area = self.compute_extended_area()
        area_extension = extended_area / self.compute_area()
        return int(self.width * math.sqrt(area_extension))

    def get_extended_height(self) -> int:
        return int(self.height * (1 - self.extension))

    def compute_volume(self) -> int:
        return self.compute_area() * self.height

    def compute_area(self) -> int:
        return self.length * self.width

    def compute_extended_volume(self) -> float:
        return self.compute_extended_area() * self.height

    def compute_extended_area(self) -> float:
        volume = self.compute_volume()
        extended_height = self.get_extended_height()
        return volume / extended_height

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.extension

    def __str__(self) -> str:
        return f'Volume parameters: ({self._key()})'


