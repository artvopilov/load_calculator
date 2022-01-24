from item_fabric import ItemFabric
from loader import Loader
from src.image_3d_creator import Image3dCreator
from src.testing_constants import SMALL_CONTAINER_PARAMETERS, SMALL_SHIPMENT_COUNTS, SMALL_PALLET_PARAMETERS


def test_loading():
    item_fabric = ItemFabric()
    loader = Loader(SMALL_CONTAINER_PARAMETERS, SMALL_SHIPMENT_COUNTS, SMALL_PALLET_PARAMETERS, item_fabric)

    loader.load()

    containers = loader.containers
    print(len(containers))
    non_loadable_shipments = loader.non_loadable_shipments

    image_3d_creator = Image3dCreator()
    for container in containers:
        print(container)
        # for id_, min_point in container.id_to_min_point.items():
        #     if min_point.z == 0:
        #         print(f'Is pallet: {id_ in container.id_to_pallet}')
        image_3d_creator.create(container)
    for shipment in non_loadable_shipments:
        print(shipment)


if __name__ == '__main__':
    test_loading()
