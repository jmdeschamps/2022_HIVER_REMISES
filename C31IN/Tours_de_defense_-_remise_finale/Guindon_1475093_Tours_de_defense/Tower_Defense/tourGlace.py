from tour import Tour
import math
from projectileGlace import ProjectileGlace

class TourGlace(Tour):
    def __init__(self, parent, clic_x, clic_y):
        super().__init__(clic_x, clic_y, 35, 35)
        self.parent = parent  # Partie
        self.type = "GLACE"
        self.multiplicateur_portee_attaque = 4
        self.portee_attaque = self.longueur * self.multiplicateur_portee_attaque
        self.aire_attaque = self.determine_circonference_attaque()
        self.cibles = []
        self.projectiles = []
        self.image = "images\Towers\Tour_bois.png"  # image de tour glace
        self.attaque_en_cours = None
        self.creeps_attaquer = []
        self.cout_amelioration = 150
        self.niveau = 1
        self.max_niveau=2
        self.degat = 0
        self.augmentation = 2

    def determine_circonference_attaque(self):
        return 2 * math.pi * self.portee_attaque

    def attaque(self, creep_cible):
        if creep_cible.est_mobile and not creep_cible.est_attaquer_par_glace:  # si la cible n'est pas déjà immobilisé et attaqué
            self.cibles.append(creep_cible)
            self.projectiles.append(ProjectileGlace(
                self,  # TourGlace source
                self.x,
                self.y,
                creep_cible,
                self.parent,  # Partie: pour transmettre la projection du missile au contrôleur; pour ensuite signaler l'affichage
                self.degat
            ))

    def est_en_mode_attaque(self):
       if len(self.creeps_attaquer) > 0:
           self.attaque_en_cours = True
       else:
           self.attaque_en_cours = False
           for cible in self.cibles:
               cible.est_mobile = True
               cible.est_attaquer_par_glace = False
           self.cibles = []

    def ameliorer(self, niv):
        if niv >= self.augmentation:
            self.niveau += 1
            return True
        else:
            return False