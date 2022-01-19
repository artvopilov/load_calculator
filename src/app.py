from item_fabric import ItemFabric
from loader import Loader
from parameters.container_parameters import ContainerParameters
from parameters.pallet_parameters import PalletParameters
from parameters.shipment_parameters import ShipmentParameters
from src.image_3d_creator import Image3dCreator
from src.point import Point

CONTAINER_PARAMETERS = ContainerParameters(10000, 2000, 4000, 100)
SHIPMENT_COUNTS = {ShipmentParameters(1000, 500, 500, 2): 10, ShipmentParameters(1000, 1000, 1000, 200): 1}
PALLET_PARAMETERS = PalletParameters(1000, 1000, 100, 20, 20)

POSITIONS = [Point(0, 0, 0), Point(10, 0, 5)]
SIZES = [Point(1, 1, 1), Point(2, 6, 4)]
COLORS = ['b', 'r']


def test_loading():
    item_fabric = ItemFabric()
    loader = Loader(CONTAINER_PARAMETERS, SHIPMENT_COUNTS, PALLET_PARAMETERS, item_fabric)

    loader.load()

    containers = loader.containers
    non_loadable_shipments = loader.non_loadable_shipments

    for container in containers:
        print(container)
    for shipment in non_loadable_shipments:
        print(shipment)


def test_3d_plotting_cube():
    image_3d_creator = Image3dCreator()
    image_3d_creator.create(POSITIONS, SIZES, COLORS)


if __name__ == '__main__':
    test_3d_plotting_cube()
