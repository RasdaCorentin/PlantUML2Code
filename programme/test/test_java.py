"""Test complet de l'extension Java : héritage, implémentation, composition, etc."""
import os
import sys

# Ajout du dossier racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.commun import ParseurPuml
from src.specialisation_java.generateur_java import GenerateurJava

def main():
    puml_path = os.path.join(os.path.dirname(__file__), "exemple_complet.puml")
    output_dir = os.path.join(os.path.dirname(__file__), "output_java")

    # Créer le dossier output_java s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Parsing du modèle UML
    parseur = ParseurPuml(puml_path)
    diagramme = parseur.parser()

    print("== MODELE UML PARSE (JAVA) ==")
    for cls in diagramme.get_liste_classes():
        print(f"\nClasse: {cls.nom} | abstraite: {cls.est_abstraite} | interface: {getattr(cls, 'est_interface', False)}")
        print("  Attributs:", [(a.nom, a.type) for a in cls.get_attributs()])
        for type_rel, rel in cls.get_relations():
            print(f"  Relation: {type_rel} | cible: {rel.cible.nom}")

    print("\n== GENERATION JAVA EN COURS... ==")
    # 2. Utilisation de TON générateur
    generateur = GenerateurJava()
    fichiers = generateur.generer_classe2_langage(diagramme)

    # 3. Écriture des fichiers
    for fichier_dict in fichiers:
        chemin_complet = os.path.join(output_dir, fichier_dict["nom_fichier"])
        contenu = fichier_dict["contenu"]
        
        # Sauvegarde sur le disque
        with open(chemin_complet, "w", encoding="utf-8") as f:
            f.write(contenu)
            
        print(f"\n--- {fichier_dict['nom_fichier']} ---")
        print(contenu)
        
    print(f"\n Terminé ! Les fichiers Java sont dans : {output_dir}")

if __name__ == "__main__":
    main()