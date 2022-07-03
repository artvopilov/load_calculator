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
CONTAINER_COUNTS_2 = {
    ContainerParameters('Фура', length=13600, width=2400, height=2600, lifting_capacity=28200): 1,
}
SHIPMENT_COUNTS = {
    ShipmentParameters('', '', length=1000, width=500, height=300, weight=100, color='blue', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0): 100,  # 100
    ShipmentParameters('', '', length=600, width=300, height=200, weight=50, color='green', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 50,  # 50
    ShipmentParameters('', '', length=500, width=500, height=300, weight=30, color='red', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 80,  # 80
}
SHIPMENT_COUNTS_2 = {
    ShipmentParameters('', '', length=1200, width=4600, height=1300, weight=100, color='darkblue', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 1,
    ShipmentParameters('', '', length=800, width=1200, height=1600, weight=100, color='lightgreen', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 1,
    ShipmentParameters('', '', length=800, width=1200, height=1900, weight=100, color='brown', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 2,
    ShipmentParameters('', '', length=900, width=1300, height=1900, weight=100, color='darkred', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 3,
}
SHIPMENT_COUNTS_3 = {
    ShipmentParameters('', '', length=1000, width=500, height=300, weight=100, color='blue', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 10,
    ShipmentParameters('', '', length=600, width=300, height=200, weight=50, color='green', can_stack=True,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 10,
    ShipmentParameters('', '', length=500, width=500, height=300, weight=30, color='red', can_stack=False,
                       height_as_height=True, length_as_height=True, width_as_height=True, extension=0.01): 10,
}
