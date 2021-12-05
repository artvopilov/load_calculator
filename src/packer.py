from typing import Dict

from src.parameters.shipment_parameters import ShipmentParameters
from src.parameters.container_parameters import ContainerParameters


class Packer:
    def __init__(self):
        pass

    def pack(self, container: ContainerParameters, shipments: Dict[ShipmentParameters, int]):
        pass
