import random
from datetime import datetime

import matplotlib.colors as mcolors
import pandas as pd

from item_fabric import ItemFabric
from loader import Loader
from src.container_selector import ContainerSelector
from src.image_3d_creator import Image3dCreator
from src.parameters.shipment_parameters import ShipmentParameters
from src.testing_constants import CONTAINER_COUNTS, SHIPMENT_COUNTS

COLORS = list(mcolors.CSS4_COLORS.keys())


def test_from_file():
    file_path = '/home/artem/Documents/Business/LoadCalculator/testCases/caseOne.ods'
    df = pd.read_excel(file_path, engine='odf', header=1, usecols=['Наименование', 'Упаковок', 'Размер коробки'],
                       skiprows=[2], skipfooter=1)

    names = df['Наименование']
    counts = df['Упаковок']
    sizes = df['Размер коробки']

    shipment_counts = {}
    for n, c, s in zip(names, counts, sizes):
        length, width, height = list(map(lambda x: int(x), s.split('×')))
        shipment_params = ShipmentParameters(n, length, width, height, 1, random.choice(COLORS), True, True)
        shipment_counts[shipment_params] = c
    print(shipment_counts)

    now = datetime.now()

    item_fabric = ItemFabric()
    container_selector = ContainerSelector()
    loader = Loader(CONTAINER_COUNTS, shipment_counts, item_fabric, container_selector)

    loader.load()

    containers = loader.containers
    left_shipment_counts = loader.shipments_counts

    image_3d_creator = Image3dCreator(now)
    for container in containers:
        print(container)
        image_3d_creator.create_iterative(container)
    for shipment, count in left_shipment_counts.items():
        print(f'Not loaded {shipment}: {count}')


def test():
    now = datetime.now()

    item_fabric = ItemFabric()
    container_selector = ContainerSelector()
    loader = Loader(CONTAINER_COUNTS, SHIPMENT_COUNTS, item_fabric, container_selector)

    loader.load()

    containers = loader.containers
    left_shipment_counts = loader.shipments_counts

    image_3d_creator = Image3dCreator(now)
    for container in containers:
        print(container)
        image_3d_creator.create_iterative(container)
    for shipment, count in left_shipment_counts.items():
        print(f'Not loaded {shipment}: {count}')


if __name__ == '__main__':
    test_from_file()
