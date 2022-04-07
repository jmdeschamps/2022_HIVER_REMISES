import math
from tour import Tour
from projectileMitraille import ProjectileMitraille

class TourMitraille(Tour):
    def __init__(self, parent, clic_x, clic_y):
        super().__init__(clic_x, clic_y, 35, 35)
        self.parent = parent # Partie
        self.type = "MITRAILLE"
        self.multiplicateur_portee_attaque = 2
        self.portee_attaque = self.largeur + self.longueur * self.multiplicateur_portee_attaque
        self.aire_attaque = self.determine_circonference_attaque()
        self.cible = None
        self.projectiles = []
        self.image = "images\Towers\Tour_roche.png"
        self.cout_amelioration = 400
        self.niveau = 1
        self.max_niveau=2
        self.augmentation = 8

    def determine_circonference_attaque(self):
        return 2 * math.pi * self.portee_attaque

    def attaque(self, creep_cible):
        if not creep_cible.est_mitraille and not creep_cible.est_tuer:
            self.attaque_en_cours = True
            creep_cible.est_mitraille = True
            self.cible = creep_cible
            self.projectiles.append(ProjectileMitraille(self, self.x, self.y, self.cible, self.parent, self.niveau))

    def ameliorer(self, niv):
        if niv >= self.augmentation:
            self.niveau += 1

            self.multiplicateur_portee_attaque * 2
            self.portee_attaque = self.largeur * self.longueur * self.multiplicateur_portee_attaque
            self.aire_attaque = self.determine_circonference_attaque()

            for projectile in self.projectiles:
                projectile.vitesse * self.niveau

            return True
        else :
            return False