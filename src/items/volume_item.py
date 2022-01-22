from abc import abstractmethod

from src.items.item import Item
from src.parameters.volume_parameters import VolumeParameters


class VolumeItem(Item[VolumeParameters]):
    @property
    @abstractmethod
    def parameters(self) -> VolumeParameters:
        ...
