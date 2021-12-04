from abc import ABC, abstractmethod


class Shipment(ABC):
    def __init__(self, length, width, height, weight):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
