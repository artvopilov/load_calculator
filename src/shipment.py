from src.parameters.shipment_parameters import ShipmentParameters
from src.loadable_item import LoadableItem


class Shipment(LoadableItem):
    def __init__(self, parameters: ShipmentParameters, id_: int):
        super(Shipment, self).__init__(
            id_,
            parameters.length,
            parameters.width,
            parameters.height,
            parameters.weight)

    def _key(self):
        return self.id, self.length, self.width, self.height, self.weight

    def __str__(self):
        return f'Shipment: ({self._key()})'


