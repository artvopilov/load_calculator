from abc import ABC


class LoadParameters(ABC):
    _length: int
    _width: int
    _height: int

    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LoadParameters):
            return self.length == other.length \
                   and self.width == other.width \
                   and self.height == other.height

        return False


