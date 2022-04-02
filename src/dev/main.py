import random
from datetime import datetime

import matplotlib.colors as mcolors
import pandas as pd

from src.items.item_fabric import ItemFabric
from src.loading.container_selector import ContainerSelector
from src.dev.image_3d_creator import Image3dCreator
from src.dev.testing_constants import CONTAINER_COUNTS, SHIPMENT_COUNTS
from src.loading.loader import Loader

COLORS = list(mcolors.CSS4_COLORS.keys())


def test_from_file() -> None:
    file_path = '/home/artem/Documents/Business/LoadCalculator/testCases/caseOne.ods'
    df = pd.read_excel(file_path, engine='odf', header=1, usecols=['Наименование', 'Упаковок', 'Размер коробки'],
                       skiprows=[2], skipfooter=1)
    names = df['Наименование']
    counts = df['Упаковок']
    sizes = df['Размер коробки']

    item_fabric = ItemFabric()
    shipment_counts = {}
    for n, c, s in zip(names, counts, sizes):
        length, width, height = list(map(lambda x: int(x), s.split('×')))
        shipment_params = item_fabric.create_shipment_params(n, 'type', length, width, height, 1,
                                                             random.choice(COLORS), True, True)
        shipment_counts[shipment_params] = c
    print(f'Read {len(shipment_counts)} shipments')

    container_selector = ContainerSelector()
    loader = Loader(CONTAINER_COUNTS, shipment_counts, item_fabric, container_selector)
    test_loading(loader)


def test_from_constants() -> None:
    item_fabric = ItemFabric()
    container_selector = ContainerSelector()
    loader = Loader(CONTAINER_COUNTS, SHIPMENT_COUNTS, item_fabric, container_selector)
    test_loading(loader)


def test_loading(loader: Loader) -> None:
    loader.load()
    containers = loader.containers
    left_shipment_counts = loader.shipments_counts

    now = datetime.now()
    image_3d_creator = Image3dCreator(now)
    for container in containers:
        print(container)
        image_3d_creator.create_iterative(container)
    for shipment, count in left_shipment_counts.items():
        if count:
            print(f'Not loaded {shipment}: {count}')


if __name__ == '__main__':
    test_from_file()