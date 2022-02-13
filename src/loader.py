from typing import Dict, List, Tuple, Optional

from src.item_fabric import ItemFabric
from src.items.container import Container
from src.items.shipment import Shipment
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Loader:
    _CONTAINER_COEFFICIENT_THRESHOLD = 1.1

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
    def shipments_counts(self) -> Dict[ShipmentParameters, int]:
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
                # s.can_stack,
                max(s.length, s.width, s.height),
                s.length + s.width + s.height,
                s.weight),
            reverse=True))

    def _load_shipments(self, shipments_order: List[ShipmentParameters]) -> None:
        for shipment_params in shipments_order:
            possible_shipment_params = [shipment_params]
            if not shipment_params.can_stack:
                possible_shipment_params = [shipment_params.get_smallest_area_params()]
            if shipment_params.can_cant:
                for params in shipment_params.swap_length_width_height():
                    if params == possible_shipment_params[0]:
                        continue
                    possible_shipment_params.append(params)

            loading = True
            while self._shipments_counts[shipment_params] and loading:
                loading = False
                for cur_shipment_params in possible_shipment_params:
                    shipment = self._create_shipment(cur_shipment_params)
                    if self._load_shipment(shipment):
                        self._shipments_counts[shipment_params] -= 1
                        loading = True
                        break

    def _create_shipment(self, shipment_parameters: ShipmentParameters) -> Shipment:
        return self._load_item_fabric.create_shipment(shipment_parameters)

    def _load_shipment(self, shipment: Shipment) -> bool:
        print(f'Loading {shipment}')
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
        # no container available
        if not container_parameters:
            return False
        container = self._load_item_fabric.create_container(container_parameters)
        if container.load(shipment):
            self._containers.append(container)
            self._container_counts[container_parameters] -= 1
            return True
        return False

    def _compute_next_container_parameters(self) -> Optional[ContainerParameters]:
        shipments_weight, shipments_volume = self._compute_shipments_weight_and_volume()

        possible_container_params = self._get_possible_container_params()
        if len(possible_container_params) <= 0:
            return None

        selected_container_params = None
        selected_weight_c, selected_volume_c = 0, 0
        for container_params in possible_container_params:
            weight_c = container_params.lifting_capacity / shipments_weight
            volume_c = container_params.compute_volume() / shipments_volume

            if self._should_use_params(selected_weight_c, selected_volume_c, weight_c, volume_c):
                selected_container_params = container_params
                selected_weight_c, selected_volume_c = weight_c, volume_c

        return selected_container_params

    def _compute_shipments_weight_and_volume(self) -> Tuple[float, float]:
        shipments_volume = 0
        shipments_weight = 0
        for shipment_params, count in self._shipments_counts.items():
            shipments_volume += shipment_params.compute_volume() * count
            shipments_weight += shipment_params.weight * count
        return shipments_weight, shipments_volume

    def _get_possible_container_params(self) -> List[ContainerParameters]:
        return list(map(lambda x: x[0], filter(lambda x: x[1] > 0, self._container_counts.items())))

    def _should_use_params(
            self,
            selected_weight_c: float,
            selected_volume_c: float,
            weight_c: float,
            volume_c: float
    ) -> bool:
        min_selected_c = min(selected_weight_c, selected_volume_c)
        min_c = min(weight_c, volume_c)
        # selected params do not fit threshold
        if min_selected_c < self._CONTAINER_COEFFICIENT_THRESHOLD:
            if min_c > min_selected_c:
                return True
        # both selected params and current params fit threshold
        elif min_c > self._CONTAINER_COEFFICIENT_THRESHOLD:
            if weight_c + volume_c < selected_weight_c + selected_volume_c:
                return True
        return False
