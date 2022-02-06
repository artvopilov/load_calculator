from typing import Dict, Set, List

from src.item_fabric import ItemFabric
from src.items.container import Container
from src.items.shipment import Shipment
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Loader:
    _container_counts: Dict[ContainerParameters, int]
    _shipments_counts: Dict[ShipmentParameters, int]

    _load_item_fabric: ItemFabric

    _containers: List[Container]

    def __init__(self,
                 container_counts: Dict[ContainerParameters, int],
                 shipments_counts: Dict[ShipmentParameters, int],
                 load_item_fabric: ItemFabric):
        self._container_counts = container_counts
        self._shipments_counts = shipments_counts
        self._load_item_fabric = load_item_fabric
        self._containers = []

    @property
    def containers(self) -> List[Container]:
        return self._containers

    @property
    def non_loadable_shipments(self) -> Dict[ShipmentParameters, int]:
        return self._shipments_counts

    def load(self) -> None:
        shipments_order = self._calculate_shipments_order()
        self._load_shipments(shipments_order)

    def unload(self) -> None:
        self._containers = []

    def _calculate_shipments_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipments_counts.keys(),
            key=lambda s: (
                s.can_stack,
                max(s.length, s.width, s.height),
                s.length + s.width + s.height,
                s.weight),
            reverse=True))

    def _load_shipments(self, shipments_order: List[ShipmentParameters]) -> None:
        for shipment_parameters in shipments_order:
            while self._shipments_counts[shipment_parameters]:
                shipment = self._create_shipment(shipment_parameters)
                if not self._load_shipment(shipment):
                    break
                self._shipments_counts[shipment_parameters] -= 1

    def _create_shipment(self, shipment_parameters: ShipmentParameters) -> Shipment:
        return self._load_item_fabric.create_shipment(shipment_parameters)

    def _load_shipment(self, shipment: Shipment) -> bool:
        if self._load_into_existing_container(shipment):
            return True
        if self._load_into_new_container(shipment):
            return True
        return False

    def _load_into_existing_container(self, shipment: Shipment) -> bool:
        for container in self._containers:
            if container.load(shipment):
                return True
        return False

    def _load_into_new_container(self, shipment: Shipment) -> bool:
        container_parameters = self._compute_next_container_parameters()
        container = self._load_item_fabric.create_container(container_parameters)
        if container.load(shipment):
            self._containers.append(container)
            return True
        return False

    def _compute_next_container_parameters(self) -> ContainerParameters:
        return list(self._container_counts.keys())[0]


