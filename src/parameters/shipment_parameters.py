from typing import Tuple, List, Dict

from src.parameters.util_parameters.item_parameters import ItemParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ShipmentParameters(VolumeParameters, ItemParameters):
    _form_type: str
    _weight: int
    _color: str
    _can_stack: bool
    _height_as_height: bool
    _length_as_height: bool
    _width_as_height: bool

    def __init__(
            self,
            id_: int,
            name: str,
            form_type: str,
            length: int,
            width: int,
            height: int,
            weight: int,
            color: str,
            can_stack: bool,
            height_as_height: bool,
            length_as_height: bool,
            width_as_height: bool,
            extension: float
    ) -> None:
        ItemParameters.__init__(self, id_, name)
        VolumeParameters.__init__(self, length, width, height, extension)
        self._form_type = form_type
        self._weight = weight
        self._color = color
        self._can_stack = can_stack
        self._height_as_height = height_as_height
        self._length_as_height = length_as_height
        self._width_as_height = width_as_height

    def with_volume_params(self, length: int, width: int, height: int) -> 'ShipmentParameters':
        return ShipmentParameters(self.id, self.name, self.form_type, length, width, height,
                                  self.weight, self.color, self._can_stack,
                                  self.height_as_height, self.length_as_height, self.width_as_height,
                                  self.extension)

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
    def can_stack(self) -> bool:
        return self._can_stack

    @property
    def height_as_height(self) -> bool:
        return self._height_as_height

    @property
    def length_as_height(self) -> bool:
        return self._length_as_height

    @property
    def width_as_height(self) -> bool:
        return self._width_as_height

    def _key(self) -> Tuple:
        return self.id, self.name, self.form_type, self.length, self.width, self.height, self.weight

    def __str__(self) -> str:
        return f'Shipment parameters: ({self._key()})'

    def get_volume_params_variations(self) -> List['ShipmentParameters']:
        variations = []
        if self.height_as_height:
            variations.append(self.with_volume_params(self.length, self.width, self.height))
            variations.append(self.with_volume_params(self.width, self.length, self.height))
        if self.length_as_height:
            variations.append(self.with_volume_params(self.height, self.width, self.length))
            variations.append(self.with_volume_params(self.width, self.height, self.length))
        if self.width_as_height:
            variations.append(self.with_volume_params(self.length, self.height, self.width))
            variations.append(self.with_volume_params(self.height, self.length, self.width))
        return sorted(variations, key=lambda v: [v.length, v.width, v.height], reverse=True)

    def get_volume_params_sorted(self) -> List[int]:
        return sorted([self.length, self.width, self.height], reverse=True)

    def build_response(self) -> Dict:
        return {
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'type': self.form_type,
            'color': self.color,
            'stack': self.can_stack,
            'height_as_height': self.height_as_height,
            'length_as_height': self.length_as_height,
            'width_as_height': self.width_as_height,
            'extension': self.extension,
        }
