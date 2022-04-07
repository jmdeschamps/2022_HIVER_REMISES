from projectile import Projectile
from helper import Helper

class ProjectileGlace(Projectile):
    def __init__(self, tour_source, clic_x, clic_y, cible, parent):
        super().__init__(tour_source, clic_x, clic_y)
        self.parent = parent  # Partie
        self.cible = cible
        self.largeur = 10
        self.longueur = 10
        self.vitesse = 10
        self.degat = None  # la tour glace n'inflige aucun dégât
        self.direction = None

    # à changer
    def parcours_la_zone_de_jeu(self):
        # if self.x != self.cible.pos_x:
        #     if self.x < self.cible.pos_x:
        #         self.x += self.vitesse
        #     elif self.x > self.cible.pos_x:
        #         self.x -= self.vitesse
        #
        # if self.y != self.cible.pos_y:
        #     if self.y < self.cible.pos_y:
        #         self.y += self.vitesse
        #     elif self.y > self.cible.pos_y:
        #         self.y -= self.vitesse
        angle = Helper.calcAngle(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        distance = Helper.calcDistance(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        x, y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        self.x = x
        self.y = y

        if self.cible.pos_x - 3 < self.x < self.cible.pos_x + 3 or self.cible.pos_y - 3 < self.y < self.cible.pos_y + 3:
            # collision entre projectile et creep
            self.cible.est_attaquer = False
            return self.cible
        return None

    def est_hors_portee(self, tour_source):
        if ((self.x - tour_source.x) ** 2) + ((self.y - tour_source.y) ** 2) > (tour_source.portee_attaque ** 2):
            return True
        else:
            return False