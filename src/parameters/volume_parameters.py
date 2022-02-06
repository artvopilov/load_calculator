from abc import ABC, abstractmethod
from itertools import permutations
from typing import List


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
