from .notes import Notes


class Relation(Notes):

    def __init__(self, id_relation, cardinalite_source="1", role_source="",
                 cardinalite_cible="1", role_cible=""):
        self.id_relation = id_relation
        self.cardinalite_source = cardinalite_source
        self.role_source = role_source
        self.cardinalite_cible = cardinalite_cible
        self.role_cible = role_cible
        self.notes = []

    def ajouter_notes(self, texte):
        self.notes.append(texte)


class Composition(Relation):
    pass


class Agregation(Relation):
    pass


class Heritage(Relation):
    pass
