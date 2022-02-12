from typing import Dict, Set, List, Tuple, Optional

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
        for shipment_params in shipments_order:
            possible_shipment_params = [shipment_params]
            if shipment_params.can_cant:
                possible_shipment_params.append(shipment_params.swap_length_width_height())

            while self._shipments_counts[shipment_params]:
                for cur_shipment_params in possible_shipment_params:
                    shipment = self._create_shipment(cur_shipment_params)
                    if self._load_shipment(shipment):
                        self._shipments_counts[shipment_params] -= 1
                        break

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

    def _compute_next_container_parameters(self) -> Optional[ContainerParameters]:
        shipments_weight, shipments_volume = self._compute_shipments_weight_and_volume()

        possible_container_params = list(map(
            lambda x: x[0],
            filter(lambda x: x[1] > 0, self._container_counts.items())))
        if len(possible_container_params) <= 0:
            return None

        best_container_params = None
        best_weight_diff, best_volume_diff = -1e5, -1e5
        for container_params in possible_container_params:
            weight_diff = container_params.lifting_capacity - shipments_weight
            volume_diff = container_params.compute_volume() - shipments_volume
            # TODO!!!

            if (weight_diff + volume_diff < best_weight_diff + best_volume_diff) \
                    or (best_weight_diff < 0 or best_volume_diff < 0):
                best_container_params = container_params
                best_weight_diff, best_volume_diff = weight_diff, volume_diff



        return best_container_params

    def _compute_shipments_weight_and_volume(self) -> Tuple[float, float]:
        shipments_weight = 0
        shipments_volume = 0
        for shipment_params, count in self._shipments_counts.items():
            shipments_weight += shipment_params.weight * count
            shipments_volume += shipment_params.compute_volume() * count
        return shipments_weight, shipments_volume
