from typing import Dict, List, Set

from parameters.container_parameters import ContainerParameters
from parameters.pallet_parameters import PalletParameters
from parameters.load_parameters import LoadParameters
from src.container import Container
from src.load_item_fabric import LoadItemFabric
from src.shipment import Shipment


class Loader:
    _container_parameters: ContainerParameters
    _shipments_counts: Dict[LoadParameters, int]
    _pallet_parameters: PalletParameters
    _load_item_fabric: LoadItemFabric
    _containers: List[Container]
    _non_loadable_shipments: Set[LoadParameters]

    def __init__(self,
                 container_parameters: ContainerParameters,
                 shipments_counts: Dict[LoadParameters, int],
                 pallet_parameters: PalletParameters,
                 load_item_fabric: LoadItemFabric):
        self._container_parameters = container_parameters
        self._shipments_counts = shipments_counts
        self._pallet_parameters = pallet_parameters
        self._load_item_fabric = load_item_fabric
        self._containers = []
        self._non_loadable_shipments = set()

    @property
    def containers(self):
        return self._containers

    @property
    def non_loadable_shipments(self):
        return self._non_loadable_shipments

    def load(self) -> None:
        shipments_order = self._calculate_shipments_order()
        self._load_shipments(shipments_order)

    def unload(self) -> None:
        self._containers = []
        self._non_loadable_shipments = set()

    def _calculate_shipments_order(self) -> List[LoadParameters]:
        return list(sorted(self._shipments_counts.keys(), key=lambda s: (s.length + s.width + s.height, s.weight)))

    def _load_shipments(self, shipments_order: List[LoadParameters]) -> None:
        for shipment_parameters in shipments_order:
            shipment_count = self._shipments_counts[shipment_parameters]
            print(f'shipment parameters: {shipment_parameters}, count: {shipment_count}')

            for i in range(shipment_count):
                shipment = self._load_item_fabric.create_shipment(shipment_parameters)
                if not self._try_load_shipment(shipment):
                    self._non_loadable_shipments.add(shipment_parameters)
                    break

    def _try_load_shipment(self, shipment: Shipment) -> bool:
        print(f'loading {shipment}')
        if self._try_load_into_existing_container(shipment):
            return True

        if self._try_load_into_new_container(shipment):
            return True

        print('not loaded')
        return False

    def _try_load_into_existing_container(self, shipment: Shipment) -> bool:
        for container in self._containers:
            if container.try_load_shipment(shipment):
                print('loaded in existing')
                return True
        return False

    def _try_load_into_new_container(self, shipment: Shipment) -> bool:
        container = Container(self._container_parameters)
        self._load_pallets(container)

        if container.try_load_shipment(shipment):
            self._containers.append(container)
            print('loaded in new')
            return True
        return False

    def _load_pallets(self, container: Container):
        loading = False if not self._pallet_parameters else True
        while loading:
            pallet = self._load_item_fabric.create_pallet(self._pallet_parameters)
            loading = container.try_load_pallet(pallet)
