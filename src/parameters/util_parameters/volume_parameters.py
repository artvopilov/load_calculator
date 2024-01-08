import math
from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters
from src.loading.point.point import Point


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

    def get_loading_length(self) -> int:
        return int(self.length * math.sqrt((1 + self._extension)))

    def get_length_diff(self) -> float:
        return self.get_loading_length() - self.length

    def get_loading_width(self) -> int:
        return int(self.width * math.sqrt((1 + self._extension)))

    def get_width_diff(self) -> float:
        return self.get_loading_width() - self.width

    def compute_area(self) -> int:
        return self.length * self.width

    def compute_loading_area(self) -> float:
        return self.compute_area() * (1 + self._extension)

    def compute_volume(self) -> int:
        return self.compute_area() * self.height

    def compute_loading_volume(self) -> float:
        return self.compute_loading_area() * self.height

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.extension

    def __str__(self) -> str:
        return f'Volume parameters: ({self._key()})'


