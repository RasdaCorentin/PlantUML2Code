"""

umlfactory2Java - Générateur automatique de classes Java à partir de fichiers PlantUML
V0.1 - Remy Courdier - 2025

DESCRIPTION
-----------
Ce script lit un fichier PlantUML (.puml) et génère les classes Java correspondantes
en respectant les relations, héritages, interfaces et structures définies dans le diagramme UML.

Ce qui est pris en compte :
    • Classes, interfaces et classes abstraites.
    • Attributs et méthodes déclarés dans les classes PlantUML.
    • Héritage des classes (notation <|--).
    • Implémentation d'interfaces (notation ..|>).
    • Relations entre classes :
        - Association directionnelle (-->) avec cardinalité.
        - Association bidirectionnelle (--).
        - Agrégation (o--).
        - Composition (*--).
    • Cardinalités des relations : 1, 1..1, 0..1, 0..*, *..*, etc.
        - Les relations à cardinalité simple créent un attribut simple.
        - Les relations multiples créent une liste (List<T>) dans Java.
    • Commentaires de classe :
        - Inline après le nom de la classe : class Customer "représente un client".
        - Notes PlantUML attachées à la classe.
    • Commentaires ajoutés aux attributs représentant des relations, précisant le type de relation.
    • Génération automatique des getters/setters pour tous les attributs (y compris ceux issus des relations).
    • Génération de méthodes vides pour les méthodes déclarées dans les interfaces ou les classes.
    • Nettoyage du dossier de sortie avant génération.

USAGE
-----
Exécuter le script depuis la ligne de commande :

    python umlfactory2Java.py [fichier_puml] [-o dossier_sortie]

Paramètres :
    fichier_puml : (optionnel) chemin vers le fichier PlantUML à traduire.
                   Par défaut : "model.puml".
    -o, --output_dir : (optionnel) dossier dans lequel seront générés les fichiers Java.
                       Par défaut : "java_classes".

Exemple :
    python umlfactory2Java.py mon_diagramme.puml
    python umlfactory2Java.py mon_diagramme.puml -o sortie_java

Notes :
    - Si le dossier de sortie existe, tous les fichiers qu'il contient seront supprimés
      avant génération pour éviter les conflits.
    - Le script gère les cardinalités et les types de relations pour produire
      un code Java cohérent avec la structure UML.
"""

import re
import os
import argparse
from collections import defaultdict

defaultFile = "model2.1.puml"
# ===== Arguments ligne de commande =====
parser = argparse.ArgumentParser(description="Générateur de classes Java à partir d'un fichier PlantUML")
parser.add_argument("input_file", nargs="?", default=defaultFile,
                    help="Fichier PlantUML à traiter (par défaut 'model.puml')")
parser.add_argument("-o", "--output_dir", default="java_classes",
                    help="Répertoire de sortie pour les fichiers Java (par défaut 'java_classes')")
args = parser.parse_args()

input_file = args.input_file
output_dir = args.output_dir

# ===== Nettoyer le dossier de sortie =====
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

# ===== Regex =====
class_pattern = re.compile(
    r'(?:(abstract)\s+)?'                    # capture explicite du mot 'abstract'
    r'(class|interface)\s+'                  
    r'(\w+)'                                 # nom de la classe
    r'(?:\s+implements\s+[\w\s,]+)?'        # implements optionnel (ignoré ici, géré par interface_impl_pattern)
    r'(?:\s*\{([^}]*)\})?',                  # corps optionnel entre accolades
    re.MULTILINE
)

attribute_pattern = re.compile(r'([+\-#~])\s*(\w+)\s*:\s*(\w+)(?:\s*(?!=\())') # attribut avec type obligatoire
method_pattern = re.compile(r'([+\-#~])\s*(\w+)\s*\(([^)]*)\)(?:\s*:\s*(\w+))?') # méthode avec parenthèses
inheritance_pattern = re.compile(r'(\w+)\s*<\|--\s*(\w+)')
interface_impl_pattern = re.compile(r'(\w+)\s*\.\.\|>\s*(\w+)')

