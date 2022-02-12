from itertools import permutations
from typing import Tuple, List

from src.parameters.color_parameters import ColorParameters
from src.parameters.volume_parameters import VolumeParameters
from src.parameters.weight_parameters import WeightParameters


class ShipmentParameters(VolumeParameters, WeightParameters, ColorParameters):
    _length: int
    _width: int
    _height: int
    _weight: int
    _color: str
    _can_cant: bool
    _can_stack: bool

    def __init__(self,
                 length: int,
                 width: int,
                 height: int,
                 weight: int,
                 color: str,
                 can_cant: bool,
                 can_stack: bool) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._weight = weight
        self._color = color
        self._can_cant = can_cant
        self._can_stack = can_stack

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
    def color(self) -> str:
        return self._color

    @property
    def can_cant(self) -> bool:
        return self._can_cant

    @property
    def can_stack(self) -> bool:
        return self._can_stack

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.weight, self.color

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key())

    def swap_length_width_height(self) -> List['ShipmentParameters']:
        parameters = []
        for p in permutations([self.length, self.width, self.height]):
            if p[0] == self.length and p[1] == self.width and p[2] == self.height:
                continue
            parameters.append(ShipmentParameters(
                p[0],
                p[1],
                p[2],
                self.weight,
                self.color,
                self.can_cant,
                self.can_stack))
        return parameters
