from .generable_java import GenerableJava
from .visibilite import Visibilite

class AttributJava(GenerableJava):
    """
    Générateur d'État :
    Cette classe gère la déclaration de l'attribut, mais c'est aussi elle 
    qui est responsable de générer ses propres Getters et Setters (Spécificité Java).
    """
    def __init__(self, nom: str, type_java: str, visibilite: Visibilite = Visibilite.PRIVATE):
        self.nom = nom
        self.type = type_java
        self.visibilite = visibilite
        self.est_static = False
        self.est_final = False

    def generer_code(self) -> str:
        # Je construis la liste des modificateurs (public, static, final...)
        mods = []
        if self.visibilite != Visibilite.PACKAGE:
            mods.append(str(self.visibilite))
        if self.est_static:
            mods.append("static")
        if self.est_final:
            mods.append("final")
            
        mod_str = " ".join(mods) + " " if mods else ""
        return f"    {mod_str}{self.type} {self.nom};"

    def generer_getter(self) -> str:
        """Génération automatique de l'accesseur (Getter)."""
        nom_maj = self.nom[0].upper() + self.nom[1:]
        return f"""    public {self.type} get{nom_maj}() {{
        return this.{self.nom};
    }}"""

    def generer_setter(self) -> str:
        """Génération automatique du mutateur (Setter)."""
        nom_maj = self.nom[0].upper() + self.nom[1:]
        return f"""    public void set{nom_maj}({self.type} {self.nom}) {{
        this.{self.nom} = {self.nom};
    }}"""