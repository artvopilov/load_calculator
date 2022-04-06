from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters


class ItemParameters(Parameters):
    _id: int
    _name: str

    def __init__(self, id_: int, name: str) -> None:
        self._id = id_
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def _key(self) -> Tuple:
        return self._id, self._name

    def __str__(self) -> str:
        return f'Item parameters: ({self._key()})'

