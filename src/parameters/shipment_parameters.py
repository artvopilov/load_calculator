from typing import Tuple

from src.parameters.color_parameters import ColorParameters
from src.parameters.volume_parameters import VolumeParameters
from src.parameters.weight_parameters import WeightParameters


class ShipmentParameters(VolumeParameters, WeightParameters, ColorParameters):
    _length: int
    _width: int
    _height: int
    _weight: int
    _color: str

    def __init__(self, length: int, width: int, height: int, weight: int, color: str) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._weight = weight
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
    def color(self) -> str:
        return self._color

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.weight

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key())
