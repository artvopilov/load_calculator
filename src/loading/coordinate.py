from enum import Enum


class Coordinate(Enum):
    X = 1
    Y = 2
    Z = 3

    @staticmethod
    def from_name(name: str) -> 'Coordinate':
        return Coordinate[name.upper()]
