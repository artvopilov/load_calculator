from src.parameters.volume_parameters import VolumeParameters


class ColorVolumeParameters(VolumeParameters):
    _color: str

    def __init__(self, length: int, width: int, height: int, color: str) -> None:
        super().__init__(length, width, height)
        self._color = color

    @property
    def color(self) -> str:
        return self._color
