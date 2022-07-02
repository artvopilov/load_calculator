from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2

    @staticmethod
    def from_name(name: str) -> 'Direction':
        return Direction[name.upper()]