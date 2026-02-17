import re
import os
import argparse
from collections import defaultdict

# ===== Arguments ligne de commande =====
parser = argparse.ArgumentParser(description="Générateur de classes Python à partir d'un fichier PlantUML")
parser.add_argument("input_file", nargs="?", default="diagramme_generateur_python.puml",
                    help="Fichier PlantUML à traiter (par défaut 'diagramme_generateur_python.puml')")
parser.add_argument("-o", "--output_dir", default="python_classes",
                    help="Répertoire de sortie pour les fichiers Python (par défaut 'python_classes')")
args = parser.parse_args()

input_file = args.input_file
output_dir = args.output_dir

# ===== Nettoyer le dossier de sortie (minimal: ne supprimer que les .py) =====
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".py"):
            os.remove(file_path)

# ===== Regex (minimal: réutiliser IDENT partout) =====
IDENT = r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*'
TYPE = r'[^()\n{=]+'   # accepte List<T>, Map<K,V>, String[], etc.

class_pattern = re.compile(
    rf'(?:(abstract)\s+)?'                    # capture explicite du mot 'abstract'
    rf'(class|interface)\s+'
    rf'({IDENT})'                             # nom de la classe (plus robuste)
    rf'(?:\s+implements\s+[{IDENT}\s,]+)?'    # implements optionnel
    rf'(?:\s*\{{([^}}]*)\}})?',               # corps optionnel entre accolades
    re.MULTILINE
)

attribute_pattern = re.compile(
    rf'([+\-#~])\s*({IDENT})\s*:\s*({TYPE})'
)

method_pattern = re.compile(
    rf'([+\-#~])\s*({IDENT})\s*\(([^)]*)\)\s*(?::\s*({TYPE}))?'
)

inheritance_pattern = re.compile(rf'({IDENT})\s*<\|--\s*({IDENT})')
interface_impl_pattern = re.compile(rf'({IDENT})\s*\.\.\|>\s*({IDENT})')

# Relations avec cardinalités
relation_pattern = re.compile(
    rf'({IDENT})\s*(?:"([^"]*)")?\s*(-->|--|o--|\*--)\s*(?:"([^"]*)")?\s*({IDENT})(?:\s*:\s*"?([^"]*)"?\s*)?'
)

# ===== Commentaires de classes =====
inline_comment_pattern = re.compile(
    rf'(?:abstract\s+)?(class|interface)\s+({IDENT})\s*(?:"([^"]*)")?'
)
note_pattern = re.compile(
    rf'note\s+(?:left|right|top|bottom)\s+of\s+({IDENT})\s*(.*?)\s*end note',
    re.DOTALL | re.IGNORECASE
)
class_comments = defaultdict(list)

# ===== Lire fichier PUML =====
with open(input_file, "r", encoding="utf-8") as f:
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
for src, src_card, rel_type, dst_card, dst, label in relation_pattern.findall(content):
    # minimal: ne pas inventer si absent (tu décideras plus tard lors de la génération)
    src_card = src_card if src_card else None
    dst_card = dst_card if dst_card else None
    label = label.strip() if label else ""

    relations_dict[src].append((dst, dst_card, rel_type, label, "source"))
    # Lien inverse uniquement si bidirectionnel
    if rel_type in ["--", "o--", "*--"]:
        relations_dict[dst].append((src, src_card, rel_type, label, "target"))
