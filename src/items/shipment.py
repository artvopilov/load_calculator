from typing import Tuple

from src.items.item import Item
from src.parameters.shipment_parameters import ShipmentParameters


class Shipment(Item):
    _parameters: ShipmentParameters

    def __init__(self, parameters: ShipmentParameters, id_: int):
        super().__init__(id_)
        self._parameters = parameters

    @property
    def length(self) -> int:
        return self._parameters.length

    @property
    def width(self) -> int:
        return self._parameters.width

    @property
    def height(self) -> int:
        return self._parameters.height

    @property
    def weight(self) -> int:
        return self._parameters.weight

    @property
    def color(self) -> str:
        return self._parameters.color

    @property
    def parameters(self):
        return self._parameters

    def compute_part_weight(self, volume: int) -> float:
        shipment_part = volume / self.compute_volume()
        return shipment_part * self.weight

    def compute_volume(self) -> int:
        return self.length * self.width * self.height

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight

    def __str__(self) -> str:
        return f'Shipment: ({self._key()})'
