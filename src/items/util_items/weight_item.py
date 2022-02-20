from abc import abstractmethod

from src.items.util_items.item import Item
from src.parameters.util_parameters.weight_parameters import WeightParameters


class WeightItem(Item[WeightParameters]):
    @property
    @abstractmethod
    def parameters(self) -> WeightParameters:
        ...
