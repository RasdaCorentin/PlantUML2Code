from ..generateur.generateur import Generateur
from ..generateur.langage_sortie import LangageSortie
from .type_fichier_cpp import TypeFichierCpp
from .fichier_cpp import FichierCpp
from .classe_cpp import ClasseCpp
from .attribut_cpp import AttributCpp
from .operation_cpp import OperationCpp
from .heritage import Heritage
from .implementation import Implementation
from .relation_cpp import RelationCpp
from .type_relation_cpp import TypeRelationCpp


# Mapping type de relation PUML vers TypeRelationCpp
RELATION_MAP = {
    "*--": TypeRelationCpp.AGREGATION,
    "o--": TypeRelationCpp.AGREGATION,
    "-->": TypeRelationCpp.ASSOCIATION,
    "--": TypeRelationCpp.ASSOCIATION,
}


class GenerateurCpp(Generateur):

    def __init__(self):
        super().__init__(langage=LangageSortie.CPP)

    def generer_bloc_commentaire(self) -> str:
        return "// Auto-generated C++ from PlantUML avec UMLFactory"

    def generer_classe2_langage(self, diagramme_classe):
        """Redefinition par specialisation (polymorphisme)."""
        # Premier passage : creer toutes les ClasseCpp
        classes_map = {}
        for uml_classe in diagramme_classe.get_liste_classes():
            classes_map[uml_classe.nom] = self._traduire_classe(uml_classe)

        # Second passage : traduire les relations avec les references reelles
        for uml_classe in diagramme_classe.get_liste_classes():
            classe_cpp = classes_map[uml_classe.nom]
            for type_rel, rel in uml_classe.get_relations():
                self._traduire_relation(
                    classe_cpp, type_rel, rel, classes_map
                )

        # Generer les fichiers
        fichiers = []
        for classe_cpp in classes_map.values():
            fichiers.append(self._generer_header(classe_cpp))
            fichiers.append(self._generer_source(classe_cpp))
        return fichiers

    def _traduire_classe(self, uml_classe):
        """Traduit une UMLClasse du modele commun en ClasseCpp."""
        classe = ClasseCpp(
            nom=uml_classe.nom,
            est_abstraite=uml_classe.est_abstraite
        )
        classe.notes = list(uml_classe.notes)

        # Attributs
        for attr in uml_classe.get_attributs():
            classe.attributs_cpp.append(AttributCpp(
                nom=attr.nom,
                type_cpp=attr.type
            ))

        # Operations
        for op in uml_classe.get_operations():
            classe.operations_cpp.append(OperationCpp(
                nom=op.nom,
                type_retour_cpp=op.type_retour
            ))

        return classe

    def _traduire_relation(self, classe_cpp, type_rel, rel, classes_map):
        """Traduit une relation UML en relation C++ avec cardinalite."""
        if type_rel == "heritage":
            cible = classes_map.get(rel.cible.nom, ClasseCpp(nom=rel.cible.nom))
            classe_cpp.relations_cpp.append(Heritage(
                id_heritage=rel.id_relation,
                source=classe_cpp,
                cible=cible
            ))
        elif type_rel == "implementation":
            cible = classes_map.get(rel.cible.nom, ClasseCpp(nom=rel.cible.nom))
            classe_cpp.relations_cpp.append(Implementation(
                id_impl=rel.id_relation,
                source=classe_cpp,
                cible=cible
            ))
        elif type_rel in RELATION_MAP:
            # Determiner source et cible depuis la relation
            if rel.source.nom == classe_cpp.nom:
                cible_nom = rel.cible.nom
                cardinalite = rel.cardinalite_cible
            else:
                cible_nom = rel.source.nom
                cardinalite = rel.cardinalite_source

            cible = classes_map.get(cible_nom, ClasseCpp(nom=cible_nom))
            rel_cpp = RelationCpp(
                id_relation=rel.id_relation,
                source=classe_cpp,
                cible=cible,
                type_relation=RELATION_MAP[type_rel]
            )
            rel_cpp.cardinalite = cardinalite
            classe_cpp.relations_cpp.append(rel_cpp)

    def _generer_header(self, classe_cpp) -> FichierCpp:
        fichier = FichierCpp(
            nom_fichier=classe_cpp.nom + ".h",
            type_fichier=TypeFichierCpp.HEADER
        )
        fichier.classes.append(classe_cpp)
        return fichier

    def _generer_source(self, classe_cpp) -> FichierCpp:
        fichier = FichierCpp(
            nom_fichier=classe_cpp.nom + ".cpp",
            type_fichier=TypeFichierCpp.SOURCE
        )
        fichier.classes.append(classe_cpp)
        return fichier
