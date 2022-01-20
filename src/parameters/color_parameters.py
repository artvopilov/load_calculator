from abc import ABC, abstractmethod


class ColorParameters(ABC):
    @abstractmethod
    def color(self) -> str:
        pass
