from src.iterator.corner_space_iterator import SpaceIterator
from src.parameters.pallet_parameters import PalletParameters
from src.point import Point


START_POINT = Point(0, 0, 0)


class PalletSpaceIterator(SpaceIterator):
    def __init__(self, space, pallet_parameters: PalletParameters):
        super().__init__(space, START_POINT)
        self._pallet_parameters = pallet_parameters

    # TODO
    def _compute_next_point(self) -> Point:
        return self._current_point




