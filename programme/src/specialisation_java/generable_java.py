from abc import ABC, abstractmethod

class GenerableJava(ABC):
    """
    Le Contrat (Interface) :
    J'ai créé cette interface pour standardiser la génération.
    Au lieu que la ClasseJava s'occupe de formater ses enfants manuellement, 
    tout élément Java (Classe, Attribut, Méthode) implémente ce contrat et 
    sait se transformer lui-même en chaîne de caractères (String).
    C'est du polymorphisme pur.
    """
    @abstractmethod
    def generer_code(self) -> str:
        pass