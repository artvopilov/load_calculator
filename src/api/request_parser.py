from typing import Dict

from flask import Request

from src.api.request_data import RequestData
from src.loading.loading_type import LoadingType
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class RequestParser:
    def __init__(self) -> None:
        pass

    def parse(self, request: Request) -> RequestData:
        container_params_to_count = self._parse_container_params_to_count(request)
        shipment_params_to_count = self._parse_shipment_params_to_count(request)
        loading_type = self._parse_loading_type(request)
        return RequestData(container_params_to_count, shipment_params_to_count, loading_type)

    def _parse_container_params_to_count(self, request: Request) -> Dict[ContainerParameters, int]:
        if 'containers' not in request.json:
            return {}
        container_counts = {}
        for container in request.json['containers']:
            container_params = self._create_container_params(container)
            container_counts[container_params] = container['number']
        return container_counts

    def _parse_shipment_params_to_count(self, request: Request) -> Dict[ShipmentParameters, int]:
        shipment_counts = {}
        for cargo in request.json['cargo']:
            shipment_params = self._create_shipment_params(cargo)
            shipment_counts[shipment_params] = cargo['number']
        return shipment_counts

    def _parse_loading_type(self, request: Request) -> LoadingType:
        if 'loading_type' in request.json:
            return LoadingType.from_name(request.json['loading_type'])
        return LoadingType.STABLE

    def _create_shipment_params(self, cargo_request: Dict) -> ShipmentParameters:
        length = cargo_request['length']
        width = cargo_request['width']
        height = cargo_request['height']
        diameter = cargo_request['diameter']
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

    def _create_container_params(self, container_request: Dict) -> ContainerParameters:
        return ContainerParameters(
            container_request['type'],
            container_request['length'],
            container_request['width'],
            container_request['height'],
            container_request['weight'])
