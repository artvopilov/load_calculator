from typing import Dict

from src.loading.loading_type import LoadingType
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class RequestData:
    _container_params_to_count: Dict[ContainerParameters, int]
    _shipment_params_to_count: Dict[ShipmentParameters, int]
    _loading_type: LoadingType

    def __init__(
            self,
            container_params_to_count: Dict[ContainerParameters, int],
            shipment_params_to_count: Dict[ShipmentParameters, int],
            loading_type: LoadingType
    ) -> None:
        self._container_params_to_count = container_params_to_count
        self._shipment_params_to_count = shipment_params_to_count
        self._loading_type = loading_type

    @property
    def container_params_to_count(self) -> Dict[ContainerParameters, int]:
        return self._container_params_to_count

    @property
    def shipment_params_to_count(self) -> Dict[ShipmentParameters, int]:
        return self._shipment_params_to_count

    @property
    def loading_type(self) -> LoadingType:
        return self._loading_type

