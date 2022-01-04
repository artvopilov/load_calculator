from abc import ABC, abstractmethod


class LoadableItem(ABC):
    _id_: int
    _length: int
    _width: int
    _height: int
    _weight: int

    def __init__(self,  id_: int, length: int, width: int, height: int, weight: int):
        self._id_ = id_
        self._length = length
        self._width = width
        self._height = height
        self._weight = weight

    @property
    def id(self) -> int:
        return self._id_

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def weight(self) -> int:
        return self._weight

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._key() == other._key()
        return NotImplemented

    def __hash__(self):
        return hash(self._key())

    @abstractmethod
    def _key(self):
        ...

    @abstractmethod
    def __str__(self):
        ...

