from abc import abstractmethod

from src.items.volume_item import VolumeItem
from src.parameters.color_volume_parameters import ColorVolumeParameters


class ColorVolumeItem(VolumeItem):
    def __init__(self, id_: int):
        super().__init__(id_)

    @property
    def color(self) -> str:
        return self._get_parameters().color

    @abstractmethod
    def _get_parameters(self) -> ColorVolumeParameters:
        ...
