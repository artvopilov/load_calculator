from abc import ABC, abstractmethod


class VolumeParameters(ABC):
    @property
    @abstractmethod
    def length(self) -> int:
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass
