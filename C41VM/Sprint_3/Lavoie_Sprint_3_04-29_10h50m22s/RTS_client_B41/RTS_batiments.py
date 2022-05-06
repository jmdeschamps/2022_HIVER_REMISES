import ast

import json
import random
from helper import Helper
from RTS_divers import *
import math
import time

from RTS_valeurs import valeurs


class SiteConstruction:
    def __init__(self, parent, id, x, y, sorte, case, perso):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.case = case
        self.sorte = sorte
        self.delai = valeurs[self.sorte]["delai"]
        self.or_par_seconde = 0
        self.constructeur = perso
        self.zone_controle = []

    def decremente_delai(self):
        self.delai -= 1


class Batiment:
    def __init__(self, parent, id, x, y, case):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.case = case
        self.caseinitiale = case.montype
        self.image = None
        self.montype = None
        # carte batiment n'est plus utiliser
        self.cartebatiment = []
        self.life = 200
        self.zone_controle = []
        self.or_par_seconde = 0

    def recevoir_coup(self, force):
        self.life -= force
        print("Ouch Batiment")
        if self.life < 1:
            print("MORTS")
            self.parent.annoncer_mort_batiment(self)
            return 1


class Scierie(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.foret_total = 0

        for x in range(case.x - 1, case.x + 2):
            for y in range(case.y - 1, case.y + 2):
                cpt_forret = self.parent.partie.cartecase[y][x]
                if cpt_forret is not case:
                    if cpt_forret.montype == "arbre":
                        self.foret_total += 1

        self.or_par_seconde = self.foret_total
        print("foret_total", self.foret_total)


class Pecherie(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.eau_total = 0

        for x in range(case.x - 1, case.x + 2):
            for y in range(case.y - 1, case.y + 2):
                cpt_eau = self.parent.partie.cartecase[y][x]
                if cpt_eau is not case:
                    if cpt_eau.montype == "eau":
                        self.eau_total += 1

        self.or_par_seconde = self.eau_total
        print("eau_total", self.eau_total)


class Mine(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.montange_total = 0

        for x in range(case.x - 1, case.x + 2):
            for y in range(case.y - 1, case.y + 2):
                cpt_montange = self.parent.partie.cartecase[y][x]
                if cpt_montange is not case:
                    if cpt_montange.montype == "roche":
                        self.montange_total += 1

        self.or_par_seconde = self.montange_total
        print("montange_total", self.montange_total)


class Village(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.delai_unite = 0

    def jouer_prochain_coup(self):
        if self.delai_unite > 0:
            self.decremente_delai()

    def decremente_delai(self):
        self.delai_unite -= 1
        if self.delai_unite <= 0:
            self.creer_unite()

    def creer_unite(self):
        id = get_prochain_id()
        x = self.x + (random.randrange(50) - 15)
        y = self.y + (random.randrange(50) - 15)
        self.parent.persos["ouvrier"][id] = self.parent.classespersos["ouvrier"](self.parent, id, self, self.parent.couleur, x, y,
                                                                       "ouvrier")


class Ferme(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.or_par_seconde = 1


class Caserne(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.delai_unite = 0

    def jouer_prochain_coup(self):
        if self.delai_unite > 0:
            self.decremente_delai()

    def decremente_delai(self):
        self.delai_unite -= 1
        if self.delai_unite <= 0:
            self.creer_unite()

    def creer_unite(self):
        id = get_prochain_id()
        x = self.x + (random.randrange(50) - 15)
        y = self.y + (random.randrange(50) - 15)
        self.parent.persos["soldat"][id] = self.parent.classespersos["soldat"](self.parent, id, self,
                                                                                 self.parent.couleur, x, y,
                                                                                 "soldat")




#Patrice: La classe de tour est une nouvelle classe. Tout le code a été volé de quelque part d'autre ou fait from scratch
class Tour(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.champ_de_vision = 288
        #self.life = 400
        self.fleches = []
        self.fleches_morts = []
        self.cible = None
        self.delai = 0

    def jouer_prochain_coup(self):
        cible_morte = 0
        if self.cible == None:
            self.scanner_alentour()
        elif self.delai == 0:
            dist = Helper.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
            if dist <= self.champ_de_vision:
                self.tirer()
            else:
                self.cible = None
        else:
            self.delai -= 1
        for fleche in self.fleches:
            touche = fleche.bouger()
            if touche:
                self.fleches_morts.append(fleche)
        for fleche in self.fleches_morts:
            self.fleches.remove(fleche)
        self.fleches_morts = []

    def retirer_cible(self):
        self.cible = None

    def scanner_alentour(self):
        dicojoueurs = self.parent.partie.joueurs
        for joueur in dicojoueurs.values():
            if joueur.nom != self.parent.nom:
                for soldat in joueur.persos["soldat"].values():
                    if Helper.calcDistance(self.x, self.y, soldat.x, soldat.y) <= self.champ_de_vision and self.cible == None:
                        self.cible = soldat
                for ouvrier in joueur.persos["ouvrier"].values():
                    if Helper.calcDistance(self.x, self.y, ouvrier.x, ouvrier.y) <= self.champ_de_vision and self.cible == None:
                        self.cible = ouvrier

    def tirer(self):
        id = get_prochain_id()
        self.fleches.append(Fleche(self, id, self.cible))
        self.delai = 25


class Fleche:
    # Patrice: Toutes références à la proie ont été remplacé par cible
    def __init__(self, parent, id, cible):
        self.parent = parent
        self.id = id
        self.vitesse = 35
        self.taille = 20
        self.force = 50
        self.cible = cible
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
        angquad = math.degrees(self.ang)
        dir = "DB"
        if 0 <= angquad <= 89:
            dir = "DB"
        elif -90 <= angquad <= -1:
            dir = "DH"
        if 90 <= angquad <= 179:
            dir = "GB"
        elif -180 <= angquad <= -91:
            dir = "GH"
        self.image = "javelot" + dir

    # Patrice: La fonction bouger n'était pas vraiment fonctionnelle, elle a dû être modifiée.
    def bouger(self):
        for i in range(self.vitesse):
            if self.x < self.cible.x:
                self.x += 1
            elif self.x > self.cible.x:
                self.x -= 1
            if self.y < self.cible.y:
                self.y += 1
            elif self.y > self.cible.y:
                self.y -= 1
            dist = Helper.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
            if dist <= self.taille:
                rep = self.cible.recevoir_coup(self.force)
                if rep:
                    self.parent.retirer_cible()
                return 1

