## - Encoding: UTF-8 -*-

import ast

import json
import random
from helper import Helper
from RTS_divers import *
import math
import time


class SiteConstruction():
    def __init__(self, parent, id, x, y, sorte):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.etat = "attente"
        self.sorte = sorte
        self.delai = Partie.valeurs[self.sorte]["delai"]
        self.size = 0

    def decremente_delai(self):
        self.delai -= 1


class Batiment():
    def __init__(self, parent, id, x, y):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.hp = 20
        self.image = None
        self.montype = None
        self.maxperso = 0
        self.perso = 0
        self.cartebatiment = []
        self.mana = 200

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort_batiment(self)
            return 1


class Usineballiste(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0
        self.size = 20

class Maison(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0
        self.size = 20


class Abri():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0
        self.size = 20


class Caserne():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0
        self.size = 20


class CelluleBlanche():
    def __init__(self, parent, id, x, y, notyperegion=-1, idregion=None):
        self.parent = parent
        self.id = id
        self.etat = "vivant"
        self.nomimg = "daim"
        self.montype = "daim"
        self.idregion = idregion
        self.img = ""
        self.x = x
        self.y = y
        self.hp = 1
        self.champvision = 200
        self.valeur = 40
        self.position_visee = None
        self.angle = None
        self.dir = "GB"
        self.img = self.nomimg + self.dir
        self.cibleennemi = None
        self.mana = 100
        self.force = 5
        self.vitesse = 3

    def mourir(self):
        self.etat = "mort"
        self.position_visee = None

    def deplacer(self):
        if self.position_visee:
            x = self.position_visee[0]
            y = self.position_visee[1]
            x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
            # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
            case = self.parent.trouver_case(x1, y1)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    self.cible=None
            # elif case[1]>self.parent.taillecarte or case[1]<0:
            #    self.cible=None
            # else:
            if case.montype != "plaine":
                pass
                # print("marche dans ",self.parent.regionstypes[self.parent.cartecase[case[1]][case[0]]])
            # changer la vitesse tant qu'il est sur un terrain irregulier
            # FIN DE TEST POUR SURFACE MARCHEE
            self.x, self.y = x1, y1
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.cible = None
                self.position_visee = None
        else:
            if self.etat == "vivant":
                self.trouver_cible()

    def trouver_cible(self):
        n = 1
        while n:
            x = (random.randrange(100) - 50) + self.x
            y = (random.randrange(100) - 50) + self.y
            case = self.parent.trouver_case(x, y)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    continue
            # if case[1]>self.parent.taillecarte or case[1]<0:
            #    continue

            if case.montype == "plaine":
                self.position_visee = [x, y]
                n = 0
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"
        self.img = self.nomimg + self.dir


    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.attaquerennemi()
        else:
            self.cibleennemi()

    def attaquerennemi(self):
        rep = self.cibleennemi.recevoir_coup(self.force)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.trouverennemi()

    def trouverennemi(self):

        for i in self.parent.parent.joueurs:
           # if self.parent.parent.joueurs[]
            for j in self.parent.parent.joueurs[i].persos:
                for k in self.parent.parent.joueurs[i].persos[j]:
                    ennemi = self.parent.parent.joueurs[i].persos[j][k]
                    if self.id != ennemi.id:
                        distance = Helper.calcDistance(self.x, self.y, ennemi.x, ennemi.y)
                        if distance <= self.champvision:
                            self.cibleennemi = ennemi

        if self.cibleennemi:
            x = self.cibleennemi.x
            y = self.cibleennemi.y
            self.cibler(ennemi)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.attaquer(ennemi)
            else:
                self.deplacer()
        else:
            self.trouver_cible()


    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort(self)
            return 1

    def cibler_ennemi(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "attaquerennemi"

    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee = [self.cible.x, self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.image = self.image[:-1] + self.dir
        else:

            self.position_visee = None

    def testCollisionUnite(self, x1, y1):
        for i in self.parent.parent.joueurs:
            for j in self.parent.parent.joueurs[i].persos:
                for k in self.parent.parent.joueurs[i].persos[j]:
                    obj = self.parent.parent.joueurs[i].persos[j][k]
                    if len(self.parent.parent.joueurs[i].persos["ouvrier"]) > 1:
                        if self.id != obj.id:
                            if Helper.calcDistance(obj.x, obj.y, x1, y1) < obj.size:
                                return False


    def testCollisionBatiment(self, x1, y1):
        for i in self.parent.parent.joueurs:
            for j in self.parent.parent.joueurs[i].batiments:
                for k in self.parent.parent.joueurs[i].batiments[j]:
                    obj = self.parent.parent.joueurs[i].batiments[j][k]
                    if Helper.calcDistance(obj.x, obj.y, x1, y1) < obj.size:
                        return False



class Daim():
    def __init__(self, parent, id, x, y, notyperegion=-1, idregion=None):
        self.parent = parent
        self.id = id
        self.etat = "vivant"
        self.nomimg = "daim"
        self.montype = "daim"
        self.idregion = idregion
        self.img = ""
        self.x = x
        self.y = y
        self.hp = 1
        self.valeur = 40
        self.position_visee = None
        self.angle = None
        self.dir = "GB"
        self.img = self.nomimg + self.dir
        self.vitesse = random.randrange(3) + 3

    def mourir(self):
        self.etat = "mort"
        self.position_visee = None

    def deplacer(self):
        if self.position_visee:
            x = self.position_visee[0]
            y = self.position_visee[1]
            x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
            # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
            case = self.parent.trouver_case(x1, y1)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    self.cible=None
            # elif case[1]>self.parent.taillecarte or case[1]<0:
            #    self.cible=None
            # else:
            if case.montype != "plaine":
                pass
                # print("marche dans ",self.parent.regionstypes[self.parent.cartecase[case[1]][case[0]]])
            # changer la vitesse tant qu'il est sur un terrain irregulier
            # FIN DE TEST POUR SURFACE MARCHEE
            self.x, self.y = x1, y1
            dist = Helper.calcDistance(self.x, self.y, x, y)
            # dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.cible = None
                self.position_visee = None
        else:
            if self.etat == "vivant":
                self.trouver_cible()

    def trouver_cible(self):
        n = 1
        while n:
            x = (random.randrange(100) - 50) + self.x
            y = (random.randrange(100) - 50) + self.y
            case = self.parent.trouver_case(x, y)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    continue
            # if case[1]>self.parent.taillecarte or case[1]<0:
            #    continue

            if case.montype == "plaine":
                self.position_visee = [x, y]
                n = 0
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"
        self.img = self.nomimg + self.dir


class Biotope():
    def __init__(self, parent, id, monimg, x, y, montype, idregion=0, posid="0"):
        self.parent = parent
        self.id = id
        self.img = monimg
        self.x = x
        self.y = y
        self.montype = montype
        self.sprite = None
        self.spriteno = 0
        self.idregion = idregion
        self.idcaseregion = posid


class Beacon(Biotope):
    typeressource = ['beacon']

    def __init__(self, parent, id, monimg, x, y, montype, case):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, case)
        self.valeur = 100
        self.case = case
    #     n = random.randrange(50)
    #     if n == 6:
    #         self.spritelen = 12  # len(self.parent.parent.vue.gifs["poissons"])
    #         self.sprite = "beacon"
    #         self.spriteno = random.randrange(self.spritelen)
    #         self.valeur = 100
    #     else:
    #         self.valeur = 10
    #
    # def jouer_prochain_coup(self):  #beacongif
    #     if self.sprite:
    #         self.spriteno += 1
    #         if self.spriteno > self.spritelen - 1:
    #             self.spriteno = 0


class Organe(Biotope):
    typeressource = ['coeur','cerveau','poumon','reins','intestins','foie','estomac','oeil']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 100



# class Baie(Biotope):
#     typeressource = ['arbustebaiesgrand',
#                      'arbustebaiespetit',
#                      'arbustevert']
#
#     def __init__(self, parent, id, monimg, x, y, montype):
#         Biotope.__init__(self, parent, id, monimg, x, y, montype)
#         self.valeur = 30


# class Marais(Biotope):
#     typeressource = ['marais1',
#                      'marais2',
#                      'marais3']
#
#     def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
#         Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
#         self.valeur = 100


# class Eau(Biotope):
#     typeressource = ['eaugrand1',
#                      'eaugrand2',
#                      'eaugrand3',
#                      'eaujoncD',
#                      'eaujoncG',
#                      'eauquenouillesD',
#                      'eauquenouillesG',
#                      'eauquenouillesgrand',
#                      'eautourbillon',
#                      'eautroncs']
#
#     def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
#         Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
#         n = random.randrange(50) #beacongif
#         if n == 6:
#             self.spritelen = 6  # len(self.parent.parent.vue.gifs["poissons"])
#             self.sprite = "poissons"
#             self.spriteno = random.randrange(self.spritelen)
#             self.valeur = 100
#         else:
#             self.valeur = 10
#
#     def jouer_prochain_coup(self):
#         if self.sprite:
#             self.spriteno += 1
#             if self.spriteno > self.spritelen - 1:
#                 self.spriteno = 0



#
# class Roche(Biotope):
#     typeressource = ['roches1 grand',
#                      'roches1petit',
#                      'roches2grand',
#                      'roches2petit',
#                      'roches3grand',
#                      'roches3petit',
#                      'roches4grand',
#                      'roches4petit',
#                      'roches5grand']
#
#     def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
#         Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
#         self.valeur = 100


# class Arbre(Biotope):
#     typeressource = ['arbre0grand',
#                      'arbre0petit',
#                      'arbre1grand',
#                      'arbre2grand',
#                      'arbresapin0grand',
#                      'arbresapin0petit']
#
#     def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
#         Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
#         self.valeur = 30

class DNAObjet(Biotope):  # version physique du DNA pour les events entre autres
    typeressource = ['arbre0grand',
                     'arbre0petit',
                     'arbre1grand',
                     'arbre2grand',
                     'arbresapin0grand',
                     'arbresapin0petit']  # à changer

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 30


class Fleche():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.taille = 20
        self.force = 10
        self.proie = proie
        self.proiex = self.proie.x
        self.proiey = self.proie.y
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.proiex, self.proiey)
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

    def bouger(self):
        self.x, self.y, = Helper.getAngledPoint(self.ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, self.proie.x, self.proie.y)
        if dist <= self.taille:
            rep = self.cibleennemi.recevoircoup(self.force)
            return self


class Javelot():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.distance = 150
        self.taille = 20
        self.demitaille = 10
        self.proie = proie
        self.proiex = self.proie.x
        self.proiey = self.proie.y
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.proiex, self.proiey)
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

    def bouger(self):
        self.x, self.y, = Helper.getAngledPoint(self.ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, self.proie.x, self.proie.y)
        if dist <= self.demitaille:
            # tue daim
            self.parent.actioncourante = "ciblerressource"
            self.parent.javelots.remove(self)
            self.proie.hp -= 1
            if self.proie.hp <= 0:
                self.proie.mourir()
            # self.proie.mourir()
        else:
            dist = Helper.calcDistance(self.x, self.y, self.proiex, self.proiey)
            if dist < self.vitesse:
                self.parent.javelots.remove(self)
                self.parent.actioncourante = "ciblerproie"


class Perso():
    def __init__(self, parent, id, batiment, couleur, x, y, montype):
        self.parent = parent
        self.id = id
        self.actioncourante = None
        self.batimentmere = batiment
        self.dir = "D"
        self.image = couleur[0] + "_" + montype + self.dir
        self.x = x
        self.y = y
        self.movX = 0
        self.movY = 0
        self.montype = montype
        self.cible = None
        self.position_visee = None
        self.cibleennemi = None
        self.mana = 100
        self.force = 5
        self.champvision = 100
        self.vitesse = 5
        self.angle = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblerennemi": self.cibler_ennemi,
                                 "attaquerennemi": self.attaquerennemi,
                                 "retourbatimentmere": None,
                                 "bougerGroupe": self.bougerGroupe,
                                 "trouverennemi": self.trouverennemi,
                                 }

    def attaquer(self, ennemi):
        print("aaa")
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"

    def attaquerennemi(self):
        rep = self.cibleennemi.recevoir_coup(self.force)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.actioncourante = "trouverennemi"

    def trouverennemi(self):

        for i in self.parent.parent.joueurs:
            for j in self.parent.parent.joueurs[i].persos:
                for k in self.parent.parent.joueurs[i].persos[j]:
                    ennemi = self.parent.parent.joueurs[i].persos[j][k]
                    if self.id != ennemi.id:
                        distance = Helper.calcDistance(self.x, self.y, ennemi.x, ennemi.y)
                        if distance <= self.champvision:
                            self.cibleennemi = ennemi

        if self.cibleennemi:
            x = self.cibleennemi.x
            y = self.cibleennemi.y
            self.cibler(ennemi)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.actioncourante = "attaquerennemi"
            else:
                self.actioncourante = "ciblerennemi"
        else:
            self.actioncourante = None

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort(self)
            return 1

    def cibler_ennemi(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "attaquerennemi"

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def deplacer(self, pos):
        self.position_visee = pos
        self.actioncourante = "bouger"

    def deplacerGroupe(self, pos, len):
        self.position_visee = pos
        self.actioncourante = "bougerGroupe"
        self.movX = self.position_visee[0] + random.randrange(-15 + (-5 * len), 15 + (5 * len))
        self.movY = self.position_visee[1] + random.randrange(-15 + (-5 * len), 15 + (5 * len))

    def bougerGroupe(self):
        if self.position_visee:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le daim
            x = self.movX
            y = self.movY
            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            if self.testCollisionBatiment(x1, y1) != False:
                if self.testCollisionUnite(x1, y1) != False:
                    ######## FIN DE TEST POUR SURFACE MARCHEE
                    # si tout ba bien on continue avec la nouvelle valeur
                    self.x, self.y = x1, y1
                    # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
                    dist = Helper.calcDistance(self.x, self.y, x, y)
                    if dist <= self.vitesse:
                        if self.actioncourante == "bougerGroupe":
                            self.actioncourante = None
                        return "rendu"
                    else:
                        return dist
                else:
                    if self.actioncourante == "bougerGroupe":
                        self.actioncourante = None
                    return "rendu"
            else:
                if self.actioncourante == "bougerGroupe":
                    self.actioncourante = None
                return "rendu"

    def bouger(self):
        if self.position_visee:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le daim
            x = self.position_visee[0]
            y = self.position_visee[1]
            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            if self.testCollisionBatiment(x1, y1) != False:
                if self.testCollisionUnite(x1, y1) != False:
                    ######## FIN DE TEST POUR SURFACE MARCHEE
                    # si tout ba bien on continue avec la nouvelle valeur
                    self.x, self.y = x1, y1
                    # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
                    dist = Helper.calcDistance(self.x, self.y, x, y)
                    if dist <= self.vitesse:
                        if self.actioncourante == "bouger":
                            self.actioncourante = None
                        return "rendu"
                    else:
                        return dist
                else:
                    if self.actioncourante == "bouger":
                        self.actioncourante = None
                    return "rendu"
            else:
                if self.actioncourante == "bouger":
                    self.actioncourante = None
                return "rendu"

    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee = [self.cible.x, self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.image = self.image[:-1] + self.dir
        else:
            self.position_visee = None

    def test_etat_du_sol(self, x1, y1):
        ######## SINON TROUVER VOIE DE CONTOURNEMENT
        # ici oncalcule sur quelle case on circule
        casex = x1 / self.parent.parent.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.parent.taillecase
        if casey != int(casey):
            casey = int(casey) + 1
        #####AJOUTER TEST DE LIMITE
        case = self.parent.parent.trouver_case(x1, y1)
        #
        # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
        if case.montype != "plaine":

            # test pour être sur que de n'est 9 (9=batiment)
            if case.montype != "batiment":
                print("marche dans ", case.montype)
            else:
                print("marche dans batiment")
            return False
        else:
            return True


    def testCollisionUnite(self, x1, y1):
        for i in self.parent.parent.joueurs:
            for j in self.parent.parent.joueurs[i].persos:
                for k in self.parent.parent.joueurs[i].persos[j]:
                    obj = self.parent.parent.joueurs[i].persos[j][k]
                    if len(self.parent.parent.joueurs[i].persos["ouvrier"]) > 1:
                        if self.id != obj.id:
                            if Helper.calcDistance(obj.x, obj.y, x1, y1) < obj.size:
                                return False


    def testCollisionBatiment(self, x1, y1):
        for i in self.parent.parent.joueurs:
            for j in self.parent.parent.joueurs[i].batiments:
                for k in self.parent.parent.joueurs[i].batiments[j]:
                    obj = self.parent.parent.joueurs[i].batiments[j][k]
                    if Helper.calcDistance(obj.x, obj.y, x1, y1) < obj.size:
                        return False

class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20
        self.hp = 2
        self.size = 10  # nombre à ajuster

class Archer(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.hp = 2
        self.size = 2

class Druide(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.hp = 2
        self.size = 2


class Ballista(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "DH"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible = None
        self.angle = None
        self.distancefeumax = 30
        self.distancefeu = 30
        self.hp = 2
        self.size = 2
        self.fleches = []
        self.cibleennemi = None

        # self.nomimg="ballista"

    def cibler(self, pos):
        self.position_visee = pos

        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"

        self.image = self.image[:-2] + self.dir

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.distancefeu:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"

    def attaquerennemi(self):
        if self.delaifeu == 0:
            id = get_prochain_id()
            fleche = Fleche(self, id, self.ciblennemi)
            self.delaifeu = self.delaifeumax
        for i in self.fleches:
            rep = i.bouger()
        if rep:
            rep = self.cibleennemi.recevoir_coup(self.force)
            self.fleches.remove(rep)


class Ouvrier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.activite = None  # sedeplacer, cueillir, chasser, pecher, construire, reparer, attaquer, fuir, promener,explorer,chercher
        self.typeressource = None
        self.quota = 20
        self.hp = 2
        self.size = 5
        self.ramassage = 0
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = 200
        self.champchasse = 120
        self.javelots = []
        self.vitesse = 7
        self.etats_et_actions = {"bouger": self.bouger,
                                 "bougerGroupe": self.bougerGroupe,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerproie": self.cibler_proie,
                                 "ciblerennemi": self.cibler_ennemi,
                                 "attaquerennemi": self.attaquerennemi,
                                 "construirebatiment": self.construire_batiment,
                                 "ramasserressource": self.ramasser,
                                 "ciblerressource": self.cibler_ressource,
                                 "retourbatimentmere": self.retour_batiment_mere,
                                 "validerjavelot": self.valider_javelot,
                                 "trouverennemi": self.trouverennemi,
                                 }

    def chasser_ramasser(self, objetcible, sontype, actiontype):
        self.cible = objetcible
        self.typeressource = sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "daim":
                    self.parent.ressources["sang"] += self.ramassage
                elif self.typeressource == "organe":
                    self.parent.ressources["matiere organique"] += self.ramassage
                self.ramassage = 0
                if self.cible.valeur < 1:
                    rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)           # a fixer
                    self.cibler(rep)
                if self.cible:
                    self.cibler(self.cible)
                    if self.cible.montype == "daim":
                        self.actioncourante = "ciblerproie"
                    else:
                        self.actioncourante = "ciblerressource"
                else:
                    self.actioncourante = None
        else:
            pass

    def cibler_ressource(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "ramasserressource"

    def cibler_ennemi(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "attaquerennemi"

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        if reponse == "rendu":
            if self.typeressource == "daim":
                self.actioncourante = "ramasserressource"
        elif reponse <= self.champchasse and self.cible.etat == "vivant":
            self.actioncourante = "validerjavelot"

    def valider_javelot(self):
        self.lancer_javelot(self.cible)
        for i in self.javelots:
            i.bouger()

    def ramasser(self):
        self.ramassage += 1
        self.cible.valeur -= 1
        if self.cible.valeur == 0 or self.ramassage == self.quota:
            self.actioncourante = "retourbatimentmere"
            self.position_visee = [self.batimentmere.x, self.batimentmere.y]
            if self.cible.valeur == 0:
                self.parent.avertir_ressource_mort(self.typeressource, self.cible)
                # rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                # if rep:
                #     if self.id != rep.id:
                #         self.cible=rep
        else:
            self.x = self.x + random.randrange(4) - 2
            self.y = self.y + random.randrange(4) - 2

    def construire_batiment(self):
        self.cible.decremente_delai()
        if self.cible.delai < 1:
            #test pour multiouvrier de construction
            if self.cible.id in self.parent.batiments['siteconstruction'].keys():

                batiment = self.parent.parent.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                                 self.cible.x, self.cible.y,
                                                                                 self.cible.sorte)
                self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

                sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)
                print(sitecons)
                self.parent.installer_batiment(batiment)

                # if batiment.montype == "watchtower":
                #     nouveau_territoire = self.parent.parent.aggrandir_territoire_watchtower(self.cible.x, self.cible.y)
                # else:
                #     nouveau_territoire = self.parent.parent.aggrandir_territoire(self.cible.x, self.cible.y)

                nouveau_territoire = self.parent.parent.aggrandir_territoire(self.cible.x, self.cible.y, batiment.montype, self.parent.couleur[1])

                # territoire_a_dessiner = []

                for i in nouveau_territoire:
                    if i not in self.parent.territoire:
                        self.parent.territoire.append(i)
                        # territoire_a_dessiner.append(i)

                self.parent.parent.calculer_supply()
                # self.parent.parent.parent.afficher_territoire(territoire_a_dessiner)
                self.parent.parent.parent.afficher_territoire(nouveau_territoire, self.parent.couleur[1])


                self.x = self.cible.x + 20
                self.y = self.cible.y - 20

            #mise a jour des ouvriers
            if self.cible.sorte == "maison":
                batiment = self.parent.batiments[self.cible.sorte][self.cible.id]
                self.batimentmere = batiment
            self.cible = None
            self.actioncourante = None

    def construire_site_construction(self, site_construction):
        self.cibler(site_construction)
        self.actioncourante = "ciblersiteconstruction"
        # pass #monte le batiment par etapes on pourrait montrer l'anavancement de la construciton

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def lancer_javelot(self, proie):
        if self.javelots == []:
            id = get_prochain_id()
            self.javelots.append(Javelot(self, id, proie))

    def chercher_nouvelle_ressource(self, typ, idreg):
        print("Je cherche nouvelle ressource")
        if typ != "daim" and typ != "organe":  # and typ != "baie"
            reg = self.parent.parent.regions[typ]
            if idreg in reg:
                regspec = self.parent.parent.regions[typ][idreg]
                n = len(regspec.dicocases)
                while n > 0:
                    clecase = list(regspec.dicocases.keys())
                    case = regspec.dicocases[random.choice(clecase)]
                    n -= 1
                    if case.ressources:
                        clecase2 = list(case.ressources.keys())
                        newress = case.ressources[random.choice(clecase2)]
                        if newress.montype == typ:
                            return newress
                return None
        else:
            nb = len(self.parent.parent.biotopes[typ])
            for i in range(nb):
                rep = random.choice(list(self.parent.parent.biotopes[typ].keys()))
                obj = self.parent.parent.biotopes[typ][rep]
                if obj != self.cible:
                    distance = Helper.calcDistance(self.x, self.y, obj.x, obj.y)
                    if distance <= self.champvision:
                        return obj
            return None

    # def deplacer(self,pos):
    #     self.position_visee = pos
    #     self.actioncourante = "bouger"
    #
    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.test_etat_du_sol(x1, y1)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         self.x, self.y = x1, y1
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #         if dist <= self.vitesse:
    #             if self.actioncourante=="bouger":
    #                 self.actioncourante=None
    #             return "rendu"
    #         else:
    #             return dist

    # def test_etat_du_sol(self,x1, y1):
    #     ######## SINON TROUVER VOIE DE CONTOURNEMENT
    #     # ici oncalcule sur quelle case on circule
    #     casex = x1 / self.parent.parent.taillecase
    #     if casex != int(casex):
    #         casex = int(casex) + 1
    #     casey = y1 / self.parent.parent.taillecase
    #     if casey != int(casey):
    #         casey = int(casey) + 1
    #     #####AJOUTER TEST DE LIMITE
    #     # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
    #     if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "plaine":
    #         # test pour être sur que de n'est 9 (9=batiment)
    #         if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "batiment":
    #             print("marche dans ", )
    #         else:
    #             print("marche dans batiment")

    def abandonner_ressource(self, ressource):
        if ressource == self.cible:
            if self.actioncourante == "ciblerressource" or self.actioncourante == "retourbatimentmere" or self.actioncourante == "ramasserresource":
                self.actioncourante = "retourbatimentmere"
            else:
                self.actioncourante = "retourbatimentmere"
                self.position_visee = [self.batimentmere.x, self.batimentmere.y]

    ## PAS UTILISER POUR LE MOMENT          
    def scanner_alentour(self):
        dicojoueurs = self.parent.parent.joueurs
        for i in dicojoueurs.values():
            for j in i.ouvriers.values():
                if j != self:
                    if Helper.calcDistance(self.x, self.y, j.x, j.y) <= self.champvision:
                        pass
        return 0

    # def trouver_cible(self, joueurs):
    #     c = None
    #     while c == None:
    #         listeclesj = list(joueurs.keys())
    #         c = random.choice(listeclesj)
    #         if joueurs[c].nom != self.parent.nom:
    #             listeclesm = list(joueurs[c].maisons.keys())
    #             maisoncible = random.choice(listeclesm)
    #             self.cible = joueurs[c].maisons[maisoncible]
    #         else:
    #             c = None
    #     self.angle = Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

class NPC1(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20
        self.hp = 2
        self.size = 10
        self.supply_cost = 10
        self.delai_action = 40
        self.delai_action_max = 40
        self.image = "npc"


    def deplacer(self):
        if self.position_visee:
            x = self.position_visee[0]
            y = self.position_visee[1]
            x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
            # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
            case = self.parent.trouver_case(x1, y1)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    self.cible=None
            # elif case[1]>self.parent.taillecarte or case[1]<0:
            #    self.cible=None
            # else:
            if case.montype != "plaine":
                pass
                # print("marche dans ",self.parent.regionstypes[self.parent.cartecase[case[1]][case[0]]])
            # changer la vitesse tant qu'il est sur un terrain irregulier
            # FIN DE TEST POUR SURFACE MARCHEE
            self.x, self.y = x1, y1
            dist = Helper.calcDistance(self.x, self.y, x, y)
            # dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.cible = None
                self.position_visee = None
        else:
            self.trouver_cible()

    def trouver_cible(self):
        n = 1
        while n:
            x = (random.randrange(100) - 50) + self.x
            y = (random.randrange(100) - 50) + self.y
            case = self.parent.trouver_case(x, y)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    continue
            # if case[1]>self.parent.taillecarte or case[1]<0:
            #    continue

            if case.montype == "plaine":
                self.position_visee = [x, y]
                n = 0
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])

    def trouverennemi(self):

        for i in self.parent.joueurs:
            for j in self.parent.joueurs[i].persos:
                for k in self.parent.joueurs[i].persos[j]:
                    ennemi = self.parent.joueurs[i].persos[j][k]
                    if self.id != ennemi.id:
                        distance = Helper.calcDistance(self.x, self.y, ennemi.x, ennemi.y)
                        if distance <= self.champvision:
                            self.cibleennemi = ennemi

        if self.cibleennemi:
            x = self.cibleennemi.x
            y = self.cibleennemi.y
            self.cibler(ennemi)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.actioncourante = "attaquerennemi"
            else:
                self.actioncourante = "ciblerennemi"
        else:
            self.actioncourante = None

    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee = [self.cible.x, self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
        else:
            self.position_visee = None


class Region():
    def __init__(self, parent, id, x, y, taillex, tailley, montype):
        self.parent = parent
        self.id = id
        self.debutx = x
        self.taillex = taillex
        self.debuty = y
        self.tailley = tailley
        self.montype = montype
        self.dicocases = {}


class Caseregion():
    def __init__(self, parent, id, x, y):
        self.parent = parent
        self.id = id
        self.montype = "plaine"
        self.ressources = {}
        self.x = x
        self.y = y


class Joueur():
    classespersos = {"ouvrier": Ouvrier,
                     "soldat": Soldat,
                     "archer": Archer,
                     "druide": Druide,
                     "ballista": Ballista
                     }
    ressources = {"Azteque": {"sang": 999,
                              "matiere organique": 200},
                  "Congolaise": {"sang": 10,
                                 "matiere organique": 200},
                  }

    def __init__(self, parent, id, nom, couleur, x, y):
        self.parent = parent
        self.nom = nom
        self.id = id
        self.x = x
        self.y = y
        self.couleur = couleur
        self.monchat = []
        self.chatneuf = 0
        self.territoire = []
        self.total_supply = 0
        self.current_supply = 0
        self.ressourcemorte = []
        self.ressources = {"sang": 200,
                           "matiere organique": 200,
                           "DNA": 50,
                           "Supply": self.total_supply - self.current_supply,}
        self.persos = {"ouvrier": {},
                       "soldat": {},
                       "archer": {},
                       "chevalier": {},
                       "druide": {},
                       "ingenieur": {},
                       "ballista": {}}

        self.batiments = {"maison": {},
                          "watchtower": {},
                          "barracks": {},
                          "turrets": {},
                          "siteconstruction": {}}

        # self.batiments = {"maison": {},
        #                   "lymphocyte": {},
        #                   "monocyte": {},
        #                   "neutrophil": {},
        #                   "siteconstruction": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "deplacerGroupe": self.deplacerGroupe,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner}

        self.skilltree = {"skill1": 0,
                          "skill2": 0,
                          "skill3": 0}
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)

    def get_stats(self):
        total = 0
        for i in self.persos:
            total += len(self.persos[i])
        for i in self.batiments:
            total += len(self.batiments[i])
        return total

    def annoncer_mort(self, perso):
        self.persos[perso.montype].pop(perso.id)

    def annoncer_mort_batiment(self, perso):
        self.batiments[perso.montype].pop(perso.id)

    def attaquer(self, param):
        attaquants, attaque = param
        nomjoueur, idperso, sorte = attaque


        ennemi = None
        # ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
        if idperso in self.parent.joueurs[nomjoueur].persos[sorte].keys():
            ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]

        if sorte in self.parent.NPCs.keys():             #a fixer
            ennemi = self.parent.NPCs[sorte][idperso]


        # elif sorte in self.parent.joueurs[nomjoueur].persos.keys():
        #     ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
        #     if idperso in attaque:



        elif sorte in self.parent.joueurs[nomjoueur].batiments.keys():
            ennemi = self.parent.joueurs[nomjoueur].batiments[sorte][idperso]



        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)


    def movAttaque(self, param):
        attaquants, attaque = param
        nomjoueur, idperso, sorte = attaque
        ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]


        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)

    def abandonner(self, param):
        # ajouter parametre nom de l'Abandonneux, et si c'est moi, envoyer une action
        # quitter au serveur et faire destroy
        msg = param[0]
        self.parent.montrer_msg_general(msg)

    def chatter(self, param):
        txt, envoyeur, receveur = param
        self.parent.joueurs[envoyeur].monchat.append(txt)
        self.parent.joueurs[receveur].monchat.append(txt)
        self.parent.joueurs[envoyeur].chatneuf = 1
        self.parent.joueurs[receveur].chatneuf = 1

    def avertir_ressource_mort(self, type, ress):
        for i in self.persos["ouvrier"]:
            self.persos["ouvrier"][i].abandonner_ressource(ress)  # ajouer libereressource
        self.parent.eliminer_ressource(type, ress)

    def chasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def deplacerGroupe(self, param):
        pos, troupe, len = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacerGroupe(pos, len)

    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        self.batiments["maison"][idmaison] = Maison(self, idmaison, self.couleur, x, y, "maison")

    def construire_batiment(self, param):
        perso, sorte, pos = param

        # payer batiment

        case = self.parent.cartecase[int(param[2][1] / 20)][int(param[2][0] / 20)]

        if case in self.territoire:
            id = get_prochain_id()
            vals = Partie.valeurs
            for k, val in self.ressources.items():
                self.ressources[k] = val - vals[sorte][k]

            siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte)
            self.batiments["siteconstruction"][id] = siteconstruction
            for i in perso:
                self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
                # self.persos["ouvrier"][i].construire_batiment(siteconstruction)

        else:
            print("Doit construire les nouveaux batiments à l'intérieur de son territoire")

    def installer_batiment(self, batiment):
        # self.batiments['siteconstruction'].pop(batiment.id)
        self.parent.installer_batiment(self.nom, batiment, self.territoire)

    # transmet à tous ses persos de jouer
    def jouer_prochain_coup(self):
        for j in self.persos.keys():
            for i in self.persos[j].keys():
                self.persos[j][i].jouer_prochain_coup()
        # gestion des site des construction
        # sitesmorts = []
        # for i in self.batiments["siteconstruction"]:
        #     site = self.batiments["siteconstruction"][i].jouer_prochain_coup()
        #     if site:
        #         sitesmorts.append(site)
        # for i in sitesmorts:
        #     self.batiments['siteconstruction'].pop(i.id)

    def creer_perso(self, param):
        sorteperso, batimentsource, idbatiment, pos = param

        vals = Partie.valeurs
        for k, val in self.ressources.items():
            if k != "Supply":
                self.ressources[k] = val - vals[sorteperso][k]


        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]

        x = batiment.x + 100 + (random.randrange(50) - 15)
        y = batiment.y + (random.randrange(50) - 15)

        self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                       sorteperso)
        # self.parent.calculer_current_supply()
        self.parent.calculer_supply()

