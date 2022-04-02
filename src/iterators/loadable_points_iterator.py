from typing import Optional, List

from src.items.container import Container
from src.iterators.space_iterator import SpaceIterator
from src.items.point import Point


class LoadablePointsIterator(SpaceIterator):
    _points: List[Point]
    _i: int

    def __init__(self, container: Container) -> None:
        super().__init__()
        self._points = sorted(container.loadable_point_to_max_points.keys(), key=lambda p: (p.y, p.x, p.z))
        # print('Loadable points:')
        # for p in self._points:
        #     print(p)
        #     for m_p in container.loadable_point_to_max_points[p]:
        #         print(f'Loadable point {m_p}')
        self._i = 0

    def _compute_start_point(self) -> Optional[Point]:
        return self._points[self._i]

    def _compute_next_empty_point(self) -> Optional[Point]:
        self._i += 1
        if self._i < len(self._points):
            return self._points[self._i]
        return None
