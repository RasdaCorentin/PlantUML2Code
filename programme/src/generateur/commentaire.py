from abc import ABC, abstractmethod


class Commentaire(ABC):

    @abstractmethod
    def generer_bloc_commentaire(self) -> str:
        pass
