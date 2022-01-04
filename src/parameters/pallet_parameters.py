from src.parameters.load_parameters import LoadParameters


class PalletParameters(LoadParameters):
    _weight: int
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, weight: int, lifting_capacity: int) -> None:
        super().__init__(length, width, height)
        self._weight = weight
        self._lifting_capacity = lifting_capacity

    @property
    def weight(self):
        return self._weight

    @property
    def lifting_capacity(self):
        return self._lifting_capacity

    def _key(self):
        return self.length, self.width, self.height, self.weight, self.lifting_capacity
