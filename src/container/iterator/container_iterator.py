from abc import ABC


class ContainerIterator(ABC):
    def __init__(self, space):
        self._space = space

    def __iter__(self):
        return self
