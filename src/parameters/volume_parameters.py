from abc import ABC, abstractmethod


class VolumeParameters(ABC):
    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass
