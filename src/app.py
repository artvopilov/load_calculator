from loader import Loader
from parameters.container_parameters import ContainerParameters
from parameters.shipment_parameters import ShipmentParameters


CONTAINER_PARAMETERS = ContainerParameters(10, 2, 4, 100)
SHIPMENT_COUNTS = {ShipmentParameters(2, 1, 1, 1): 10, ShipmentParameters(1, 1, 1, 200): 1}


if __name__ == '__main__':
    loader = Loader(CONTAINER_PARAMETERS, SHIPMENT_COUNTS)
    containers, non_loadable_shipments = loader.load()

    for container in containers:
        print(container)
    for shipment in non_loadable_shipments:
        print(shipment)
