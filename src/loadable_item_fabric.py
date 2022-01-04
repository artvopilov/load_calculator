from src.pallet import Pallet
from src.parameters.pallet_parameters import PalletParameters
from src.parameters.shipment_parameters import ShipmentParameters
from src.shipment import Shipment


class LoadableItemFabric:
    _current_id: int

    def __init__(self):
        self._current_id = 0

    def create_shipment(self, shipment_parameters: ShipmentParameters) -> Shipment:
        shipment = Shipment(shipment_parameters, self._current_id)
        self._current_id += 1
        return shipment

    def create_pallet(self, pallet_parameters: PalletParameters) -> Pallet:
        pallet = Pallet(pallet_parameters, self._current_id)
        self._current_id += 1
        return pallet
