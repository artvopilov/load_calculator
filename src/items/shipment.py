from typing import Tuple

from src.items.color_item import ColorItem
from src.items.volume_item import VolumeItem
from src.items.weight_item import WeightItem
from src.parameters.shipment_parameters import ShipmentParameters


class Shipment(VolumeItem, WeightItem, ColorItem):
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
        shipment_part = volume / self.compute_volume()
        return shipment_part * self.weight

    def compute_volume(self) -> int:
        return self.length * self.width * self.height

    def _key(self) -> Tuple:
        return self.id, self.length, self.width, self.height, self.weight, self.color

    def __str__(self) -> str:
        return f'Shipment: ({self._key()})'
