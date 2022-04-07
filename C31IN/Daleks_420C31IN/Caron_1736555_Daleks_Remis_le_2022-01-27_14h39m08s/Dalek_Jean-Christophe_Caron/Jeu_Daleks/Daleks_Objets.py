import math
import random



class Feraille():
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Dalek():
    def __init__(self, largeur, hauteur):
        self.x = random.randrange(0, largeur)
        self.y = random.randrange(0, hauteur)

    def modifier_coordonne(self, vecteur):
        self.x += vecteur[0]
        self.y += vecteur[1]
        return None




class Docteur():
    def __init__(self,largeur,hauteur):
        self.x = math.ceil(largeur/2)
        self.y = math.ceil(hauteur/2)
        self.etat = True

    def depacler_docteur(self, vecteur):
        self.x += vecteur[0]
        self.y += vecteur[1]
        return None

    def zapper(self,quantiteZapp,daleks,deplacement):
        daleks_mort = []
        if quantiteZapp > 0:
            for dalek in daleks:
                for mouvement in deplacement:
                    temp_x = self.x + deplacement[mouvement][0]
                    temp_y = self.y + deplacement[mouvement][1]
                    if temp_x == dalek.x:
                        if temp_y == dalek.y:
                            daleks_mort.append(dalek)
        else:
            print("Vous avez pas de zappeur")
        return daleks_mort

    def teleporter(self,quantite,largeur,hauteur):
        if quantite > 0:
            print("TELEPORT")
            self.x = random.randrange(0,largeur)
            self.y = random.randrange(0,hauteur)


class Jeu():
    def __init__(self):
        self.largeur = 10
        self.hauteur = 10
        self.niveaucourant = None
        self.difficulte = 0
        self.deplacement = {
            "q": (-1, -1),
            "w": (0, -1),
            "e": (1, -1),
            "a": (-1, 0),
            "s": (0, 0),
            "d": (1, 0),
            "z": (-1, 1),
            "x": (0, 1),
            "c": (1, 1),
            "k": (0,0),
            "l": (0,0)
            }


    def demarrer_niveau(self):
        self.niveaucourant = Niveau(self.largeur,self.hauteur)
        return None

    def niveau_qui_roule(self, direction):
        self.bouger_docteur(direction)
        self.analyse_partie()
        self.deplacer_dalek(self.niveaucourant.docteur.x, self.niveaucourant.docteur.y)
        self.analyse_partie()
        return self.niveaucourant.docteur.etat

    def bouger_docteur(self, direction):
        if direction in self.deplacement:
            if direction == "k":
                self.niveaucourant.daleks_mort.extend(self.niveaucourant.docteur.zapper(self.niveaucourant.nombre_zappeur,self.niveaucourant.dalek_list,self.deplacement))
            elif direction == "l":
                self.niveaucourant.docteur.teleporter(self.niveaucourant.nombre_teleporteur,self.niveaucourant.largeur,self.niveaucourant.hauteur)
            self.niveaucourant.docteur.depacler_docteur(self.deplacement[direction])


    def deplacer_dalek(self, docX, docY):
        for dalek in self.niveaucourant.dalek_list:
            if dalek.x > docX:
                dalek.x = dalek.x-1
            if dalek.x < docX:
                dalek.x = dalek.x + 1
            if dalek.y > docY:
                dalek.y = dalek.y-1
            if dalek.y < docY:
                dalek.y = dalek.y + 1


    def analyse_partie(self):
        daleks_mort = self.niveaucourant.daleks_mort
        for dalek in self.niveaucourant.dalek_list:
             if dalek.x == self.niveaucourant.docteur.x:
                if dalek.y == self.niveaucourant.docteur.y:
                    self.niveaucourant.docteur.etat = False
        for feraille in self.niveaucourant.ferailles_list:
            if feraille.x == self.niveaucourant.docteur.x:
                if feraille.y == self.niveaucourant.docteur.y:
                    self.niveaucourant.docteur.etat = False

        for dal in self.niveaucourant.dalek_list:
            x = dal.x
            y = dal.y
            for dalek in self.niveaucourant.dalek_list:
                if dalek != dal:  # prouve qui ne sont pas le même objet
                    if dalek.x == x and dalek.y == y:
                        self.niveaucourant.daleks_mort.append(dalek)
                        self.niveaucourant.dalek_list.remove(dal)
        if len(daleks_mort) > 0:
            for dalek in self.niveaucourant.dalek_list:
                for mort in daleks_mort:
                    if dalek.x == mort.x:
                        if dalek.y == mort.y:
                            self.niveaucourant.ferailles_list.append(Feraille(dalek.x,dalek.y))
                            self.niveaucourant.dalek_list.remove(dalek)



    def changer_option_largeur(self, largeur):
        self.largeur = largeur


    def changer_option_hauteur(self, hauteur):
        self.hauteur = hauteur

class Niveau():
    def __init__(self,largeur,hauteur):
        self.niveau = 1
        self.largeur = largeur
        self.hauteur = hauteur
        self.docteur = Docteur(self.largeur,self.hauteur)
        self.nombre_zappeur = 1
        self.nombre_teleporteur = 1
        self.daleks_mort = []
        self.ferailles_list = []

        self.dalek_list = []
        if self.niveau == 1:
            for i in range(5):
                self.dalek_list.append(Dalek(self.largeur, self.hauteur))
        if self.niveau == 2:
            for i in range(10):
                self.dalek_list.append(Dalek(self.largeur, self.hauteur))