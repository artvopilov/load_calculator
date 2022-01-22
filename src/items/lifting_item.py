from abc import abstractmethod

from src.items.item import Item
from src.parameters.lifting_parameters import LiftingParameters


class LiftingItem(Item[LiftingParameters]):
    @property
    @abstractmethod
    def parameters(self) -> LiftingParameters:
        ...
