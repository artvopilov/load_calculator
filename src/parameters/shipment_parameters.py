from src.parameters.load_parameters import LoadParameters


class ShipmentParameters(LoadParameters):
    _weight: int

    def __init__(self, length: int, width: int, height: int, weight: int) -> None:
        super().__init__(length, width, height)
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ShipmentParameters):
            return super().__eq__(other) \
                   and self._weight == other.weight

        return False
