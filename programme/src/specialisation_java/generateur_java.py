from ..generateur.generateur import Generateur
from ..generateur.langage_sortie import LangageSortie

from .visibilite import Visibilite
from .classe_java import ClasseJava
from .attribut_java import AttributJava
from .methode_java import MethodeJava

class GenerateurJava(Generateur):
    """
    Le Chef d'Orchestre (Pattern Factory) :
    C'est la classe de référence de mon extension. Elle lit le modèle UML partagé,
    instancie mes classes Java intermédiaires, gère la traduction des types, 
    résout les relations (Héritage/Associations) et génère les fichiers.
    """

    def __init__(self):
        super().__init__(langage=LangageSortie.JAVA)
        self._package_par_defaut = "com.projet.generated"
        # STOCAKGE BIDIRECTIONNEL : Je garde une trace de toutes les classes créées 
        # pour pouvoir résoudre les relations croisées lors du second passage.
        self.classes_generees = {} # Dict[nom_classe, ClasseJava]

    def generer_bloc_commentaire(self) -> str:
        return "/* Auto-generated Java code by UMLFactory (Extension par B.DIJOUX) */"

    def generer_classe2_langage(self, diagramme_classe) -> list:
        """Redéfinition de la méthode commune pour traiter le diagramme."""
        self.classes_generees.clear()
        
        # PREMIER PASSAGE : Création coquille vide + attributs/méthodes simples
        # Je dois d'abord instancier toutes les classes avant de lier les relations,
        # sinon je pourrais pointer vers une classe qui n'existe pas encore.
        for uml_classe in diagramme_classe.get_liste_classes():
            classe_java = self._traduire_classe(uml_classe)
            self.classes_generees[classe_java.nom] = classe_java
            
        # SECOND PASSAGE : Traduction des relations (Héritage, Agrégation, etc.)
        for uml_classe in diagramme_classe.get_liste_classes():
            classe_java = self.classes_generees[uml_classe.nom]
            for type_rel, rel in uml_classe.get_relations():
                self._traduire_relation(classe_java, type_rel, rel)
            
        # TROISIÈME PASSAGE : Écriture finale des fichiers
        fichiers = []
        for c_java in self.classes_generees.values():
            fichiers.append(self._sauvegarder_fichier(c_java))
            
        return fichiers

    def _traduire_classe(self, uml_classe) -> ClasseJava:
        """Fabrique une ClasseJava à partir d'une UMLClasse du métamodèle."""
        # J'injecte 'self' pour respecter l'association bidirectionnelle du diagramme
        classe_java = ClasseJava(nom=uml_classe.nom, generateur_parent=self)
        
        # Récupération du type de classe (abstraite ou interface)
        classe_java.est_abstraite = uml_classe.est_abstraite
        # ---> POUR LES INTERFACES <---
        classe_java.est_interface = getattr(uml_classe, 'est_interface', False)
        
        # 1. Copie des attributs simples
        for attr in uml_classe.get_attributs():
            attr_java = AttributJava(
                nom=attr.nom,
                type_java=self._traduire_type(attr.type),
                visibilite=self._traduire_visibilite(attr.visibilite)
            )
            classe_java.attributs.append(attr_java)
            
        # 2. Copie des opérations simples
        for op in uml_classe.get_operations():
            meth_java = MethodeJava(
                nom=op.nom,
                type_retour=self._traduire_type(op.type_retour),
                visibilite=self._traduire_visibilite(op.visibilite)
            )
            
            # --- LA CORRECTION EST ICI ---
            # Si la classe est une interface, toutes ses méthodes sont sans corps (abstraites)
            if classe_java.est_interface:
                meth_java.est_abstraite = True
            # -----------------------------
                
            classe_java.methodes.append(meth_java)
            
        return classe_java

    def _traduire_relation(self, classe_source: ClasseJava, type_rel: str, rel):
        """
        La magie des relations Java :
        L'UML a des flèches, Java a des 'extends', 'implements' et des attributs objets.
        Ici, je traduis la relation UML dans le bon concept Java.
        """
        # Identification de la cible (celui en face de la relation)
        nom_cible = rel.cible.nom if rel.source.nom == classe_source.nom else rel.source.nom
        
        # 1. Cas de l'Héritage (extends)
        if type_rel == "heritage" or getattr(rel, 'estHeritage', False):
            classe_source.nom_mere = nom_cible
            
        # 2. Cas de l'Implémentation d'interface (implements)
        elif type_rel == "implementation" or getattr(rel, 'estImplementation', False):
            classe_source.interfaces.append(nom_cible)
            
        # 3. Cas des Associations/Agrégations/Compositions
        # En Java, cela se traduit par la création d'un Attribut dans la classe source !
        else:
            # Récupération de la cardinalité pour savoir si c'est une Liste ou un Objet simple
            cardinalite = rel.cardinalite_cible if rel.source.nom == classe_source.nom else rel.cardinalite_source
            nom_attribut = nom_cible.lower() # Par défaut le nom de la classe en minuscule
            
            # Si cardinalité multiple (*, 0..*, 1..n), on crée une List<>
            if "*" in str(cardinalite) or "n" in str(cardinalite).lower():
                type_java = f"List<{nom_cible}>"
                nom_attribut += "s" # Pluriel
                classe_source.ajouter_import("java.util.List") # Import automatique natif Java !
            else:
                type_java = nom_cible
                
            # Création de l'attribut de relation et ajout à la classe
            attr_relation = AttributJava(
                nom=nom_attribut,
                type_java=type_java,
                visibilite=Visibilite.PRIVATE # Les relations sont privées par défaut (Encapsulation)
            )
            classe_source.attributs.append(attr_relation)

    def _traduire_type(self, type_uml: str) -> str:
        """
        Traduction des types agnostiques de l'UML vers les types primitifs/objets Java.
        """
        if not type_uml: return "Object"
        
        mapping = {
            "entier": "int",
            "integer": "Integer",
            "chaine": "String",
            "string": "String",
            "booleen": "boolean",
            "boolean": "Boolean",
            "date": "LocalDate",
            "float": "float",
            "double": "double"
        }
        type_clean = type_uml.strip().lower()
        
        # Astuce : si on a un type complexe identifié, on pourrait ajouter l'import ici !
        if type_clean == "date":
            # Si on était dans _traduire_classe, on pourrait appeler classe.ajouter_import("java.time.LocalDate")
            return "LocalDate"
            
        return mapping.get(type_clean, type_uml)

    def _traduire_visibilite(self, visibilite_uml) -> Visibilite:
        """
        Convertit la visibilité UML en Enum Java sécurisée.
        Blindée pour accepter des String ("+", "public") ou des objets Enum du parseur commun.
        """
        if not visibilite_uml: 
            return Visibilite.PRIVATE
            
        # Si c'est DÉJÀ notre objet Visibilite (cas rare mais sécurisant)
        if isinstance(visibilite_uml, Visibilite):
            return visibilite_uml
            
        # On force la conversion en chaîne de caractères, et on met tout en minuscules
        # Si c'est une Enum du parseur commun, str() récupérera son nom ou sa valeur
        vis_str = str(visibilite_uml).strip().lower()
        
        # On cherche des correspondances larges
        if "+" in vis_str or "public" in vis_str:
            return Visibilite.PUBLIC
        if "#" in vis_str or "protected" in vis_str:
            return Visibilite.PROTECTED
        if "-" in vis_str or "private" in vis_str:
            return Visibilite.PRIVATE
        if "~" in vis_str or "package" in vis_str:
            return Visibilite.PACKAGE
            
        # Par défaut (encapsulation)
        return Visibilite.PRIVATE

    def _sauvegarder_fichier(self, classe_java: ClasseJava):
        """
        Packagage final :
        Assemble le bloc de commentaire global (auteur, timestamp) et le code 
        généré par la ClasseJava. Retourne un dictionnaire exploitable par 
        le convertisseur principal du projet de groupe.
        """
        code = self.generer_bloc_commentaire() + "\n\n"
        code += classe_java.generer_code()
        
        # Le format de retour (dict) dépend de l'attente de "ConvertisseurUmlVersCode"
        return {
            "nom_fichier": f"{classe_java.nom}.java",
            "contenu": code
        }