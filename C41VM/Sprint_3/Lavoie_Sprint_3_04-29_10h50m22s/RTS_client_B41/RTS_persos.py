import ast

import json
import random
from helper import Helper
from RTS_divers import *
import math
import time

from RTS_valeurs import valeurs
from navigation import *


class Perso:
    def __init__(self, parent, id, batiment, couleur, x, y, montype):
        self.parent = parent
        self.waypoint = []
        self.id = id
        self.actioncourante = None
        self.batimentmere = batiment
        self.dir = "D"
        self.couleur = couleur
        self.image = couleur[0] + "_" + montype # + self.dir
        self.annimation_queue = []
        self.x = x
        self.y = y
        self.montype = montype
        self.cible = None
        self.position_visee = None
        self.cibleennemi = None
        self.life = 100
        self.force = 5
        self.champvision = 100
        self.vitesse = 3
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "retourbatimentmere": None,
                                 }

    def recevoir_coup(self, force):
        self.life -= force
        print("Ouch")
        if self.life < 1:
            print("MORTS")
            self.parent.annoncer_mort(self)
            return 1

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def deplacer(self, pos):
        self.position_visee = pos
        case = self.parent.partie.trouver_case(self.x, self.y)
        self.waypoint = case.pathfinding(self.x, self.y, pos[0], pos[1])
        self.actioncourante = "bouger"

    def bouger(self):
        if self.position_visee:
            if len(self.waypoint) != 0:
                x, y = self.waypoint[0]
            else:
                x = self.position_visee[0]
                y = self.position_visee[1]

            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)

            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            self.test_etat_du_sol(x1, y1)
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            self.x, self.y = x1, y1
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                if len(self.waypoint) == 0:
                    if self.actioncourante == "bouger":
                        self.actioncourante = None
                    return "rendu"
                else:
                    self.waypoint.pop(0)
                    return dist
            else:
                return dist

    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee = [self.cible.x, self.cible.y]
            case = self.parent.partie.trouver_case(self.x, self.y)
            self.waypoint = case.pathfinding(self.x, self.y, self.cible.x, self.cible.y)
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            # self.image = self.image[:-1] + self.dir
        else:

            self.position_visee = None

    def test_etat_du_sol(self, x1, y1):
        ######## SINON TROUVER VOIE DE CONTOURNEMENT
        # ici oncalcule sur quelle case on circule
        casex = x1 / self.parent.partie.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.partie.taillecase
        if casey != int(casey):
            casey = int(casey) + 1
        #####AJOUTER TEST DE LIMITE
        case = self.parent.partie.trouver_case(x1, y1)
        #
        # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
        if case.montype != "plaine":
            # test pour être sur que de n'est 9 (9=batiment)
            if case.montype != "batiment":
                print("marche dans ", case.montype)
            else:
                print("marche dans batiment")

    def test_etat_du_sol1(self, x1, y1):
        ######## SINON TROUVER VOIE DE CONTOURNEMENT
        # ici oncalcule sur quelle case on circule
        casex = x1 / self.parent.controleur.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.controleur.taillecase
        if casey != int(casey):
            casey = int(casey) + 1
        #####AJOUTER TEST DE LIMITE
        # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
        if self.parent.controleur.cartecase[int(casey)][int(casex)].montype != "plaine":
            # test pour être sur que de n'est 9 (9=batiment)
            if self.parent.controleur.cartecase[int(casey)][int(casex)].montype != "batiment":
                print("marche dans ", )
            else:
                print("marche dans batiment")


