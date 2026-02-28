from .formattage import Formattage
from .type_relation_cpp import TypeRelationCpp


class RelationCpp(Formattage):

    def __init__(self, id_relation, source, cible, type_relation):
        super().__init__(id_format=id_relation)
        self.id_relation = id_relation
        self.source = source
        self.cible = cible
        self.type_relation = type_relation
        self.cardinalite = "1"

    def _est_multiple(self):
        return self.cardinalite in ["*", "0..*", "1..*", "*..*"]

    def generer_code(self) -> str:
        nom_attr = self.cible.nom.lower()
        if self._est_multiple():
            return "    std::vector<" + self.cible.nom + "*> " + nom_attr + "List;"
        else:
            return "    " + self.cible.nom + "* " + nom_attr + ";"

    def generer_include(self) -> str:
        includes = '#include "' + self.cible.nom + '.h"'
        if self._est_multiple():
            includes = "#include <vector>\n" + includes
        return includes
