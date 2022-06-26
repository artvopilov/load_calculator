from enum import Enum


class Extension(Enum):
    UP = 1
    DOWN = 2

    @staticmethod
    def from_name(name: str) -> 'Extension':
        return Extension[name.upper()]