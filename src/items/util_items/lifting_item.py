from abc import abstractmethod

from src.items.util_items.item import Item
from src.parameters.util_parameters.lifting_parameters import LiftingParameters


class LiftingItem(Item[LiftingParameters]):
    @property
    @abstractmethod
    def parameters(self) -> LiftingParameters:
        ...
