from abc import ABC, abstractmethod


class SpaceIterator(ABC):
    def __init__(self, space):
        self._space = space
        self._last_point = None

    def __iter__(self):
        return self
