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
            length: int,
            width: int,
            height: int,
            lifting_capacity: int
    ) -> ContainerParameters:
        container_params = ContainerParameters(self._current_id, length, width, height, lifting_capacity)
        self._current_id += 1
        return container_params

    def create_container_params(self, container_request) -> ContainerParameters:
        return self.create_container_params(container_request['length'], container_request['width'],
                                            container_request['height'], container_request['weight'])

    def create_shipment_params(
            self,
            name: str,
            length: int,
            width: int,
            height: int,
            weight: int,
            color: str,
            can_cant: bool,
            can_stack: bool
    ) -> ShipmentParameters:
        shipment_params = ShipmentParameters(self._current_id, name, length, width, height, weight, color, can_cant, can_stack)
        self._current_id += 1
        return shipment_params

    def create_shipment_params(self, cargo_request: Dict) -> ShipmentParameters:
        length = cargo_request['length']
        width = cargo_request['width']
        height = cargo_request['height']
        diameter = cargo_request['diameter']
        if diameter:
            length = diameter
            width = diameter
        return self.create_shipment_params(cargo_request['name'], length, width, height, cargo_request['weight'],
                                           cargo_request['color'], cargo_request['cant'], cargo_request['stack'])
