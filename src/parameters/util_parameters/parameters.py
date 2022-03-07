from abc import ABC, abstractmethod
from typing import Tuple


class Parameters(ABC):

    @abstractmethod
    def _key(self) -> Tuple:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key())
