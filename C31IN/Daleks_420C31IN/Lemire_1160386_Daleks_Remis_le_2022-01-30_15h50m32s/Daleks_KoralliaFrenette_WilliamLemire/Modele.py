
import random

class Docteur():
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y
        self.vivant = True


class Dalek():
    def __init__(self, pos):
        x, y = pos
        self.x = x
        self.y = y


class Feraille():
        def __init__(self, x, y):

            self.x = x
            self.y = y


class Jeu():
    def __init__(self):
        self.largeur = 8
        self.hauteur = 6
        self.partie_courante=None
        self.nbdaleks_par_niveau = 5
        self.game_over = False
        self.highscore = 0

    def demarrer_partie(self):
        self.partie_courante = Partie(self)

    def changer_option(self, largeur, hauteur, nbdaleks_par_niveau ,niveau_difficulter):
        self.largeur = largeur
        self.hauteur = hauteur
        self.nbdaleks_par_niveau = nbdaleks_par_niveau

    def obtenir_depuis_xy(self, x, y, liste):
        for item in liste:
            if item.x == x and item.y == y:
                return item
        return False

    def obtenir_autre_depuis_xy(self, x, y, liste,original):
        for item in liste:
            if item.x == x and item.y == y and original != item:
                return item
        return False

    def deplacer_docteur(self,deplacement):
        hauteur_maximal = self.hauteur
        largeur_maximal = self.largeur
        if(self.partie_courante.docteur.x + deplacement[0] < largeur_maximal and self.partie_courante.docteur.x +deplacement[0]>=0 and
           self.partie_courante.docteur.y + deplacement[1] < hauteur_maximal and self.partie_courante.docteur.y +deplacement[1]>=0):
                if not self.obtenir_depuis_xy( self.partie_courante.docteur.x + deplacement[0], self.partie_courante.docteur.y + deplacement[1], self.partie_courante.ferailles):
                    self.partie_courante.docteur.x += deplacement[0]
                    self.partie_courante.docteur.y += deplacement[1]
                    return True
                else:
                    return False
        else:
            return False

    def zapper(self):
        if( self.partie_courante.nb_zappeur > 0):
            for checkx in range(self.partie_courante.docteur.x - 1, self.partie_courante.docteur.x + 2):
                for checky in range(self.partie_courante.docteur.y - 1, self.partie_courante.docteur.y + 2):
                    dalek = self.obtenir_depuis_xy(checkx, checky, self.partie_courante.daleks)
                    if dalek:
                        self.partie_courante.daleks.remove(dalek);
                        self.partie_courante.scoregame += 500
            self.partie_courante.nb_zappeur -= 1
            return [0,0]
        else:
            return False

    def teleporter_docteur(self):
        positionvide = False
        while positionvide == False:
            positionoccup??e = False
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            for checkx in range(x-1, x+2):
                for checky in range(y-1, y+2):
                    if self.obtenir_depuis_xy(checkx, checky,self.partie_courante.daleks):
                        positionoccup??e = True

            if self.obtenir_depuis_xy(x, y, self.partie_courante.ferailles):
                positionoccup??e = True

            if positionoccup??e == False:
                positionvide = True
        return [x- self.partie_courante.docteur.x, y - self.partie_courante.docteur.y]

    def deplacer_daleks(self):
        for i in range(len(self.partie_courante.daleks)):
            diff??rencex = self.partie_courante.docteur.x -self.partie_courante.daleks[i].x
            diff??rencey = self.partie_courante.docteur.y - self.partie_courante.daleks[i].y

            if(abs(diff??rencex) > 1):
              if (diff??rencex < 0):
                  diff??rencex =-1
              else:
                  diff??rencex =1

            if(abs(diff??rencey)>1):
                if(diff??rencey<0):
                    diff??rencey =-1
                else:
                    diff??rencey =1

            hauteur_maximal = self.hauteur
            largeur_maximal = self.largeur

            if diff??rencex + self.partie_courante.daleks[i].x > 0 and diff??rencex + self.partie_courante.daleks[i].x < largeur_maximal:
                 self.partie_courante.daleks[i].x =diff??rencex + self.partie_courante.daleks[i].x
            if diff??rencey + self.partie_courante.daleks[i].y >0 and diff??rencey + self.partie_courante.daleks[i].y < hauteur_maximal:
                self.partie_courante.daleks[i].y =diff??rencey + self.partie_courante.daleks[i].y

    def est_collision(self):
        for i in self.partie_courante.daleks:
            duplicat = False;
            while True:
                autre = self.obtenir_autre_depuis_xy(i.x, i.y,self.partie_courante.daleks, i )
                if (not autre):
                    break;
                duplicat = True;
                self.partie_courante.daleks.remove(autre);
                self.partie_courante.scoregame += 500
            if (duplicat):
                self.partie_courante.ferailles.append(Feraille(i.x, i.y))
                self.partie_courante.daleks.remove(i)
                self.partie_courante.scoregame += 500

    def a_frapper_feraille(self):
        for i in self.partie_courante.daleks:
            if self.obtenir_depuis_xy(i.x, i.y, self.partie_courante.ferailles):
                self.partie_courante.daleks.remove(i)
                self.partie_courante.scoregame += 500

    def valider_si_doctor_mort(self):
        for i in self.partie_courante.daleks:
            if( i.x ==self.partie_courante.docteur.x and i.y ==self.partie_courante.docteur.y):
                self.game_over=True

    def est_meilleur_score(self):
        if(self.partie_courante.scoregame > self.highscore):
            self.highscore = self.partie_courante.scoregame


class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.docteur = Docteur(int(self.largeur/2), (int(self.hauteur/2)))
        self.niveau = 0
        self.daleks = []
        self.ferailles = []
        self.nbDalek = 0
        self.nb_zappeur = 0
        self.nb_daleks_par_niv = self.parent.nbdaleks_par_niveau
        self.game_over = False
        self.creer_niveau()
        self.scoregame = 0

    def creer_niveau(self):
        self.niveau += 1
        self.nb_zappeur += 1
        nbDalek = self.niveau * self.nb_daleks_par_niv
        nbpossible=[[self.docteur.x,
                     self.docteur.y]]
        while nbDalek:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x,y] not in nbpossible:
                nbpossible.append([x, y])
                nbDalek -= 1
        nbpossible.pop(0)
        for i in nbpossible:
            self.daleks.append(Dalek(i))
        self.ferailles.clear()


if __name__ == '__main__':
    print("Je suis le mod??le")


