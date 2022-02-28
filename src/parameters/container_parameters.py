from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ContainerParameters(VolumeParameters):
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, lifting_capacity: int) -> None:
        VolumeParameters.__init__(self, length, width, height)
        self._lifting_capacity = lifting_capacity

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity
