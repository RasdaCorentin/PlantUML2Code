from enum import Enum

class Visibilite(Enum):
    """
    Pourquoi une Enumération ? 
    J'ai choisi d'utiliser une Enum (comme modélisé dans mon diagramme UML) 
    pour avoir un typage fort. Au lieu de manipuler des String ("public", "privat" -> faute de frappe), 
    je contrains les valeurs possibles. C'est beaucoup plus robuste.
    """
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    PACKAGE = ""  # Spécificité Java : le package-private s'écrit sans mot-clé
    
    def __str__(self):
        # Permet de convertir l'Enum directement en texte quand on génère le code
        return self.value