# Relations avec cardinalités
relation_pattern = re.compile(
    r'(\w+)\s*'                                   # classe source
    r'(?:"(?:(.*?)\\n)?([^"]*)")?\s*'             # rôle source (opt) + cardinalité source
    r'(-->|--|o--|\*--)\s*'                       # type de relation
    r'(?:"(?:(.*?)\\n)?([^"]*)")?\s*'             # rôle cible (opt) + cardinalité cible
    r'(\w+)'                                      # classe cible
    r'(?:\s*:\s*"?([^"]*)"?\s*)?'                 # libellé
)

# ===== Commentaires de classes =====
inline_comment_pattern = re.compile(
    r'(?:abstract\s+)?(class|interface)\s+(\w+)\s*(?:"([^"]*)")?'
)
note_pattern = re.compile(
    r'note\s+(?:left|right|top|bottom)\s+of\s+(\w+)\s*(.*?)\s*end note',
    re.DOTALL | re.IGNORECASE
)
class_comments = defaultdict(list)

# ===== Lire fichier PUML =====
with open(input_file, "r") as f:
    content = f.read()

# Extraction commentaires inline
for type_, name, comment in inline_comment_pattern.findall(content):
    if comment:
        class_comments[name].append(comment.strip())

# Extraction notes attachées
for class_name, note_text in note_pattern.findall(content):
    lines = [line.strip() for line in note_text.strip().splitlines() if line.strip()]
    if lines:
        class_comments[class_name].append(" ".join(lines))

# ===== Classes / Interfaces =====
classes = {}
for abstract_flag, type_, name, body in class_pattern.findall(content):
    # body peut être None si pas d'accolades
    if type_ == "interface":
        classes[name] = ("interface", body if body else "")
    elif abstract_flag:
        classes[name] = ("abstract", body if body else "")
    else:
        classes[name] = ("class", body if body else "")

print(f"Found {len(classes)} classes/interfaces in the PUML file.")

# ===== Héritage =====
inheritance = {child: parent for parent, child in inheritance_pattern.findall(content)}
print(f"Found {len(inheritance)} inheritance relationships.")

# ===== Interfaces implémentées =====
interfaces_impl = defaultdict(list)
for cls, iface in interface_impl_pattern.findall(content):
    interfaces_impl[cls].append(iface)
print(f"Found {sum(len(v) for v in interfaces_impl.values())} interface implementations.")

# ===== Relations =====
relations_dict = defaultdict(list)
for src, src_role, src_card, rel_type, dst_role, dst_card, dst, label in relation_pattern.findall(content):
    # print(f"Relation found: {src} ({src_role} {src_card}) {rel_type} ({dst_role} {dst_card}) {dst} Label: '{label}'") 
    src_card = src_card if src_card else "1"
    dst_card = dst_card if dst_card else "1"
    label = label.strip() if label else ""
     
    relations_dict[src].append((dst, dst_card, rel_type, label, dst_role if dst_role else dst))
    # Lien inverse uniquement si bidirectionnel
    if rel_type in ["--", "o--", "*--"]:
        relations_dict[dst].append((src, src_card, rel_type, label, src_role if src_role else src))
print(f"Found {sum(len(v) for v in relations_dict.values())} relations.")

