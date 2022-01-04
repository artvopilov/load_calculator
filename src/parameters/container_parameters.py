from src.parameters.load_parameters import LoadParameters


class ContainerParameters(LoadParameters):
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, lifting_capacity: int) -> None:
        super().__init__(length, width, height)
        self._lifting_capacity = lifting_capacity

    @property
    def lifting_capacity(self):
        return self._lifting_capacity

    def _key(self):
        return self.length, self.width, self.height, self.lifting_capacity
