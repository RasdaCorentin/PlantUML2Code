from .visibilite import Visibilite
from .notes import Notes


class Operation(Notes):

    def __init__(self, nom, type_retour="void", visibilite=Visibilite.PUBLIC):
        self.nom = nom
        self.type_retour = type_retour
        self.visibilite = visibilite
        self.notes = []

    def ajouter_notes(self, texte):
        self.notes.append(texte)
