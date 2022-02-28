from typing import Tuple

from src.items.util_items.volume_item import VolumeItem
from src.parameters.shipment_parameters import ShipmentParameters


class Shipment(VolumeItem):
    _id_: int
    _parameters: ShipmentParameters

    def __init__(self, parameters: ShipmentParameters, id_: int):
        self._id_ = id_
        self._parameters = parameters

    @property
    def id(self) -> int:
        return self._id_

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
    def can_cant(self) -> bool:
        return self._parameters.can_cant

    @property
    def can_stack(self) -> bool:
        return self._parameters.can_stack

    @property
    def parameters(self) -> ShipmentParameters:
        return self._parameters

    def compute_part_weight(self, volume: int) -> float:
        shipment_part = volume / self.parameters.compute_volume()
        return shipment_part * self.weight

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight, self.color

    def __str__(self) -> str:
        return f'Shipment: ({self._key()})'
