from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from src.items.container import Container
from src.parameters.volume_parameters import VolumeParameters
from src.point import Point


class Image3dCreator:
    POLYGONS = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
                [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
                [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
                [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
                [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
                [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]

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

    def create(self, container: Container) -> None:
        print(f'Plotting {container}')

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_aspect('equal')

        # self._plot_cubes(ax, container)
        cubes_collections = self._create_cubes_collection(container)
        ax.add_collection3d(cubes_collections)

        ax.set_xlim(0, container.length)
        ax.set_ylim(0, container.width)
        ax.set_zlim(0, container.height)

        plt.show()

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
                alpha=0.5)

    def _compute_cube_coordinates(self, position: Point, size: VolumeParameters) -> Tuple:
        x = np.array(self.X) * size.length
        y = np.array(self.Y) * size.width
        z = np.array(self.Z) * size.height

        x += position.x
        y += position.y
        z += position.z

        return x, y, z

    def _create_cubes_collection(self, container: Container) -> Poly3DCollection:
        cubes = []
        colors = []
        for id_, point in container.id_to_min_point.items():
            is_shipment = id_ in container.id_to_shipment
            item = container.id_to_shipment[id_] if is_shipment else container.id_to_pallet[id_]

            cube = self._compute_cube_data(point, item.parameters)

            # print(f'Plotting {item} on {cube}')
            print(f'Plotting {item} on {point}')

            cubes.append(cube)
            colors.append(item.color)

        return Poly3DCollection(np.concatenate(cubes), facecolors=np.repeat(colors, 6), edgecolor='k')

    def _compute_cube_data(self, point: Point, size: VolumeParameters) -> np.array:
        polygons = np.array(self.POLYGONS, dtype=float)

        polygons[:, :, 0] *= size.length
        polygons[:, :, 1] *= size.width
        polygons[:, :, 2] *= size.height

        polygons += np.array([point.x, point.y, point.z])
        return polygons
