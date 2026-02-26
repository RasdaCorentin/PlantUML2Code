# CCO — TP Projet noté : Architecture avec composants partagés

**Cours :** Conception et Construction Orientées Objet
**Année universitaire :** 2025–2026
**Professeur :** Rémy COURDIER
**Établissement :** Université de La Réunion — ESIROI (Informatique)

---

## Description

Ce projet implémente un générateur de code orienté objet à partir de diagrammes UML écrits en PlantUML (`.puml`).
L'outil lit un fichier PlantUML, construit un modèle UML en mémoire, puis génère du code source dans le langage cible choisi.

L'architecture repose sur **une partie commune partagée** entre tous les étudiants et **trois extensions spécialisées**, chacune développée individuellement.

---

## Étudiants et contributions

| Étudiant | Extension | Classe de référence | Branche |
|---|---|---|---|
| **Corentin RASDA** | C++ | `GenerateurCpp` | `feature/Corentin` |
| **Enzo POIRIER** | Python | `GenerateurPython` | `feature/Enzo` |
| **Benoît DIJOUX** | Java | `GenerateurJava` | `feature/Benoit` |

---

## Architecture du projet

```
programme/
├── src/
│   ├── commun/                  # Composants partagés (métamodèle UML)
│   │   ├── uml_classe.py        # Représentation d'une classe UML
│   │   ├── attribut.py          # Attribut d'une classe
│   │   ├── operation.py         # Opération / méthode
│   │   ├── relation.py          # Relation entre classes
│   │   ├── notes.py             # Notes PlantUML
│   │   ├── visibilite.py        # Visibilité (public, private, protected)
│   │   ├── diagramme_classe.py  # Conteneur du diagramme complet
│   │   └── parseur_puml.py      # Parseur de fichiers .puml
│   ├── generateur/              # Couche d'abstraction de génération
│   │   ├── generateur.py        # Classe abstraite Generateur
│   │   ├── commentaire.py       # Génération des commentaires
│   │   ├── convertisseur.py     # Convertisseur de types UML
│   │   └── langage_sortie.py    # Enumération des langages cibles
│   ├── specialisation_cpp/      # Extension C++ (Corentin RASDA)
│   │   ├── generateur_cpp.py
│   │   ├── classe_cpp.py
│   │   ├── attribut_cpp.py
│   │   ├── operation_cpp.py
│   │   ├── fichier_cpp.py
│   │   ├── relation_cpp.py
│   │   ├── heritage.py
│   │   ├── implementation.py
│   │   ├── formattage.py
│   │   ├── type_fichier_cpp.py
│   │   └── type_relation_cpp.py
│   ├── specialisation_python/   # Extension Python (Enzo POIRIER)
│   │   └── generateur_python.py
│   └── specialisation_java/     # Extension Java (Benoît DIJOUX)
│       ├── generateur_java.py
│       ├── classe_java.py
│       ├── attribut_java.py
│       ├── methode_java.py
│       ├── generable_java.py
│       └── visibilite.py
├── test/                        # Fichiers de test
│   ├── exemple_complet.puml
│   ├── test_complet.py
│   └── test_java.py
└── umlfactory2java.py           # Point d'entrée principal
doc/
├── fichier_puml/                # Diagrammes UML du projet
│   ├── diagramme_commun.puml
│   ├── diagramme_generateur_cpp.puml
│   ├── diagramme_generateur_python.puml
│   └── diagramme_generateur_java.puml
└── images/                      # Exports PNG des diagrammes
```

---

## Partie commune partagée

La partie commune, co-développée par les trois étudiants, comprend :

- **Métamodèle UML** : `UmlClasse`, `Attribut`, `Operation`, `Relation`, `Notes`, `Visibilite`
- **`DiagrammeClasse`** : conteneur représentant l'ensemble du diagramme
- **`ParseurPuml`** : analyse les fichiers `.puml` et construit le métamodèle
- **`Generateur`** (classe abstraite) : définit le contrat de génération via `generer_classe2_langage(diagramme_classe)`
- **`Commentaire`**, **`Convertisseur`**, **`LangageSortie`** : utilitaires de génération

---

## Extensions spécialisées

### Extension C++ — Corentin RASDA

La classe `GenerateurCpp` hérite de `Generateur` et produit des fichiers `.h` et `.cpp` à partir du modèle UML commun.

Caractéristiques :
- Génération des fichiers d'en-tête (`.h`) et d'implémentation (`.cpp`)
- Support de l'héritage, de l'agrégation, de l'association
- Gestion des types C++ et de la visibilité
- Formatage conforme aux conventions C++

### Extension Python — Enzo POIRIER

La classe `GenerateurPython` hérite de `Generateur` et produit des fichiers `.py`.

Caractéristiques :
- Génération de classes Python avec `__init__`, méthodes et propriétés
- Traduction des types UML en types Python
- Respect des conventions PEP 8

### Extension Java — Benoît DIJOUX

La classe `GenerateurJava` hérite de `Generateur` et produit des fichiers `.java` via une approche Factory.

Caractéristiques :
- Interface `GenerableJava` définissant un contrat standard
- Classes intermédiaires : `ClasseJava`, `AttributJava`, `MethodeJava`
- Génération automatique des getters/setters
- Gestion des imports et résolution des dépendances entre classes
- Typage fort via l'énumération `Visibilite`

---

## Prérequis

- Python 3.10+
- PlantUML (pour visualiser les diagrammes `.puml`)

---

## Utilisation

```bash
# Générer du code C++
python programme/umlfactory2java.py --langage cpp --input mon_diagramme.puml --output ./sortie_cpp/

# Générer du code Python
python programme/umlfactory2java.py --langage python --input mon_diagramme.puml --output ./sortie_python/

# Générer du code Java
python programme/umlfactory2java.py --langage java --input mon_diagramme.puml --output ./sortie_java/
```

---

## Lancer les tests

```bash
# Tests de l'extension C++
python -m pytest programme/test/test_complet.py

# Tests de l'extension Java
python -m pytest programme/test/test_java.py
```

---

## Diagrammes UML

Les diagrammes de classes du projet sont disponibles dans `doc/fichier_puml/` :

- `diagramme_commun.puml` — architecture partagée
- `diagramme_generateur_cpp.puml` — extension C++
- `diagramme_generateur_python.puml` — extension Python
- `diagramme_generateur_java.puml` — extension Java

---

## Dépôt

[git.inge.re — tp_architecture_composants_partages](https://git.inge.re/enzo.poirier/tp_architecture_composants_partages)
