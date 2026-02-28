from abc import ABC, abstractmethod
from .commentaire import Commentaire


class Generateur(Commentaire, ABC):

    def __init__(self, langage):
        self.langage = langage

    @abstractmethod
    def generer_classe2_langage(self, diagramme_classe):
        pass
