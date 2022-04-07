from projectile import Projectile
from helper import Helper

class ProjectileGlace(Projectile):
    def __init__(self, tour_source, clic_x, clic_y, cible, parent, degat):
        super().__init__(tour_source, clic_x, clic_y)
        self.parent = parent  # Partie
        self.cible = cible
        self.largeur = 10
        self.longueur = 10
        self.vitesse = self.cible.vitesse
        self.degat = degat  # la tour glace n'inflige aucun dégât au premier niveau; sauf si améliorations effectuées
        self.direction = None

    # à changer
    def parcours_la_zone_de_jeu(self):
        angle = Helper.calcAngle(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        distance = Helper.calcDistance(self.x, self.y, self.cible.pos_x, self.cible.pos_y)
        x, y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        self.x = x
        self.y = y

        if self.cible.pos_x - 3 < self.x < self.cible.pos_x + 3 or self.cible.pos_y - 3 < self.y < self.cible.pos_y + 3:
            # self.cible.est_attaquer = False  # après collision, la cible n'est plus attaqué
            # self.cible.est_mobile = False
            # self.tour_source.attaque_en_cours = False
            return self.cible
        return None

    def est_hors_portee(self, tour_source):
        if ((self.x - tour_source.x) ** 2) + ((self.y - tour_source.y) ** 2) > (tour_source.portee_attaque ** 2):
            return True
        else:
            return False