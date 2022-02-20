from abc import ABC, abstractmethod


class ColorParameters(ABC):
    @property
    @abstractmethod
    def color(self) -> str:
        pass
