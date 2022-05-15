from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


AUTO_CONTAINERS = [
    ContainerParameters('20DV', length=5895, width=2350, height=2393, lifting_capacity=28200),
    ContainerParameters('40DV', length=12032, width=2350, height=2393, lifting_capacity=28800),
    ContainerParameters('40HQ', length=12032, width=2350, height=2697, lifting_capacity=28620),
    ContainerParameters('45HQ', length=13556, width=2350, height=2697, lifting_capacity=27600),
]
CONTAINER_COUNTS = {
    ContainerParameters('Фура', length=5895, width=2350, height=2393, lifting_capacity=28200): 1,
}
SHIPMENT_COUNTS = {
    ShipmentParameters('', '', length=1000, width=1000, height=1000, weight=100, color='blue', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 100,
}
