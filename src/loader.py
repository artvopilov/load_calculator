from typing import Dict, List

from parameters.shipment_parameters import ShipmentParameters
from parameters.container_parameters import ContainerParameters
from container.container import Container


class Loader:
    def __init__(self, container_parameters: ContainerParameters, shipments_counts: Dict[ShipmentParameters, int]):
        self._container_parameters = container_parameters
        self._shipments_counts = shipments_counts

        self._containers = []

    def load(self):
        shipments_order = self._calculate_shipments_order()
        non_loadable_shipments = set()

        for shipment in shipments_order:
            shipment_count = self._shipments_counts[shipment]
            print(f'shipment: {shipment}, count: {shipment_count}')
            for i in range(shipment_count):
                if not self._try_load_shipment(shipment):
                    non_loadable_shipments.add(shipment)
                    break

        return self._containers, non_loadable_shipments

    def _calculate_shipments_order(self) -> List[ShipmentParameters]:
        return list(sorted(self._shipments_counts.keys(), key=lambda s: (s.length + s.width + s.height, s.weight)))

    def _try_load_shipment(self, shipment: ShipmentParameters) -> bool:
        print(f'loading {shipment}')
        for container in self._containers:
            if container.try_load(shipment):
                print('loaded in existing')
                return True

        container = Container(self._container_parameters)
        if container.try_load(shipment):
            self._containers.append(container)
            print('loaded in new')
            return True

        print('not loaded')
        return False

