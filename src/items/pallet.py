from typing import Tuple

from src.items.color_volume_item import ColorVolumeItem
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.volume_parameters import VolumeParameters


class Pallet(ColorVolumeItem):
    _parameters: PalletParameters

    def __init__(self, parameters: PalletParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters

    @property
    def weight(self) -> int:
        return self._parameters.weight

    @property
    def lifting_capacity(self) -> int:
        return self._parameters.lifting_capacity

    def compute_part_weight(self, volume: int) -> float:
        shipment_part = volume / self.compute_volume()
        return shipment_part * self.weight

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight, self.lifting_capacity

    def _get_parameters(self) -> VolumeParameters:
        return self._parameters

    def __str__(self) -> str:
        return f'Pallet: ({self._key()})'
