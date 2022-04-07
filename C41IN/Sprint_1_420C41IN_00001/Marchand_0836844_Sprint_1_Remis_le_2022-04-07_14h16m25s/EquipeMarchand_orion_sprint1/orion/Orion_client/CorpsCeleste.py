from Id import *
import random
from Ressource import *

class CorpsCeleste:
    def __init__(self, parent, x, y):
        self.id = get_prochain_id()
        self.parent = parent
        self.x = x
        self.y = y
        self.taille = 0
        self.hp = random.randrange(100, 200)
        self.population = 0


class Etoile(CorpsCeleste):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.proprietaire = ""
        self.couleur = "white"
        self.taille = random.randrange(4, 8)
        self.energie = Energie(random.randrange(10, 1001))
        self.ressources = self.generer_ressources()
        self.taille = random.randrange(6, 12)
        self.habitable = True if random.uniform(0, 1) < 0.2 else False
        self.max_figure_importance = 0
        self.max_batiment = 0
        self.max_satellite = 0
        self.max_merveille = 0
        self.max_infrastructures()

    def generer_etoile_mere(self):
        self.max_figure_importance = 2
        self.max_batiment = 4
        self.max_satellite = 1
        self.max_merveille = 1

    def max_infrastructures(self):
        if self.habitable:
            self.max_figure_importance = random.randrange(1, 3)
            self.max_batiment = random.randrange(1, 4)
            self.max_satellite = random.randrange(0, 2)
            self.max_merveille = random.randrange(0, 2)

    # une étoile peut avoir/générer [0, 3] ressources
    # Energie n'est pas une ressource générée
    def generer_ressources(self):
        ressources = []

        nom_ressources_pouvant_exister_sur_etoile = list(
            self.parent.ressources_pouvant_exister_sur_etoile.keys()
        )

        random.shuffle(nom_ressources_pouvant_exister_sur_etoile)

        for nom_ressource in nom_ressources_pouvant_exister_sur_etoile:
            chance_possession_ressource = random.uniform(0, 1)
            if chance_possession_ressource >= self.parent.ressources_pouvant_exister_sur_etoile[nom_ressource][1]:
                ressources.append(self.parent.ressources_pouvant_exister_sur_etoile[nom_ressource][0])

            if len(ressources) == 3:
                return ressources
        return ressources