import random
from docteur import Docteur
from dalek import Dalek
from ferraille import Ferraille


class Partie():
    def __init__(self, largeur, hauteur, teleportation):
        self.score = 0
        self.niveau = 0
        self.largeur = largeur
        self.hauteur = hauteur
        self.teleportation = teleportation
        self.nbr_zappeurs = 1
        self.nbr_daleks_par_niveau = 5
        self.docteur = Docteur(self.largeur, self.hauteur)
        self.position_docteur = []
        self.daleks = []
        self.positions_daleks = []
        self.ferrailles = []
        self.positions_ferrailles = []
        self.actions_menu_jeu = {
            "q": self.deplacer_docteur,
            "w": self.deplacer_docteur,
            "e": self.deplacer_docteur,
            "a": self.deplacer_docteur,
            "s": self.deplacer_docteur,
            "d": self.deplacer_docteur,
            "z": self.deplacer_docteur,
            "x": self.deplacer_docteur,
            "c": self.deplacer_docteur,
            "t": self.teleporter,
            "y": self.zapper
        }
        self.creer_niveau()

    def creer_niveau(self):
        self.niveau += 1
        nbr_daleks = self.niveau * self.nbr_daleks_par_niveau
        self.trouver_positions_occupees()
        while nbr_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x, y] not in self.position_docteur and [x, y] not in self.positions_daleks:
                self.positions_daleks.append([x, y])
                self.daleks.append(Dalek([x, y]))
                nbr_daleks -= 1

    def changer_niveau(self):
        self.ferrailles = []
        self.positions_ferrailles = []
        self.creer_niveau()
        print(str(self.daleks))

    def trouver_positions_occupees(self):
        self.position_docteur = []
        self.positions_daleks = []
        position = [self.docteur.x, self.docteur.y]
        self.position_docteur.append(position)
        for i in self.daleks:
            position = [i.x, i.y]
            self.positions_daleks.append(position)

    def deplacer_docteur(self, touche):
        nouveau_x = self.docteur.x
        nouveau_y = self.docteur.y
        if touche == "q":
            nouveau_x -= 1
            nouveau_y -= 1
        if touche == "w":
            nouveau_y -= 1
        if touche == "e":
            nouveau_x += 1
            nouveau_y -= 1
        if touche == "a":
            nouveau_x -= 1
        if touche == "d":
            nouveau_x += 1
        if touche == "z":
            nouveau_x -= 1
            nouveau_y += 1
        if touche == "x":
            nouveau_y += 1
        if touche == "c":
            nouveau_x += 1
            nouveau_y += 1
        if 0 <= nouveau_x < self.largeur and 0 <= nouveau_y < self.hauteur:
            nouvelles_coordonnees = [nouveau_x, nouveau_y]
            if nouvelles_coordonnees not in self.positions_daleks:
                if nouvelles_coordonnees not in self.positions_ferrailles:
                    self.docteur.x = nouveau_x
                    self.docteur.y = nouveau_y
                    return True
        else:
            return False

    def teleporter(self):
        nouveau_x = self.docteur.x
        nouveau_y = self.docteur.y
        a_verifier = True
        est_valide = True
        while a_verifier:
            nouveau_x = random.randrange(self.largeur)
            nouveau_y = random.randrange(self.hauteur)
            if self.teleportation == 1:
                for coordonnees_dalek in self.positions_daleks:
                    for coordonees in range(coordonnees_dalek[1] - 1, coordonnees_dalek[1] + 2):
                        for j in range(coordonnees_dalek[0] - 1, coordonnees_dalek[0] + 2):
                            if [nouveau_y, nouveau_x] == [coordonees, j]:
                                est_valide = False
                                break
                            else:
                                est_valide = True
                        if not est_valide:
                            break
                    if not est_valide:
                        break
            elif self.teleportation == 2:
                for coordonees in self.positions_daleks:
                    if [nouveau_x, nouveau_y] == [coordonees[0], coordonees[1]]:
                        est_valide = False
                        break
            if [nouveau_x, nouveau_y] in self.positions_ferrailles:
                est_valide = False
            if est_valide:
                a_verifier = False
        self.docteur.x = nouveau_x
        self.docteur.y = nouveau_y
        return True

    def zapper(self):
        if self.nbr_zappeurs > 0:
            for i in range(self.docteur.y - 1, self.docteur.y + 2):
                for j in range(self.docteur.x - 1, self.docteur.x + 2):
                    print(i, j)
                    for dalek in self.daleks:
                        if dalek.y == i and dalek.x == j:
                            dalek.est_mort = True
            self.retirer_daleks_morts()
            self.nbr_zappeurs -= 1
            return True
        else:
            return False

    def deplacer_dalek(self, dalek):
        if not dalek.est_mort:
            if dalek.x < self.docteur.x:
                if dalek.y < self.docteur.y:
                    dalek.x += 1
                    dalek.y += 1
                elif dalek.y == self.docteur.y:
                    dalek.x += 1
                else:
                    dalek.x += 1
                    dalek.y -= 1
            elif dalek.x == self.docteur.x:
                if dalek.y < self.docteur.y:
                    dalek.y += 1
                else:
                    dalek.y -= 1
            else:
                if dalek.y < self.docteur.y:
                    dalek.x -= 1
                    dalek.y += 1
                elif dalek.y == self.docteur.y:
                    dalek.x -= 1
                else:
                    dalek.x -= 1
                    dalek.y -= 1

    def verifier_collision(self, dalek):
        if [dalek.x, dalek.y] in self.positions_daleks:
            position_collision = [dalek.x, dalek.y]
            for i in self.daleks:
                if [i.x, i.y] == position_collision:
                    i.est_mort = True
            self.ajouter_ferraille(position_collision)

    def ajouter_ferraille(self, valeurs):
        self.ferrailles.append(Ferraille(valeurs))
        self.positions_ferrailles.append(valeurs)

    def verifier_mort_par_ferraille(self, dalek):
        if [dalek.x, dalek.y] in self.positions_ferrailles:
            dalek.est_mort = True

    def verifier_attaque(self, dalek):
        if [dalek.x, dalek.y] in self.position_docteur:
            return True
        else:
            return False

    def retirer_daleks_morts(self):
        daleks_morts = []
        for i in self.daleks:
            if i.est_mort:
                daleks_morts.append(i)
        for i in reversed(daleks_morts):
            self.daleks.remove(i)
            self.score += 5
