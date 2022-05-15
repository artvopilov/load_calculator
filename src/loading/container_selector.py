from typing import List, Optional, Tuple, Dict

from src.loading.shipments_statistics import ShipmentsStatistics
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class ContainerSelector:
    _CONTAINER_VOLUME_COEFFICIENT_THRESHOLD: float = 1.2
    _CONTAINER_WEIGHT_COEFFICIENT_THRESHOLD: float = 1.0

    def select_params(
            self,
            possible_params: List[ContainerParameters],
            shipments_counts: Dict[ShipmentParameters, int]
    ) -> Optional[ContainerParameters]:
        selected_params = None
        if len(possible_params) <= 0:
            return selected_params

        shipments_statistics = self._compute_shipments_statistics(shipments_counts)
        selected_volume_c, selected_weight_c = 0, 0
        for params in possible_params:
            volume_c = params.compute_volume() / shipments_statistics.volume / self._CONTAINER_VOLUME_COEFFICIENT_THRESHOLD
            weight_c = params.lifting_capacity / shipments_statistics.weight / self._CONTAINER_WEIGHT_COEFFICIENT_THRESHOLD
            if self._should_use_params(selected_weight_c, selected_volume_c, weight_c, volume_c):
                selected_params = params
                selected_weight_c, selected_volume_c = weight_c, volume_c
        return selected_params

    def _compute_shipments_statistics(self, shipments_counts: Dict[ShipmentParameters, int]) -> ShipmentsStatistics:
        weight = 0
        volume = 0
        min_dimension = 0
        max_dimension = 0
        for shipment_params, count in shipments_counts.items():
            volume += shipment_params.compute_extended_volume() * count
            weight += shipment_params.weight * count
            max_dimension = max(max_dimension, shipment_params.get_volume_params_sorted()[0])
            min_dimension = max(min_dimension, shipment_params.get_volume_params_sorted()[-1])
        return ShipmentsStatistics(volume, weight, max_dimension, min_dimension)

    def _should_use_params(
            self,
            selected_weight_c: float,
            selected_volume_c: float,
            weight_c: float,
            volume_c: float
    ) -> bool:
        min_selected_c = min(selected_weight_c, selected_volume_c)
        min_c = min(weight_c, volume_c)
        if min_selected_c < 1:
            if min_c > min_selected_c:
                return True
        elif min_c > 1:
            if weight_c + volume_c < selected_weight_c + selected_volume_c:
                return True
        return False
