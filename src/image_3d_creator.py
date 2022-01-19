from typing import List

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from src.point import Point


class Image3dCreator:
    POLYGONS = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
                [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
                [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
                [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
                [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
                [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]

    def create(self, positions: List[Point], sizes: List[Point], colors=List[str]) -> None:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_aspect('equal')

        cubes_collections = self._create_cubes_collection(positions, sizes, colors)
        ax.add_collection3d(cubes_collections)

        # ax.set_xlabel('X')
        ax.set_xlim(0, 20)
        # ax.set_ylabel('Y')
        ax.set_ylim(0, 20)
        # ax.set_zlabel('Z')
        ax.set_zlim(0, 20)

        plt.show()

    def _create_cubes_collection(
            self,
            positions: List[Point],
            sizes: List[Point],
            colors=List[str]
    ) -> Poly3DCollection:
        cubes = [self._compute_cube_data(position, size) for position, size in zip(positions, sizes)]
        return Poly3DCollection(np.concatenate(cubes), facecolors=np.repeat(colors, 6), edgecolor='k', alpha=0.1)

    def _compute_cube_data(self, point: Point, size: Point) -> np.array:
        polygons = np.array(self.POLYGONS, dtype=float)

        polygons[:, :, 0] *= size.x
        polygons[:, :, 1] *= size.y
        polygons[:, :, 2] *= size.z

        polygons += np.array([point.x, point.y, point.z])
        return polygons