# ===== Génération Java =====
for class_name, (class_type, body) in classes.items():
    java_file = os.path.join(output_dir, f"{class_name}.java")
    with open(java_file, "w") as out:
        out.write("/* Auto-generated from PlantUML avec UMLFactory */\n")
        
        # Commentaires de classe
        if class_name in class_comments:
            for comment in class_comments[class_name]:
                out.write(f"// {comment}\n")
        out.write("\n")
        
        # Définir extends et implements
        extends_str = f" extends {inheritance[class_name]}" if class_name in inheritance else ""
        implements_str = ""
        if class_name in interfaces_impl:
            implements_str = f" implements {', '.join(interfaces_impl[class_name])}"
        
        # Signature de la classe / interface
        if class_type == "interface":
            out.write(f"public interface {class_name} "+"{\n")
        elif class_type == "abstract":
            out.write(f"public abstract class {class_name}{extends_str}{implements_str} "+"{\n")
        else:
            out.write(f"public class {class_name}{extends_str}{implements_str} "+"{\n")
        
        # Extraire séparément les attributs et méthodes du body
        attributes_list = []
        methods_list = []
        
        if body:
            # D'abord extraire les méthodes (pour éviter de les confondre avec attributs)
            for vis, method_name, params, return_type in method_pattern.findall(body):
                methods_list.append((vis, method_name, params, return_type if return_type else "void"))
            
            # Ensuite extraire les attributs
            for vis, attr_name, attr_type in attribute_pattern.findall(body):
                attributes_list.append((vis, attr_name, attr_type))
        
        # ===== ATTRIBUTS =====
        out.write("    // ===== ATTRIBUTS =====\n")
        for visibility, name, typ in attributes_list:
            vis = {'+':'public','-':'private','#':'protected','~':''}.get(visibility,'')
            out.write(f"    {vis} {typ} {name};\n")
        
        # Relations comme attributs
        if class_name in relations_dict:
            for target, card, rel_type, label, role in relations_dict[class_name]:
                
                comment = ""
                if rel_type == "-->":
                    comment = f"association directionnelle avec {target}" + (f" (rôle '{role}')" if role != target else "")
                elif rel_type == "--":
                    comment = f"association bidirectionnelle avec {target}" + (f" (rôle '{role}')" if role != target else "")
                elif rel_type == "o--":
                    comment = f"agrégation avec {target}" + (f" (rôle '{role}')" if role != target else "")
                elif rel_type == "*--":
                    comment = f"composition avec {target}" + (f" (rôle '{role}')" if role != target else "")
                else:
                    comment = f"relation avec {target}" + (f" (rôle '{role}')" if role != target else "")
                if label:
                    comment += f" ('{label}')"

                # Attribut simple ou liste
                attr_name = (role if role != target else target).lower()  
                if card in ["1","1..1","0..1"]:
                    out.write(f"    // {comment}\n")
                    out.write(f"    private {target} {attr_name};\n")
                else:
                    out.write(f"    // {comment} (liste)\n")
                    out.write(f"    private List<{target}> {attr_name}List = new ArrayList<>();\n")

        # ===== GETTERS & SETTERS =====
        out.write("\n    // ===== GETTERS & SETTERS =====\n")
        for visibility, name, typ in attributes_list:
            out.write(f"    public {typ} get{name.capitalize()}() {{ return {name}; }}\n")
            out.write(f"    public void set{name.capitalize()}({typ} {name}) {{ this.{name} = {name}; }}\n")
        
        # Relations getters/setters
        if class_name in relations_dict:
            for target, card, rel_type, label, role in relations_dict[class_name]:
                attr_name = target.lower()
                if card in ["1","1..1","0..1"]:
                    out.write(f"    public {target} get{target}() {{ return {attr_name}; }}\n")
                    out.write(f"    public void set{target}({target} obj) {{ {attr_name} = obj; }}\n")
                else:
                    out.write(f"    public List<{target}> get{target}List() {{ return {attr_name}List; }}\n")
                    out.write(f"    public void add{target}({target} obj) {{ {attr_name}List.add(obj); }}\n")

        # ===== AUTRES METHODES =====
        out.write("\n    // ===== AUTRES METHODES =====\n")
        for visibility, method_name, params, return_type in methods_list:
            vis = {'+':'public','-':'private','#':'protected','~':''}.get(visibility,'')
            if class_type == "abstract":
                out.write(f"    {vis} abstract {return_type} {method_name}({params});\n")
            elif class_type == "interface":
                out.write(f"    {return_type} {method_name}({params});\n")
            else:
                out.write(f"    {vis} {return_type} {method_name}({params}) {{\n        // TODO\n    }}\n")

        # Méthodes des interfaces
        if class_type.lower() != "interface" and class_name in interfaces_impl:
            for iface_name in interfaces_impl[class_name]:
                iface_body = classes.get(iface_name, ("interface",""))[1]
                if iface_body:
                    for _, method_name, params, return_type in method_pattern.findall(iface_body):
                        ret_type = return_type if return_type else "void"
                        out.write(f"    public {ret_type} {method_name}({params}) {{\n")
                        out.write(f"        // TODO: implement interface method from {iface_name}\n")
                        out.write(f"    }}\n")

        out.write("}\n")

print(f"{len(classes)} Java class files generated in '{output_dir}' directory.")