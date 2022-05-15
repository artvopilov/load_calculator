from collections import defaultdict
from typing import Dict, List, Tuple, Optional

from src.items.container import Container
from src.items.item_fabric import ItemFabric
from src.items.point import Point
from src.iterators.loadable_points_iterator import LoadablePointsIterator
from src.loading.container_selection_type import ContainerSelectionType
from src.loading.container_selector import ContainerSelector
from src.logger.logger import Logger
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Loader:
    _container_counts: Dict[ContainerParameters, int]
    _auto_containers: List[ContainerParameters]
    _container_selection_type: ContainerSelectionType

    _shipments_counts: Dict[ShipmentParameters, int]

    _load_item_fabric: ItemFabric
    _container_selector: ContainerSelector

    _containers: List[Container]

    _logger: Logger

    def __init__(
            self,
            container_counts: Dict[ContainerParameters, int],
            auto_containers: List[ContainerParameters],
            container_selection_type: ContainerSelectionType,
            shipments_counts: Dict[ShipmentParameters, int],
            load_item_fabric: ItemFabric,
            container_selector: ContainerSelector,
            logger: Logger
    ) -> None:
        self._container_counts = container_counts
        self._auto_containers = auto_containers
        self._container_selection_type = container_selection_type
        self._shipments_counts = shipments_counts
        self._load_item_fabric = load_item_fabric
        self._container_selector = container_selector
        self._containers = []
        self._logger = logger

    @property
    def containers(self) -> List[Container]:
        return self._containers

    @property
    def shipments_counts(self) -> Dict[ShipmentParameters, int]:
        return self._shipments_counts

    def load(self) -> None:
        shipment_params_order = self._calculate_shipment_params_order()
        while self._count_shipments() > 0:
            containers_to_shipment_counts = self._load_shipments_into_available_containers(shipment_params_order)
            max_loaded_container = self._select_max_loaded_container(list(containers_to_shipment_counts.keys()))
            if not max_loaded_container:
                break
            self._containers.append(max_loaded_container)
            if self._container_selection_type == ContainerSelectionType.FIXED:
                self._container_counts[max_loaded_container.parameters] -= 1
            for shipment_params, count in containers_to_shipment_counts[max_loaded_container].items():
                self._shipments_counts[shipment_params] -= count

    def _calculate_shipment_params_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipments_counts.keys(),
            key=lambda s: [s.can_stack] + s.get_volume_params_sorted() + [s.weight],
            reverse=True))

    def _count_shipments(self):
        return sum(list(self._shipments_counts.values()))

    def _load_shipments_into_available_containers(
            self,
            shipment_params_order: List[ShipmentParameters]
    ) -> Dict[Container, Dict[ShipmentParameters, int]]:
        containers_to_shipment_counts = {}
        for container_params in self._get_available_container_params():
            self._logger.info(f'Loading into {container_params}')
            container = self._load_item_fabric.create_container(container_params)
            container_shipment_counts = self._load_shipments(shipment_params_order, container)
            containers_to_shipment_counts[container] = container_shipment_counts
        return containers_to_shipment_counts

    def _get_available_container_params(self) -> List[ContainerParameters]:
        if self._container_selection_type == ContainerSelectionType.AUTO:
            return self._auto_containers
        return list(map(lambda x: x[0], filter(lambda x: x[1] > 0, self._container_counts.items())))

    def _select_max_loaded_container(self, containers: List[Container]) -> Container:
        max_loaded_container = None
        max_loaded_volume = 0
        for container in containers:
            loaded_volume = container.compute_loaded_volume()
            if loaded_volume > max_loaded_volume:
                max_loaded_volume = loaded_volume
                max_loaded_container = container
        return max_loaded_container

    def _load_shipments(
            self,
            shipment_params_order: List[ShipmentParameters],
            container: Container
    ) -> Dict[ShipmentParameters, int]:
        container_shipment_counts = defaultdict(int)
        for shipment_params in shipment_params_order:
            self._logger.info(f'Loading {shipment_params}')
            shipment_count = self._shipments_counts.get(shipment_params, 0)
            while container_shipment_counts[shipment_params] < shipment_count:
                self._logger.info(f'Left: {shipment_count - container_shipment_counts[shipment_params]}')
                if not self._load_shipment(shipment_params, container):
                    break
                container_shipment_counts[shipment_params] += 1
        return container_shipment_counts

    def _load_shipment(self, shipment_params: ShipmentParameters, container: Container) -> bool:
        self._logger.info("Selecting loading point")
        shipment_params_variations = shipment_params.get_volume_params_variations()
        loading_point_and_shipment_params = self._select_loading_point(shipment_params_variations, container)
        if loading_point_and_shipment_params:
            loading_point, shipment_params = loading_point_and_shipment_params
            self._logger.info(f"Loading point found: {loading_point}, loading")
            shipment = self._load_item_fabric.create_shipment(shipment_params)
            container.load(loading_point, shipment)
            return True
        return False

    def _select_loading_point(
            self,
            shipment_params_variations: List[ShipmentParameters],
            container: Container
    ) -> Optional[Tuple[Point, ShipmentParameters]]:
        self._logger.info("Iterating container")
        for shipment_params in shipment_params_variations:
            # self._logger.info(f'Loading variation: {shipment_params}')
            for point in LoadablePointsIterator(container):
                # self._logger.info(f"Checking point {point}")
                can_load = container.can_load_into_point(point, shipment_params)
                if can_load:
                    return point, shipment_params
        return None
