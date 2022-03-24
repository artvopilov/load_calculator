from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters


class ItemParameters(Parameters):
    _id: int

    def __init__(self, id_: int) -> None:
        self._id = id_

    @property
    def id(self):
        return self._id

    def _key(self) -> Tuple:
        return (self._id,)

    def __str__(self) -> str:
        return f'Item parameters: ({self._key()})'

