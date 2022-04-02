import random
from datetime import datetime

import matplotlib.colors as mcolors
import pandas as pd

from item_fabric import ItemFabric
from loader import Loader
from src.loading.container_selector import ContainerSelector
from src.dev.image_3d_creator import Image3dCreator
from src.dev.testing_constants import CONTAINER_COUNTS, SHIPMENT_COUNTS

COLORS = list(mcolors.CSS4_COLORS.keys())


def test_from_file():
    file_path = '/testCases/caseOne.ods'
    df = pd.read_excel(file_path, engine='odf', header=1, usecols=['Наименование', 'Упаковок', 'Размер коробки'],
                       skiprows=[2], skipfooter=1)

    names = df['Наименование']
    counts = df['Упаковок']
    sizes = df['Размер коробки']

    item_fabric = ItemFabric()

    shipment_counts = {}
    for n, c, s in zip(names, counts, sizes):
        length, width, height = list(map(lambda x: int(x), s.split('×')))
        shipment_params = item_fabric.create_shipment_params(n, length, width, height, 1,
                                                             random.choice(COLORS), True, True)
        shipment_counts[shipment_params] = c
    print(f'Read {len(shipment_counts)} shipments')

    now = datetime.now()

    container_selector = ContainerSelector()
    loader = Loader(CONTAINER_COUNTS, shipment_counts, item_fabric, container_selector)

    loader.load()

    containers = loader.containers
    left_shipment_counts = loader.shipments_counts

    image_3d_creator = Image3dCreator(now)
    for container in containers:
        print(container)
        image_3d_creator.create(container)
    for shipment, count in left_shipment_counts.items():
        if count:
            print(f'Not loaded {shipment}: {count}')

    return containers, left_shipment_counts


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
        if count:
            print(f'Not loaded {shipment}: {count}')


# def dump_to_json(containers: List[Container], left_shipment_counts: Dict[ShipmentParameters, int]) -> None:
#     json_data = {'containers': [], 'cargos_left': []}
#     for c in containers:
#         shipment_params_id_to_shipment = {}
#         points = []
#         for shipment_id in c.shipment_id_order:
#             point = c.id_to_min_point[shipment_id]
#             shipment = c.id_to_shipment[shipment_id]
#
#             shipment_params_id = shipment.parameters.id
#             shipment_meta = {
#                 'width': shipment.width,
#                 'height': shipment.height,
#                 'length': shipment.length,
#                 'diameter': 0,
#                 'type': 'type',
#                 'name': shipment.parameters.name,
#                 'stack': shipment.parameters.can_stack,
#                 'cant': shipment.parameters.can_cant,
#             }
#             shipment_params_id_to_shipment[shipment_params_id] = shipment_meta
#
#             point_meta = {
#                 'x': point.x,
#                 'y': point.y,
#                 'z': point.z,
#                 'cargo_id': shipment_params_id
#             }
#             points.append(point_meta)
#
#         container_meta = {
#             'height': c.height,
#             'length': c.length,
#             'width': c.width,
#             'weight': c.lifting_capacity,
#             'type': 'type',
#         }
#         json_data['containers'].append(container_meta)
#         json_data['containers'][-1]['cargos'] = shipment_params_id_to_shipment
#         json_data['containers'][-1]['load_points'] = points
#
#     with open('response.json', 'w', encoding='utf-8') as f:
#         json.dump(json_data, f, ensure_ascii=False)


if __name__ == '__main__':
    containers, left_shipment_counts = test_from_file()
    # dump_to_json(containers, left_shipment_counts)
