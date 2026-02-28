import os
from .formattage import Formattage
from .type_fichier_cpp import TypeFichierCpp


class FichierCpp(Formattage):

    def __init__(self, nom_fichier, type_fichier, chemin_complet=""):
        super().__init__(id_format=nom_fichier)
        self.nom_fichier = nom_fichier
        self.type_fichier = type_fichier
        self.chemin_complet = chemin_complet
        self.classes = []

    def generer_code(self) -> str:
        """Delegation : appelle ClasseCpp.genererCode()"""
        lignes = []

        if self.type_fichier == TypeFichierCpp.HEADER:
            guard = self.nom_fichier.replace(".", "_").upper()
            lignes.append("#ifndef " + guard)
            lignes.append("#define " + guard)
            lignes.append("")

            # Includes des relations (chaque ligne dedupliquee)
            includes_set = set()
            for classe in self.classes:
                for rel in classe.relations_cpp:
                    if hasattr(rel, 'generer_include'):
                        for line in rel.generer_include().split("\n"):
                            if line and line not in includes_set:
                                includes_set.add(line)
                                lignes.append(line)
            if len(lignes) > 3:
                lignes.append("")

            for classe in self.classes:
                lignes.append(classe.generer_code())
                lignes.append("")

            lignes.append("#endif")

        elif self.type_fichier == TypeFichierCpp.SOURCE:
            header = self.nom_fichier.replace(".cpp", ".h")
            lignes.append('#include "' + header + '"')
            lignes.append("")
            for classe in self.classes:
                for op in classe.get_operations_cpp():
                    if not op.est_virtuelle_pure:
                        lignes.append(op.type_retour_cpp + " " + classe.nom
                                      + "::" + op.nom + "() {")
                        lignes.append("}")
                        lignes.append("")

        return "\n".join(lignes)

    def sauvegarder(self):
        chemin = os.path.join(self.chemin_complet, self.nom_fichier)
        os.makedirs(self.chemin_complet, exist_ok=True)
        with open(chemin, "w") as f:
            f.write(self.generer_code())
