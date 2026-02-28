from .formattage import Formattage


class AttributCpp(Formattage):

    def __init__(self, nom, type_cpp, est_const=False, est_static=False):
        super().__init__(id_format=nom)
        self.nom = nom
        self.type_cpp = type_cpp
        self.est_const = est_const
        self.est_static = est_static

    def generer_code(self) -> str:
        parties = []
        if self.est_static:
            parties.append("static")
        if self.est_const:
            parties.append("const")
        parties.append(self.type_cpp)
        parties.append(self.nom + ";")
        return "    " + " ".join(parties)
