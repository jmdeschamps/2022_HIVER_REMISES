from tkinter import *
import time
class Partie():
    def __init__(self,parent):
        self.parent = parent
        self.debut = None
        self.duree = 0


    def recibler_pion(self, x, y):
        self.parent.pion.reciblerPion(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut




class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 450
        self.hauteur = 450
        self.pion = Pion(self)
        self.bordure= Bordure(self)
        self.sentinelles = []
        self.creer_sentinelles()
        self.partie_en_cours = Partie(self)

    def reset_partie(self):
        self.pion.x = 225
        self.pion.y = 225
        self.sentinelles.clear()
        self.creer_sentinelles()

    def creer_sentinelles(self):
        self.sentinelles.append(Sentinelles(self, 100, 100, 30, 30, 6, -5))
        self.sentinelles.append(Sentinelles(self, 300, 85, 30, 25, -5, -6))
        self.sentinelles.append(Sentinelles(self, 85, 350, 15, 30, 5, 6))
        self.sentinelles.append(Sentinelles(self, 350, 340, 50, 10, -6, 5))

# CADRE NOIR
class Bordure():
    def __init__(self, parent):
        self.parent = parent
        self.x = 0
        self.y = 0
        self.demitaille = 50


class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.x = 225
        self.y = 225
        self.demitaille = 20
        self.isCollision = False


    def reciblerPion(self, x, y):
        self.x = x
        self.y = y
        self.tester_collisionBordure()
        self.tester_collision_sentinelle()

    def tester_collisionBordure(self):
        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        bordure = self.parent.bordure

        #tester cadre haut
        bordure_top_x1 = bordure.x - bordure.demitaille
        bordure_top_y1 = bordure.y - bordure.demitaille
        bordure_top_x2 = 500 + bordure.demitaille
        bordure_top_y2 = bordure.y + bordure.demitaille
        #tester cadre bas
        bordure_bottom_x1 = bordure.x - bordure.demitaille
        bordure_bottom_y1 = 450 - bordure.demitaille
        bordure_bottom_x2 = 500 + bordure.demitaille
        bordure_bottom_y2 = 500 + bordure.demitaille
        #tester cadre gauche
        bordure_left_x1 = bordure.x - bordure.demitaille
        bordure_left_y1 = bordure.y - bordure.demitaille
        pot_left_left_x2 = bordure.x + bordure.demitaille
        bordure_left_y2 = 500 + bordure.demitaille
        #tester cadre droite
        bordure_right_x1 = 450 - bordure.demitaille
        bordure_right_y1 = bordure.y - bordure.demitaille
        bordure_right_x2 = 500 + bordure.demitaille
        bordure_right_y2 = 500 + bordure.demitaille

        # tester cadre haut
        if (x2 > bordure_top_x1 and x1 < bordure_top_x2) and (y2 > bordure_top_y1 and y1 < bordure_top_y2):
            self.isCollision = True

        # tester cadre bas
        if (x2 > bordure_bottom_x1 and x1 < bordure_bottom_x2) and (y2 > bordure_bottom_y1 and y1 < bordure_bottom_y2):
            self.isCollision = True

        # tester cadre gauche
        if (x2 > bordure_left_x1 and x1 < pot_left_left_x2) and (y2 > bordure_left_y1 and y1 < bordure_left_y2):
            self.isCollision = True

        # tester cadre droite
        if (x2 > bordure_right_x1 and x1 < bordure_right_x2) and (y2 > bordure_right_y1 and y1 < bordure_right_y2):
            self.isCollision = True

    def tester_collision_sentinelle(self):
        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        for i in self.parent.sentinelles:
            i_x1 = i.x - i.dt1
            i_y1 = i.y - i.dt2
            i_x2 = i.x + i.dt1
            i_y2 = i.y + i.dt2

            if (x2 > i_x1 and x1 < i_x2) and (y2 > i_y1 and y1 < i_y2):
                self.isCollision = True

class Sentinelles():
    def __init__(self, parent, x, y, dt1, dt2, vitesse_x, vitesse_y):
        self.parent = parent
        self.x = x
        self.y = y
        self.dt1 = dt1
        self.dt2 = dt2
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y

    def move(self):

        self.x += self.vitesse_x
        self.y -= self.vitesse_y

        self.x1 = self.x - self.dt1
        self.y1 = self.y - self.dt2
        self.x2 = self.x + self.dt1
        self.y2 = self.y + self.dt2

        if self.x1 <= 0 or self.x2 >= 450:
            self.vitesse_x *= -1
        if self.y1 <= 0 or self.y2 >= 450:
            self.vitesse_y *= -1