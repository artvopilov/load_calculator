from typing import List

from src.parameters.color_volume_parameters import ColorVolumeParameters


class PalletParameters(ColorVolumeParameters):
    _weight: int
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, color: str, weight: int, lifting_capacity: int) -> None:
        super().__init__(length, width, height, color)
        self._weight = weight
        self._lifting_capacity = lifting_capacity

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity

    def swap_length_width(self) -> List['PalletParameters']:
        parameters = []
        for p in super().swap_length_width():
            parameters.append(PalletParameters(p.length, p.width, p.height, self.weight, self.lifting_capacity))
        return parameters
