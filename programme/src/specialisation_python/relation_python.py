class RelationPython:
    def __init__(self, id_relation, source, cible, type_relation, cardinalite=None):
        self.id_relation = id_relation
        self.source = source
        self.cible = cible
        self.type_relation = type_relation
        self.cardinalite = cardinalite
