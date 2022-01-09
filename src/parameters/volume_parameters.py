from abc import ABC
from itertools import permutations
from typing import List


class VolumeParameters(ABC):
    _length: int
    _width: int
    _height: int

    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def swap_length_width(self) -> List['VolumeParameters']:
        parameters = []
        for p in permutations([self.length, self.width]):
            parameters.append(VolumeParameters(p[0], p[1], self.height))
        return parameters

    def swap_length_width_height(self) -> List['VolumeParameters']:
        parameters = []
        for p in permutations([self.length, self.width, self.height]):
            parameters.append(VolumeParameters(p[0], p[1], p[2]))
        return parameters


