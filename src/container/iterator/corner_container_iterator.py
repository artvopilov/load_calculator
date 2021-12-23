from src.container.iterator.container_iterator import ContainerIterator
from src.point import Point


class CornerContainerIterator(ContainerIterator):
    def __init__(self, space):
        super().__init__(space)
        self._current_point = Point(0, 0, 0)

    def __next__(self) -> Point:
        self._current_point =  self._compute_next_point()
        return self._current_point

    def _compute_next_point(self) -> Point:
        if self._current_point.x < self._space.shape[0] - 1:
            return self._move_x()

        if self._current_point.y < self._space.shape[1] - 1:
            return self._move_y()

        if self._current_point.z < self._space.shape[2] - 1:
            return self._move_z()

        raise StopIteration

    def _move_x(self) -> Point:
        return Point(self._current_point.x + 1, self._current_point.y, self._current_point.z)

    def _move_y(self) -> Point:
        return Point(0, self._current_point.y + 1, self._current_point.z)

    def _move_z(self) -> Point:
        return Point(0, 0, self._current_point.z + 1)
