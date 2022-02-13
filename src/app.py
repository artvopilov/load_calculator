from datetime import datetime

from item_fabric import ItemFabric
from loader import Loader
from src.image_3d_creator import Image3dCreator
from src.testing_constants import CONTAINER_COUNTS, SHIPMENT_COUNTS


def test_loading():
    now = datetime.now()

    item_fabric = ItemFabric()
    loader = Loader(CONTAINER_COUNTS, SHIPMENT_COUNTS, item_fabric)

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
    test_loading()
