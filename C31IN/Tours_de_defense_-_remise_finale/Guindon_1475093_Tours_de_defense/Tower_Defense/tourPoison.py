import math
from tour import Tour
from projectilePoison import ProjectilePoison


class TourPoison(Tour):
    def __init__(self, parent, clic_x, clic_y):
        super().__init__(clic_x, clic_y, 35, 35)
        self.parent = parent # Partie
        self.type = "POISON"
        self.portee_attaque = self.largeur + self.longueur * 2
        self.aire_attaque = self.determine_circonference_attaque()
        self.cible = None
        self.projectiles = []
        self.image = "images\Towers\Tour_poison.png"
        # POUR ATTAQUE
        self.nbr_attaques_en_cours = 0
        self.cout_amelioration = 180
        self.niveau = 1
        self.max_niveau = 2
        self.degats_additionnels = 0
        self.augmentation = 2

    def determine_circonference_attaque(self):
        return 2 * math.pi * self.portee_attaque

    def attaque(self, creep_cible):
        if not self.attaque_en_cours and self.nbr_attaques_en_cours <= 1 and not creep_cible.a_poison:
            self.attaque_en_cours = True
            self.cible = creep_cible
            self.projectiles.append(ProjectilePoison(self, self.x, self.y, self.cible, self.parent,
                                                     self.degats_additionnels))
            self.nbr_attaques_en_cours += 1

    def ameliorer(self, niv):
        if niv >= self.augmentation:
            print(niv)
            self.niveau += 1
            self.degats_additionnels += 1
            return True
        else :
            return False