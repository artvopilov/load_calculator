from src.parameters.volume_parameters import VolumeParameters
from typing import Tuple


class ShipmentParameters(VolumeParameters):
    _weight: int

    def __init__(self, length: int, width: int, height: int, weight: int) -> None:
        super().__init__(length, width, height)
        self._weight = weight

    @property
    def weight(self) -> int:
        return self._weight

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.weight

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key())
