from src.parameters.load_parameters import LoadParameters


class ShipmentParameters(LoadParameters):
    _weight: int

    def __init__(self, length: int, width: int, height: int, weight: int) -> None:
        super().__init__(length, width, height)
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def _key(self):
        return self.length, self.width, self.height, self.weight
