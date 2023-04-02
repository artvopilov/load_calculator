from collections import defaultdict
from typing import Dict, List, Tuple, Optional

from loguru import logger

from src.items.container import Container
from src.items.item_fabric import ItemFabric
from src.iterators.points.horizontal_points_iterator import HorizontalPointsIterator
from src.iterators.points.points_iterator import PointsIterator
from src.iterators.points.vertical_points_iterator import VerticalPointsIterator
from src.loading.loading_type import LoadingType
from src.loading.point import Point
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Loader:
    _container_params: Dict[ContainerParameters, int]
    _shipment_params: Dict[ShipmentParameters, int]
    _loading_type: LoadingType
    _item_fabric: ItemFabric
    _containers: List[Container]

    def __init__(
            self,
            container_params: Dict[ContainerParameters, int],
            shipment_params: Dict[ShipmentParameters, int],
            loading_type: LoadingType,
            item_fabric: ItemFabric,
    ) -> None:
        self._container_params = container_params
        self._shipment_params = shipment_params
        self._loading_type = loading_type
        self._item_fabric = item_fabric
        self._containers = []

    @property
    def containers(self) -> List[Container]:
        return self._containers

    @property
    def shipment_params(self) -> Dict[ShipmentParameters, int]:
        return self._shipment_params

    def load(self) -> None:
        self._compute_loading_locations()
        self._compute_loading_order()
        logger.info(f'Loaded, '
                    f'containers: {len(self._containers)}, '
                    f'loaded shipments: {sum([c.container_statistics.shipments for c in self.containers])}, '
                    f'left shipments: {self._count_shipments()}')

    def _compute_loading_locations(self) -> None:
        self._containers = []
        shipment_params_order = self._calculate_shipment_params_order()
        while self._count_shipments() > 0:
            containers_to_shipment_counts = self._load_shipments_into_available_containers(shipment_params_order)
            max_loaded_container = self._select_max_loaded_container(list(containers_to_shipment_counts.keys()))
            if not max_loaded_container:
                break
            self._containers.append(max_loaded_container)
            self._container_params[max_loaded_container.parameters] -= 1
            for shipment_params, count in containers_to_shipment_counts[max_loaded_container].items():
                self._reduce_shipments(shipment_params, count)

    def _compute_loading_order(self) -> None:
        for container in self._containers:
            min_point_to_id = container.min_point_to_id
            id_to_shipment = container.id_to_shipment
            container.unload()
            while len(min_point_to_id) > 0:
                last_loaded_point = None
                for point in VerticalPointsIterator(min_point_to_id.keys()):
                    shipment = id_to_shipment[min_point_to_id[point]]
                    can_load = container.can_load_into_point(point, shipment.parameters)
                    if can_load:
                        if last_loaded_point and last_loaded_point.x != point.x:  # or last_loaded_point.z != point.z):
                            break
                        container.load(point, shipment)
                        min_point_to_id.pop(point)
                        last_loaded_point = point

    def _calculate_shipment_params_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipment_params.keys(),
            key=lambda s: [s.form_type == 'barrel', s.weight, s.can_stack] + s.get_volume_params_sorted(),
            reverse=True))

    def _count_shipments(self) -> int:
        return sum(list(self._shipment_params.values()))

    def _reduce_shipments(self, shipment_params: ShipmentParameters, count: int) -> None:
        if self._shipment_params.get(shipment_params, 0) > count:
            self._shipment_params[shipment_params] -= count
        elif shipment_params in self._shipment_params:
            self._shipment_params.pop(shipment_params)

    def _load_shipments_into_available_containers(
            self,
            shipment_params_order: List[ShipmentParameters]
    ) -> Dict[Container, Dict[ShipmentParameters, int]]:
        containers_to_shipment_counts = {}
        for container_params in self._get_available_container_params():
            logger.debug(f'Loading into {container_params}')
            container = self._item_fabric.create_container(container_params)
            container_shipment_counts = self._load_shipments(shipment_params_order, container)
            containers_to_shipment_counts[container] = container_shipment_counts
        return containers_to_shipment_counts

    def _get_available_container_params(self) -> List[ContainerParameters]:
        return list(map(lambda x: x[0], filter(lambda x: x[1] != 0, self._container_params.items())))

    @staticmethod
    def _select_max_loaded_container(containers: List[Container]) -> Container:
        max_loaded_container = None
        for container in containers:
            logger.debug(f'{container} loaded volume: {container.get_loaded_volume()}')
            if container.get_loaded_volume() <= 0:
                continue
            if max_loaded_container is None or container.get_loaded_volume() > max_loaded_container.get_loaded_volume():
                max_loaded_container = container
        logger.debug(f'{max_loaded_container} has max loaded volume: {max_loaded_container.get_loaded_volume()}')
        return max_loaded_container

    def _load_shipments(
            self,
            shipment_params_order: List[ShipmentParameters],
            container: Container
    ) -> Dict[ShipmentParameters, int]:
        container_shipment_counts = defaultdict(int)
        for shipment_params in shipment_params_order:
            logger.debug(f'Loading {shipment_params}')
            shipment_count = self._shipment_params.get(shipment_params, 0)
            while container_shipment_counts[shipment_params] < shipment_count:
                logger.debug(f'Left: {shipment_count - container_shipment_counts[shipment_params]}')
                if not self._load_shipment(shipment_params, container):
                    break
                container_shipment_counts[shipment_params] += 1
        return container_shipment_counts

    def _load_shipment(self, shipment_params: ShipmentParameters, container: Container) -> bool:
        logger.debug("Selecting loading point")
        shipment_params_variations = shipment_params.get_volume_params_variations()
        loading_point_and_shipment_params = self._select_loading_point(shipment_params_variations, container)
        if loading_point_and_shipment_params:
            loading_point, shipment_params = loading_point_and_shipment_params
            logger.debug(f"Loading point found: {loading_point}, loading")
            shipment = self._item_fabric.create_shipment(shipment_params)
            container.load(loading_point, shipment)
            return True
        return False

    def _select_loading_point(
            self,
            shipment_params_variations: List[ShipmentParameters],
            container: Container
    ) -> Optional[Tuple[Point, ShipmentParameters]]:
        logger.debug("Iterating container")
        for shipment_params in shipment_params_variations:
            for point in self._get_points_iterator(container):
                can_load = container.can_load_into_point(point, shipment_params)
                if can_load:
                    return point, shipment_params
        return None

    def _get_points_iterator(self, container: Container) -> PointsIterator:
        points = container.loadable_point_to_max_points.keys()
        if self._loading_type == LoadingType.STABLE:
            return HorizontalPointsIterator(points)
        else:
            return VerticalPointsIterator(points)
