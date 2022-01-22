from abc import ABC, abstractmethod


class LiftingParameters(ABC):
    @property
    @abstractmethod
    def lifting_capacity(self) -> int:
        pass
