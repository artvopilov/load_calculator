from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

CONTAINER_COUNTS = {
    ContainerParameters(length=605, width=235, height=239, lifting_capacity=1000): 1,
}
SHIPMENT_COUNTS = {
    ShipmentParameters(length=42, width=25, height=17, weight=1, color='blue', can_cant=True, can_stack=True): 19,
    ShipmentParameters(length=42, width=25, height=17, weight=1, color='red', can_cant=True, can_stack=True): 88,
    ShipmentParameters(length=38, width=29, height=23, weight=1, color='green', can_cant=True, can_stack=True): 100,
    ShipmentParameters(length=69, width=18, height=15, weight=1, color='yellow', can_cant=True, can_stack=True): 4,
}
