# CCO - TP PROJET noté - Architecture avec composants partagés

## Extension spécifique : Générateur Java

**Année universitaire :** 2025–2026

**Étudiant :** Benoît DIJOUX

**Professeur :** Rémy COURDIER

**Établissement :** Université de La Réunion – ESIROI (Informatique)

---

## 1. Langage considéré

Dans le cadre de la partie personnelle du projet, le langage choisi pour l'extension est :

**Java**

---

## 2. Étudiants avec composants partagés

La partie commune du projet, comprenant le métamodèle UML (Classes, Attributs, Opérations, Relations), ainsi que l’architecture générale en couches (Analyse et Génération via la classe abstraite `Generateur`), a été réalisée en collaboration avec :

* Enzo POIRIER
* Corentin RASDA

---

## 3. Classe de référence – Contribution personnelle

La classe principale correspondant à mon implication spécifique dans le projet est :

**`GenerateurJava`**

Cette classe orchestre la transformation du modèle UML vers le code Java. Elle :

* Hérite de la classe abstraite commune `Generateur`.
* Implémente la méthode `genererClasse2Langage(DiagrammeClasse)` pour produire une liste de fichiers `.java`.
* Utilise une **approche objet** pour la génération (Factory) plutôt qu'une simple concaténation de chaînes.

### Architecture interne de l'extension

Pour garantir un code robuste et maintenable, l'extension Java s'appuie sur plusieurs composants spécifiques :

1. **Interface `GenerableJava**` : Définit un contrat standard pour tous les éléments capables de produire du code Java (`genererCode()`).
2. **Classes Métiers (`ClasseJava`, `AttributJava`, `MethodeJava`)** :
* Ces classes servent de structure intermédiaire (tampon) entre le modèle UML et le fichier texte final.
* Elles gèrent leur propre formatage (ex: `AttributJava` génère automatiquement ses Getters et Setters).


3. **Énumération `Visibilite**` : Assure un **typage fort** des modificateurs d'accès (`public`, `private`, `protected`) pour éviter les erreurs de syntaxe.
4. **Gestion des Imports** : Le générateur résout et optimise automatiquement les imports nécessaires.

Le générateur produit un code Java respectant les conventions standard (encapsulation, fichiers séparés, package par défaut).