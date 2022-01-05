from typing import Tuple

from src.parameters.volume_parameters import VolumeParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.items.volume_item import VolumeItem


class Shipment(VolumeItem):
    _parameters: ShipmentParameters

    def __init__(self, parameters: ShipmentParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters

    @property
    def weight(self) -> int:
        return self._parameters.weight

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight

    def _get_parameters(self) -> VolumeParameters:
        return self._parameters

    def __str__(self) -> str:
        return f'Shipment: ({self._key()})'
