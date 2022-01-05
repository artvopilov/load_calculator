from abc import ABC, abstractmethod
from typing import Tuple

from src.parameters.volume_parameters import VolumeParameters


class VolumeItem(ABC):
    _id_: int

    def __init__(self,  id_: int):
        self._id_ = id_

    @property
    def id(self) -> int:
        return self._id_

    @property
    def length(self) -> int:
        return self._get_parameters().length

    @property
    def width(self) -> int:
        return self._get_parameters().width

    @property
    def height(self) -> int:
        return self._get_parameters().height

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
    def _get_parameters(self) -> VolumeParameters:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

