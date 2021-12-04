from abc import ABC, abstractmethod


class Container(ABC):
    def __init__(self, length, width, height, lifting_capacity):
        self.length = length
        self.width = width
        self.height = height
        self.lifting_capacity = lifting_capacity
