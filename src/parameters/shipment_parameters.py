from itertools import permutations
from typing import Tuple, List, Dict

from src.parameters.util_parameters.item_parameters import ItemParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ShipmentParameters(VolumeParameters, ItemParameters):
    _name: str
    _form_type: str
    _weight: int
    _color: str
    _can_cant: bool
    _can_stack: bool

    def __init__(self,
                 id_: int,
                 name: str,
                 form_type: str,
                 length: int,
                 width: int,
                 height: int,
                 weight: int,
                 color: str,
                 can_cant: bool,
                 can_stack: bool) -> None:
        ItemParameters.__init__(self, id_)
        VolumeParameters.__init__(self, length, width, height)
        self._name = name
        self._form_type = form_type
        self._weight = weight
        self._color = color
        self._can_cant = can_cant
        self._can_stack = can_stack

    def with_volume_params(self, length: int, width: int, height: int) -> 'ShipmentParameters':
        return ShipmentParameters(self.id, self.name, self.form_type, length, width, height, self.weight,
                                  self.color, self.can_cant, self._can_stack)

    @property
    def name(self) -> str:
        return self._name

    @property
    def form_type(self) -> str:
        return self._form_type

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

    def build_response(self) -> Dict:
        return {
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'type': self.form_type,
            'stack': self.can_stack,
            'cant': self.can_cant,
        }
