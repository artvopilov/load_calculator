from typing import Tuple

from src.items.color_item import ColorItem
from src.items.lifting_item import LiftingItem
from src.items.volume_item import VolumeItem
from src.items.weight_item import WeightItem
from src.parameters.pallet_parameters import PalletParameters


class Pallet(VolumeItem, WeightItem, LiftingItem, ColorItem):
    _id_: int
    _parameters: PalletParameters

    def __init__(self, parameters: PalletParameters, id_: int):
        self._id_ = id_
        self._parameters = parameters

    @property
    def id(self) -> int:
        return self._id_

    @property
    def length(self) -> int:
        return self._parameters.length

    @property
    def width(self) -> int:
        return self._parameters.width

    @property
    def height(self) -> int:
        return self._parameters.height

    @property
    def weight(self) -> int:
        return self._parameters.weight

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    @property
    def color(self) -> str:
        return self._parameters.color

    @property
    def parameters(self) -> PalletParameters:
        return self._parameters

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight, self.lifting_capacity, self.color

    def __str__(self) -> str:
        return f'Pallet: ({self._key()})'
