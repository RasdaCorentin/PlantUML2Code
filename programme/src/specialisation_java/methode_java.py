from typing import Dict
from .generable_java import GenerableJava
from .visibilite import Visibilite

class MethodeJava(GenerableJava):
    """
    Générateur de Comportement :
    Construit la signature complète et gère la différence entre 
    une méthode concrète (avec corps) et abstraite (sans corps).
    """
    def __init__(self, nom: str, type_retour: str = "void", visibilite: Visibilite = Visibilite.PUBLIC):
        self.nom = nom
        self.type_retour = type_retour
        self.visibilite = visibilite
        self.parametres: Dict[str, str] = {}
        self.contenu: str = "// TODO: Implémenter le comportement"
        
        # NOUVEAU : Flag pour savoir si la méthode a un corps ou non
        self.est_abstraite = False 

    def generer_code(self) -> str:
        vis = f"{self.visibilite} " if self.visibilite != Visibilite.PACKAGE else ""
        params_str = ", ".join([f"{t} {n}" for n, t in self.parametres.items()])
        
        signature = f"    {vis}{self.type_retour} {self.nom}({params_str})"
        
        # Si la méthode est abstraite (ou dans une interface), pas d'accolades !
        if self.est_abstraite:
            return signature + ";"
        else:
            # Sinon on génère le corps avec le fameux TODO
            code = signature + " {\n"
            code += f"        {self.contenu}\n"
            code += "    }"
            return code