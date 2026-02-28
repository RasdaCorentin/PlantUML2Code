from .notes import Notes


class UMLClasse(Notes):

    def __init__(self, nom, est_abstraite=False, est_interface=False):
        self.nom = nom
        self.est_abstraite = est_abstraite
        self.est_interface = est_interface
        self.attributs = []
        self.operations = []
        self.relations = []
        self.notes = []

    def get_attributs(self):
        return self.attributs

    def get_operations(self):
        return self.operations

    def get_relations(self):
        return self.relations

    def ajouter_notes(self, texte):
        self.notes.append(texte)
