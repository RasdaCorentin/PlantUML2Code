from abc import ABC, abstractmethod


class Formattage(ABC):

    def __init__(self, id_format):
        self.id_format = id_format

    @abstractmethod
    def generer_code(self) -> str:
        pass
