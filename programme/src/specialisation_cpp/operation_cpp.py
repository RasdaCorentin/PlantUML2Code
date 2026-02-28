from .formattage import Formattage


class OperationCpp(Formattage):

    def __init__(self, nom, type_retour_cpp, est_virtuelle=False,
                 est_virtuelle_pure=False):
        super().__init__(id_format=nom)
        self.nom = nom
        self.type_retour_cpp = type_retour_cpp
        self.est_virtuelle = est_virtuelle
        self.est_virtuelle_pure = est_virtuelle_pure

    def generer_code(self) -> str:
        parties = []
        if self.est_virtuelle or self.est_virtuelle_pure:
            parties.append("virtual")
        parties.append(self.type_retour_cpp)
        parties.append(self.nom + "()")
        if self.est_virtuelle_pure:
            parties.append("= 0")
        return "    " + " ".join(parties) + ";"
