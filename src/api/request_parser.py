from typing import Dict, Optional

from flask import Request

from src.api.request_data import RequestData
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class RequestParser:
    def __init__(self) -> None:
        pass

    def parse(self, request: Request) -> RequestData:
        shipment_params_to_count = self._parse_shipment_params_to_count(request)
        container_params_to_count = self._parse_container_params_to_count(request)
        loading_type_name = self._parse_loading_type_name(request)
        return RequestData(shipment_params_to_count, container_params_to_count, loading_type_name)

    def _parse_shipment_params_to_count(self, request: Request) -> Dict[ShipmentParameters, int]:
        shipment_counts = {}
        for cargo in request.json['cargo']:
            shipment_params = self._create_shipment_params(cargo)
            shipment_counts[shipment_params] = cargo['number']
        return shipment_counts

    def _parse_container_params_to_count(self, request: Request) -> Optional[Dict[ContainerParameters, int]]:
        if 'containers' not in request.json:
            return None
        container_counts = {}
        for container in request.json['containers']:
            container_params = self._create_container_params(container)
            container_counts[container_params] = container['number']
        return container_counts

    @staticmethod
    def _parse_loading_type_name(request: Request) -> Optional[str]:
        if 'loading_type' in request.json:
            return request.json['loading_type']
        return None

    @staticmethod
    def _create_shipment_params(cargo_request: Dict) -> ShipmentParameters:
        length = cargo_request['length']
        width = cargo_request['width']
        height = cargo_request['height']
        diameter = cargo_request.get('diameter', None)
        if diameter:
            length = diameter
            width = diameter
        extension = VolumeParameters.DEFAULT_EXTENSION
        if 'extension' in cargo_request:
            extension = cargo_request['extension']
        return ShipmentParameters(
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
            cargo_request['width_as_height'],
            extension)

    @staticmethod
    def _create_container_params(container_request: Dict) -> ContainerParameters:
        return ContainerParameters(
            container_request['type'],
            container_request['length'],
            container_request['width'],
            container_request['height'],
            container_request['weight'])
