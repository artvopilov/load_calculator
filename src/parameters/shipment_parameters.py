from itertools import permutations
from typing import Tuple, List

from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ShipmentParameters(VolumeParameters):
    _name: str
    _weight: int
    _color: str
    _can_cant: bool
    _can_stack: bool

    def __init__(self,
                 name: str,
                 length: int,
                 width: int,
                 height: int,
                 weight: int,
                 color: str,
                 can_cant: bool,
                 can_stack: bool) -> None:
        VolumeParameters.__init__(self, length, width, height)
        self._name = name
        self._weight = weight
        self._color = color
        self._can_cant = can_cant
        self._can_stack = can_stack

    def with_volume_params(self, length: int, width: int, height: int) -> 'ShipmentParameters':
        return ShipmentParameters(self.name, length, width, height, self.weight,
                                  self.color, self.can_cant, self._can_stack)

    @property
    def name(self) -> str:
        return self._name

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
        return self.name, self.length, self.width, self.height, self.weight, self.color

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
            variations.append(self.with_volume_params(p[0], p[1], p[2]))
        return sorted(variations, key=lambda v: sorted([v.length, v.width, v.height]), reverse=True)

    def get_smallest_area_params(self) -> 'ShipmentParameters':
        smallest_area_params, smallest_area = None, None
        for params in self.get_volume_params_variations():
            if not smallest_area_params or params.compute_area() < smallest_area:
                smallest_area = params.compute_area()
                smallest_area_params = params
        return smallest_area_params
