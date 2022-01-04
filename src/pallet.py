from src.parameters.pallet_parameters import PalletParameters
from src.loadable_item import LoadableItem


class Pallet(LoadableItem):
    _lifting_capacity: int

    def __init__(self, parameters: PalletParameters, id_: int):
        super(Pallet, self).__init__(
            id_,
            parameters.length,
            parameters.width,
            parameters.height,
            parameters.weight)
        _lifting_capacity = parameters.lifting_capacity

    @property
    def lifting_capacity(self) -> int:
        return self._lifting_capacity

    def _key(self):
        return self.id, self.length, self.width, self.height, self.weight, self.lifting_capacity

    def __str__(self):
        return f'Pallet: ({self._key()})'



