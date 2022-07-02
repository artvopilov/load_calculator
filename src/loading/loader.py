from collections import defaultdict
from typing import Dict, List, Tuple, Optional

from src.items.container import Container
from src.items.item_fabric import ItemFabric
from src.loading.point import Point
from src.iterators.points.horizontal_points_iterator import HorizontalPointsIterator
from src.iterators.points.points_iterator import PointsIterator
from src.iterators.points.vertical_points_iterator import VerticalPointsIterator
from src.loading.loading_type import LoadingType
from src.logger.logger import Logger
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class Loader:
    _container_params_to_count: Dict[ContainerParameters, int]
    _shipment_params_to_count: Dict[ShipmentParameters, int]
    _loading_type: LoadingType
    _item_fabric: ItemFabric
    _logger: Logger

    def __init__(
            self,
            container_params_to_count: Dict[ContainerParameters, int],
            shipment_params_to_count: Dict[ShipmentParameters, int],
            loading_type: LoadingType,
            load_item_fabric: ItemFabric,
            logger: Logger
    ) -> None:
        self._container_params_to_count = container_params_to_count
        self._shipment_params_to_count = shipment_params_to_count
        self._loading_type = loading_type
        self._item_fabric = load_item_fabric
        self._logger = logger

    def get_left_shipments_counts(self) -> Dict[ShipmentParameters, int]:
        return self._shipment_params_to_count

    def load(self) -> List[Container]:
        containers = self._compute_loading_locations()
        self._compute_loading_order(containers)
        return containers

    def _compute_loading_locations(self) -> List[Container]:
        containers = []
        shipment_params_order = self._calculate_shipment_params_order()
        while self._count_shipments() > 0:
            containers_to_shipment_counts = self._load_shipments_into_available_containers(shipment_params_order)
            max_loaded_container = self._select_max_loaded_container(list(containers_to_shipment_counts.keys()))
            if not max_loaded_container:
                break
            containers.append(max_loaded_container)
            self._container_params_to_count[max_loaded_container.parameters] -= 1
            for shipment_params, count in containers_to_shipment_counts[max_loaded_container].items():
                self._shipment_params_to_count[shipment_params] -= count
        return containers

    @staticmethod
    def _compute_loading_order(containers: List[Container]) -> None:
        for container in containers:
            min_point_to_id = container.min_point_to_id
            id_to_shipment = container.id_to_shipment
            container.unload()
            while len(min_point_to_id) > 1:
                last_loaded_point = None
                for point in VerticalPointsIterator(min_point_to_id.keys()):
                    print(point)
                    shipment = id_to_shipment[min_point_to_id[point]]
                    print(shipment.parameters)
                    print('Points loadable:')
                    for p, max_points in container.loadable_point_to_max_points.items():
                        for max_p in max_points:
                            print('{}: {}'.format(p, max_p))
                    print('-------')
                    can_load = container.can_load_into_point(point, shipment.parameters)
                    if can_load:
                        if last_loaded_point and last_loaded_point.x != point.x:  # or last_loaded_point.z != point.z):
                            break
                        container.load(point, shipment)
                        min_point_to_id.pop(point)
                        last_loaded_point = point
                # print(len(min_point_to_id))


    def _calculate_shipment_params_order(self) -> List[ShipmentParameters]:
        return list(sorted(
            self._shipment_params_to_count.keys(),
            key=lambda s: [s.can_stack] + s.get_volume_params_sorted() + [s.weight],
            reverse=True))

    def _count_shipments(self):
        return sum(list(self._shipment_params_to_count.values()))

    def _load_shipments_into_available_containers(
            self,
            shipment_params_order: List[ShipmentParameters]
    ) -> Dict[Container, Dict[ShipmentParameters, int]]:
        containers_to_shipment_counts = {}
        for container_params in self._get_available_container_params():
            self._logger.info(f'Loading into {container_params}')
            container = self._item_fabric.create_container(container_params)
            container_shipment_counts = self._load_shipments(shipment_params_order, container)
            containers_to_shipment_counts[container] = container_shipment_counts
        return containers_to_shipment_counts

    def _get_available_container_params(self) -> List[ContainerParameters]:
        return list(map(lambda x: x[0], filter(lambda x: x[1] != 0, self._container_params_to_count.items())))

    def _select_max_loaded_container(self, containers: List[Container]) -> Container:
        max_loaded_container = None
        for container in containers:
            if max_loaded_container is None or container.get_loaded_volume() > max_loaded_container.get_loaded_volume():
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
            shipment_count = self._shipment_params_to_count.get(shipment_params, 0)
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
            shipment = self._item_fabric.create_shipment(shipment_params)
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
            for point in self._get_points_iterator(container):
                # self._logger.info(f"Checking point {point}")
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
