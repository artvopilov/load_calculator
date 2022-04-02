from abc import abstractmethod, ABC
from typing import Dict

from src.items.util_items.item import Item
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class VolumeItem(ABC):
    _parameters: VolumeParameters

    def __init__(self, parameters: VolumeParameters):
        self._parameters = parameters

    @property
    def length(self) -> int:
        return self._parameters.length

    @property
    def width(self) -> int:
        return self._parameters.width

    @property
    def height(self) -> int:
        return self._parameters.height
