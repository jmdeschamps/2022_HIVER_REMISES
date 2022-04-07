import time

class Jeu:
    def __init__(self, controller):
        self.parent = controller
        self.largeur = 550
        self.hauteur = 550
        self.partie = None

    def nouvelle_partie(self):
        self.partie = Partie(self)

class Partie:
    def __init__(self, jeu):
        self.parent = jeu
        self.aire_de_jeu = Aire_de_jeu(self.parent.largeur, self.parent.hauteur)
        self.joueur = Joueur(self)
        self.sentinellesListe = []
        self.ajouter_sentinelles()
        self.debut = None
        self.duree = 0

    def ajouter_sentinelles(self):
        self.sentinellesListe.append(Sentinelle(self, hauteur=60, largeur=60, x=100, y=100))
        self.sentinellesListe.append(Sentinelle(self, hauteur=60, largeur=50, x=300, y=85))
        self.sentinellesListe.append(Sentinelle(self, hauteur=30, largeur=60, x=85, y=350))
        self.sentinellesListe.append(Sentinelle(self, hauteur=100, largeur=20, x=355, y=340))

    def bouger_sentinelles(self):
        for sentinelle in self.sentinellesListe:
            sentinelle.bouger()

    def recibler_joueur(self, x, y):
        self.joueur.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def tester_collision(self):
        x1 = self.joueur.x - self.joueur.demitaille
        y1 = self.joueur.y - self.joueur.demitaille
        x2 = self.joueur.x + self.joueur.demitaille
        y2 = self.joueur.y + self.joueur.demitaille

        bx1 = self.aire_de_jeu.bordure_x1+self.aire_de_jeu.marge
        bx2 = self.aire_de_jeu.bordure_x2+self.aire_de_jeu.marge
        by1 = self.aire_de_jeu.bordure_y1+self.aire_de_jeu.marge
        by2 = self.aire_de_jeu.bordure_y2+self.aire_de_jeu.marge

        if x1 <= bx1:
            self.parent.parent.fin_partie()
        if x2 >= bx2:
            self.parent.parent.fin_partie()
        if y1 <= by1:
            self.parent.parent.fin_partie()
        if y2 >= by2:
            self.parent.parent.fin_partie()

        for sentinelle in self.sentinellesListe:
            sentinellex1 = sentinelle.x - sentinelle.demitailleX + self.aire_de_jeu.marge
            sentinelley1 = sentinelle.y - sentinelle.demitailleY + self.aire_de_jeu.marge
            sentinellex2 = sentinelle.x + sentinelle.demitailleX + self.aire_de_jeu.marge
            sentinelley2 = sentinelle.y + sentinelle.demitailleY + self.aire_de_jeu.marge

            if (x2 > sentinellex1 and x1 < sentinellex2) and (y2 > sentinelley1 and y1 < sentinelley2):
                self.parent.parent.fin_partie()

class Aire_de_jeu:
    def __init__(self, largeur_externe, hauteur_externe):
        self.largeur_externe = largeur_externe
        self.hauteur_externe = hauteur_externe
        self.couleur_externe = "black"
        self.marge = 50
        self.largeur_interne = largeur_externe-2*self.marge
        self.hauteur_interne = hauteur_externe-2*self.marge
        self.couleur_interne = "white"
        self.bordure_x1 = 0
        self.bordure_x2 = self.largeur_interne
        self.bordure_y1 = 0
        self.bordure_y2 = self.hauteur_interne


class Joueur:
    def __init__(self, parent, largeur=40, hauteur=40):
        self.parent = parent
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = "red"
        self.x = self.parent.aire_de_jeu.hauteur_externe/2
        self.y = self.parent.aire_de_jeu.largeur_externe/2
        self.demitaille = largeur/2

    def recibler(self, x, y):
        self.x = x
        self.y = y
        self.parent.tester_collision()


class Sentinelle:
    def __init__(self, parent, largeur, hauteur, x, y):
        self.parent = parent
        self.largeur = largeur
        self.hauteur = hauteur
        self.x = x
        self.y = y
        self.couleur = "blue"
        self.vitesse_x = 5
        self.vitesse_y = 5
        self.demitailleX = largeur/2
        self.demitailleY = hauteur/2

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.parent.tester_collision()

        if self.y > self.parent.aire_de_jeu.bordure_y2 or self.y < self.parent.aire_de_jeu.bordure_y1:
            self.vitesse_y = self.vitesse_y*-1.2

        if self.x > self.parent.aire_de_jeu.bordure_x2 or self.x < self.parent.aire_de_jeu.bordure_x1:
            self.vitesse_x = self.vitesse_x*-1.2
