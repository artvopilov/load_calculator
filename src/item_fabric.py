from src.items.pallet import Pallet
from src.items.shipment import Shipment
from src.container import Container
from src.parameters.container_parameters import ContainerParameters
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.shipment_parameters import ShipmentParameters


class ItemFabric:
    _current_id: int

    def __init__(self):
        self._current_id = 0

    def create_container(self, container_parameters: ContainerParameters):
        container = Container(container_parameters, self._current_id)
        self._current_id += 1
        return container

    def create_shipment(self, shipment_parameters: ShipmentParameters) -> Shipment:
        shipment = Shipment(shipment_parameters, self._current_id)
        self._current_id += 1
        return shipment

    def create_pallet(self, pallet_parameters: PalletParameters) -> Pallet:
        pallet = Pallet(pallet_parameters, self._current_id)
        self._current_id += 1
        return pallet
