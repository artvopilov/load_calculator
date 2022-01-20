from src.parameters.lifting_parameters import LiftingParameters
from src.parameters.volume_parameters import VolumeParameters


class ContainerParameters(VolumeParameters, LiftingParameters):
    _length: int
    _width: int
    _height: int
    _lifting_capacity: int

    def __init__(self, length: int, width: int, height: int, lifting_capacity: int) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._lifting_capacity = lifting_capacity

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity
