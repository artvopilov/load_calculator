from typing import Dict

from src.items.container import Container
from src.items.shipment import Shipment
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class ItemFabric:
    _current_id: int

    def __init__(self):
        self._current_id = 1

    def create_container(self, container_parameters: ContainerParameters):
        container = Container(container_parameters, self._current_id)
        self._current_id += 1
        return container

    def create_shipment(self, shipment_parameters: ShipmentParameters) -> Shipment:
        shipment = Shipment(shipment_parameters, self._current_id)
        self._current_id += 1
        return shipment

    def create_container_params(
            self,
            name: str,
            length: int,
            width: int,
            height: int,
            lifting_capacity: int
    ) -> ContainerParameters:
        container_params = ContainerParameters(self._current_id, name, length, width, height, lifting_capacity)
        self._current_id += 1
        return container_params

    def create_shipment_params(
            self,
            name: str,
            form_type: str,
            length: int,
            width: int,
            height: int,
            weight: int,
            color: str,
            can_stack: bool,
            height_as_height: bool,
            length_as_height: bool,
            width_as_height: bool
    ) -> ShipmentParameters:
        shipment_params = ShipmentParameters(self._current_id, name, form_type, length, width, height, weight, color,
                                             can_stack, height_as_height, length_as_height, width_as_height)
        self._current_id += 1
        return shipment_params
