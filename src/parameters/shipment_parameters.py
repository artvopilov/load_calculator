from itertools import permutations
from typing import Tuple, List

from src.parameters.util_parameters.color_parameters import ColorParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.parameters.util_parameters.weight_parameters import WeightParameters


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

    def from_volume_params(self, length: int, width: int, height: int) -> 'ShipmentParameters':
        return ShipmentParameters(length, width, height, self.weight, self.color, self.can_cant, self._can_stack)

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
        return self._weight

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

    def __str__(self) -> str:
        return f'Shipment parameters: ({self._key()})'

    def get_volume_params_variations(self) -> List['ShipmentParameters']:
        if not self.can_cant:
            return [self]
        variations = []
        for p in permutations([self.length, self.width, self.height]):
            variations.append(self.from_volume_params(p[0], p[1], p[2]))
        return variations

    def get_smallest_area_params(self) -> 'ShipmentParameters':
        smallest_area_params, smallest_area = None, None
        for params in self.get_volume_params_variations():
            if not smallest_area_params or params.compute_area() < smallest_area:
                smallest_area = params.compute_area()
                smallest_area_params = params
        return smallest_area_params
