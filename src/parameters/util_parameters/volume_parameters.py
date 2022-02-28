class VolumeParameters:
    _length: int
    _width: int
    _height: int

    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def compute_volume(self) -> int:
        return self.length * self.width * self.height

    def compute_area(self) -> int:
        return self.length * self.width
