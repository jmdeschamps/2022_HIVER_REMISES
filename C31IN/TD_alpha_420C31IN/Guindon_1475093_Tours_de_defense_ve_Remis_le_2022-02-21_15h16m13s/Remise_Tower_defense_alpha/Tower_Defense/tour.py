from projectile import Projectile


class Tour:
    def __init__(self, clic_x, clic_y, largeur, longueur):
        self.largeur = largeur
        self.longueur = longueur
        self.x = clic_x
        self.y = clic_y
        self.attaque_en_cours = False
        self.creeps_attaquer = []
