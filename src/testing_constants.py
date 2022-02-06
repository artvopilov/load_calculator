from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

SMALL_CONTAINER_COUNTS = {ContainerParameters(40, 20, 20, 1000): 10}
SMALL_SHIPMENT_COUNTS = {
    ShipmentParameters(2, 2, 2, 1, 'blue', True, True): 100,
    ShipmentParameters(4, 4, 4, 1, 'r', True, True): 1,
    ShipmentParameters(6, 5, 12, 1, 'darkred', True, True): 20,
    ShipmentParameters(5, 5, 5, 1, 'orange', True, True): 5
}

CONTAINER_PARAMETERS = ContainerParameters(400, 200, 200, 100)
SHIPMENT_COUNTS = {
    ShipmentParameters(10, 10, 10, 2, 'b, True, True', True, True): 10,
    ShipmentParameters(50, 50, 50, 10, 'r', True, True): 1}
