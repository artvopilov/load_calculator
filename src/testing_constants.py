from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

SMALL_CONTAINER_COUNTS = {
    ContainerParameters(length=40, width=20, height=20, lifting_capacity=1000): 2,
    ContainerParameters(length=10, width=10, height=10, lifting_capacity=1000): 4,
}
SMALL_SHIPMENT_COUNTS = {
    ShipmentParameters(length=2, width=2, height=2, weight=1, color='blue', can_cant=True, can_stack=True): 100,
    ShipmentParameters(length=4, width=4, height=4, weight=1, color='r', can_cant=True, can_stack=True): 1,
    ShipmentParameters(length=6, width=5, height=12, weight=1, color='darkred', can_cant=True, can_stack=True): 20,
    ShipmentParameters(length=5, width=5, height=5, weight=1, color='orange', can_cant=True, can_stack=True): 5
}

CONTAINER_PARAMETERS = ContainerParameters(400, 200, 200, 100)
SHIPMENT_COUNTS = {
    ShipmentParameters(10, 10, 10, 2, 'b, True, True', True, True): 10,
    ShipmentParameters(50, 50, 50, 10, 'r', True, True): 1}
