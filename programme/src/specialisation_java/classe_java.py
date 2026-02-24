from typing import List, Set
from .generable_java import GenerableJava
from .visibilite import Visibilite
from .attribut_java import AttributJava
from .methode_java import MethodeJava

class ClasseJava(GenerableJava):
    """
    Structure Intermédiaire (Le coeur du produit Factory) :
    Cette classe agit comme un buffer. Elle accumule les attributs, méthodes, 
    et relations (imports, héritage) avant de tout cracher sous forme de texte final.
    """
    def __init__(self, nom: str, generateur_parent):
        self.nom = nom
        # On récupère le package par défaut défini dans le générateur parent
        self.package = generateur_parent._package_par_defaut if generateur_parent else ""
        
        # J'utilise un Set pour les imports pour éviter les doublons automatiquement
        self.imports: Set[str] = set()
        self.est_abstraite = False
        self.visibilite = Visibilite.PUBLIC
        self.nom_mere = ""
        self.interfaces: List[str] = []
        
        # ASSOCIATION BIDIRECTIONNELLE :
        # La classe connait le générateur qui l'a créée. Cela permet, par exemple, 
        # de lui redemander des infos globales si besoin plus tard.
        self.generateur_parent = generateur_parent
        
        # COMPOSITIONS : La classe possède strictement ses attributs et méthodes
        self.attributs: List[AttributJava] = []
        self.methodes: List[MethodeJava] = []

    def ajouter_import(self, import_str: str):
        self.imports.add(import_str)

    def generer_code(self) -> str:
        """
        Ici, la ClasseJava délègue la génération à ses enfants. 
        Elle ne sait pas comment s'écrit un attribut, elle appelle juste generer_code().
        """
        lignes = []
        
        # 1. Package
        if self.package:
            lignes.append(f"package {self.package};\n")
            
        # 2. Imports
        for imp in sorted(self.imports):
            lignes.append(f"import {imp};")
        if self.imports:
            lignes.append("")
            
        # 3. Signature de classe (Corrigée avec gestion des interfaces)
        mod_vis = f"{self.visibilite} " if self.visibilite != Visibilite.PACKAGE else ""
        
        if getattr(self, 'est_interface', False):
            mot_cle = "interface"
            mod_abs = ""
        else:
            mot_cle = "class"
            mod_abs = "abstract " if self.est_abstraite else ""
            
        signature = f"{mod_vis}{mod_abs}{mot_cle} {self.nom}"
        
        # Ajout de l'héritage et implémentations
        if self.nom_mere:
            signature += f" extends {self.nom_mere}"
        if self.interfaces:
            signature += " implements " + ", ".join(self.interfaces)
            
        signature += " {"
        lignes.append(signature) # <--- C'EST CA QUI AVAIT DISPARU !
        
        # 4. Attributs
        for attr in self.attributs:
            lignes.append(attr.generer_code())
        if self.attributs:
            lignes.append("")
            
        # 5. Méthodes
        for meth in self.methodes:
            lignes.append(meth.generer_code())
            lignes.append("")
            
        # 6. Getters/Setters 
        for attr in self.attributs:
            lignes.append(attr.generer_getter())
            lignes.append(attr.generer_setter())
            
        lignes.append("}")
        return "\n".join(lignes)