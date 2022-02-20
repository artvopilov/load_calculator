from abc import abstractmethod

from src.items.util_items.item import Item
from src.parameters.util_parameters.color_parameters import ColorParameters


class ColorItem(Item[ColorParameters]):
    @property
    @abstractmethod
    def parameters(self) -> ColorParameters:
        ...
