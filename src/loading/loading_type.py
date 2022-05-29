from enum import Enum


class LoadingType(Enum):
    COMPACT = 1
    STABLE = 2

    @staticmethod
    def from_name(name: str) -> 'LoadingType':
        return LoadingType[name.upper()]
