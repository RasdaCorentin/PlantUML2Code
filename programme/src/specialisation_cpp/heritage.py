from .relation_cpp import RelationCpp


class Heritage(RelationCpp):

    def __init__(self, id_heritage, source, cible):
        super().__init__(id_heritage, source, cible, type_relation=None)
        self.id_heritage = id_heritage

    def generer_code(self) -> str:
        return "public " + self.cible.nom
