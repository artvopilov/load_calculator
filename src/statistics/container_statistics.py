from src.loading.point.point import Point
from src.parameters.shipment_parameters import ShipmentParameters


class ContainerStatistics:
    _LDM_WIDTH_COEFFICIENT: int = 2400

    _shipments: int
    _loaded_volume: float
    _loaded_length: float
    _loaded_width: float
    _ldm: float

    def __init__(self) -> None:
        self.reset()

    @property
    def shipments(self) -> int:
        return self._shipments

    @property
    def loaded_volume(self) -> float:
        return self._loaded_volume

    @property
    def loaded_length(self) -> float:
        return self._loaded_length

    @property
    def loaded_width(self) -> float:
        return self._loaded_width

    @property
    def ldm(self) -> float:
        return self._ldm

    def reset(self) -> None:
        self._shipments = 0
        self._loaded_volume = 0
        self._loaded_length = 0
        self._loaded_width = 0
        self._ldm = 0

    def update(self, point: Point, shipment_params: ShipmentParameters) -> None:
        self._shipments += 1
        self._loaded_volume += shipment_params.compute_loading_volume()
        self._loaded_length = max(self._loaded_length, point.x + shipment_params.get_loading_length())
        self._loaded_width = max(self._loaded_width, point.y + shipment_params.get_loading_width())
        self._ldm = self._loaded_length * self._loaded_width / self._LDM_WIDTH_COEFFICIENT
