import time

from pion import Pion
from sentinelle import Sentinelle


class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.largeur_fenetre = self.parent.largeur_fenetre
        self.hauteur_fenetre = self.parent.hauteur_fenetre
        self.largeur_zone = self.parent.largeur_zone
        self.hauteur_zone = self.parent.hauteur_zone
        self.duree = None
        self.est_termine = False
        self.dimension_pion = 1
        self.dimension_sentinelles = 1
        self.vitesse = 5
        self.vitesse_a_modifier = True
        self.pion = Pion(self, self.parent.largeur_fenetre, self.parent.hauteur_fenetre)
        self.sentinelles = []
        self.creer_sentinelles()
        self.points = 0

    def demarrer_chrono(self):
        self.duree = time.time()

    def arreter_chrono(self):
        self.duree = time.time() - self.duree

    def incrementer_vitesse(self):
        if self.parent.choix_difficulte == "4":
            if int((time.time() - self.duree) % 10) == 0:
                if self.vitesse_a_modifier:
                    for i in self.sentinelles:
                        i.incrementer_vitesse()
                    self.vitesse_a_modifier = False
            elif int((time.time() - self.duree) % 10) > 1:
                self.vitesse_a_modifier = True

    def deplacer_pion(self, x, y):
        self.pion.deplacer(x, y)

    def creer_sentinelles(self, dimension_sentinelles=1, vitesse=5):
        self.sentinelles.append(
            Sentinelle(self, 60 * dimension_sentinelles, 60 * dimension_sentinelles, 100, 100, vitesse))
        self.sentinelles.append(
            Sentinelle(self, 60 * dimension_sentinelles, 50 * dimension_sentinelles, 300, 85, vitesse))
        self.sentinelles.append(
            Sentinelle(self, 30 * dimension_sentinelles, 60 * dimension_sentinelles, 85, 350, vitesse))
        self.sentinelles.append(
            Sentinelle(self, 100 * dimension_sentinelles, 20 * dimension_sentinelles, 355, 340, vitesse))

    def deplacer_sentinelles(self):
        for i in self.sentinelles:
            i.deplacer()

    def verifier_collision(self):
        for i in self.sentinelles:
            x1 = self.pion.position_x - self.pion.largeur / 2
            y1 = self.pion.position_y - self.pion.hauteur / 2
            x2 = self.pion.position_x + self.pion.largeur / 2
            y2 = self.pion.position_y + self.pion.hauteur / 2
            potx1 = i.position_x - i.largeur / 2
            poty1 = i.position_y - i.hauteur / 2
            potx2 = i.position_x + i.largeur / 2
            poty2 = i.position_y + i.hauteur / 2
            if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
                self.est_termine = True

    def verifier_sortie(self):
        if self.pion.position_x - self.pion.largeur / 2 <= 0 or self.pion.position_x + self.pion.largeur / 2 >= self.largeur_zone or self.pion.position_y - self.pion.hauteur / 2 <= 0 or self.pion.position_y + self.pion.hauteur / 2 >= self.hauteur_zone:
            self.est_commence = False
            self.est_termine = True
            print("Sortie du jeu")

    def reinitialiser_objets(self):
        self.pion = Pion(self, self.parent.largeur_fenetre, self.parent.hauteur_fenetre, self.dimension_pion)
        self.sentinelles = []
        self.creer_sentinelles(self.dimension_sentinelles, self.vitesse)

    def calculer_points(self):
        points = int(self.duree)
        if self.parent.choix_sentinelles == "1":
            points *= 0.5
        elif self.parent.choix_sentinelles == "3":
            points *= 2
        if self.parent.choix_pion == "1":
            points *= 0.75
        elif self.parent.choix_pion == "3":
            points *= 1.5
        if self.parent.choix_jeu == "2":
            points *= 0.75
        elif self.parent.choix_jeu == "3":
            points *= 0.5
        if self.parent.choix_difficulte == "1":
            points *= 0.20
        elif self.parent.choix_difficulte == "3":
            points *= 3
        elif self.parent.choix_difficulte == "4":
            points *= 1.5
        self.points = int(points)

    def sauvegarder_options(self):
        if self.parent.choix_sentinelles == "1":
            self.dimension_sentinelles = 0.5
        elif self.parent.choix_sentinelles == "2":
            self.dimension_sentinelles = 1
        elif self.parent.choix_sentinelles == "3":
            self.dimension_sentinelles = 2
        if self.parent.choix_difficulte == "1" or self.parent.choix_difficulte == "4":
            self.vitesse = 5
        elif self.parent.choix_difficulte == "2":
            self.vitesse = 10
        elif self.parent.choix_difficulte == "3":
            self.vitesse = 15
        self.sentinelles = []
        self.creer_sentinelles(self.dimension_sentinelles, self.vitesse)
        if self.parent.choix_pion == "1":
            self.dimension_pion = 0.5
        elif self.parent.choix_pion == "2":
            self.dimension_pion = 1
        elif self.parent.choix_pion == "3":
            self.dimension_pion = 2
        self.pion = Pion(self, self.parent.largeur_fenetre, self.parent.hauteur_fenetre, self.dimension_pion)
