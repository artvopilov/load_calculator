from typing import Tuple, Dict

from src.parameters.util_parameters.item_parameters import ItemParameters
from src.parameters.util_parameters.volume_parameters import VolumeParameters


class ContainerParameters(VolumeParameters, ItemParameters):
    _lifting_capacity: int

    def __init__(self, id_: int, length: int, width: int, height: int, lifting_capacity: int) -> None:
        ItemParameters.__init__(self, id_)
        VolumeParameters.__init__(self, length, width, height)
        self._lifting_capacity = lifting_capacity

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity

    def _key(self) -> Tuple:
        return self.length, self.width, self.height, self.lifting_capacity

    def __str__(self) -> str:
        return f'Container parameters: ({self._key()})'

    def build_response(self) -> Dict:
        return {
            'height': self.height,
            'length': self.length,
            'width': self.width,
            'weight': self.lifting_capacity,
            'type': 'type'
        }


