from projectile import Projectile
from helper import Helper

# tête chercheuse
class ProjectilePoison(Projectile):
    def __init__(self, tour_source, tour_x, tour_y, cible, parent):
        super().__init__(tour_source, tour_x, tour_y)
        self.parent = parent # Partie
        self.largeur = 10
        self.longueur = 10
        self.cible = cible
        self.vitesse = 10
        self.degat = 1

    def parcours_la_zone_de_jeu(self):
        angle = Helper.calcAngle(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        distance = Helper.calcDistance(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        x, y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        self.x = x
        self.y = y
        if self.cible.pos_x - 3 < self.x < self.cible.pos_x + 3 or self.cible.pos_y - 3 < self.y < self.cible.pos_y + 3:
            # collision entre projectile et creep
            self.cible.est_attaquer = False
            self.cible.a_poison = True
            self.cible.vitesse -= 3
            return self.cible
        return None

    def est_hors_portee(self, tour_source):
        if ((self.x - tour_source.x) ** 2) + ((self.y - tour_source.y) ** 2) > (tour_source.portee_attaque ** 2):
            return True
        else:
            return False
