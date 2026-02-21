from .visibilite import Visibilite


class Attribut:

    def __init__(self, nom, type_, visibilite=Visibilite.PRIVE):
        self.nom = nom
        self.type = type_
        self.visibilite = visibilite
