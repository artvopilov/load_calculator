from abc import ABC, abstractmethod
from typing import Tuple, TypeVar, Generic


T = TypeVar('T')


class Item(ABC, Generic[T]):
    @property
    @abstractmethod
    def id(self) -> int:
        ...

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self):
        return hash(self._key())

    @property
    @abstractmethod
    def parameters(self) -> T:
        ...

    @abstractmethod
    def _key(self) -> Tuple:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

