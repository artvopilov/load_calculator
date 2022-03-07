from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters


class VolumeParameters(Parameters):
    _length: int
    _width: int
    _height: int

    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height

    def with_length(self, length: int) -> 'VolumeParameters':
        return VolumeParameters(length, self.width, self.height)

    def with_width(self, width: int) -> 'VolumeParameters':
        return VolumeParameters(self.length, width, self.height)

    def with_height(self, height: int) -> 'VolumeParameters':
        return VolumeParameters(self.length, self.width, height)

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def _key(self) -> Tuple:
        return self.length, self.width, self.height

    def __str__(self) -> str:
        return f'Volume parameters: ({self._key()})'

    def compute_volume(self) -> int:
        return self.length * self.width * self.height

    def compute_area(self) -> int:
        return self.length * self.width


