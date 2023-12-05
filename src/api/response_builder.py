from typing import Dict, List, Any

from flask import Response

from src.items.container import Container
from src.parameters.shipment_parameters import ShipmentParameters


class ResponseBuilder:
    def build(self, containers: List[Container], left_shipment_counts: Dict[ShipmentParameters, int]) -> Response:
        response = {'containers': [], 'left_cargos': []}
        for container in containers:
            response['containers'].append(self._build_container_response(container))

        for shipment_params, left_count in left_shipment_counts.items():
            response['left_cargos'].append(self._build_left_cargo_response(shipment_params, left_count))

        return response

    def _build_container_response(self, container: Container) -> Dict[str, Any]:
        id_to_shipment_params = {}
        points = []
        if container.loading_order:
            last_shipment_params = None
            last_shipment_params_id = 0
            for shipment_id in container.loading_order:
                shipment = container.id_to_shipment[shipment_id]
                point = container.id_to_min_point_shifted[shipment_id]

                if shipment.parameters != last_shipment_params:
                    last_shipment_params = shipment.parameters
                    last_shipment_params_id += 1
                    id_to_shipment_params[last_shipment_params_id] = last_shipment_params.build_response()
                    points.append([])
                points[-1].append(point.build_response(last_shipment_params_id))

        container_response = container.build_response()
        container_response['cargos'] = id_to_shipment_params
        container_response['load_points'] = points
        return container_response

    def _build_left_cargo_response(self, shipment_params: ShipmentParameters, left_count: int) -> Dict[str, Any]:
        left_cargo_response = shipment_params.build_response()
        left_cargo_response['number'] = left_count
        return left_cargo_response
