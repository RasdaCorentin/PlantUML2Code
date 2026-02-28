from ..generateur.generateur import Generateur
from ..generateur.langage_sortie import LangageSortie

from .fichier_python import FichierPython
from .classe_python import ClassePython
from .attribut_python import AttributPython
from .operation_python import OperationPython
from .relation_python import RelationPython
from .type_relation_python import TypeRelationPython


RELATION_MAP = {
    "*--": TypeRelationPython.AGREGATION,
    "o--": TypeRelationPython.AGREGATION,
    "-->": TypeRelationPython.ASSOCIATION,
    "--": TypeRelationPython.ASSOCIATION,
}


class GenerateurPython(Generateur):

    def __init__(self):
        super().__init__(langage=LangageSortie.PYTHON)

    def generer_bloc_commentaire(self) -> str:
        return "# Auto-generated Python from PlantUML avec UMLFactory"

    def generer_classe2_langage(self, diagramme_classe):

        classes_map = {}

        for uml_classe in diagramme_classe.get_liste_classes():
            classes_map[uml_classe.nom] = self._traduire_classe(uml_classe)

        for uml_classe in diagramme_classe.get_liste_classes():
            classe_py = classes_map[uml_classe.nom]
            for type_rel, rel in uml_classe.get_relations():
                self._traduire_relation(classe_py, type_rel, rel, classes_map)

        fichiers = []
        for classe_py in classes_map.values():
            fichiers.append(self._generer_module(classe_py))

        return fichiers

    def _traduire_classe(self, uml_classe):

        classe = ClassePython(
            nom=uml_classe.nom,
            est_abstraite=uml_classe.est_abstraite
        )

        classe.est_interface = uml_classe.est_interface
        classe.notes = list(getattr(uml_classe, "notes", []))

        for attr in uml_classe.get_attributs():
            classe.attributs_py.append(
                AttributPython(
                    nom=attr.nom,
                    type_py=getattr(attr, "type", "Any")
                )
            )

        for op in uml_classe.get_operations():
            classe.operations_py.append(
                OperationPython(
                    nom=op.nom,
                    type_retour_py=getattr(op, "type_retour", "Any")
                )
            )

        return classe

    def _traduire_relation(self, classe_py, type_rel, rel, classes_map):

        if type_rel == "heritage":
            cible = classes_map.get(rel.cible.nom, ClassePython(nom=rel.cible.nom))
            classe_py.parent = cible.nom

        elif type_rel == "implementation":
            cible = classes_map.get(rel.cible.nom, ClassePython(nom=rel.cible.nom))
            classe_py.interfaces.append(cible.nom)

        elif type_rel in RELATION_MAP:

            if rel.source.nom == classe_py.nom:
                cible_nom = rel.cible.nom
                cardinalite = rel.cardinalite_cible
            else:
                cible_nom = rel.source.nom
                cardinalite = rel.cardinalite_source

            cible = classes_map.get(cible_nom, ClassePython(nom=cible_nom))

            rel_py = RelationPython(
                id_relation=rel.id_relation,
                source=classe_py,
                cible=cible,
                type_relation=RELATION_MAP[type_rel],
                cardinalite=cardinalite
            )

            classe_py.relations_py.append(rel_py)

    def _generer_module(self, classe_py: ClassePython) -> FichierPython:
        fichier = FichierPython(nom_fichier=classe_py.nom + ".py")
        fichier.classes.append(classe_py)
        return fichier
