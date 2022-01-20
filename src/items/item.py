from abc import ABC, abstractmethod
from typing import Tuple


class Item(ABC):
    _id_: int

    def __init__(self,  id_: int):
        self._id_ = id_

    @property
    def id(self) -> int:
        return self._id_

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self):
        return hash(self._key())

    @abstractmethod
    def _key(self) -> Tuple:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

