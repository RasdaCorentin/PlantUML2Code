class ClassePython:

    def __init__(self, nom: str, est_abstraite: bool = False):
        self.nom = nom
        self.est_abstraite = est_abstraite
        self.notes = []
        self.attributs_py = []
        self.operations_py = []
        self.relations_py = []
        self.parent = None
        self.interfaces = []
        self.est_interface = False
