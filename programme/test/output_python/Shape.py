from abc import ABC, abstractmethod

class Shape(ABC):
    """Classe abstraite de base pour toutes les formes"""
    def __init__(self):
        self.color = None
        self.x = None
        self.y = None

    @abstractmethod
    def getArea(self):
        pass

    @abstractmethod
    def move(self):
        pass
