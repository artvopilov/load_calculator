from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Container:
    def __init__(self, container_params: ContainerParameters) -> None:
        self._container_params = container_params
        self._shipments = []

    def load(self, shipment: ShipmentParameters) -> bool:
        pass

    def unload(self) -> None:
        self._shipments = []
