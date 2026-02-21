from abc import ABC, abstractmethod

class Drawable(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass
