from typing import Dict, List, Set, Optional

from parameters.container_parameters import ContainerParameters
from parameters.pallet_parameters import PalletParameters
from parameters.shipment_parameters import ShipmentParameters
from src.items.container import Container
from src.item_fabric import ItemFabric
from src.items.shipment import Shipment


class Loader:
    _container_parameters: ContainerParameters
    _shipments_counts: Dict[ShipmentParameters, int]
    _pallet_parameters: Optional[PalletParameters]
    _load_item_fabric: ItemFabric
    _containers: List[Container]
    _non_loadable_shipments: Set[ShipmentParameters]

    def __init__(self,
                 container_parameters: ContainerParameters,
                 shipments_counts: Dict[ShipmentParameters, int],
                 pallet_parameters: Optional[PalletParameters],
                 load_item_fabric: ItemFabric):
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
        self._unload_empty_pallets()

    def unload(self) -> None:
        self._containers = []
        self._non_loadable_shipments = set()

    def _calculate_shipments_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipments_counts.keys(),
            key=lambda s: (s.length + s.width + s.height, s.weight),
            reverse=True))

    def _load_shipments(self, shipments_order: List[ShipmentParameters]) -> None:
        for shipment_parameters in shipments_order:
            shipment_count = self._shipments_counts[shipment_parameters]
            for i in range(shipment_count):
                shipment = self._load_item_fabric.create_shipment(shipment_parameters)

                # print(f'Loading {shipment}')

                if not self._load_shipment(shipment):
                    self._non_loadable_shipments.add(shipment_parameters)
                    break

                # print('Loaded')

    def _load_shipment(self, shipment: Shipment) -> bool:
        if self._load_into_existing_container(shipment):
            return True
        if self._create_container_and_load(shipment):
            return True

        return False

    def _load_into_existing_container(self, shipment: Shipment) -> bool:
        # print(f'Loading {shipment}')
        for container in self._containers:
            if container.load_shipment_if_fits(shipment):
                return True
        return False

    def _create_container_and_load(self, shipment: Shipment) -> bool:
        container = self._create_container_with_pallets()

        # print(f'Loading {shipment}')
        if container.load_shipment_if_fits(shipment):
            self._containers.append(container)
            return True
        return False

    def _create_container_with_pallets(self) -> Container:
        container = self._load_item_fabric.create_container(self._container_parameters)
        self._load_pallets(container)
        return container

    def _load_pallets(self, container: Container) -> None:
        if not self._pallet_parameters:
            return

        pallet_parameters = self._optimize_pallet_parameters(container)
        loading = True
        while loading:
            pallet = self._load_item_fabric.create_pallet(pallet_parameters)
            # print(f'Loading {pallet}')
            loading = container.load_pallet_if_fits(pallet)
            # print(f'Loaded: {loading}')

    def _optimize_pallet_parameters(self, container: Container) -> PalletParameters:
        swapped_pallet_parameters = self._pallet_parameters.swap_length_width()

        max_pallets_count = 0
        optimized_pallet_parameters = None
        for p in swapped_pallet_parameters:
            pallets_count = container.compute_max_pallets_count(p)
            if pallets_count > max_pallets_count:
                max_pallets_count = pallets_count
                optimized_pallet_parameters = p

        return optimized_pallet_parameters

    def _unload_empty_pallets(self):
        for container in self._containers:
            container.unload_empty_pallets()
