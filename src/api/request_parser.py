from typing import Dict

from flask import Request

from src.items.item_fabric import ItemFabric
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class RequestParser:
    _item_fabric: ItemFabric

    def __init__(self, item_fabric: ItemFabric) -> None:
        self._item_fabric = item_fabric

    def parse_shipment_counts(self, request: Request) -> Dict:
        shipment_counts = {}
        for cargo in request.json['cargo']:
            shipment_params = self._create_shipment_params(cargo)
            shipment_counts[shipment_params] = cargo['number']
        return shipment_counts

    def parse_container_counts(self, request: Request) -> Dict:
        container_counts = {}
        for container in request.json['containers']:
            container_params = self._create_container_params(container)
            container_counts[container_params] = container['number']
        return container_counts

    def _create_shipment_params(self, cargo_request: Dict) -> ShipmentParameters:
        length = cargo_request['length']
        width = cargo_request['width']
        height = cargo_request['height']
        diameter = cargo_request['diameter']
        if diameter:
            length = diameter
            width = diameter
        return self._item_fabric.create_shipment_params(
            cargo_request['name'],
            cargo_request['type'],
            length,
            width,
            height,
            cargo_request['weight'],
            cargo_request['color'],
            cargo_request['stack'],
            cargo_request['height_as_height'],
            cargo_request['length_as_height'],
            cargo_request['width_as_height'])

    def _create_container_params(self, container_request) -> ContainerParameters:
        return self._item_fabric.create_container_params(
            container_request['type'],
            container_request['length'],
            container_request['width'],
            container_request['height'],
            container_request['weight'])
