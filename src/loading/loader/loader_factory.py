from typing import Dict, Optional, ClassVar

from src.items.item_fabric import ItemFabric
from src.loading.loader.loader import Loader
from src.loading.loading_type import LoadingType
from src.parameters.container_parameters import ContainerParameters
from src.parameters.shipment_parameters import ShipmentParameters


class LoaderFactory:
    _DEFAULT_CONTAINER_PARAMS: ClassVar[Dict[ContainerParameters, int]] = {
        ContainerParameters('20DV', length=5895, width=2350, height=2393, lifting_capacity=28200): -1,
        ContainerParameters('40DV', length=12032, width=2350, height=2393, lifting_capacity=28800): -1,
        ContainerParameters('40HQ', length=12032, width=2350, height=2697, lifting_capacity=28620): -1,
        ContainerParameters('45HQ', length=13556, width=2350, height=2697, lifting_capacity=27600): -1
    }

    def create(
            self,
            shipment_params: Dict[ShipmentParameters, int],
            container_params: Optional[Dict[ContainerParameters, int]] = None,
            loading_type_name: Optional[str] = 'compact',
            with_order: Optional[bool] = True
    ) -> Loader:
        container_params = self._resolve_container_params(container_params)
        loading_type = LoadingType.from_name(loading_type_name)
        item_factory = ItemFabric()
        return Loader(shipment_params, container_params, loading_type, with_order, item_factory)

    def _resolve_container_params(
            self,
            container_params: Optional[Dict[ContainerParameters, int]]
    ) -> Dict[ContainerParameters, int]:
        if container_params is None:
            container_params = self._DEFAULT_CONTAINER_PARAMS
        return container_params
