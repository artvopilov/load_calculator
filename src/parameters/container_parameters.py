from src.parameters.load_parameters import LoadParameters


class ContainerParameters(LoadParameters):
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, _lifting_capacity: int) -> None:
        super().__init__(length, width, height)
        self._lifting_capacity = _lifting_capacity

    @property
    def lifting_capacity(self):
        return self._lifting_capacity

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ContainerParameters):
            return super().__eq__(other) \
                   and self.lifting_capacity == other.lifting_capacity

        return False
