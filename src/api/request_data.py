from dataclasses import dataclass
from typing import Dict

from src.loading.loading_type import LoadingType
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


@dataclass
class RequestData:
    container_params: Dict[ContainerParameters, int]
    shipment_params: Dict[ShipmentParameters, int]
    loading_type: LoadingType
