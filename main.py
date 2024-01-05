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
from src.loading.loader_factory import LoaderFactory
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

COLORS = list(mcolors.CSS4_COLORS.keys())


def parse_container_counts(file_path: str) -> Dict[ContainerParameters, int]:
    df = pd.read_excel(file_path)
    logger.info(f'Read df from {file_path}')

    container_counts = {}
    for ind, container in df.iterrows():
        container_params = ContainerParameters(
            container['Name'],
            container['Length'],
            container['Width'],
            container['Height'],
            container['Lifting capacity']
        )
        container_counts[container_params] = container['Quantity']

    logger.info(f'Read {len(container_counts)} containers')
    return container_counts


def parse_shipment_counts(file_path: str) -> Dict[ShipmentParameters, int]:
    df = pd.read_excel(file_path)
    logger.info(f'Read df from {file_path}')

    shipment_counts = {}
    for ind, shipment in df.iterrows():
        shipment_params = ShipmentParameters(
            shipment['Name'],
            shipment['Cargo type'],
            shipment['Length (cm)'] * 10,
            shipment['Width / Diameter for barrels (cm)'] * 10,
            shipment['Height (cm)'] * 10,
            shipment['Weight (kg)'],
            random.choice(COLORS),
            not pd.isna(shipment['Stack']),
            not pd.isna(shipment['Turn over (height)']),
            not pd.isna(shipment['Turn over (length)']),
            not pd.isna(shipment['Turn over (width)']),
            shipment['Extension']
        )
        shipment_counts[shipment_params] = shipment['Q-ty']

    logger.info(f'Read {len(shipment_counts)} shipments')
    return shipment_counts


@click.command()
@click.option('-v', '--logger-level', default='DEBUG')
@click.option('-s', '--shipments-file-path')
@click.option('-c', '--containers-file-path', default=None)
@click.option('-l', '--loading-type-name', default='compact')
def main(
        logger_level: str,
        shipments_file_path: str,
        containers_file_path: Optional[str],
        loading_type_name: Optional[str]
):
    logger.remove()
    logger.add(sys.stdout, level=logger_level)

    shipment_counts = parse_shipment_counts(shipments_file_path)
    logger.info(f'Parsed shipment counts')
    for shipment_params, cnt in shipment_counts.items():
        logger.debug(str(shipment_params), cnt)

    container_counts = None
    if containers_file_path is not None:
        container_counts = parse_container_counts(containers_file_path)
        logger.info(f'Parsed container counts')
        for container_params, cnt in container_counts.items():
            logger.debug(str(container_params), cnt)

    loader_factory = LoaderFactory()
    loader = loader_factory.create(shipment_counts, container_counts, loading_type_name)
    loader.load()

    loaded_containers = loader.containers
    left_shipment_counts = loader.shipment_params

    response_builder = ResponseBuilder()
    response = response_builder.build(loaded_containers, left_shipment_counts)
    logger.debug(f'Built response: {response}')

    image_3d_creator = Image3dCreator(datetime.now())
    for container in loaded_containers:
        image_3d_creator.create(container)

    for shipment, count in left_shipment_counts.items():
        if count > 0:
            logger.debug(f'Not loaded {shipment}: {count}')


if __name__ == '__main__':
    main()
