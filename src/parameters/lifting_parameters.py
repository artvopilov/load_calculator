from abc import ABC, abstractmethod


class LiftingParameters(ABC):
    @abstractmethod
    def lifting_capacity(self) -> int:
        pass
