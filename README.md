# CCO - TP PROJET noté - Architecture avec composants partagés

## Extension spécifique : Générateur Python 

**Année universitaire :** 2025–2026  
**Étudiant :** Enzo POIRIER     
**Professeur :** Rémy COURDIER  
**Établissement :** Université de La Réunion – ESIROI (Informatique)    

---

## 1. Langage considéré

Dans le cadre de la partie personnelle du projet, le langage choisi est :

**Python**

---

## 2. Étudiants avec composants partagés

La partie commune du projet, comprenant le métamodèle UML (`ClasseUML`, `Attribut`, `Operation`, `Relation`, `Notes`), la classe `DiagrammeClasse`, la classe `Executeur`, la classe abstraite `Generateur` ainsi que l’architecture générale en couches (Analyse et Génération), a été réalisée en collaboration avec :

- Benoît DIJOUX  
- Corentin RASDA  

---

## 3. Classe de référence – Contribution personnelle

La classe de référence correspondant à mon implication complète dans le projet est :

**`GenerateurPython`**

Cette classe :

- Hérite de la classe abstraite `Generateur`
- Redéfinit la méthode `genererCode(DiagrammeClasse)`
- Implémente la génération de code Python à partir du modèle UML commun
- Produit des fichiers `.py` respectant la syntaxe du langage Python
