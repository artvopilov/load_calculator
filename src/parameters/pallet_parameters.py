from itertools import permutations
from typing import List

from src.parameters.color_parameters import ColorParameters
from src.parameters.lifting_parameters import LiftingParameters
from src.parameters.volume_parameters import VolumeParameters
from src.parameters.weight_parameters import WeightParameters


class PalletParameters(VolumeParameters, WeightParameters, LiftingParameters, ColorParameters):
    _length: int
    _width: int
    _height: int
    _weight: int
    _lifting_capacity: int
    _color: str

    def __init__(self, length: int, width: int, height: int, weight: int, lifting_capacity: int, color: str) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._weight = weight
        self._lifting_capacity = lifting_capacity
        self._color = color

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
    def weight(self) -> int:
        return self._width

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity

    @property
    def color(self) -> str:
        return self._color

    def swap_length_width(self) -> List['PalletParameters']:
        parameters = []
        for p in permutations([self.length, self.width]):
            parameters.append(PalletParameters(p[0], p[1], self.height, self.weight, self.lifting_capacity, self.color))
        return parameters
