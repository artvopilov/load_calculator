from collections import defaultdict
from typing import Dict, List

from flask import jsonify

from src.items.container import Container
from src.parameters.shipment_parameters import ShipmentParameters


class ResponseBuilder:
    @staticmethod
    def build(containers: List[Container], left_shipment_counts: Dict[ShipmentParameters, int]) -> Dict:
        response = defaultdict(list)
        for container in containers:
            id_to_shipment_params = {}
            points = []
            for shipment_id in container.shipment_id_order:
                shipment = container.id_to_shipment[shipment_id]
                point = container.id_to_min_point[shipment_id]
                id_to_shipment_params[shipment.parameters.id] = shipment.parameters.build_response()
                points.append(point.build_response(shipment.parameters.id))

            response['containers'].append(container.parameters.build_response())
            response['containers'][-1]['cargos'] = id_to_shipment_params
            response['containers'][-1]['load_points'] = points

        return jsonify(response)
