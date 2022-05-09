from typing import Tuple

from src.parameters.util_parameters.parameters import Parameters


class NameParameters(Parameters):
    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def _key(self) -> Tuple:
        return self._name,

    def __str__(self) -> str:
        return f'Item parameters: ({self._key()})'

