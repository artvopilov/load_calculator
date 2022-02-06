from datetime import datetime

from item_fabric import ItemFabric
from loader import Loader
from src.image_3d_creator import Image3dCreator
from src.testing_constants import SMALL_CONTAINER_COUNTS, SMALL_SHIPMENT_COUNTS


def test_loading():
    now = datetime.now()

    item_fabric = ItemFabric()
    loader = Loader(SMALL_CONTAINER_COUNTS, SMALL_SHIPMENT_COUNTS, item_fabric)

    loader.load()

    containers = loader.containers
    non_loadable_shipments = loader.non_loadable_shipments

    image_3d_creator = Image3dCreator(now)
    for container in containers:
        print(container)
        # for id_, min_point in container.id_to_min_point.items():
        #     if min_point.z == 0:
        #         print(f'Is pallet: {id_ in container.id_to_pallet}')
        image_3d_creator.create_iterative(container)
    for shipment in non_loadable_shipments:
        print(shipment)


if __name__ == '__main__':
    test_loading()
