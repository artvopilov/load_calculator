from abc import abstractmethod

from src.items.item import Item
from src.parameters.weight_parameters import WeightParameters


class WeightItem(Item[WeightParameters]):
    @property
    @abstractmethod
    def parameters(self) -> WeightParameters:
        ...
