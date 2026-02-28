from abc import ABC, abstractmethod


class Notes(ABC):

    @abstractmethod
    def ajouter_notes(self, texte) -> None:
        pass
