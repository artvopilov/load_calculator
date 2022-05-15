from abc import ABC

from src.parameters.util_parameters.item_parameters import NameParameters


class NameItem(ABC):
    _parameters: NameParameters

    def __init__(self, parameters: NameParameters) -> None:
        self._parameters = parameters

    @property
    def name(self) -> str:
        return self._parameters.name
