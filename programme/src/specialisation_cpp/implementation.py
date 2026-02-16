from .relation_cpp import RelationCpp


class Implementation(RelationCpp):

    def __init__(self, id_impl, source, cible):
        super().__init__(id_impl, source, cible, type_relation=None)
        self.id_impl = id_impl

    def generer_code(self) -> str:
        return "public " + self.cible.nom
