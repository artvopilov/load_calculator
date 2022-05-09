from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters

CONTAINER_COUNTS = {
    ContainerParameters('Фура', length=5895, width=2350, height=2393, lifting_capacity=28200): 1,
}
SHIPMENT_COUNTS = {
    ShipmentParameters('', '', length=1500, width=1000, height=1000, weight=100, color='blue', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.1): 20,
    ShipmentParameters('', '', length=1500, width=1000, height=100, weight=100, color='red', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.1): 20,
}