#######################  LE MODELE est la partie #######################
class Partie:
    valeurs = {
        ### CRAFTING COSTS BATIMENTS
        "maison": {"sang": 10,
                          "matiere organique": 20,
                          "DNA": 0,
                          "Supply": 0,
                          "delai": 50},
        "watchtower": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 0,
                          "delai": 30},
        "barracks": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 0,
                          "delai": 60},
        "turrets": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 0,
                          "delai": 80},

        ### CRAFTING COSTS UNITS
        "soldat": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 10,
                          "delai": 50},
        "archer": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 10,
                          "delai": 50},
        "druide": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 10,
                          "delai": 50},
        "ballista": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 10,
                          "delai": 50},
        "ouvrier": {"sang": 10,
                          "matiere organique": 10,
                          "DNA": 0,
                          "Supply": 10,
                          "delai": 50},
        }

    def __init__(self, parent, mondict):
        self.parent = parent
        self.actionsafaire = {}
        self.debut = int(time.time())
        self.aireX = 4000
        self.aireX = 4000
        self.aireY = 4000
        # Decoupage de la surface
        self.taillecase = 20
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()
        self.NPCs = {"NPC1": {}}

        self.delaiprochaineaction = 20

        self.joueurs = {}
        ###  reference vers les classes appropriées
        # self.classesbatiments = {"maison": Maison,
        #                          "caserne": Caserne,
        #                          "abri": Abri,
        #                          "usineballiste": Usineballiste}

        self.classesbatiments = {"maison": Maison,
                                 "watchtower": Caserne,
                                 "barracks": Abri,
                                 "turrets": Usineballiste}

        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat,
                              "archer": Archer,
                              "druide": Druide,
                              "NPC1": NPC1}
        self.ressourcemorte = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.biotopes = {"daim": {},
                         "beacon": {},
                         "organe": {}
                         }

        self.evenements = {"spawnNPC": self.creer_NPC,
                           "spawnOrgane": self.produire_organe
                           }
        self.evenementsActif = False
        self.delaiEvenement = 0

        self.regions = {}
        # self.regionstypes = [["arbre", 50, 20, 5, "forest green"],
        #                      # ["eau", 10, 20, 12, "light blue"],
        #                      # ["marais", 3, 8, 8, "DarkSeaGreen3"],
        #                      # ["roche", 8, 3, 6, "gray60"],
        #                      ["aureus", 12, 3, 4, "gold2"],]
        # self.creer_regions()
        self.creer_biotopes()
        self.creer_population(mondict)
        self.produire_beacon()

    def calc_stats(self):
        total = 0
        for i in self.joueurs:
            total += self.joueurs[i].get_stats()
        for i in self.biotopes:
            total += len(self.biotopes[i])
        self.montrer_msg_general(str(total))

    def trouver_valeurs(self):
        vals = Partie.valeurs
        return vals

    def montrer_msg_general(self, txt):
        self.msggeneral = txt

    def installer_batiment(self, nomjoueur, batiment, territoire):
        x1, y1, x2, y2 = self.parent.installer_batiment(nomjoueur, batiment, territoire)

        cartebatiment = self.get_carte_bbox(x1, y1, x2, y2)
        for i in cartebatiment:
            self.cartecase[i[1]][i[0]].montype = "batiment"
        batiment.cartebatiment = cartebatiment

    def creer_biotopes(self):
        # creer des daims éparpillés
        n = 20
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                mondaim = Daim(self, id, x, y)
                self.biotopes["daim"][id] = mondaim
                self.listebiotopes.append(mondaim)
                n -= 1

    def creer_biotope(self, region, ressource, typeclasse):  # creation des forets
        typeressource = typeclasse.typeressource

        for cleregion in self.regions[region].keys():
            listecases = self.regions[region][cleregion].dicocases
            # for listecase in self.regions[region]:
            # nressource = random.randrange(int(len(listecases) / 3)) + int((len(listecases) / 5))
            nressource = int((random.randrange(len(listecases)) / 3) + 1)
            while nressource:
                cases = list(listecases.keys())
                pos = listecases[random.choice(cases)]
                # pos=random.choice(listecases)
                x = random.randrange(self.taillecase)
                y = random.randrange(self.taillecase)
                xa = (pos.x * self.taillecase) + x
                ya = (pos.y * self.taillecase) + y

                styleress = random.choice(typeressource)
                id = get_prochain_id()
                objet = typeclasse(self, id, styleress, xa, ya, ressource, cleregion, pos.id)
                pos.ressources[id] = objet
                self.biotopes[ressource][id] = (objet)
                self.listebiotopes.append(objet)
                nressource -= 1

    # def creer_regions(self):
    #     for reg in self.regionstypes:
    #         nomregion = reg[0]
    #         nbrreg = reg[1]
    #         minreg = reg[2]
    #         rndreg = reg[3]
    #         coulreg = reg[4]
    #         self.regions[nomregion] = {}
    #         for i in range(nbrreg):
    #             listecasereg = []
    #             # trouve une case dans la carte
    #             x = random.randrange(self.taillecarte)
    #             y = random.randrange(self.taillecarte)
    #             # calcule la largeur (x) et hauteur(y) de la regtion
    #             taillex = random.randrange(reg[3]) + reg[2]
    #             tailley = random.randrange(reg[3]) + reg[2]
    #             # verifie que la region de deborde pas vers l'exterieur du jeu
    #             # (ex: si le centre de la region est case 1,1
    #             # et on la veut 10 case de large, cette region debuterait a la case -5, qui n'existe pas
    #             x0 = x - int(taillex / 2)
    #             if x0 < 0:
    #                 x0 = 0
    #
    #             x1 = x + int(taillex / 2)
    #             if x1 > self.taillecarte - 1:
    #                 x1 = self.taillecarte - 1
    #
    #             y0 = y - int(tailley / 2)
    #             if y0 < 0:
    #                 y0 = 0
    #
    #             y1 = y + int(tailley / 2)
    #             if y1 > self.taillecarte - 1:
    #                 y1 = self.taillecarte - 1
    #
    #             taillex = x1 - x0
    #             tailley = y1 - y0
    #
    #             id = get_prochain_id()
    #             newregion = Region(self, id, x0, y0, taillex, tailley, nomregion)
    #
    #             dicoreg = {}
    #             for i in range(tailley):
    #                 for j in range(taillex):
    #                     self.cartecase[y0 + i][x0 + j].parent = newregion
    #                     self.cartecase[y0 + i][x0 + j].montype = nomregion
    #                     # listereg.append(self.cartecase[y0+i][x0+j])
    #                     casereg = self.cartecase[y0 + i][x0 + j]
    #                     casereg.parent = newregion
    #                     dicoreg[casereg.id] = casereg
    #
    #             newregion.dicocases = dicoreg
    #             self.regions[nomregion][id] = newregion

    def creer_population(self, mondict):
        couleurs = [["R", "indianred"], ["B", "deepskyblue3"], ["J", "lightgoldenrod2"], ["V", "lightgreen"]]
        # couleurs = [["V", "virus"], ["F", "fungus"], ["W", "worm"], ["B", "bacteria"]]

        quadrantsspawn = [[[0, 0], [int(self.aireX * 0.20), int(self.aireY * 0.20)]],
                          [[int(self.aireX * 0.80), 0], [self.aireX, int(self.aireY * 0.20)]],
                          [[0, int(self.aireY * 0.80)], [int(self.aireX * 0.20), self.aireY]],
                          [[int(self.aireX * 0.80), int(self.aireY * 0.80)], [self.aireX, self.aireY]]]
        nquadspawn = 4

        bord = 175
        for i in mondict:
            id = get_prochain_id()
            coul = couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad = random.choice(range(nquadspawn))
            nquadspawn -= 1
            quad = quadrantsspawn.pop(choixquad)

            x = random.randrange(quad[0][0] + bord, quad[1][0] - bord)
            y = random.randrange(quad[0][1] + bord, quad[1][1] - bord)
            self.joueurs[i] = Joueur(self, id, i, coul, x, y)

        # quadrants = [[[0, 0], [int(self.aireX / 2), int(self.aireY / 2)]],
        #              [[int(self.aireX / 2), 0], [self.aireX, int(self.aireY / 2)]],
        #              [[0, int(self.aireY / 2)], [int(self.aireX / 2), self.aireY]],
        #              [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]],
        #              [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]]]
        #
        # nquad = 5
        # bord = 50
        # for i in mondict:
        #     id = get_prochain_id()
        #     coul = couleurs.pop()
        #     # placer les joueurs dans des quandrants differents
        #     choixquad = random.choice(range(nquad))
        #     nquad -= 1
        #     quad = quadrants.pop(choixquad)
        #
        #     n = 1
        #     while n:
        #         x = random.randrange(quad[0][0] + bord, quad[1][0] - bord)
        #         y = random.randrange(quad[0][1] + bord, quad[1][1] - bord)
        #         case = self.trouver_case(x, y)
        #         if case.montype == "plaine":
        #             self.joueurs[i] = Joueur(self, id, i, coul, x, y)
        #             n = 0


   ############################# ZONE EVENEMENTS #########################

    def creer_NPC(self, nbr):
        x = random.randrange(self.aireX)
        y = random.randrange(self.aireY)
        h = 0
        while nbr:
            x +=50
            if h == 10:
                y += 60
                x -= 500
                h = 0
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                sorte = "NPC1"
               # monNPC = NPC1(self, id, None, "red", x, y, "NPC")
               # monNPC.image = None
                self.NPCs[sorte][id] = self.classespersos[sorte](self, id, None, "red", x, y, sorte)
                self.NPCs[sorte][id].image = "npc"
                #self.NPCs.append(monNPC)
                nbr -= 1
                h+=1

    def deplacer(self):
        for i in self.joueurs:
            self.joueurs[i].deplacer()

    def jouer_prochain_coup(self, cadrecourant):
        self.ressourcemorte = []
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER 
        if cadrecourant in self.actionsafaire:
            for i in self.actionsafaire[cadrecourant]:
                print(i)
                self.joueurs[i[0]].actions[i[1]](i[2])
        ##################################################################

        # demander aux objets de s'activer
        for i in self.biotopes["daim"].keys():
            self.biotopes["daim"][i].deplacer()

        for i in self.NPCs["NPC1"].keys():
            self.NPCs["NPC1"][i].trouverennemi()
            if self.NPCs["NPC1"][i].actioncourante == None:                      #a fixer
                self.NPCs["NPC1"][i].deplacer()
          #  i.jouer_prochain_coup()

        # for i in self.biotopes["eau"].keys():
        #     self.biotopes["eau"][i].jouer_prochain_coup()

        # for i in self.biotopes["beacon"].keys(): #beacongif
        #     self.biotopes["beacon"][i].jouer_prochain_coup()

        # demander aux objets de s'activer
        for i in self.joueurs.keys():
            self.joueurs[i].jouer_prochain_coup()

        if self.msggeneral and "cadre" not in self.msggeneral:
            self.msggeneralcompteur += 1
            if self.msggeneralcompteur == self.msggeneraldelai:
                self.msggeneral = ""
                self.msggeneralcompteur = 0
        else:
            t = int(time.time())
            msg = "cadre: " + str(cadrecourant) + " - secs: " + str(t - self.debut)
            self.msggeneral = msg

        self.faire_action_partie()

    def faire_action_partie(self):

        if self.delaiprochaineaction % 60 == 0: #le reste
            self.produireDNA()

      #  if self.delaiEvenement % 180 == 0: #sert a donner un temp limite aux évenements
       #     self.evenementsActif = False
       #     self.NPCs.pop("NPC1")
       #     self.NPCs["NPC1"] = {}

        if self.delaiprochaineaction % 120 == 0:
            if len(self.biotopes["organe"].keys()) < 12:
                self.produire_organe()


        if self.delaiprochaineaction % 100 == 0: # EVENEMENTS
           # if self.evenementsActif == False:

            act = random.choice(list(self.evenements.keys()))
            if len(self.NPCs["NPC1"].keys()) < 21:
                if act == "spawnNPC":
                    action = self.evenements[act]
                    action(3)
                    self.evenementsActif = True
                # elif act == "spawnOrgane":
                #     action = self.evenements[act]
                #     action()
                #     self.evenementsActif = True

        if self.evenementsActif == True:
            self.delaiEvenement += 1
        self.delaiprochaineaction += 1

    # def produire_action(self):  #baies
    #     typeressource = Baie.typeressource
    #     n = 1
    #     while n:
    #         x = random.randrange(self.aireX)
    #         y = random.randrange(self.aireY)
    #         case = self.trouver_case(x, y)
    #         if case.montype == "plaine":
    #             id = get_prochain_id()
    #             img = random.choice(typeressource)
    #             baie = Baie(self, id, img, x, y, "baie")
    #             self.biotopes["baie"][id] = baie
    #             n -= 1
    #             self.parent.afficher_bio(baie)

    def produire_beacon(self):
        typeressource = Beacon.typeressource
        n = 12
        distraisonable = 600
        coords = []

        while n:
            x = random.randint(self.aireX / 5, self.aireX / 5 * 4)
            y = random.randint(self.aireX / 5, self.aireX / 5 * 4)

            distinvalide = 0

            for i in coords:
                dist = Helper.calcDistance(x, y, i[0], i[1])
                if dist < distraisonable:
                    distinvalide = 1
            if distinvalide == 0:
                coords.append([x, y])
                n -= 1

        img = random.choice(typeressource)

        for i in coords:
            case = self.trouver_case(i[0], i[1])
            id = get_prochain_id()
            beacon = Beacon(self, id, img, i[0], i[1], "beacon", case)
            self.biotopes["beacon"][id] = beacon
            self.parent.afficher_bio(beacon)

    def produire_organe(self):
        typeressource = Organe.typeressource

        distraisonable = 600
        position_trouvee = False

        while position_trouvee == False:

            x = random.randrange(self.aireX / 5 + 20, self.aireX / 5 * 4 - 20)
            y = random.randrange(20, self.aireY / 5 - 20)
            x1 = random.randrange(20, self.aireX / 5 - 20)
            y1 = random.randrange(self.aireY / 5 * 4 + 20, self.aireY - 20)
            x2 = random.randrange(self.aireX / 5 * 4 + 20, self.aireX - 20)
            y2 = random.randrange(self.aireY / 5 + 20, self.aireY / 5 * 4 - 20)

            rand = random.randrange(1, 5)

            if rand == 1:
                case = self.trouver_case(x, y)
            elif rand == 2:
                case = self.trouver_case(x1, y2)
            elif rand == 3:
                case = self.trouver_case(x2, y2)
            else:
                case = self.trouver_case(x, y1)

            distinvalide = 0

            if len(self.biotopes["organe"].keys()) > 0:
                for i in self.biotopes["organe"].keys():
                    j = self.biotopes["organe"][i]
                    dist = Helper.calcDistance(case.x * 20, case.y * 20, j.x, j.y)
                    if dist < distraisonable:
                        distinvalide = 1
                        break

            if distinvalide == 0:
                id = get_prochain_id()
                img = random.choice(typeressource)
                organe = Organe(self, id, img, case.x * 20, case.y * 20, "organe")
                self.biotopes["organe"][id] = organe
                self.parent.afficher_bio(organe)
                position_trouvee = True

    def produireDNA(self):
        for i in self.joueurs:
            self.joueurs[i].ressources["DNA"] += 1

    # def calculer_total_supply(self):
    #     for i in self.joueurs:
    #         self.joueurs[i].ressources["Supply"] = int(len(self.joueurs[i].territoire) / 10) - self.joueurs[i].current_supply
    #         self.joueurs[i].total_supply = int(len(self.joueurs[i].territoire) / 10)
    #
    # def calculer_current_supply(self):
    #     for i in self.joueurs:
    #         self.joueurs[i].current_supply = 0
    #         for j in self.joueurs[i].persos:
    #             # if j == "ouvrier":
    #             self.joueurs[i].current_supply += len(self.joueurs[i].persos[j]) * 10

    def calculer_supply(self):
        for i in self.joueurs:
            self.joueurs[i].total_supply = int(len(self.joueurs[i].territoire) / 10)
            self.joueurs[i].current_supply = 0
            for j in self.joueurs[i].persos:
                # if j == "ouvrier":
                self.joueurs[i].current_supply += len(self.joueurs[i].persos[j]) * 10
            self.joueurs[i].ressources["Supply"] = int(len(self.joueurs[i].territoire) / 10) - self.joueurs[i].current_supply


    # VERIFIER CES FONCTIONS SUR LA CARTECASE
    def make_carte_case(self):
        # NOTE: cette carte est carre
        taille = self.taillecarte
        self.cartecase = []
        for i in range(taille):
            t1 = []
            for j in range(taille):
                id = get_prochain_id()
                t1.append(Caseregion(None, id, j, i))
            self.cartecase.append(t1)

    def aggrandir_territoire(self, x, y, type, coul):

        territoire = []
        beacon_territoire = []

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > (self.aireX - 1):
            x = self.aireX - 1
        if y > (self.aireY - 1):
            y = self.aireY - 1

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        if cx != 0 and x % self.taillecase > 0:
            cx += 1

        if cy != 0 and y % self.taillecase > 0:
            cy += 1

        if cx == self.taillecarte:
            cx -= 1
        if cy == self.taillecarte:
            cy -= 1

        if type == "watchtower":
            for i in range(cx - 15, cx + 15):
                for j in range(cy - 15, cy + 15):

                    for k in self.biotopes["beacon"]:
                        case = self.biotopes["beacon"][k].case
                        if case.x == i and case.y == j:
                            print("beacon!")
                            for l in range(case.x - 20, case.x + 20):
                                for m in range(case.y - 20, case.y + 20):
                                    if self.cartecase[m][l] not in territoire:
                                        if 200 > m >= 0 and 200 > l >= 0:
                                            territoire.append(self.cartecase[m][l])
                                            beacon_territoire.append(self.cartecase[m][l])

                    if 200 > j >= 0 and 200 > i >= 0:
                        if self.cartecase[j][i] not in territoire:
                            territoire.append(self.cartecase[j][i])

        else:
            for i in range(cx - 10, cx + 10):
                for j in range(cy - 10, cy + 10):

                    for k in self.biotopes["beacon"]:
                        case = self.biotopes["beacon"][k].case
                        if case.x == i and case.y == j:
                            print("beacon!")
                            for l in range(case.x - 20, case.x + 20):
                                for m in range(case.y - 20, case.y + 20):
                                    if self.cartecase[m][l] not in territoire:
                                        if 200 > m >= 0 and 200 > l >= 0:
                                            territoire.append(self.cartecase[m][l])

                    if 200 > j >= 0 and 200 > i >= 0:
                        if self.cartecase[j][i] not in territoire:
                            territoire.append(self.cartecase[j][i])

        if beacon_territoire:
            self.parent.afficher_territoire(beacon_territoire, coul)

        return territoire

    # def radar_beacon(self, i, j, territoire):
    #     for k in self.biotopes["beacon"]:
    #         case = self.biotopes["beacon"][k].case
    #         if case.x == i and case.y == j:
    #             print("beacon!")
    #             for l in range(case.x - 20, case.x + 20):
    #                 for m in range(case.y - 20, case.y + 20):
    #                     if self.cartecase[m][l] not in territoire:
    #                         if 200 > m >= 0 and 200 > l >= 0:
    #                             territoire.append(self.cartecase[m][l])

    def territoire_initial(self, x, y, coul):
        cx = int(x/20)
        cy = int(y/20)
        for i in self.joueurs.keys():
            if coul != self.joueurs[i].couleur[1]:
                continue
            else:
                for j in range(cx - 10, cx + 10):
                    for k in range(cy - 10, cy + 10):
                        if 200 > j >= 0 and 200 > k >= 0:
                            self.joueurs[i].territoire.append(self.cartecase[k][j])
                self.parent.afficher_territoire(self.joueurs[i].territoire, coul)
                self.calculer_supply()

    def trouver_case(self, x, y):

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > (self.aireX - 1):
            x = self.aireX - 1
        if y > (self.aireY - 1):
            y = self.aireY - 1

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        if cx != 0 and x % self.taillecase > 0:
            cx += 1

        if cy != 0 and y % self.taillecase > 0:
            cy += 1

        # possible d'etre dans une case trop loin
        if cx == self.taillecarte:
            cx -= 1
        if cy == self.taillecarte:
            cy -= 1
        # print(self.cartecase[cy][cx])
        return self.cartecase[cy][cx]  # [cx,cy]

    def get_carte_bbox(self, x1, y1, x2, y2):  # case d'origine en cx et cy,  pour position pixels x, y
        # case d'origine en cx et cy,  pour position pixels x, y
        if x1 < 0:
            x1 = 1
        if y1 < 0:
            y1 = 1
        if x2 >= self.aireX:
            x2 = self.aireX - 1
        if y2 >= self.aireY:
            y2 = self.aireY - 1

        cx1 = int(x1 / self.taillecase)
        cy1 = int(y1 / self.taillecase)

        cx2 = int(x2 / self.taillecase)
        cy2 = int(y2 / self.taillecase)
        t1 = []
        for i in range(cy1, cy2):
            for j in range(cx1, cx2):
                case = self.cartecase[i][j]
                t1.append([j, i])
        return t1

    # CORRECTION REQUISE : PAS SUR QUE CETTE FONCITON SOIT ENCORE REQUISE
    # VA DEPENDRE DE L'IMPLANTATION S'IL Y A TROP D'OBJETS À VÉRIFIER
    def get_subcarte(self, x, y, d):

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        # possible d'etre dans une case trop loin
        if cx == self.largeurcase:
            cx -= 1
        if cy == self.hauteurcase:
            cy -= 1

        # le centre en pixels de la case d'origine
        pxcentrex = (cx * self.taillecase) + self.demicase
        pxcentrey = (cy * self.taillecase) + self.demicase

        # la case superieur gauche de la case d'origine
        casecoinx1 = cx - d
        casecoiny1 = cy - d
        # assure qu'on deborde pas
        if casecoinx1 < 0:
            casecoinx1 = 0
        if casecoiny1 < 0:
            casecoiny1 = 0
        # la case inferieur droite
        casecoinx2 = cx + d
        casecoiny2 = cy + d
        # assure qu'on deborde pas
        if casecoinx2 >= self.largeurcase:
            casecoinx2 = self.largeurcase - 1
        if casecoiny2 >= self.hauteurcase:
            casecoiny2 = self.hauteurcase - 1

        distmax = (d * self.taillecase) + self.demicase

        t1 = []
        for i in range(casecoiny1, casecoiny2):
            for j in range(casecoinx1, casecoinx2):
                case = self.carte[i][j]
                pxcentrecasex = (j * self.taillecase) + self.demicase
                pxcentrecasey = (i * self.taillecase) + self.demicase
                distcase = Helper.calcDistance(pxcentrex, pxcentrey, pxcentrecasex, pxcentrecasey)
                if distcase <= distmax:
                    t1.append(case)
        return t1

    def eliminer_ressource(self, type, ress):
        if ress.idregion:
            # self.regions[ress.montype][ress.idregion].listecases.pop(ress.id)
            cr = self.regions[ress.montype][ress.idregion].dicocases[ress.idcaseregion]
            if ress.id in cr.ressources.keys():
                cr.ressources.pop(ress.id)

        if ress.id in self.biotopes[type]:
            self.biotopes[type].pop(ress.id)
        if ress not in self.ressourcemorte:
            self.ressourcemorte.append(ress)

    #############################################################################    
    # ATTENTION : NE PAS TOUCHER                 
    def ajouter_actions_a_faire(self, actionsrecues):
        for i in actionsrecues:
            cadrecle = i[0]
            if (self.parent.cadrejeu - 1) > int(cadrecle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            action = ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle] = action
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
