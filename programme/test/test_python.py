"""Test complet : heritage, implementation, composition, association, notes."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.commun import ParseurPuml
from src.specialisation_python import GenerateurPython


def main():
    puml_path = os.path.join(os.path.dirname(__file__), "exemple_complet.puml")
    output_dir = os.path.join(os.path.dirname(__file__), "output_python")

    os.makedirs(output_dir, exist_ok=True)

    parseur = ParseurPuml(puml_path)
    diagramme = parseur.parser()

    print("== MODELE UML PARSE ==")
    for cls in diagramme.get_liste_classes():
        print("\nClasse:", cls.nom,
              "| abstraite:", cls.est_abstraite,
              "| interface:", cls.est_interface)
        print("  Notes:", cls.notes)
        print("  Attributs:", [(a.nom, a.type) for a in cls.get_attributs()])
        print("  Operations:", [(o.nom, o.type_retour) for o in cls.get_operations()])
        for type_rel, rel in cls.get_relations():
            print("  Relation:", type_rel,
                  "| id:", rel.id_relation,
                  "| card_src:", rel.cardinalite_source,
                  "| card_cible:", rel.cardinalite_cible)

    print("\n== GENERATION PYTHON ==")
    generateur = GenerateurPython()
    fichiers = generateur.generer_classe2_langage(diagramme)

    for fichier in fichiers:
        fichier.chemin_complet = output_dir
        fichier.sauvegarder()
        print("\n--- " + fichier.nom_fichier + " ---")
        print(fichier.generer_code())


if __name__ == "__main__":
    main()