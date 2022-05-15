from typing import Tuple

from src.items.util_items.item import Item
from src.items.util_items.name_item import NameItem
from src.items.util_items.volume_item import VolumeItem
from src.parameters.shipment_parameters import ShipmentParameters


class Shipment(Item[ShipmentParameters], VolumeItem, NameItem):
    _parameters: ShipmentParameters

    def __init__(self, parameters: ShipmentParameters, id_: int):
        Item.__init__(self, id_)
        VolumeItem.__init__(self, parameters)
        NameItem.__init__(self, parameters)

        self._parameters = parameters

    @property
    def weight(self) -> int:
        return self._parameters.weight

    @property
    def color(self) -> str:
        return self._parameters.color

    @property
    def can_stack(self) -> bool:
        return self._parameters.can_stack

    @property
    def parameters(self) -> ShipmentParameters:
        return self._parameters

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight, self.color

    def __str__(self) -> str:
        return f'Shipment: ({self._key()})'
