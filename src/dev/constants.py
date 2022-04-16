from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

CONTAINER_COUNTS = {
    ContainerParameters(6, '20DV', length=605, width=235, height=239, lifting_capacity=10000): 1,
}
SHIPMENT_COUNTS = {
    ShipmentParameters(2, '', '', length=42, width=25, height=17, weight=1, color='blue', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True): 19,
    ShipmentParameters(3, '', '', length=42, width=25, height=17, weight=1, color='red', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True): 88,
    ShipmentParameters(4, '', '', length=38, width=29, height=23, weight=1, color='green', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True): 100,
    ShipmentParameters(5, '', '', length=69, width=18, height=15, weight=1, color='yellow', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True): 4,
}