class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20
        self.champvision = 288
        self.delai_attaque = 0
        self.desengager = False
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblerennemi": None,
                                 "attaquerennemi": self.attaquer_ennemi,
                                 "retourbatimentmere": None,
                                 "attaquer": self.attaquer,
                                 }
        self.vitesse = 20

    def jouer_prochain_coup(self):
        if self.cible == None:
            self.scanner_alentour()
        if self.cible and not self.desengager:
            self.actioncourante = "attaquer"
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def add_attaque_animation(self):
        animation = []
        for i in range(0, 3):
            img = f"{self.couleur[0]}_soldat_attack{i}"
            frame = {"img": img, "frame_rem": 2}
            animation.append(frame)

        self.annimation_queue.append(animation)

    def attaquer(self):
        x = self.cible.x
        y = self.cible.y
        ang = Helper.calcAngle(self.x, self.y, x, y)
        x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.attaquer_ennemi()
        else:
            self.x, self.y = x1, y1

    def attaquer_ennemi(self):
        if self.delai_attaque <= 0:
            rep = self.cible.recevoir_coup(self.force)
            self.add_attaque_animation()
            if rep == 1:
                self.cible = None

                self.actioncourante = None
            self.delai_attaque = 15
        self.delai_attaque -= 1

    def scanner_alentour(self):
        dicojoueurs = self.parent.partie.joueurs
        for joueur in dicojoueurs.values():
            if joueur.nom != self.parent.nom:
                for type_batiment in joueur.batiments.keys():
                    if type_batiment != "Tour" and type_batiment != "siteconstruction":
                        for batiment in joueur.batiments[type_batiment].values():
                            if Helper.calcDistance(self.x, self.y, batiment.x, batiment.y) <= self.champvision:
                                self.cibler(batiment)
                for ouvrier in joueur.persos["ouvrier"].values():
                    if ouvrier != self:
                        if Helper.calcDistance(self.x, self.y, ouvrier.x, ouvrier.y) <= self.champvision:
                            self.cibler(ouvrier)
                for tour in joueur.batiments["Tour"].values():
                    if Helper.calcDistance(self.x, self.y, tour.x, tour.y) <= self.champvision:
                        self.cibler(tour)
                for soldat in joueur.persos["soldat"].values():
                    if soldat != self:
                        if Helper.calcDistance(self.x, self.y, soldat.x, soldat.y) <= self.champvision:
                            self.cibler(soldat)

    def deplacer(self, pos):
        self.position_visee = pos
        case = self.parent.partie.trouver_case(self.x, self.y)
        self.waypoint = case.pathfinding(self.x, self.y, pos[0], pos[1])
        self.desengager = True
        self.actioncourante = "bouger"

    def bouger(self):
        if self.position_visee:
            if len(self.waypoint) != 0:
                x, y = self.waypoint[0]
            else:
                x = self.position_visee[0]
                y = self.position_visee[1]

            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)

            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            self.test_etat_du_sol(x1, y1)
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            self.x, self.y = x1, y1
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                if len(self.waypoint) == 0:
                    if self.actioncourante == "bouger":
                        self.desengager = False
                        self.cible = None
                        self.actioncourante = None
                    return "rendu"
                else:
                    self.waypoint.pop(0)
                    return dist
            else:
                return dist


class Ouvrier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.champvision = 400
        self.vitesse = 20
        self.occupe = False
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "construirebatiment": self.construire_batiment,
                                 "cibler_reparation": self.cibler_reparation,
                                 "effectuer_reparation": self.effectuer_reparation
                                 }

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def construire_batiment(self):
        self.cible.decremente_delai()
        if self.cible.delai <= 0:
            case = self.parent.partie.trouver_case(self.cible.x, self.cible.y)
            batiment = self.parent.partie.classesbatiments[self.cible.sorte](self.parent, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte, case)
            self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

            if batiment.id in self.parent.batiments['siteconstruction']:
                sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)
                print(sitecons)

            self.parent.installer_batiment(batiment)
            if self.cible.sorte == "Village":
                self.batimentmere = batiment
            self.cible = None
            self.actioncourante = None
            self.occupe = False

    def construire_site_construction(self, site_construction):
        self.occupe = True
        self.cibler(site_construction)
        self.actioncourante = "ciblersiteconstruction"
        # pass #monte le batiment par etapes on pourrait montrer l'avancement de la construciton

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def reparer_batiment(self, batiment, pos):
        self.cibler(batiment)
        self.actioncourante = "cibler_reparation"

    def cibler_reparation(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "effectuer_reparation"

    def effectuer_reparation(self):
        if self.cible.life < 200:
            self.cible.life += 1
        else:
            self.cible = None
            self.actioncourante = None


    ## PAS UTILISER POUR LE MOMENT
    def scanner_alentour(self):
        dicojoueurs = self.parent.controleur.joueurs
        for i in dicojoueurs.values():
            for j in i.ouvriers.values():
                if j != self:
                    if Helper.calcDistance(self.x, self.y, j.x, j.y) <= self.champvision:
                        pass
        return 0
