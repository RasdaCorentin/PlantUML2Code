Voici une fusion des deux documents. J'ai conservé le contexte universitaire et technique de votre version, tout en y intégrant les explications architecturales détaillées et la mise en page de ma proposition précédente. C'est le `README.md` parfait et complet pour la racine de votre projet.

---

# UMLFactory2Code — Générateur de Code Multi-Langages

**CCO — TP Projet noté : Architecture avec composants partagés**

**Année universitaire :** 2025–2026

**Professeur :** Rémy COURDIER

**Établissement :** Université de La Réunion — ESIROI (Informatique)

---

## 📝 Description

Ce projet implémente un générateur de code orienté objet à partir de diagrammes UML modélisés en PlantUML (`.puml`).
L'outil lit un fichier PlantUML, construit un modèle UML abstrait en mémoire, puis génère automatiquement le code source dans le langage cible choisi.

L'architecture respecte les principes de la conception orientée objet (polymorphisme, encapsulation, pattern Factory/Strategy) et repose sur **une partie commune partagée** entre tous les étudiants et **trois extensions spécialisées**, chacune développée individuellement.

---

## 👥 Étudiants et contributions

| Étudiant | Extension | Classe de référence | Branche |
| --- | --- | --- | --- |
| **Corentin RASDA** | C++ | `GenerateurCpp` | `feature/Corentin` |
| **Enzo POIRIER** | Python | `GenerateurPython` | `feature/Enzo` |
| **Benoît DIJOUX** | Java | `GenerateurJava` | `feature/Benoit` |

---

## 🏗️ Architecture du projet

Notre application se divise en deux couches strictes.

### 1. Le Cœur Commun (Analyse & Métamodèle)

Cette partie, conçue en groupe, est indépendante du langage de sortie. Elle comprend :

* **Le Parseur (`ParseurPuml`)** : Analyse les fichiers `.puml` via des expressions régulières pour en extraire la structure.
* **Le Métamodèle UML** : Représentation abstraite en mémoire (`UmlClasse`, `Attribut`, `Operation`, `Relation`, `Notes`, `Visibilite`).
* **`DiagrammeClasse`** : Conteneur représentant l'ensemble du diagramme.
* **Le Contrat (`Generateur`)** : Classe abstraite définissant la méthode `generer_classe2_langage(diagramme_classe)` que chaque extension implémente.

### 2. Les Extensions Spécialisées (Génération)

Chaque extension hérite du `Generateur` commun pour adapter le modèle aux paradigmes de son langage :

* **Extension C++ (Corentin RASDA)** : Produit systématiquement une paire de fichiers (`.h` et `.cpp`). Gère nativement l'héritage, les pointeurs, les vecteurs (`std::vector`), et inclut la délégation dans sa génération.
* **Extension Python (Enzo POIRIER)** : Génère des classes avec constructeurs `__init__`, gère l'héritage multiple, respecte la PEP 8 et exploite le module `abc` pour matérialiser les interfaces et classes abstraites.
* **Extension Java (Benoît DIJOUX)** : Utilise une approche par Factory avec des classes intermédiaires (`ClasseJava`, etc.). Traduit les relations en attributs typés (`List<>` si cardinalité multiple), résout les imports, et génère automatiquement les Getters/Setters.

### Arborescence des fichiers

```text
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
│   │   └── ... (classes_cpp, attribut_cpp, fichiers_cpp, etc.)
│   ├── specialisation_python/   # Extension Python (Enzo POIRIER)
│   │   └── generateur_python.py
│   └── specialisation_java/     # Extension Java (Benoît DIJOUX)
│       ├── generateur_java.py
│       └── ... (classes_java, attribut_java, etc.)
├── test/                        # Fichiers de test
│   ├── exemple_complet.puml
│   ├── test_complet.py          # Suite de tests intégrée (3 langages)
│   └── test_java.py
│   └── test_python.py
│   └── test_cpp.py
doc/
├── fichier_puml/                # Diagrammes UML du projet
│   ├── diagramme_commun.puml
│   ├── diagramme_generateur_cpp.puml
│   ├── diagramme_generateur_python.puml
│   └── diagramme_generateur_java.puml
└── images/                      # Exports PNG des diagrammes

```

---

## ⚙️ Prérequis

* Python 3.10+
* PlantUML (pour visualiser ou modifier les diagrammes `.puml`)
* *Optionnel* : `pytest` pour l'exécution avancée des tests.

---

## 🚀 Utilisation (CLI)

Générez le code source depuis un terminal en spécifiant le langage cible, le fichier d'entrée et le dossier de sortie :

```bash
# Générer du code C++
python programme/umlfactory2java.py --langage cpp --input mon_diagramme.puml --output ./sortie_cpp/

# Générer du code Python
python programme/umlfactory2java.py --langage python --input mon_diagramme.puml --output ./sortie_python/

# Générer du code Java
python programme/umlfactory2java.py --langage java --input mon_diagramme.puml --output ./sortie_java/

```

---

## 🧪 Lancer les tests

Une suite de tests robuste (`test_complet.py`) valide la génération simultanée des trois langages à partir d'un diagramme complexe (`exemple_complet.puml`).

**Lancer le test complet (Script standard) :**

```bash
python programme/test/test_complet.py

```

**Exécution avec Pytest :**

```bash
# Tester toutes les extensions
python -m pytest programme/test/test_complet.py -v

# Tester spécifiquement l'extension Java
python -m pytest programme/test/test_java.py

```

Les fichiers générés par les tests sont sauvegardés dans `programme/test/output/{langage}/`.

---

## 📊 Diagrammes UML

Les diagrammes de classes documentant notre propre architecture sont disponibles dans le dossier `doc/fichier_puml/` :

* `diagramme_commun.puml` — Architecture partagée et modèle abstrait.
* `diagramme_generateur_cpp.puml` — Extension C++.
* `diagramme_generateur_python.puml` — Extension Python.
* `diagramme_generateur_java.puml` — Extension Java.

---

## 🔗 Dépôt Git

[git.inge.re — tp_architecture_composants_partages](https://git.inge.re/enzo.poirier/tp_architecture_composants_partages)
