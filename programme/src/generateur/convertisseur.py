class ConvertisseurUmlVersCode:

    def __init__(self, chemin_entree, chemin_sortie):
        self.chemin_entree = chemin_entree
        self.chemin_sortie = chemin_sortie

    def convertir(self, diagramme_classe, generateur):
        return generateur.generer_classe2_langage(diagramme_classe)
