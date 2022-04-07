from tour import Tour
import math
from projectileGlace import ProjectileGlace

class TourGlace(Tour):
    def __init__(self, parent, clic_x, clic_y):
        super().__init__(clic_x, clic_y, 35, 35)
        self.parent = parent  # Partie
        self.type = "GLACE"
        self.portee_attaque = self.largeur + self.longueur * 2
        self.aire_attaque = self.determine_circonference_attaque()
        self.cible = None
        self.projectiles = []
        self.image = "images\Towers\Tour_bois.png"  # image de tour glace

    def determine_circonference_attaque(self):
        return 2 * math.pi * self.portee_attaque

    def attaque(self, creep_cible):
        if not self.attaque_en_cours:
            self.attaque_en_cours = True
            self.cible = creep_cible
            if self.cible.est_mobile and len(self.projectiles) == 0:
                self.projectiles.append(ProjectileGlace(self, self.x, self.y, self.cible, self.parent))
        else:
            if self.cible.est_mobile:
                self.attaque_en_cours = False
                self.cible = None
