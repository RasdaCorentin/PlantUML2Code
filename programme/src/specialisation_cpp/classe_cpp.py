from .formattage import Formattage


class ClasseCpp(Formattage):

    def __init__(self, nom, est_abstraite=False):
        super().__init__(id_format=nom)
        self.nom = nom
        self.est_abstraite = est_abstraite
        self.attributs_cpp = []
        self.operations_cpp = []
        self.relations_cpp = []
        self.notes = []

    def get_attributs_cpp(self):
        return self.attributs_cpp

    def get_operations_cpp(self):
        return self.operations_cpp

    def generer_code(self) -> str:
        lignes = []

        # Commentaires depuis les notes UML
        for note in self.notes:
            lignes.append("// " + note)

        # Separer heritages/implementations des autres relations
        heritages = []
        autres = []
        for r in self.relations_cpp:
            if hasattr(r, 'id_heritage') or hasattr(r, 'id_impl'):
                heritages.append(r)
            else:
                autres.append(r)

        # Signature de classe
        if heritages:
            parents = ", ".join(r.generer_code() for r in heritages)
            lignes.append("class " + self.nom + " : " + parents + " {")
        else:
            lignes.append("class " + self.nom + " {")

        # Section public
        lignes.append("public:")
        for op in self.operations_cpp:
            lignes.append(op.generer_code())

        # Section private
        lignes.append("private:")
        for attr in self.attributs_cpp:
            lignes.append(attr.generer_code())
        for rel in autres:
            lignes.append("    // " + rel.type_relation.value.lower()
                          + " avec " + rel.cible.nom)
            lignes.append(rel.generer_code())

        lignes.append("};")
        return "\n".join(lignes)
