import random
from datetime import datetime

import matplotlib.colors as mcolors
import pandas as pd

from src.api.response_builder import ResponseBuilder
from src.dev.constants import CONTAINER_COUNTS, SHIPMENT_COUNTS, SHIPMENT_COUNTS_2, CONTAINER_COUNTS_2, \
    SHIPMENT_COUNTS_3
from src.dev.image_3d_creator import Image3dCreator
from src.items.item_fabric import ItemFabric
from src.loading.loader import Loader
from src.loading.loading_type import LoadingType
from src.logger.console_logger import ConsoleLogger
from src.parameters.shipment_parameters import ShipmentParameters

COLORS = list(mcolors.CSS4_COLORS.keys())


def test_from_file() -> None:
    file_path = '/Users/artemvopilov/Business/LoadCalculator/testCases/caseOne.ods'
    df = pd.read_excel(file_path, engine='odf', header=1, usecols=['Наименование', 'Упаковок', 'Размер коробки'],
                       skiprows=[2], skipfooter=1)
    names = df['Наименование']
    counts = df['Упаковок']
    sizes = df['Размер коробки']

    shipment_counts = {}
    for n, c, s in zip(names, counts, sizes):
        length, width, height = list(map(lambda x: int(x), s.split('×')))
        shipment_params = ShipmentParameters(n, 'type', length, width, height, 1,
                                             random.choice(COLORS), True, True, True, True, 0.1)
        shipment_counts[shipment_params] = c
    print(f'Read {len(shipment_counts)} shipments')

    item_fabric = ItemFabric()
    logger = ConsoleLogger()
    loader = Loader(CONTAINER_COUNTS, shipment_counts, LoadingType.STABLE, item_fabric, logger)
    test_loading(loader)


def test_from_constants() -> None:
    item_fabric = ItemFabric()
    logger = ConsoleLogger()
    loader = Loader(CONTAINER_COUNTS_2, SHIPMENT_COUNTS, LoadingType.COMPACT, item_fabric, logger)
    test_loading(loader)


def test_loading(loader: Loader) -> None:
    loaded_containers = loader.load()
    left_shipment_counts = loader.get_left_shipments_counts()

    response_builder = ResponseBuilder()
    print(response_builder.build(loaded_containers, loader.get_left_shipments_counts()))

    now = datetime.now()
    image_3d_creator = Image3dCreator(now)
    for container in loaded_containers:
        print(container)
        image_3d_creator.create(container)
    for shipment, count in left_shipment_counts.items():
        if count:
            print(f'Not loaded {shipment}: {count}')


if __name__ == '__main__':
    test_from_constants()
