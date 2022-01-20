from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from src.point import Point


class Image3dCreator:
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

    def create(self, positions: List[Point], sizes: List[Point], colors=List[str]) -> None:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_aspect('equal')

        self._plot_cubes(ax, positions, sizes, colors)

        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)
        ax.set_zlim(0, 20)

        plt.show()

    def _plot_cubes(self, ax: Axes3D, positions: List[Point], sizes: List[Point], colors=List[str]) -> None:
        cubes_coordinates = [self._compute_cube_coordinates(position, size) for position, size in zip(positions, sizes)]
        for cube_coordinates, color in zip(cubes_coordinates, colors):
            ax.plot_surface(
                cube_coordinates[0],
                cube_coordinates[1],
                cube_coordinates[2],
                color=color,
                rstride=1,
                cstride=1,
                edgecolor='k',
                alpha=0.5)

    def _compute_cube_coordinates(self, position: Point, size: Point) -> Tuple:
        x = np.array(self.X) * size.x
        y = np.array(self.Y) * size.y
        z = np.array(self.Z) * size.z

        x += position.x
        y += position.y
        y += position.z

        return x, y, z
