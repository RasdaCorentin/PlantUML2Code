"""
ParseurPuml - Lecture d'un fichier PlantUML vers le modele UML commun.
Meme logique et memes outils que umlfactory2java.py de l'enseignant :
    re, os, collections.defaultdict
"""
import re
import os
from collections import defaultdict

from .visibilite import Visibilite
from .attribut import Attribut
from .operation import Operation
from .relation import Relation, Composition, Agregation, Heritage
from .uml_classe import UMLClasse
from .diagramme_classe import DiagrammeClasse

# ===== Mapping visibilite UML =====
VISIBILITE_MAP = {
    '+': Visibilite.PUBLIC,
    '-': Visibilite.PRIVE,
    '#': Visibilite.PROTEGE,
    '~': Visibilite.PAQUETAGE,
}


class ParseurPuml:

    # ===== Regex (memes patterns que l'enseignant) =====
    class_pattern = re.compile(
        r'(?:(abstract)\s+)?'
        r'(class|interface)\s+'
        r'(?:"([^"]+)"\s+as\s+)?'
        r'(\w+)'
        r'(?:\s*\{([^}]*)\})?',
        re.MULTILINE
    )

    attribute_pattern = re.compile(
        r'([+\-#~])\s*(\w+)\s*:\s*(\{ID\}\s*)?(\w+)'
    )

    method_pattern = re.compile(
        r'([+\-#~])\s*(\w+)\s*\(([^)]*)\)(?:\s*:\s*(\w+))?'
    )

    inheritance_pattern = re.compile(r'(\w+)\s*<\|--\s*(\w+)')
    interface_impl_pattern = re.compile(r'(\w+)\s*\.\.\|>\s*(\w+)')

    relation_pattern = re.compile(
        r'(\w+)\s*'
        r'(?:"(?:(.*?)\\n)?([^"]*)")?\s*'
        r'(-->|--|o--|\*--)\s*'
        r'(?:"(?:(.*?)\\n)?([^"]*)")?\s*'
        r'(\w+)'
        r'(?:\s*:\s*"?([^"\n]*)"?\s*)?'
    )

    note_pattern = re.compile(
        r'note\s+(?:left|right|top|bottom)\s+of\s+(\w+)\s*(.*?)\s*end note',
        re.DOTALL | re.IGNORECASE
    )

    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier
        self.contenu = ""

    def parser(self) -> DiagrammeClasse:
        """Parse le fichier PUML et retourne un DiagrammeClasse."""
        nom = os.path.splitext(os.path.basename(self.chemin_fichier))[0]
        diagramme = DiagrammeClasse(nom)

        with open(self.chemin_fichier, "r") as f:
            self.contenu = f.read()

        classes_dict = {}

        # ===== Classes / Interfaces =====
        for abstract_flag, type_, alias, name, body in self.class_pattern.findall(self.contenu):
            est_interface = (type_ == "interface")
            est_abstraite = bool(abstract_flag)

            classe = UMLClasse(
                nom=name,
                est_abstraite=est_abstraite,
                est_interface=est_interface
            )

            if body:
                # Extraire methodes d'abord
                noms_methodes = set()
                for vis, method_name, params, ret in self.method_pattern.findall(body):
                    op = Operation(
                        nom=method_name,
                        type_retour=ret if ret else "void",
                        visibilite=VISIBILITE_MAP.get(vis, Visibilite.PUBLIC)
                    )
                    classe.operations.append(op)
                    noms_methodes.add(method_name)

                # Puis attributs
                for vis, attr_name, _id_tag, attr_type in self.attribute_pattern.findall(body):
                    if attr_name not in noms_methodes:
                        attr = Attribut(
                            nom=attr_name,
                            type_=attr_type,
                            visibilite=VISIBILITE_MAP.get(vis, Visibilite.PRIVE)
                        )
                        classe.attributs.append(attr)

            classes_dict[name] = classe
            diagramme.classes.append(classe)

        # ===== Notes attachees =====
        class_comments = defaultdict(list)
        for class_name, note_text in self.note_pattern.findall(self.contenu):
            lines = [l.strip() for l in note_text.strip().splitlines() if l.strip()]
            if lines and class_name in classes_dict:
                classes_dict[class_name].ajouter_notes(" ".join(lines))

        # ===== Heritage (<|--) =====
        for parent, child in self.inheritance_pattern.findall(self.contenu):
            if parent in classes_dict and child in classes_dict:
                rel = Heritage(
                    id_relation=child + "_extends_" + parent
                )
                rel.source = classes_dict[child]
                rel.cible = classes_dict[parent]
                classes_dict[child].relations.append(("heritage", rel))

        # ===== Implementation (..|>) =====
        for cls, iface in self.interface_impl_pattern.findall(self.contenu):
            if cls in classes_dict and iface in classes_dict:
                rel = Heritage(
                    id_relation=cls + "_implements_" + iface
                )
                rel.source = classes_dict[cls]
                rel.cible = classes_dict[iface]
                classes_dict[cls].relations.append(("implementation", rel))

        # ===== Relations (association, agregation, composition) =====
        for src, src_role, src_card, rel_type, dst_role, dst_card, dst, label in self.relation_pattern.findall(self.contenu):
            if src not in classes_dict or dst not in classes_dict:
                continue

            src_card = src_card if src_card else "1"
            dst_card = dst_card if dst_card else "1"
            label = label.strip() if label else ""

            if rel_type == "*--":
                rel = Composition(
                    id_relation=src + "_comp_" + dst,
                    cardinalite_source=src_card,
                    role_source=src_role,
                    cardinalite_cible=dst_card,
                    role_cible=dst_role
                )
            elif rel_type == "o--":
                rel = Agregation(
                    id_relation=src + "_agreg_" + dst,
                    cardinalite_source=src_card,
                    role_source=src_role,
                    cardinalite_cible=dst_card,
                    role_cible=dst_role
                )
            else:
                rel = Relation(
                    id_relation=src + "_assoc_" + dst,
                    cardinalite_source=src_card,
                    role_source=src_role,
                    cardinalite_cible=dst_card,
                    role_cible=dst_role
                )

            rel.source = classes_dict[src]
            rel.cible = classes_dict[dst]
            classes_dict[src].relations.append((rel_type, rel))

            # Lien inverse si bidirectionnel
            if rel_type in ["--", "o--", "*--"]:
                classes_dict[dst].relations.append((rel_type, rel))

        return diagramme
