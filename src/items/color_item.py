from abc import abstractmethod

from src.items.item import Item
from src.parameters.color_parameters import ColorParameters


class ColorItem(Item[ColorParameters]):
    @property
    @abstractmethod
    def parameters(self) -> ColorParameters:
        ...
