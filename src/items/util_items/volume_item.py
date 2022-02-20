from abc import abstractmethod

from src.items.util_items.item import Item
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class VolumeItem(Item[VolumeParameters]):
    @property
    @abstractmethod
    def parameters(self) -> VolumeParameters:
        ...
