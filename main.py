import random
import sys
from datetime import datetime
from typing import Optional, Dict

import click
import matplotlib.colors as mcolors
import pandas as pd
from loguru import logger

from src.api.response_builder import ResponseBuilder
from src.image_3d_creator import Image3dCreator
from src.items.item_fabric import ItemFabric
from src.loading.loader import Loader
from src.loading.loading_type import LoadingType
from src.parameters.shipment_parameters import ShipmentParameters

COLORS = list(mcolors.CSS4_COLORS.keys())


def parse_shipment_counts(file_path: str) -> Dict[ShipmentParameters, int]:
    df = pd.read_excel(file_path)
    logger.info(f'Read df from {file_path}')

    shipment_counts = {}
    for ind, shipment in df.iterrows():
        shipment_params = ShipmentParameters(
            shipment['Наименование'],
            shipment['Упаковка'],
            shipment['Длина'],
            shipment['Ширина'],
            shipment['Высота'],
            shipment['Вес'],
            random.choice(COLORS),
            True,
            True,
            True,
            True,
            0
        )
        shipment_counts[shipment_params] = shipment['Количество']

    logger.info(f'Read {len(shipment_counts)} shipments')
    return shipment_counts


@click.command()
@click.option('-f', '--file-path', default='/Users/artemvopilov/Downloads/loading_example.xlsx')
@click.option('-l', '--loading-type', default='stable')
def main(file_path: Optional[str], loading_type: str):
    logger.remove()
    logger.add(sys.stdout, level='DEBUG')

    shipment_counts = parse_shipment_counts(file_path)
    logger.info(f'Shipment counts:')
    for shipment_params, cnt in shipment_counts.items():
        logger.info(str(shipment_params), cnt)

    loader = Loader({}, shipment_counts, LoadingType.from_name(loading_type), False, ItemFabric())
    loader.load()

    loaded_containers = loader.containers
    left_shipment_counts = loader.shipment_params

    response_builder = ResponseBuilder()
    response = response_builder.build(loaded_containers, left_shipment_counts)
    logger.info(f'Response: {response}')

    image_3d_creator = Image3dCreator(datetime.now())
    for container in loaded_containers:
        image_3d_creator.create(container)
    for shipment, count in left_shipment_counts.items():
        if count:
            logger.info(f'Not loaded {shipment}: {count}')


if __name__ == '__main__':
    main()
