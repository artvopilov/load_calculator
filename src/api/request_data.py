from dataclasses import dataclass
from typing import Dict, Optional

from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


@dataclass
class RequestData:
    shipment_params: Dict[ShipmentParameters, int]
    container_params: Optional[Dict[ContainerParameters, int]]
    loading_type_name: Optional[str]
