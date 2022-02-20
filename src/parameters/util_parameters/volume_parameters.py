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

    def compute_volume(self) -> int:
        return self.length * self.width * self.height

    def compute_area(self) -> int:
        return self.length * self.width
