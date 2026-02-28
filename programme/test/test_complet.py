#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          test_complet.py — Suite de tests intégrée UMLFactory2Code          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Teste les trois générateurs (Java · C++ · Python) à partir du diagramme    ║
║  exemple_complet.puml et sauvegarde les fichiers produits dans output/.      ║
║                                                                              ║
║  Utilisation :                                                               ║
║    python test_complet.py          ← exécution directe (rapport complet)    ║
║    pytest  test_complet.py -v      ← exécution via pytest                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Diagramme testé — exemple_complet.puml :
  • 2 interfaces       : Payable, Serialisable
  • 1 classe abstraite : Personne
  • 4 classes concrètes: Client, Employe, Commande, Produit, Adresse
  • Relations          : héritage, implémentation d'interface, composition (1-1),
                         association dirigée (0..*), agrégation (1..*)
  • Notes PlantUML attachées à Client, Commande, Personne
"""

import os
import sys

# ── Chemin racine du projet ───────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_DIR, ".."))

from src.commun import ParseurPuml
from src.specialisation_java.generateur_java import GenerateurJava
from src.specialisation_cpp import GenerateurCpp
from src.specialisation_python import GenerateurPython

# ── Chemins des ressources et des sorties ─────────────────────────────────────
PUML_PATH     = os.path.join(_DIR, "exemple_complet.puml")
OUTPUT_ROOT   = os.path.join(_DIR, "output")
OUTPUT_JAVA   = os.path.join(OUTPUT_ROOT, "java")
OUTPUT_CPP    = os.path.join(OUTPUT_ROOT, "cpp")
OUTPUT_PYTHON = os.path.join(OUTPUT_ROOT, "python")


# ══════════════════════════════════════════════════════════════════════════════
#  Collecteur de résultats
# ══════════════════════════════════════════════════════════════════════════════

class _Rapport:
    """
    Collecte les résultats de chaque vérification et produit un résumé lisible.
    Compatible avec pytest : la méthode asserter() lève une AssertionError
    si au moins une vérification a échoué.
    """

    def __init__(self, nom: str):
        self.nom = nom
        self._ok:   list = []
        self._fail: list = []

    # ── API publique ──────────────────────────────────────────────────────────

    def verifier(self, condition: bool, message: str) -> None:
        """Enregistre une vérification (ne lève pas d'exception immédiatement)."""
        if condition:
            self._ok.append(message)
        else:
            self._fail.append(message)

    def afficher(self) -> None:
        """Imprime le résultat de toutes les vérifications."""
        total = len(self._ok) + len(self._fail)
        print(f"\n{'═'*62}")
        print(f"  RÉSULTATS — {self.nom}")
        print(f"{'─'*62}")
        for m in self._ok:
            print(f"  ✓  {m}")
        for m in self._fail:
            print(f"  ✗  {m}")
        print(f"{'─'*62}")
        print(f"  → {len(self._ok)} / {total} assertions réussies"
              + ("  ✔ SUCCÈS" if not self._fail else "  ✘ ÉCHEC"))
        print(f"{'═'*62}")

    def asserter(self) -> None:
        """Lève AssertionError si des vérifications ont échoué (hook pytest)."""
        if self._fail:
            details = "\n    ".join(self._fail)
            raise AssertionError(
                f"{len(self._fail)} assertion(s) échouée(s) [{self.nom}] :\n"
                f"    {details}"
            )


# ══════════════════════════════════════════════════════════════════════════════
#  Fonctions utilitaires
# ══════════════════════════════════════════════════════════════════════════════

def _charger_diagramme():
    """Parse le fichier PUML et retourne le DiagrammeClasse."""
    return ParseurPuml(PUML_PATH).parser()


def _afficher_modele(diagramme) -> None:
    """Affiche le modèle UML parsé (utile en mode debug)."""
    print(f"\n{'─'*62}")
    print(f"  MODÈLE UML — {diagramme.nom}")
    print(f"{'─'*62}")
    for cls in diagramme.get_liste_classes():
        flags = []
        if cls.est_abstraite:
            flags.append("abstraite")
        if cls.est_interface:
            flags.append("interface")
        label = f"[{', '.join(flags)}]" if flags else ""
        print(f"  Classe : {cls.nom} {label}")
        if cls.notes:
            print(f"    Notes     : {cls.notes}")
        if cls.get_attributs():
            print(f"    Attributs : {[(a.nom, a.type) for a in cls.get_attributs()]}")
        if cls.get_operations():
            print(f"    Opérations: {[(o.nom, o.type_retour) for o in cls.get_operations()]}")
        for type_rel, rel in cls.get_relations():
            print(f"    Relation  : {type_rel} | {rel.id_relation}"
                  f" | src_card={rel.cardinalite_source}"
                  f" | dst_card={rel.cardinalite_cible}")


def _sauvegarder_java(fichiers: list, dossier: str) -> None:
    """Écrit les fichiers Java (liste de dicts) dans le dossier cible."""
    os.makedirs(dossier, exist_ok=True)
    for f in fichiers:
        chemin = os.path.join(dossier, f["nom_fichier"])
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(f["contenu"])
        print(f"    ↗  {f['nom_fichier']}")


def _sauvegarder_objets(fichiers: list, dossier: str) -> None:
    """Écrit les fichiers C++/Python (objets avec .sauvegarder()) dans le dossier cible."""
    os.makedirs(dossier, exist_ok=True)
    for f in fichiers:
        f.chemin_complet = dossier
        f.sauvegarder()
        print(f"    ↗  {f.nom_fichier}")


# ══════════════════════════════════════════════════════════════════════════════
#  TEST JAVA
# ══════════════════════════════════════════════════════════════════════════════

def test_java() -> None:
    """
    Vérifie la génération Java :
      - Présence de tous les fichiers .java
      - Déclaration de package
      - Mot-clé abstract / interface
      - Héritage (extends) et implémentation (implements)
      - Cardinalité multiple → List<T> et import java.util.List
      - Getters / Setters auto-générés
    """
    r = _Rapport("JAVA")

    print("\n  Génération Java en cours…")
    diagramme = _charger_diagramme()
    generateur = GenerateurJava()
    fichiers   = generateur.generer_classe2_langage(diagramme)
    _sauvegarder_java(fichiers, OUTPUT_JAVA)

    # Index nom → contenu
    idx = {f["nom_fichier"]: f["contenu"] for f in fichiers}

    # ── 1. Fichiers attendus ──────────────────────────────────────────────────
    r.verifier(len(fichiers) > 0,
               "Au moins un fichier .java est généré")
    for cls in ("Personne.java", "Client.java", "Payable.java",
                "Serialisable.java", "Commande.java",
                "Employe.java", "Produit.java", "Adresse.java"):
        r.verifier(cls in idx, f"Fichier {cls} présent dans la sortie")

    # ── 2. Déclaration de package dans chaque fichier ─────────────────────────
    for nom, code in idx.items():
        r.verifier(
            "package com.projet.generated" in code,
            f"{nom} → déclaration 'package com.projet.generated'"
        )

    # ── 3. Classe abstraite ───────────────────────────────────────────────────
    r.verifier(
        "abstract class Personne" in idx.get("Personne.java", ""),
        "Personne.java → mot-clé 'abstract class Personne'"
    )

    # ── 4. Interfaces ─────────────────────────────────────────────────────────
    r.verifier(
        "interface Payable" in idx.get("Payable.java", ""),
        "Payable.java → mot-clé 'interface Payable'"
    )
    r.verifier(
        "interface Serialisable" in idx.get("Serialisable.java", ""),
        "Serialisable.java → mot-clé 'interface Serialisable'"
    )

    # ── 5. Héritage (extends) ─────────────────────────────────────────────────
    r.verifier(
        "extends Personne" in idx.get("Client.java", ""),
        "Client.java → 'extends Personne' (héritage)"
    )
    r.verifier(
        "extends Personne" in idx.get("Employe.java", ""),
        "Employe.java → 'extends Personne' (héritage)"
    )

    # ── 6. Implémentation d'interface (implements) ────────────────────────────
    client_code = idx.get("Client.java", "")
    r.verifier(
        "implements" in client_code and "Payable" in client_code,
        "Client.java → 'implements Payable'"
    )
    r.verifier(
        "Serialisable" in client_code,
        "Client.java → mentionne 'Serialisable' (implémentation multiple)"
    )

    # ── 7. Cardinalité multiple → java.util.List ──────────────────────────────
    r.verifier(
        "import java.util.List" in client_code,
        "Client.java → 'import java.util.List' (relation 0..* vers Commande)"
    )
    r.verifier(
        "List<Commande>" in client_code,
        "Client.java → attribut 'List<Commande>' (cardinalité 0..*)"
    )

    # ── 8. Getters auto-générés ───────────────────────────────────────────────
    personne_code = idx.get("Personne.java", "")
    r.verifier(
        "getNom()" in personne_code,
        "Personne.java → getter 'getNom()' auto-généré pour l'attribut nom"
    )
    r.verifier(
        "getAge()" in personne_code,
        "Personne.java → getter 'getAge()' auto-généré pour l'attribut age"
    )
    r.verifier(
        "getEmail()" in client_code,
        "Client.java → getter 'getEmail()' auto-généré pour l'attribut email"
    )

    # ── 9. Setters auto-générés ───────────────────────────────────────────────
    r.verifier(
        "setNom(" in personne_code,
        "Personne.java → setter 'setNom()' auto-généré pour l'attribut nom"
    )
    r.verifier(
        "setEmail(" in client_code,
        "Client.java → setter 'setEmail()' auto-généré pour l'attribut email"
    )
    r.verifier(
        "setFidelite(" in client_code,
        "Client.java → setter 'setFidelite()' auto-généré pour l'attribut fidelite"
    )

    r.afficher()
    r.asserter()


# ══════════════════════════════════════════════════════════════════════════════
#  TEST C++
# ══════════════════════════════════════════════════════════════════════════════

def test_cpp() -> None:
    """
    Vérifie la génération C++ :
      - Séparation en fichiers .h (header) et .cpp (source)
      - Include guards (#ifndef / #define / #endif)
      - Héritage C++ (public NomParent)
      - std::vector pour les cardinalités multiples
      - Implémentation des méthodes (opérateur ::) dans les sources
    """
    r = _Rapport("C++")

    print("\n  Génération C++ en cours…")
    diagramme = _charger_diagramme()
    generateur = GenerateurCpp()
    fichiers   = generateur.generer_classe2_langage(diagramme)
    _sauvegarder_objets(fichiers, OUTPUT_CPP)

    # Index nom → contenu généré
    idx = {f.nom_fichier: f.generer_code() for f in fichiers}

    headers = [n for n in idx if n.endswith(".h")]
    sources = [n for n in idx if n.endswith(".cpp")]

    # ── 1. Séparation header / source ─────────────────────────────────────────
    r.verifier(len(headers) > 0,
               "Des fichiers .h (headers) sont générés")
    r.verifier(len(sources) > 0,
               "Des fichiers .cpp (sources) sont générés")
    r.verifier(len(headers) == len(sources),
               f"Autant de .h ({len(headers)}) que de .cpp ({len(sources)})")

    # ── 2. Paires header / source pour chaque classe attendue ─────────────────
    for base in ("Client", "Personne", "Employe",
                 "Commande", "Produit", "Adresse",
                 "Payable", "Serialisable"):
        r.verifier(f"{base}.h"   in idx, f"Header  {base}.h   présent")
        r.verifier(f"{base}.cpp" in idx, f"Source  {base}.cpp présent")

    # ── 3. Include guards dans chaque header ──────────────────────────────────
    for nom in headers:
        code = idx[nom]
        guard = nom.replace(".", "_").upper()   # ex : CLIENT_H
        r.verifier("#ifndef " + guard in code,
                   f"{nom} → #ifndef {guard} (include guard)")
        r.verifier("#define " + guard in code,
                   f"{nom} → #define {guard}")
        r.verifier("#endif" in code,
                   f"{nom} → #endif (fermeture du guard)")

    # ── 4. Héritage C++ (public NomParent dans la signature de classe) ─────────
    r.verifier(
        "public Personne" in idx.get("Client.h", ""),
        "Client.h → 'public Personne' (héritage C++)"
    )
    r.verifier(
        "public Personne" in idx.get("Employe.h", ""),
        "Employe.h → 'public Personne' (héritage C++)"
    )

    # ── 5. Implémentation d'interface (public Payable dans Client.h) ───────────
    r.verifier(
        "public Payable" in idx.get("Client.h", ""),
        "Client.h → 'public Payable' (implémentation d'interface)"
    )

    # ── 6. std::vector pour cardinalités multiples ────────────────────────────
    client_h   = idx.get("Client.h",   "")
    commande_h = idx.get("Commande.h", "")

    r.verifier(
        "std::vector" in client_h,
        "Client.h → 'std::vector' (association 0..* vers Commande)"
    )
    r.verifier(
        "#include <vector>" in client_h,
        "Client.h → '#include <vector>' (auto-inclus pour std::vector)"
    )
    r.verifier(
        "std::vector<Commande*>" in client_h,
        "Client.h → 'std::vector<Commande*>' (type exact du vecteur)"
    )
    r.verifier(
        "std::vector" in commande_h,
        "Commande.h → 'std::vector' (agrégation 1..* vers Produit)"
    )
    r.verifier(
        "std::vector<Produit*>" in commande_h,
        "Commande.h → 'std::vector<Produit*>' (type exact du vecteur)"
    )

    # ── 7. #include du header dans chaque source ──────────────────────────────
    for nom in sources:
        base_h = nom.replace(".cpp", ".h")
        r.verifier(
            f'#include "{base_h}"' in idx[nom],
            f"{nom} → #include de son header '{base_h}'"
        )

    # ── 8. Implémentation de méthodes (opérateur ::) dans les sources ─────────
    for nom in ("Client.cpp", "Commande.cpp", "Personne.cpp", "Employe.cpp",
                "Produit.cpp", "Payable.cpp", "Serialisable.cpp"):
        if nom in idx:
            r.verifier(
                "::" in idx[nom],
                f"{nom} → '::' présent (implémentation des méthodes)"
            )

    r.afficher()
    r.asserter()


# ══════════════════════════════════════════════════════════════════════════════
#  TEST PYTHON
# ══════════════════════════════════════════════════════════════════════════════

def test_python() -> None:
    """
    Vérifie la génération Python :
      - Extension .py de tous les fichiers
      - Import de ABC / abstractmethod pour interfaces et classes abstraites
      - Signature de classe avec héritage et bases ABC
      - Implémentation d'interface dans les bases (class Client(Personne, Payable, …))
      - Méthode __init__ avec super() pour les sous-classes
      - Décorateur @abstractmethod dans les interfaces / classes abstraites
      - Initialisation des attributs (self.x = None) dans __init__
    """
    r = _Rapport("PYTHON")

    print("\n  Génération Python en cours…")
    diagramme = _charger_diagramme()
    generateur = GenerateurPython()
    fichiers   = generateur.generer_classe2_langage(diagramme)
    _sauvegarder_objets(fichiers, OUTPUT_PYTHON)

    # Index nom → contenu généré
    idx = {f.nom_fichier: f.generer_code() for f in fichiers}

    # ── 1. Extension .py pour tous les fichiers ────────────────────────────────
    r.verifier(
        all(n.endswith(".py") for n in idx),
        "Tous les fichiers produits ont l'extension .py"
    )
    for cls in ("Personne.py", "Client.py", "Payable.py", "Serialisable.py",
                "Commande.py", "Employe.py", "Produit.py", "Adresse.py"):
        r.verifier(cls in idx, f"Fichier {cls} présent dans la sortie")

    # ── 2. Import ABC pour les classes abstraites et interfaces ───────────────
    r.verifier(
        "from abc import ABC, abstractmethod" in idx.get("Payable.py", ""),
        "Payable.py → 'from abc import ABC, abstractmethod' (interface)"
    )
    r.verifier(
        "from abc import ABC, abstractmethod" in idx.get("Personne.py", ""),
        "Personne.py → 'from abc import ABC, abstractmethod' (classe abstraite)"
    )
    r.verifier(
        "from abc import ABC, abstractmethod" in idx.get("Serialisable.py", ""),
        "Serialisable.py → 'from abc import ABC, abstractmethod' (interface)"
    )

    # ── 3. Signature de classe avec base ABC ──────────────────────────────────
    r.verifier(
        "class Payable(ABC):" in idx.get("Payable.py", ""),
        "Payable.py → 'class Payable(ABC):' (interface hérite de ABC)"
    )
    r.verifier(
        "class Personne(ABC):" in idx.get("Personne.py", ""),
        "Personne.py → 'class Personne(ABC):' (classe abstraite hérite de ABC)"
    )
    r.verifier(
        "class Serialisable(ABC):" in idx.get("Serialisable.py", ""),
        "Serialisable.py → 'class Serialisable(ABC):'"
    )

    # ── 4. Héritage Python (Personne <|-- Client / Employe) ───────────────────
    client_code  = idx.get("Client.py",  "")
    employe_code = idx.get("Employe.py", "")

    r.verifier(
        "class Client(" in client_code and "Personne" in client_code,
        "Client.py → hérite de Personne (héritage Python)"
    )
    r.verifier(
        "class Employe(" in employe_code and "Personne" in employe_code,
        "Employe.py → hérite de Personne (héritage Python)"
    )

    # ── 5. Implémentation d'interfaces dans les bases de Client ───────────────
    r.verifier(
        "Payable" in client_code,
        "Client.py → mentionne 'Payable' dans ses bases (implémentation)"
    )
    r.verifier(
        "Serialisable" in client_code,
        "Client.py → mentionne 'Serialisable' dans ses bases"
    )

    # ── 6. Méthode __init__ avec super() pour les sous-classes ───────────────
    r.verifier(
        "def __init__(self):" in client_code,
        "Client.py → présence de 'def __init__(self):'"
    )
    r.verifier(
        "super().__init__()" in client_code,
        "Client.py → appel de 'super().__init__()' (chaîne d'héritage)"
    )
    r.verifier(
        "def __init__(self):" in employe_code,
        "Employe.py → présence de 'def __init__(self):'"
    )
    r.verifier(
        "super().__init__()" in employe_code,
        "Employe.py → appel de 'super().__init__()'"
    )

    # ── 7. Décorateur @abstractmethod ────────────────────────────────────────
    r.verifier(
        "@abstractmethod" in idx.get("Payable.py", ""),
        "Payable.py → '@abstractmethod' (méthode d'interface)"
    )
    r.verifier(
        "@abstractmethod" in idx.get("Personne.py", ""),
        "Personne.py → '@abstractmethod' (méthode de classe abstraite)"
    )
    r.verifier(
        "@abstractmethod" in idx.get("Serialisable.py", ""),
        "Serialisable.py → '@abstractmethod'"
    )

    # ── 8. Initialisation des attributs dans __init__ ─────────────────────────
    personne_code = idx.get("Personne.py", "")
    r.verifier(
        "self.nom = None" in personne_code,
        "Personne.py → 'self.nom = None' dans __init__"
    )
    r.verifier(
        "self.age = None" in personne_code,
        "Personne.py → 'self.age = None' dans __init__"
    )
    r.verifier(
        "self.email = None" in client_code,
        "Client.py → 'self.email = None' dans __init__"
    )
    r.verifier(
        "self.fidelite = None" in client_code,
        "Client.py → 'self.fidelite = None' dans __init__"
    )
    r.verifier(
        "self.matricule = None" in employe_code,
        "Employe.py → 'self.matricule = None' dans __init__"
    )

    r.afficher()
    r.asserter()




# ══════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Lance les trois suites de tests et affiche un rapport de synthèse."""

    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║        UMLFactory2Code — Test Complet (3 générateurs)           ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"\n  Diagramme source : {PUML_PATH}")
    print(f"  Dossier de sortie : {OUTPUT_ROOT}/")

    # ── Afficher le modèle parsé ──────────────────────────────────────────────
    try:
        diagramme_debug = _charger_diagramme()
        _afficher_modele(diagramme_debug)
    except Exception as exc:
        print(f"\n  [ERREUR PARSEUR] Impossible de charger {PUML_PATH} : {exc}")
        sys.exit(1)

    # ── Exécuter chaque suite de tests ────────────────────────────────────────
    suites   = [("Java",   test_java),
                ("C++",    test_cpp),
                ("Python", test_python)]
    resultats = []

    for nom, fn in suites:
        print(f"\n{'━'*62}")
        print(f"  Lancement des tests {nom}…")
        print(f"{'━'*62}")
        try:
            fn()
            resultats.append((nom, True, ""))
        except AssertionError as err:
            resultats.append((nom, False, str(err)))
        except Exception as err:
            resultats.append((nom, False, f"ERREUR INATTENDUE : {err}"))

    # ── Synthèse finale ───────────────────────────────────────────────────────
    print("\n\n╔══════════════════════════════════════════════════════════════════╗")
    print("║                       SYNTHÈSE FINALE                           ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    tout_ok = True
    for nom, ok, err in resultats:
        statut = "✔  SUCCÈS" if ok else "✘  ÉCHEC "
        print(f"║  [{statut}]  Générateur {nom:<10}                              ║")
        if not ok:
            tout_ok = False
            # Afficher le premier message d'erreur (tronqué)
            ligne_err = err.splitlines()[0][:56] if err else ""
            print(f"║             {ligne_err:<54} ║")

    print(f"╠══════════════════════════════════════════════════════════════════╣")
    bilan = "TOUS LES TESTS SONT PASSÉS ✔" if tout_ok else "DES TESTS ONT ÉCHOUÉ ✘"
    print(f"║  {bilan:<64}║")
    print(f"╠══════════════════════════════════════════════════════════════════╣")
    print(f"║  Fichiers sauvegardés dans :                                    ║")
    print(f"║    • {OUTPUT_JAVA:<59}║")
    print(f"║    • {OUTPUT_CPP:<59}║")
    print(f"║    • {OUTPUT_PYTHON:<59}║")
    print(f"╚══════════════════════════════════════════════════════════════════╝")

    # Code de retour non-zéro si des tests ont échoué (utile en CI)
    if not tout_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
