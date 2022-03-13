from datetime import datetime
from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tqdm import tqdm

from src.items.container import Container
from src.items.util_items.item import Item
from src.parameters.util_parameters.volume_parameters import VolumeParameters
from src.point import Point


class Image3dCreator:
    POLYGONS = [
        [[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
        [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
        [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
        [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
        [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
        [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]],
    ]

    X = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
    ]
    Y = [
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
    ]
    Z = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
    ]

    _current_time: datetime

    def __init__(self, current_time: datetime):
        self._current_time = current_time

    def create(self, container: Container) -> None:
        self._create(container, len(container.id_to_shipment))

    def create_iterative(self, container: Container) -> None:
        shipments_iterations_num = []
        last_shipment_params = None
        for n, shipment_id in enumerate(container.shipment_id_order):
            shipment = container.id_to_shipment[shipment_id]
            if shipment.parameters != last_shipment_params:
                shipments_iterations_num.append(n)
                last_shipment_params = shipment.parameters
        shipments_iterations_num.append(len(container.shipment_id_order))

        # pycharm shows only first n plots
        shipments_iterations_num_limited = np.random.choice(
            shipments_iterations_num, min(len(shipments_iterations_num), 20), replace=False)
        shipments_iterations_num_limited.sort()

        for iter_num in tqdm(shipments_iterations_num_limited):
            if iter_num == 0:
                continue
            self._create(container, int(iter_num))

    def _create(self, container: Container, shipments_num: int) -> None:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_aspect('equal')

        # self._plot_cubes(ax, container)
        poly_3d_collection = self._create_poly_3d_collection(container, shipments_num)
        ax.add_collection3d(poly_3d_collection)

        ax.set_xlim(0, container.length)
        ax.set_ylim(0, container.width)
        ax.set_zlim(0, container.height)

        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')

        ax.set_title(f'{self._current_time.strftime("%H:%M:%S")}\n{container}\nShipments:{shipments_num}')

        plt.show()

    def _create_poly_3d_collection(self, container: Container, shipments_num: int) -> Poly3DCollection:
        cubes = []
        colors = []

        for shipment_id in container.shipment_id_order[:shipments_num]:
            point = container.id_to_min_point[shipment_id]
            shipment = container.id_to_shipment[shipment_id]
            self._add_cube_data(point, shipment, cubes, colors)

        return Poly3DCollection(
            np.concatenate(cubes),
            facecolors=np.repeat(colors, len(self.POLYGONS)),
            edgecolor='k')

    def _add_cube_data(self, point: Point, item: Item, cubes: List[np.array], colors: List[str]):
        cube = self._compute_cube_data(point, item.parameters)
        cubes.append(cube)
        colors.append(item.parameters.color)

    def _compute_cube_data(self, point: Point, size: VolumeParameters) -> np.array:
        polygons = np.array(self.POLYGONS, dtype=float)

        polygons[:, :, 0] *= size.length
        polygons[:, :, 1] *= size.width
        polygons[:, :, 2] *= size.height

        polygons += np.array([point.x, point.y, point.z])
        return polygons

    def _plot_cubes(self, ax: Axes3D, container: Container) -> None:
        for id_, point in container.id_to_min_point.items():
            is_shipment = id_ in container.id_to_shipment
            item = container.id_to_shipment[id_] if is_shipment else container.id_to_pallet[id_]

            cube_coordinates = self._compute_cube_coordinates(point, item.parameters)

            ax.plot_surface(
                cube_coordinates[0],
                cube_coordinates[1],
                cube_coordinates[2],
                color=item.parameters.color,
                rstride=1,
                cstride=1,
                edgecolor='k',
                alpha=1)

    def _compute_cube_coordinates(self, position: Point, size: VolumeParameters) -> Tuple:
        x = np.array(self.X) * size.length
        y = np.array(self.Y) * size.width
        z = np.array(self.Z) * size.height

        x += position.x
        y += position.y
        z += position.z

        return x, y, z
