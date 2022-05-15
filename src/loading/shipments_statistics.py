class ShipmentsStatistics:
    _volume: float
    _weight: float
    _max_dimension: float
    _min_dimension: float

    def __init__(self, volume: float, weight: float, max_dimension: float, min_dimension: float) -> None:
        self._volume = volume
        self._weight = weight
        self._max_dimension = max_dimension
        self._min_dimension = min_dimension

    @property
    def volume(self) -> float:
        return self._volume

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def max_dimension(self) -> float:
        return self._max_dimension

    @property
    def min_dimension(self) -> float:
        return self._min_dimension
