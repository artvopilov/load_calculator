from abc import ABC, abstractmethod


class WeightParameters(ABC):
    @property
    @abstractmethod
    def weight(self) -> int:
        pass
