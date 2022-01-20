from abc import ABC, abstractmethod


class WeightParameters(ABC):
    @abstractmethod
    def weight(self) -> int:
        pass
