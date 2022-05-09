from collections import defaultdict
from typing import Dict, List

from flask import jsonify, Response

from src.items.container import Container
from src.parameters.shipment_parameters import ShipmentParameters


class ResponseBuilder:
    def build(self, containers: List[Container], left_shipment_counts: Dict[ShipmentParameters, int]) -> Response:
        response = defaultdict(list)
        for container in containers:
            last_shipment_params = None
            last_shipment_params_id = 0
            id_to_shipment_params = {}
            points = []
            points_batch = []
            for shipment_id in container.shipment_id_order:
                shipment = container.id_to_shipment[shipment_id]

                if shipment.parameters != last_shipment_params:
                    if points_batch:
                        self.process_batch(points, points_batch, id_to_shipment_params,
                                           last_shipment_params, last_shipment_params_id)
                    last_shipment_params = shipment.parameters
                    last_shipment_params_id += 1
                    points_batch = []

                point = container.id_to_min_point[shipment_id]
                points_batch.append(point.build_response(last_shipment_params_id))

            self.process_batch(points, points_batch, id_to_shipment_params, last_shipment_params, last_shipment_params_id)

            response['containers'].append(container.build_response())
            response['containers'][-1]['cargos'] = id_to_shipment_params
            response['containers'][-1]['load_points'] = points

        for shipment_params, left_count in left_shipment_counts.items():
            if left_count == 0:
                continue
            response['left_cargos'].append(shipment_params.build_response())
            response['left_cargos'][-1]['number'] = left_count

        return jsonify(response)

    @staticmethod
    def process_batch(
            points: List,
            points_batch: List,
            id_to_shipment_params: Dict,
            last_shipment_params: ShipmentParameters,
            last_shipment_params_id: int
    ) -> None:
        points.append(points_batch)
        id_to_shipment_params[last_shipment_params_id] = last_shipment_params.build_response()
