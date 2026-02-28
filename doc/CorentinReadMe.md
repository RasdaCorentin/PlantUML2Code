# CCO - TP PROJET noté - Architecture avec composants partagés 

## Extension spécifique : Générateur C++

**Année universitaire :** 2025–2026 
**Étudiant :** Corentin RASDA 
**Professeur :** Rémy COURDIER 
**Établissement :** Université de La Réunion – ESIROI (Informatique) 

---

## 1. Langage considéré

Dans le cadre de la partie personnelle de ce projet, le langage cible choisi pour l'extension de génération est :

**C++** 

---

## 2. Étudiants avec composants partagés

L'architecture centrale du projet repose sur un cœur commun chargé de l'analyse (parsing) et de la construction du métamodèle UML en mémoire. Cette partie commune a été conceptualisée et développée en collaboration avec :

* Enzo POIRIER (Extension Python) 
* Benoît DIJOUX (Extension Java) 

Les composants partagés incluent notamment le métamodèle (`UmlClasse`, `Attribut`, `Operation`, `Relation`), le conteneur `DiagrammeClasse`, le `ParseurPuml`, ainsi que la classe abstraite `Generateur` qui définit le contrat de base de notre architecture.

---

## 3. Classe de référence – Contribution personnelle

La classe principale illustrant mon implication exclusive dans ce projet est :

**`GenerateurCpp`** 

Cette classe est le chef d'orchestre de l'extension C++. Elle hérite de la classe commune `Generateur` et implémente le polymorphisme attendu en redéfinissant la méthode de génération pour l'adapter aux paradigmes du C++.

### Architecture interne et spécificités de l'extension C++

Pour répondre aux contraintes techniques du langage C++, mon extension met en œuvre les concepts objets suivants :

1. **Séparation Header / Source** : Contrairement aux autres langages, le générateur C++ produit systématiquement deux fichiers physiques (`.h` et `.cpp`) pour chaque classe UML parsée. Cela est géré par la classe intermédiaire `FichierCpp`.
2. **Interface `Formattage`** : Tous les éléments structurels C++ (`ClasseCpp`, `AttributCpp`, `OperationCpp`, `RelationCpp`, `FichierCpp`) implémentent cette interface pour standardiser la production du code textuel.
3. **Principe de Délégation** : La génération s'appuie fortement sur la délégation. Par exemple, la méthode `genererCode()` de `FichierCpp` délègue la construction du corps du code à `ClasseCpp`, qui elle-même délègue à ses attributs et méthodes.
4. **Gestion fine des relations et spécificités C++** : Le générateur gère nativement la traduction de l'héritage, des agrégations et associations. Il résout automatiquement les inclusions croisées (includes) et intègre les modificateurs propres au C++ (`const`, `virtual`, méthodes virtuelles pures `= 0`, et pointeurs/vecteurs pour les cardinalités multiples).
