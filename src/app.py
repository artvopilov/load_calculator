from loader import Loader
from parameters.container_parameters import ContainerParameters
from parameters.load_parameters import LoadParameters
from parameters.pallet_parameters import PalletParameters


CONTAINER_PARAMETERS = ContainerParameters(10000, 2000, 4000, 100)
SHIPMENT_COUNTS = {LoadParameters(1000, 500, 500, 2): 10, LoadParameters(1000, 1000, 1000, 200): 1}
PALLET_PARAMETERS = PalletParameters(1000, 1000, 100, 20)


if __name__ == '__main__':
    loader = Loader(CONTAINER_PARAMETERS, SHIPMENT_COUNTS, PALLET_PARAMETERS)
    containers, non_loadable_shipments = loader.load()

    for container in containers:
        print(container)
    for shipment in non_loadable_shipments:
        print(shipment)
