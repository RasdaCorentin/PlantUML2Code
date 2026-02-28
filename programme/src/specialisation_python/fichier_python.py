import os

class FichierPython:
    def __init__(self, nom_fichier: str):
        self.nom_fichier = nom_fichier
        self.classes = []
        self.chemin_complet = "."

    def generer_code(self) -> str:
        lignes = []

        besoin_abc = False
        for c in self.classes:
            if getattr(c, "est_interface", False) or getattr(c, "est_abstraite", False):
                besoin_abc = True
                break

        if besoin_abc:
            lignes.append("from abc import ABC, abstractmethod")
            lignes.append("")

        for c in self.classes:
            parent = getattr(c, "parent", None)
            est_interface = getattr(c, "est_interface", False)
            est_abstraite = getattr(c, "est_abstraite", False)
            interfaces = getattr(c, "interfaces", []) or []

            bases = []
            if parent:
                bases.append(parent)
            for itf in interfaces:
                if itf not in bases:
                    bases.append(itf)
            if est_interface or est_abstraite:
                if "ABC" not in bases:
                    bases.append("ABC")

            if bases:
                lignes.append(f"class {c.nom}({', '.join(bases)}):")
            else:
                lignes.append(f"class {c.nom}:")

            notes = getattr(c, "notes", [])
            if notes:
                txt = "\\n".join(notes)
                lignes.append(f'    """{txt}"""')

            attributs = getattr(c, "attributs_py", []) or []
            operations = getattr(c, "operations_py", []) or []

            if attributs or operations or parent:
                lignes.append("    def __init__(self):")
                if parent:
                    lignes.append("        super().__init__()")
                if attributs:
                    for a in attributs:
                        lignes.append(f"        self.{a.nom} = None")
                else:
                    if not parent:
                        lignes.append("        pass")

                for op in operations:
                    lignes.append("")
                    if est_interface or est_abstraite:
                        lignes.append("    @abstractmethod")
                    lignes.append(f"    def {op.nom}(self):")
                    lignes.append("        pass")
            else:
                if not notes:
                    lignes.append("    pass")

            lignes.append("")

        return "\n".join(lignes).rstrip() + "\n"

    def sauvegarder(self) -> None:
        os.makedirs(self.chemin_complet, exist_ok=True)
        chemin = os.path.join(self.chemin_complet, self.nom_fichier)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(self.generer_code())
