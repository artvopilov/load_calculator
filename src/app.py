from loader import Loader
from parameters.container_parameters import ContainerParameters
from parameters.shipment_parameters import ShipmentParameters
from parameters.pallet_parameters import PalletParameters
from item_fabric import ItemFabric

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

CONTAINER_PARAMETERS = ContainerParameters(10000, 2000, 4000, 100)
SHIPMENT_COUNTS = {ShipmentParameters(1000, 500, 500, 2): 10, ShipmentParameters(1000, 1000, 1000, 200): 1}
PALLET_PARAMETERS = PalletParameters(1000, 1000, 100, 20, 20)


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
    # prepare some coordinates
    x, y, z = np.indices((8, 8, 10))

    # draw cuboids in the top left and bottom right corners, and a link between them
    cube1 = (x < 3) & (y < 1) & (z < 2)
    cube2 = (x >= 6) & (y >= 6) & (z >= 6) & (z <= 8)
    cube3 = (x >= 4) & (x <= 5) & (y >= 3) & (y <= 5) & (z >= 4) & (z <= 5)

    # combine the objects into a single boolean array
    voxels = cube1 | cube2 | cube3

    # set the colors of each object
    colors = np.empty(voxels.shape, dtype=object)
    colors[cube3] = 'red'
    colors[cube1] = 'blue'
    colors[cube2] = 'green'

    # and plot everything
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.voxels(voxels, facecolors=colors, edgecolor='k')

    plt.show()


if __name__ == '__main__':
    test_3d_plotting_cube()
