from space_iterator import SpaceIterator
from point import Point


class CornerSpaceIterator(SpaceIterator):
    def __init__(self, space):
        super().__init__(space)

    def __next__(self) -> Point:
        if self._last_point is None:
            return Point(0, 0, 0)

        x = self._last_point.x
        y = self._last_point.y
        z = self._last_point.z

        if x + 1 < self._space.shape[0]:
            x += 1
        else:
            x = 0
            if y + 1 < self._space.shape[1]:
                y += 1
            else:
                y = 0
                if z + 1 < self._space.shape[2]:
                    z += 1
                else:
                    raise StopIteration

        return Point(x, y, z)
