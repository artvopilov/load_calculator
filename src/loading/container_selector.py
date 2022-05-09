from typing import List, Optional

from src.parameters.container_parameters import ContainerParameters


class ContainerSelector:
    _CONTAINER_COEFFICIENT_THRESHOLD: float = 1.1

    def select_params(
            self,
            possible_params: List[ContainerParameters],
            volume: float,
            weight: float
    ) -> Optional[ContainerParameters]:
        selected_params = None
        selected_volume_c, selected_weight_c = 0, 0
        for params in possible_params:
            volume_c = params.compute_volume() / volume
            weight_c = params.lifting_capacity / weight
            if self._should_use_params(selected_weight_c, selected_volume_c, weight_c, volume_c):
                selected_params = params
                selected_weight_c, selected_volume_c = weight_c, volume_c
        return selected_params

    def _should_use_params(
            self,
            selected_weight_c: float,
            selected_volume_c: float,
            weight_c: float,
            volume_c: float
    ) -> bool:
        min_selected_c = min(selected_weight_c, selected_volume_c)
        min_c = min(weight_c, volume_c)
        if min_selected_c < self._CONTAINER_COEFFICIENT_THRESHOLD:
            if min_c > min_selected_c:
                return True
        elif min_c > self._CONTAINER_COEFFICIENT_THRESHOLD:
            if weight_c + volume_c < selected_weight_c + selected_volume_c:
                return True
        return False
