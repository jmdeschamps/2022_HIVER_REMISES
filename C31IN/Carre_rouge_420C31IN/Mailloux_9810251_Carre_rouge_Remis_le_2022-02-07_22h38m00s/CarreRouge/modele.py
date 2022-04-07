import time
import os

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 550
        self.hauteur = 550
        self.bordure = 50
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.pret = True
        self.liste_sentinelles = []
        self.creer_sentinelles()
        self.high_scores = [["mitch",4.2],["tch",5.1]]
        self.charger_scores()


    def charger_scores(self):
        #rep_cour = os.getcwd()
        chemin_fichier = ".\high_scores.txt"
        if os.path.isfile(chemin_fichier):
            with open(chemin_fichier) as f:
                lines = f.readlines()
                for line in lines:
                    for i in line:
                        self.high_scores.append([str(i[0]), float(i[1])])

    def sauver_scores(self):
        rep_cour = os.getcwd()
        chemin_fichier = os.path.join(rep_cour, 'high_scores.txt')
        with open(chemin_fichier) as f:
            for i in self.high_scores:
                f.write(str(i[0]) + "," + str(i[1]) + "\n")

    def gestion_score(self):
        if self.duree > self.high_scores[-1][1]:
            self.parent.vue.fenetre_high_score()
            self.high_scores.sort(key=lambda x: x[1], reverse=True)
            self.high_scores = self.high_scores[:10]

    def creer_sentinelles(self):
        s1 = Sentinelle(self, 100, 100, 30, 30, 1, 1)
        s2 = Sentinelle(self, 300, 85, 30, 25, -1, 1)
        s3 = Sentinelle(self, 85, 300, 30, 25, 1, -1)
        s4 = Sentinelle(self, 355, 340, 50, 10, -1, -1)
        self.liste_sentinelles.append(s1)
        self.liste_sentinelles.append(s2)
        self.liste_sentinelles.append(s3)
        self.liste_sentinelles.append(s4)

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def replacer_jeu(self):
        self.duree = 0
        self.high_scores.sort(reverse=True)
        self.liste_sentinelles = []
        self.creer_sentinelles()
        self.pion.x = self.largeur/2
        self.pion.y = self.hauteur/2

class Sentinelle():
    def __init__(self, parent, x, y, dx, dy, directionx, directiony):
        self.parent = parent
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.directionx = directionx
        self.directiony = directiony

    def deplacer_sentinelle(self):
        self.x += 4 * self.directionx
        self.y += 4 * self.directiony

        sentxmin = self.x - self.dx
        sentxmax = self.x + self.dx
        sentymin = self.y - self.dy
        sentymax = self.y + self.dy

       #Rebondir contre cadre de la fenêtre
        if sentxmin < 0:
            self.directionx *= -1.1
        if sentxmax > self.parent.largeur:
            self.directionx *= -1.1
        if sentymin < 0:
            self.directiony *= -1.1
        if sentymax > self.parent.hauteur:
            self.directiony *= -1.1

    def verifier_capture(self):

        carrexmin = self.parent.pion.x - self.parent.pion.demitaille
        carrexmax = self.parent.pion.x + self.parent.pion.demitaille
        carreymin = self.parent.pion.y - self.parent.pion.demitaille
        carreymax = self.parent.pion.y + self.parent.pion.demitaille

        sentxmin = self.x - self.dx
        sentxmax = self.x + self.dx
        sentymin = self.y - self.dy
        sentymax = self.y + self.dy

        if (sentxmax > carrexmin and sentxmin < carrexmax) and (sentymax > carreymin and sentymin < carreymax):
            print("capture", self.parent.duree)
            self.parent.pret = False
            self.parent.gestion_score()

class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
        self.demitaille = 10

    def recibler(self, x, y):
        self.x = x
        self.y = y
        self.tester_collision()

    def tester_collision(self):

        # Collision avec bordure noire

        limite_gauche = self.parent.bordure
        limite_droite = self.parent.largeur - self.parent.bordure
        limite_haut = self.parent.bordure
        limite_bas = self.parent.hauteur - self.parent.bordure

        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        if x1 < limite_gauche or x2 > limite_droite or y1 < limite_haut or y2 > limite_bas:
            print("mur", self.parent.duree)
            self.parent.pret = False
            self.parent.gestion_score()

        # Collision avec une sentinelle

        # for i in self.parent.liste_sentinelles:
        #     sentinellex1 = i.x - i.dx
        #     sentinelley1 = i.y - i.dy
        #     sentinellex2 = i.x + i.dx
        #     sentinelley2 = i.y + i.dy
        #
        #     if (x2 > sentinellex1 and x1 < sentinellex2) and (y2 > sentinelley1 and y1 < sentinelley2):
        #         print("collision", self.parent.duree)
        #         self.parent.pret = False
        #         self.parent.gestion_score(self.parent.duree)






