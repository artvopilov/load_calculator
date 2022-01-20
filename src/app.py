from item_fabric import ItemFabric
from loader import Loader
from parameters.container_parameters import ContainerParameters
from parameters.pallet_parameters import PalletParameters
from parameters.shipment_parameters import ShipmentParameters
from src.image_3d_creator import Image3dCreator
from src.point import Point

CONTAINER_PARAMETERS = ContainerParameters(20, 20, 20, 100)
SHIPMENT_COUNTS = {ShipmentParameters(2, 2, 1, 2, 'b'): 10, ShipmentParameters(10, 10, 2, 10, 'r'): 1}
PALLET_PARAMETERS = PalletParameters(5, 5, 1, 20, 20, 'g')

POSITIONS = [Point(0, 0, 0), Point(10, 0, 5), Point(12, 0, 5)]
SIZES = [Point(3, 3, 3), Point(2, 6, 4), Point(6, 6, 1)]
COLORS = ['b', 'r', 'r']


def test_loading():
    item_fabric = ItemFabric()
    loader = Loader(CONTAINER_PARAMETERS, SHIPMENT_COUNTS, PALLET_PARAMETERS, item_fabric)

    loader.load()

    containers = loader.containers
    non_loadable_shipments = loader.non_loadable_shipments

    image_3d_creator = Image3dCreator()
    for container in containers:
        print(container)
        image_3d_creator.create(container)
    for shipment in non_loadable_shipments:
        print(shipment)


def test_3d_plotting_cube():
    pass
    # image_3d_creator = Image3dCreator()
    # image_3d_creator.create(POSITIONS, SIZES, COLORS)


if __name__ == '__main__':
    test_loading()
