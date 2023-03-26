from typing import Dict

from src.loading.loading_type import LoadingType
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class RequestData:
    _container_params: Dict[ContainerParameters, int]
    _shipment_params: Dict[ShipmentParameters, int]
    _loading_type: LoadingType

    def __init__(
            self,
            container_params: Dict[ContainerParameters, int],
            shipment_params: Dict[ShipmentParameters, int],
            loading_type: LoadingType
    ) -> None:
        self._container_params = container_params
        self._shipment_params = shipment_params
        self._loading_type = loading_type

    @property
    def container_params(self) -> Dict[ContainerParameters, int]:
        return self._container_params

    @property
    def shipment_params(self) -> Dict[ShipmentParameters, int]:
        return self._shipment_params

    @property
    def loading_type(self) -> LoadingType:
        return self._loading_type

