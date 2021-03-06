## - Encoding: UTF-8 -*-

import ast

import json
import random
from helper import Helper
from RTS_divers import *
import math
import time
from settings import *


class SiteConstruction():
    def __init__(self, parent, id, x, y, sorte):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.etat = "attente"
        self.sorte = sorte
        self.delai = Partie.valeurs[self.sorte]["delai"]

    def decremente_delai(self):
        self.delai -= 1


class Batiment():
    def __init__(self, parent, id, x, y):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.image = None
        self.montype = None
        self.maxperso = 0
        self.perso = 0
        self.cartebatiment = []
        self.mana = 200
        self.cooldown = None  # pour le faire respawn après qu'il soit mort
        self.etat = "vivant" # SS attaquer batiment

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort_batiment(self)
            return 1


class SoulFarm(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        # self.maxperso = 10
        # self.perso = 0
        self.nbr_soul = 0  # Yoan

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.etat = "detruit"
            print(self.etat)


class Porte(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0
        self.nbr_soul = 0  # Alex

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.etat = "mort"
            print(self.etat)


class RogueFactory():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class KidFactory():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class Humain():
    def __init__(self, parent, id, x, y, notyperegion=-1, idregion=None):
        self.parent = parent
        self.id = id
        self.etat = "vivant" ##dejamos
        self.nomimg = "humain"
        self.montype = "humain"
        self.idregion = idregion
        self.x = x
        self.y = y
        self.valeur = 2
        self.position_visee = None
        self.angle = None
        self.dir = "G"
        self.img = self.nomimg + self.dir
        self.vitesse = random.randrange(0, 3)
        self.cible = None  # ajout alex pour cible kidreaper
        self.etenduReaper = 500  # ajout alex pour cible kidreaper
        self.mort = False;
        self.typeCible = ""

    def mourir(self):
        self.etat = "mort"
        self.position_visee = None

    def deplacer(self):
        if self.etat == "mort":
            if not self.mort:
                self.parent.countHumain -= 1 ## ajout alex pour incrementation des daim
                ##self.parent.biotopes["humain"].pop(self.id)
                ##monhumain = Humain(self, self.id, self.x, self.y)
                ##self.parent.listebiotopes.remove(monhumain)
                self.mort = True
            self.cible = None
        elif self.cible:  # ajout alex
            self.position_visee = [self.cible.x, self.cible.y]
            self.angle = Helper.calcAngle(self.x + random.randrange(100, 200),
                                          self.y + random.randrange(100, 200),
                                          self.cible.x + random.randrange(100, 200),
                                          self.cible.y + random.randrange(100, 200)) # Alex pour que les humain gravite autour du kid

            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.img = self.nomimg + self.dir

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
                if self.cible: ##Alex pour garder le soldat en cible
                    return
                else:
                    self.cible = None
                    self.position_visee = None
        else:
            if self.etat == "vivant":
                if self.cible: ##Alex pour garder le soldat en cible
                    return
                else:
                    self.trouver_cible()

    def trouver_cible(self):  # Alex pour que le kid reaper attire les ames
        clefj = self.parent.joueurs.keys()
        for i in clefj:
            ListKD = self.parent.joueurs[i].persos["kidReaper"]
            for j in ListKD:
                j = self.parent.joueurs[i].persos["kidReaper"][j]
                dist = Helper.calcDistance(self.x, self.y, j.x, j.y)  # calculer distance relativement au kid reaper
                if dist < self.etenduReaper:
                    self.cible = j
                    return

        else:
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
            self.img = self.nomimg + self.dir



    ##code pour que les humain se sauve avec un bug de loop infini

    ##def jouerprochainCoup(self):
    ##    self.trouverReaperNuit()
    ##    self.deplacer()
    ##
    ##def trouverReaperNuit(self):
    ##    if not self.parent.daylight:
    ##        if self.typeCible != "reaper":
    ##            if self.typeCible != "kid":
    ##                cible = None
    ##                dist = 0
    ##                distProche = self.etenduReaper
    ##                for j in self.parent.listAutreReaper:
    ##                    dist = Helper.calcDistance(self.x, self.y, j.x, j.y)  ##ALEX pour calculer la distance relativement au autre reaper si c'est la nuit
    ##                    if dist <= self.etenduReaper and dist <= distProche:
    ##                        distProche = dist
    ##                        cible = j
    ##                if cible: #and not self.parent.daylight:
    ##                    self.cible = cible
    ##                    self.position_visee = [self.cible.x, self.cible.y]
    ##                    self.typeCible = "reaper"
    ##                print(self.typeCible,self.cible,dist, self.id, self.x, self.y)
    ##
    ##
    ##def deplacer_neutre(self):
    ##    self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
    ##    x = self.position_visee[0]
    ##    y = self.position_visee[1]
    ##    dist = Helper.calcDistance(self.x, self.y, x, y)
    ##    if dist <= self.vitesse:
    ##            self.cible = None
    ##            self.position_visee = None
    ##            self.typeCible = None
    ##            ##self.trouver_cible()
    ##
    ##def deplacer_kid(self):
    ##    self.position_visee = [self.cible.x, self.cible.y]
    ##    self.angle = Helper.calcAngle(self.x + random.randrange(1, 100), self.y + random.randrange(1, 100),
    ##                                  self.cible.x + random.randrange(1, 100),
    ##                                  self.cible.y + random.randrange(1, 100))
    ##    x = self.position_visee[0]
    ##    y = self.position_visee[1]
    ##
    ##    self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
    ##    # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
    ##    dist = Helper.calcDistance(self.x, self.y, x, y)
    ##    if dist <= self.vitesse:
    ##        return ##Alex pour garder le kidreaper en cible
    ##
    ##def deplacer_reaper_nuit(self):
    ##    self.position_visee = [self.cible.x, self.cible.y]
    ##    self.angle = Helper.calcAngle(self.x + random.randrange(1, 100), self.y + random.randrange(1, 100),
    ##                                  self.cible.x + random.randrange(1, 100),
    ##                                  self.cible.y + random.randrange(1, 100))
    ##    self.angle = math.degrees(self.angle)
    ##    self.angle += 180
    ##    self.angle = math.radians(self.angle)
    ##    x = self.position_visee[0]
    ##    y = self.position_visee[1]
    ##    x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)###
    ##    # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
    ##    #case = self.parent.trouver_case(x1, y1)
    ##    #if case.montype != "plaine":  ##code j-m test a remettre
    ##    #    pass  ##code j-m test a remettre
    ##    self.x, self.y = x1, y1
    ##    dist = Helper.calcDistance(self.x, self.y, x, y)
    ##    if dist > self.etenduReaper:  ## pour regarder si le daim est bien eloigne
    ##        self.cible = None
    ##        self.position_visee = None
    ##        self.typeCible = None
    ##        #self.trouverReaperNuit()
    ##        self.trouver_cible()
    ##        #return
    ##
    ##def deplacer_reaper_jour(self):
    ##    self.cible = None
    ##    self.position_visee = None
    ##    self.typeCible = None
    ##    self.trouver_cible()
    ##    #
    ##    x = self.position_visee[0]
    ##    y = self.position_visee[1]
    ##    x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
    ##    # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
    ##    #case = self.parent.trouver_case(x1, y1)
    ##    #if case.montype != "plaine":  ##code j-m test a remettre
    ##    #    pass  ##code j-m test a remettre
    ##    self.x, self.y = x1, y1
    ##    dist = Helper.calcDistance(self.x, self.y, x, y)
    ##    if dist <= self.vitesse:
    ##        self.cible = None
    ##        self.position_visee = None
    ##        self.typeCible = None
    ##        self.trouver_cible()
    ##
    ##def deplacer(self):
    ##    if self.etat == "mort": ##lorsque le daim est mort, pourquoi recoit-il encore la fontion deplacer s'il est mort?
    ##        self.cible = None
    ##        return
    ##    if self.typeCible == "neutre":
    ##        self.deplacer_neutre()
    ##    elif self.typeCible == "kid":
    ##        self.deplacer_kid()
    ##    #
    ##    else:
    ##        if self.typeCible == "reaper" and self.parent.daylight:
    ##            self.deplacer_reaper_jour()
    ##            return
    ##        elif self.typeCible == "reaper" and not self.parent.daylight:
    ##            self.deplacer_reaper_nuit()
    ##        else:
    ##            self.trouver_cible()
    ##
    ##
    ##def trouver_cible(self):  # Alex pour que le kid reaper attire les ames
    ##    distProche = self.etenduReaper
    ##    cible = None
    ##    for j in self.parent.listKidReaper:
    ##        dist = Helper.calcDistance(self.x, self.y, j.x, j.y)  ##ALEX pour calculer la distance relativement au kid reaper
    ##        if dist <= self.etenduReaper and dist <= distProche:
    ##            cible = j
    ##            distProche = dist
    ##    if cible:
    ##        self.cible = cible
    ##        self.position_visee = [self.cible.x, self.cible.y]
    ##        self.typeCible = "kid" ##pourrait etre reaper, kid ou neutre
    ##        return
    ##    else:
    ##        for j in self.parent.listAutreReaper:
    ##            dist = Helper.calcDistance(self.x, self.y, j.x, j.y)  ##ALEX pour calculer la distance relativement au autre reaper si c'est la nuit
    ##            if dist <= self.etenduReaper and dist <= distProche:
    ##                distProche = dist
    ##                cible = j
    ##        if cible and not self.parent.daylight:
    ##            self.cible = cible
    ##            self.position_visee = [self.cible.x, self.cible.y]
    ##            self.typeCible = "reaper"
    ##            return
    ##        else:
    ##            self.cible = None
    ##            self.trouver_cible_neutre()
    ##            self.typeCible = "neutre"
    ##
    ##def trouver_cible_neutre(self):
    ##    n = 1
    ##    while n:
    ##        x = (random.randrange(100) - 50) + self.x
    ##        y = (random.randrange(100) - 50) + self.y
    ##        case = self.parent.trouver_case(x, y)
    ##        # if case[0]>self.parent.taillecarte or case[0]<0:
    ##        #    continue
    ##        # if case[1]>self.parent.taillecarte or case[1]<0:
    ##        #    continue
    ##
    ##        if case.montype == "plaine":
    ##            self.position_visee = [x, y]
    ##            n = 0
    ##    self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
    ##    if self.x < self.position_visee[0]:
    ##        self.dir = "D"
    ##    else:
    ##        self.dir = "G"
    ##    if self.y < self.position_visee[1]:
    ##        self.dir = self.dir + "B"
    ##    else:
    ##        self.dir = self.dir + "H"
    ##    self.img = self.nomimg + self.dir


class Biotope():
    def __init__(self, parent, id, monimg, x, y, montype, idregion=0, posid="0"):
        self.parent = parent
        self.id = id
        self.img = monimg
        self.img2 = "soul_sprite"
        self.x = x
        self.y = y
        self.montype = montype
        self.sprite = None
        self.spriteno = 0
        self.idregion = idregion
        self.idcaseregion = posid


class Grave(Biotope):
    typeressource = ['grave_full',
                     'grave_empty']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 1
        self.etat = "full"


class Brume(Biotope):
    typeressource = ['eaugrand1',
                     'eaugrand2',
                     'eaugrand3',
                     'eaujoncD',
                     'eaujoncG',
                     'eauquenouillesD',
                     'eauquenouillesG',
                     'eauquenouillesgrand',
                     'eautourbillon',
                     'eautroncs']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        n = random.randrange(50)
        if n == 6:
            self.spritelen = 6  # len(self.parent.parent.vue.gifs["poissons"])
            self.sprite = "poissons"
            self.spriteno = random.randrange(self.spritelen)
            self.valeur = 100
        else:
            self.valeur = 10

    def jouer_prochain_coup(self):
        if self.sprite:
            self.spriteno += 1
            if self.spriteno > self.spritelen - 1:
                self.spriteno = 0


class Aureus(Biotope):
    typeressource = ['aureusbrillant',
                     'aureusD_',
                     'aureusG',
                     'aureusrocgrand',
                     'aureusrocmoyen',
                     'aureusrocpetit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100


class Roche(Biotope):
    typeressource = ['roches1 grand',
                     'roches1petit',
                     'roches2grand',
                     'roches2petit',
                     'roches3grand',
                     'roches3petit',
                     'roches4grand',
                     'roches4petit',
                     'roches5grand']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100


class Arbre(Biotope):
    typeressource = ['arbre0grand_pix',  # Yoan
                     'arbre0petit_pix',  # Yoan
                     'arbre1grand_pix',  # Yoan
                     'arbre2grand_pix',  # Yoan
                     'arbresapin0grand_pix',  # Yoan
                     'arbresapin0petit_pix']  # Yoan

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
            # tue humain
            self.parent.actioncourante = "ciblerressource"
            self.parent.javelots.remove(self)
            self.proie.mourir()
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
        self.montype = montype
        self.cible = None
        self.position_visee = None
        self.cibleennemi = None
        self.mana = 100
        self.force = 5
        self.champvision = 100
        self.vitesse = 14
        self.angle = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "retourbatimentmere": None,
                                 }

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"

    def attaquer_ennemi(self):
        rep = self.cibleennemi.recevoir_coup(self.force)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.actioncourante = "deplacer"

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort(self)
            return 1

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def deplacer(self, pos):
        self.position_visee = pos
        self.actioncourante = "bouger"

    def bouger(self):
        if self.position_visee:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le humain
            x = self.position_visee[0]
            y = self.position_visee[1]
            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            self.test_etat_du_sol(x1, y1)
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            self.x, self.y = x1, y1

            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.image = self.image[:-1] + self.dir

            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                if self.actioncourante == "bouger":
                    self.actioncourante = None
                return "rendu"
            else:
                return dist

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

    def test_etat_du_sol1(self, x1, y1):
        ######## SINON TROUVER VOIE DE CONTOURNEMENT
        # ici oncalcule sur quelle case on circule
        casex = x1 / self.parent.parent.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.parent.taillecase
        if casey != int(casey):
            casey = int(casey) + 1
        #####AJOUTER TEST DE LIMITE
        # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
        if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "plaine":
            # test pour être sur que de n'est 9 (9=batiment)
            if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "batiment":
                print("marche dans ", )
            else:
                print("marche dans batiment")


class KidReaper(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)
        self.force = 20


class Archer(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)


class Chevalier(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)


class RogueReaper(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)
        self.batimentmere = self.parent.objet_porte  # SS RogueReaper ramasser ressource
        self.activite = None  # se deplacer, cueillir, chasser, reparer, attaquer, fuir, promener, explorer,chercher
        self.typeressource = None
        self.quota = 1 # SS ramasser max 5 âmes à la fois
        self.ramassage = 0
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = random.randrange(100) + 300
        self.champchasse = 120
        self.javelots = []
        self.vitesse = 22
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerproie": self.cibler_proie,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "construirebatiment": self.construire_batiment,
                                 "ramasserressource": self.ramasser,
                                 "ciblerressource": self.temps_cibler_ressource,
                                 "retourbatimentmere": self.retour_batiment_mere,
                                 "validerjavelot": self.valider_javelot,
                                 }

    def chasser_ramasser(self, objetcible, sontype, actiontype):
        self.cible = objetcible
        self.parent.choix()  ##Alex pour proposer un choix de retour des ames
            ##parent.parent.vue.action.choix()  ##Alex pour proposer un choix de retour des ames
        self.typeressource = sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "grave" or self.typeressource == "humain" or self.typeressource == "brume":
                    if self.batimentmere == self.parent.objet_porte:
                        self.parent.ressources["soul"] += self.ramassage
                        self.parent.objet_porte.nbr_soul += self.ramassage
                    elif self.batimentmere == self.parent.objet_usine:
                        self.parent.ressources["soul_usine"] += self.ramassage
                        self.parent.objet_usine.nbr_soul += self.ramassage
                else:
                    self.parent.ressources[self.typeressource] += self.ramassage

                if self.parent.ressources["soul"] >= 500:   # SS
                    self.parent.win()
                    print("WIN")

                self.ramassage = 0
                if self.cible.valeur < 1:
                    rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                    self.cibler(rep)
                if self.cible:
                    self.cibler(self.cible)
                    if self.cible.montype == "humain":
                        self.actioncourante = "ciblerproie"
                    else:
                        self.actioncourante = "ciblerressource"


                else:
                    self.actioncourante = None
        else:
            pass

    def temps_cibler_ressource(self):
        if self.parent.parent.daylight: # si c'est le jour, on ne peut pas ramasser les âmes dans les tombes
            self.cibler_ressource()
        else:
            print("c'est le jour, les tombes ne sont pas disponibles")

    def cibler_ressource(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "ramasserressource"

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        if reponse == "rendu":
            if self.typeressource == "humain" or self.typeressource == "brume":
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

        if self.parent.parent.on_off == 1:           ##alex retour usine/porte
            self.batimentmere = self.parent.objet_usine       ##alex retour usine/porte
            self.parent.parent.on_off = 0
            print(self.batimentmere)            ##alex retour usine/porte
        elif self.parent.parent.on_off == 2:         ##alex retour usine/porte
            self.batimentmere = self.parent.objet_porte       ##alex retour usine/porte
            self.parent.parent.on_off = 0
            print(self.batimentmere)            ##alex retour usine/porte

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
            batiment = self.parent.parent.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte)
            self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

            sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)
            print(sitecons)

            self.parent.installer_batiment(batiment)
            if self.cible.sorte == ROGUEFACTORY:
                self.batimentmere = PORTE
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
        if typ != "grave" and typ != "humain":
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
    #         # dynamique comme le humain
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


class Ingenieur(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)


class Funeral(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)

        self.dir = "D"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible = None
        self.angle = None
        self.distancefeumax = 30
        self.distancefeu = 30
        self.fleches = []
        self.cibleennemi = None
        self.exists = True #SS Attaquer batiment

    def cibler(self, pos):
        self.position_visee = pos
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
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


class Grim(Perso):
    def __init__(self, parent, id, porte, couleur, x, y, montype):
        Perso.__init__(self, parent, id, porte, couleur, x, y, montype)
        self.activite = None  # sedeplacer, cueillir, chasser, pecher, construire, reparer, attaquer, fuir, promener,explorer,chercher
        self.typeressource = None
        self.quota = 5 # SS ramasser max 5 âmes à la fois
        self.ramassage = 0
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = random.randrange(100) + 300
        self.champchasse = 120
        self.javelots = []
        self.vitesse = 10
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerproie": self.cibler_proie,
                                 "ciblerennemi": self.cibler_ennemi,
                                 "attaquerennemi": None,
                                 "construirebatiment": self.construire_batiment,
                                 "ramasserressource": self.ramasser,
                                 "ciblerressource": self.temps_cibler_ressource,
                                 "retourbatimentmere": self.retour_batiment_mere,
                                 "validerjavelot": self.valider_javelot,
                                 }

    def attaquer(self, ennemi, actiontype):
        self.cible = ennemi
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def chasser_ramasser(self, objetcible, sontype, actiontype):
        self.cible = objetcible
        self.parent.choix()  # Alex pour proposer un choix de retour des ames
        self.typeressource = sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "grave" or self.typeressource == "humain" or self.typeressource == "brume":
                    if self.batimentmere == self.parent.objet_porte:
                        self.parent.ressources["soul"] += self.ramassage
                        self.parent.objet_porte.nbr_soul += self.ramassage
                    elif self.batimentmere == self.parent.objet_usine:
                        self.parent.ressources["soul_usine"] += self.ramassage
                        self.parent.objet_usine.nbr_soul += self.ramassage
                else:
                    self.parent.ressources[self.typeressource] += self.ramassage

                if self.parent.ressources["soul"] >= 500:   # SS
                    self.parent.win()
                    print("WIN")

                self.ramassage = 0
                if self.cible.valeur < 1:
                    rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                    self.cibler(rep)
                if self.cible:
                    self.cibler(self.cible)
                    if self.cible.montype == "humain":
                        self.actioncourante = "ciblerproie"
                    else:
                        self.actioncourante = "ciblerressource"


                else:
                    self.actioncourante = None
        else:
            pass

    def temps_cibler_ressource(self):
        if not self.parent.parent.daylight or self.cible.montype == "humain":
            self.cibler_ressource()
        else:
            print("c'est le jour, les tombes sont vides")

    def cibler_ressource(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "ramasserressource"

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        if reponse == "rendu":
            if self.typeressource == "humain" or self.typeressource == "brume":
                self.actioncourante = "ramasserressource"
        elif reponse <= self.champchasse and self.cible.etat == "vivant":
            self.actioncourante = "validerjavelot"

    #SS attaquer batiment
    def cibler_ennemi(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        if reponse == "rendu" and self.cible.etat == "vivant":
            if self.cible.recevoir_coup(self.force) == 1:
                self.actioncourante = None

    def valider_javelot(self):
        self.lancer_javelot(self.cible)
        for i in self.javelots:
            i.bouger()

    def ramasser(self):
        self.ramassage += 1
        self.cible.valeur -= 1

        if self.parent.parent.on_off == 1:           ##alex retour usine/porte
            self.batimentmere = self.parent.objet_usine       ##alex retour usine/porte
            self.parent.parent.on_off = 0
            print(self.batimentmere)            ##alex retour usine/porte
        elif self.parent.parent.on_off == 2:         ##alex retour usine/porte
            self.batimentmere = self.parent.objet_porte       ##alex retour usine/porte
            self.parent.parent.on_off = 0
            print(self.batimentmere)            ##alex retour usine/porte

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
            batiment = self.parent.parent.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte)
            self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

            sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)

            self.parent.installer_batiment(batiment)
            if self.cible.sorte == PORTE:
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
        if typ != "grave" and typ != "humain" and typ != "grave_empty":
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
            if typ != "grave_empty":  # Yoan
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
    #         # dynamique comme le humain
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
            for j in i.grims.values():
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
    #             listeclesm = list(joueurs[c].portes.keys())
    #             portecible = random.choice(listeclesm)
    #             self.cible = joueurs[c].portes[portecible]
    #         else:
    #             c = None
    #     self.angle = Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y)


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
    classespersos = {"grim": Grim,
                     "kidReaper": KidReaper,
                     "archer": Archer,
                     "chevalier": Chevalier,
                     "RogueReaper": RogueReaper,
                     "funeral": Funeral,
                     "ingenieur": Ingenieur}

    ressources = {"Azteque": {"soul": 999,
                              "soul_usine": 999,
                              "arbre": 200,
                              "roche": 200,
                              "aureus": 200,
                              "grim": 0,  # SS Bâtiments ajoutés dans les ressources pour le compte pendant l'environnement test
                              "kidReaper": 0,  # SS
                              "archer": 0,  # SS
                              "chevalier": 0,  # SS
                              "RogueReaper": 0,  # SS
                              "funeral": 0,  # SS
                              "ingenieur": 0,  # SS
                              PORTE: 0,  # SS
                              ROGUEFACTORY: 0,  # SS
                              KIDFACTORY: 0,  # SS
                              SOULFARM: 0},  # SS
                  "Congolaise": {"soul": 10,
                                 "soul_usine": 10,
                                 "arbre": 200,
                                 "roche": 200,
                                 "aureus": 888888888,
                                 "grim": 0,  # SS
                                 "kidReaper": 0,  # SS
                                 "archer": 0,  # SS
                                 "chevalier": 0,  # SS
                                 "RogueReaper": 0,  # SS
                                 "funeral": 0,  # SS
                                 "ingenieur": 0,  # SS
                                 PORTE: 0,  # SS
                                 ROGUEFACTORY: 0,  # SS
                                 KIDFACTORY: 0,  # SS
                                 SOULFARM: 0}  # SS
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
        self.objet_usine = 0  #alex pour le retour des ames
        self.objet_porte = 0  #alex pour le retour des ames
        self.ressourcemorte = []
        self.ressources = {"soul": 200,
                           "soul_usine": 0,
                           "arbre": 300,
                           "roche": 200,
                           "aureus": 200,
                           "grim": 0,  # SS
                           "kidReaper": 0,  # SS
                           "archer": 0,  # SS
                           "chevalier": 0,  # SS
                           "RogueReaper": 0,  # SS
                           "funeral": 0,  # SS
                           "ingenieur": 0,  # SS
                           PORTE: 1,  # SS
                           ROGUEFACTORY: 0,  # SS
                           KIDFACTORY: 0,  # SS
                           SOULFARM: 1} # SS
        self.persos = {"grim": {},
                       "kidReaper": {},
                       "archer": {},
                       "chevalier": {},
                       "RogueReaper": {},
                       "ingenieur": {},
                       "funeral": {}}

        self.batiments = {PORTE: {},
                          ROGUEFACTORY: {},
                          KIDFACTORY: {},
                          SOULFARM: {},
                          "siteconstruction": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "transferersoul": self.transferer_soul,  # Yoan
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner
                        }

        # on va creer une porte comme centre pour le joueur
        self.creer_point_origine(x, y)

    def win(self):  #SS couleur est la manière temporaire de dire quel joeur gagne
        print("WIN")
        self.parent.win(self.nom) #SS win

    def get_stats(self):
        total = 0
        for i in self.persos:
            total += len(self.persos[i])
        for i in self.batiments:
            total += len(self.batiments[i])
        return total

    def annoncer_mort(self, perso):
        self.persos[perso.montype].pop(perso.id)

    #SS attaquer batiment
    def annoncer_mort_batiment(self, batiment):
        self.parent.eliminer_batiment(batiment, batiment.montype, self)

    def attaquer(self, param):
        attaquants, attaque = param
        nomjoueur, idperso, sorte = attaque
        ennemi = self.parent.joueurs[nomjoueur].batiments[sorte][idperso] #SS attaquer batiment
        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    for p in self.parent.joueurs[nomjoueur].persos["funeral"]:#SS Attaquer batiment
                        if self.parent.joueurs[nomjoueur].persos["funeral"][p].exists: #SS Attaquer batiment
                            print("Funeral Reaper vivant")#SS Attaquer batiment
                        else:#SS Attaquer batiment
                            self.persos[i][j].attaquer(ennemi, "ciblerennemi") #SS attaquer batiment

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
        for i in self.persos["grim"]:
            self.persos["grim"][i].abandonner_ressource(ress)  # ajouer libereressource
        for i in self.persos["RogueReaper"]:# SS RogueReaper ramasse ressource
            self.persos["RogueReaper"][i].abandonner_ressource(ress)  # ajouer libereressource
        self.parent.eliminer_ressource(type, ress)

    def chasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "grim":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerproie")
                if j == "RogueReaper": # SS RogueReaper ramasse ressource
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "grim":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")
                elif j == "RogueReaper": # SS RogueReaper ramasse ressource
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")

    def transferer_soul(self, param):  # Yoan
        id = param[0]  # id du batiment # Yoan
        ames = self.ressources["soul_usine"]  # Yoan
        self.ressources["soul"] += int(ames)  # Yoan On divise par 2 pour l'instant parce que le nbr d'âmes est doublé for some reason
        self.objet_usine.nbr_soul += 0  # Alex pour remettre le nbrs de soul a 0 dans l`usine, 2 varibale a changer ***
        self.ressources["soul_usine"] = 0  # Alex pour remettre le nbrs de soul a 0 dans l`usine
        self.batiments[SOULFARM][id].nbr_soul = 0  # On remet la banque d'âmes de l'usine à 0 après le transfert

        if self.ressources["soul"] >= 1220:  #SS
            self.parent.win(self.nom)
            print("WIN ")


    def doubler_soul_usine(self):
        self.ressources['soul_usine'] += self.ressources['soul_usine']
        print(self.ressources['soul_usine'])
        # On ne l'appelle pas encore. à suivre YOAN

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def creer_point_origine(self, x, y):
        idporte = get_prochain_id()
        idballiste = get_prochain_id()  # id pour ferme de départ YOAN ALEX
        print(idporte)
        print(idballiste)
        self.objet_porte = self.batiments[PORTE][idporte] = Porte(self, idporte, self.couleur, x, y, PORTE)  #alex pour que le porte sois un choix de batiment mere
        self.objet_usine = self.batiments[SOULFARM][idballiste] = SoulFarm(self, idballiste, self.couleur, x + 60, y + 60, SOULFARM)  # création de la ferme et on la met dans une variable YOAN ALEX

        id = get_prochain_id() ##alex pour spawn un seul ouvrier
        self.persos["grim"][id] = Joueur.classespersos["grim"](self, id, self.objet_porte, self.couleur, x, y, "grim")
        self.ressources["grim"] += 1

        self.parent.listAutreReaper.append(self.persos["grim"][id])

        id = get_prochain_id() ##alex pour spawn une seul balliste
        self.persos["funeral"][id] = Joueur.classespersos["funeral"](self, id, self.objet_usine, self.couleur, x + 60, y + 60, "funeral")
        self.ressources["funeral"] += 1
        #self.ressources[PORTE] += 1 # SS (valeur ajoutée directement dans self.ressources de joueur)

        self.parent.listAutreReaper.append(self.persos["funeral"][id])

    def construire_batiment(self, param):
        perso, sorte, pos = param
        id = get_prochain_id()
        self.ressources[sorte] += 1  # SS
        # payer batiment
        vals = Partie.valeurs
        for k, val in self.ressources.items():
            self.ressources[k] = val - vals[sorte][k]

        siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte)
        self.batiments["siteconstruction"][id] = siteconstruction
        for i in perso:
            self.persos["grim"][i].construire_site_construction(siteconstruction)
            # self.persos["grim"][i].construire_batiment(siteconstruction)

    def installer_batiment(self, batiment):
        # self.batiments['siteconstruction'].pop(batiment.id)
        self.parent.installer_batiment(self.nom, batiment)

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
        id = get_prochain_id()
        if idbatiment in self.batiments[batimentsource]:
            batiment = self.batiments[batimentsource][idbatiment]

            x = batiment.x + 100 + (random.randrange(50) - 15)
            y = batiment.y + (random.randrange(50) - 15)

            self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y, sorteperso)

            self.ressources[sorteperso] += 1  # SS& # Yoan a retiré cette ligne

    def choix(self):  # Alex pour proposer un choix de retour des ames
        self.parent.choix()


#######################  LE MODELE est la partie #######################
class Partie():
    valeurs = {PORTE: { "soul": 0,
                        "soul_usine": 0,
                        "arbre": 0,
                        "roche": 0,
                        "aureus": 0,
                        "grim": 0,
                        "kidReaper": 0,  # SS
                        "archer": 0,  # SS
                        "chevalier": 0,  # SS
                        "RogueReaper": 0,  # SS
                        "funeral": 0,  # SS
                        "ingenieur": 0,  # SS
                        "delai": 60,
                        PORTE: 0,  # SS
                        ROGUEFACTORY: 0,  # SS
                        KIDFACTORY: 0,  # SS
                        SOULFARM: 0},  # SS
               ROGUEFACTORY: {"soul": 100,
                      "soul_usine": 0,
                      "arbre": 0,
                      "roche": 0,
                      "aureus": 0,
                        "grim": 0,
                        "kidReaper": 0,  # SS
                        "archer": 0,  # SS
                        "chevalier": 0,  # SS
                        "RogueReaper": 0,  # SS
                        "funeral": 0,  # SS
                        "ingenieur": 0,  # SS
                        "delai": 100,
                              PORTE: 0,  # SS
                              ROGUEFACTORY: 0,  # SS
                              KIDFACTORY: 0,  # SS
                              SOULFARM: 0},  # SS
               KIDFACTORY: {"soul": 200,
                            "soul_usine": 0,
                            "arbre": 0,
                            "roche": 0,
                          "aureus": 0,
                          "grim": 0,
                          "kidReaper": 0,  # SS
                          "archer": 0,  # SS
                          "chevalier": 0,  # SS
                          "RogueReaper": 0,  # SS
                          "funeral": 0,  # SS
                          "ingenieur": 0,  # SS
                          "delai": 100,
                            PORTE: 0,  # SS
                            ROGUEFACTORY: 0,  # SS
                            KIDFACTORY: 0,  # SS
                            SOULFARM: 0},  # SS
               SOULFARM: {"soul": 0,  # SS
                          "soul_usine": 0,
                          "arbre": 0,
                          "roche": 0,
                               "aureus": 0,
                                "grim": 0,
                                "kidReaper": 0,  # SS
                                "archer": 0,  # SS
                                "chevalier": 0,  # SS
                                "RogueReaper": 0,  # SS
                                "funeral": 0,  # SS
                                "ingenieur": 0,  # SS
                                "delai": 1,
                          PORTE: 0,  # SS
                          ROGUEFACTORY: 0,  # SS
                          KIDFACTORY: 0,  # SS
                          SOULFARM: 0},  # SS
               }

    def __init__(self, parent, mondict):
        self.parent = parent
        self.actionsafaire = {}
        self.aireX = 4000
        self.aireY = 4000

        # Decoupage de la surface
        self.taillecase = 20
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()

        # indice de temps  # YOAN
        self.delaiprochaineaction = 20
        self.debut = int(time.time())
        self.daylight = True  # variable pour indiquer si c'est le jour YOAN
        self.indice_dico_couleur = 0

        self.on_off = 0  # Alex? pour le choix de retour du grim\ pas tres clair comme variable

        self.joueurs = {}
        # reference vers les classes appropriées
        self.classesbatiments = {PORTE: Porte,
                                 KIDFACTORY: KidFactory,
                                 ROGUEFACTORY: RogueFactory,
                                 SOULFARM: SoulFarm}
        self.classespersos = {"grim": Grim,
                              "kidReaper": KidReaper,
                              "archer": Archer,
                              "chevalier": Chevalier,
                              "RogueReaper": RogueReaper}
        self.ressourcemorte = []
        self.batimentmort = []
        self.graveempty = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.countHumain = 0  ##ajout alex pour incrementation des humains
        self.listKidReaper = [] ##ajout alex
        self.listAutreReaper = [] ##ajout alex pour la fuite des humain la nuit

        self.biotopes = {"humain": {},
                         "arbre": {},
                         "roche": {},
                         "aureus": {},
                         "brume": {},
                         "grave": {}}

        self.regions = {}
        self.regionstypes = [["arbre", 50, 20, 5, "forest green"],
                             ["brume", 10, 20, 12, "grey80"],
                             ["roche", 8, 3, 6, "gray60"],
                             ["aureus", 12, 3, 4, "gold2"], ]
        self.creer_regions()
        self.creer_biotopes()
        self.creer_population(mondict)  # BABABOU

    def win(self, nom):  #SS couleur est la manière temporaire de dire quel joeur gagne
        self.parent.win(nom)
        print("WIN")

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

    def installer_batiment(self, nomjoueur, batiment):
        x1, y1, x2, y2 = self.parent.installer_batiment(nomjoueur, batiment)

        cartebatiment = self.get_carte_bbox(x1, y1, x2, y2)
        for i in cartebatiment:
            self.cartecase[i[1]][i[0]].montype = "batiment"
        batiment.cartebatiment = cartebatiment

    def creer_biotopes(self):
        # creer des humain éparpillés
        self.countHumain = 20
        n = self.countHumain
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                monhumain = Humain(self, id, x, y)
                self.biotopes["humain"][id] = monhumain
                self.listebiotopes.append(monhumain)
                n -= 1
        self.creer_biotope("arbre", "arbre", Arbre)
        self.creer_biotope("roche", "roche", Roche)
        self.creer_biotope("brume", "brume", Brume)
        self.creer_biotope("aureus", "aureus", Aureus)

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

    def creer_regions(self):
        for reg in self.regionstypes:
            nomregion = reg[0]
            nbrreg = reg[1]
            minreg = reg[2]
            rndreg = reg[3]
            coulreg = reg[4]
            self.regions[nomregion] = {}
            for i in range(nbrreg):
                listecasereg = []
                # trouve une case dans la carte
                x = random.randrange(self.taillecarte)
                y = random.randrange(self.taillecarte)
                # calcule la largeur (x) et hauteur(y) de la regtion
                taillex = random.randrange(reg[3]) + reg[2]
                tailley = random.randrange(reg[3]) + reg[2]
                # verifie que la region de deborde pas vers l'exterieur du jeu
                # (ex: si le centre de la region est case 1,1
                # et on la veut 10 case de large, cette region debuterait a la case -5, qui n'existe pas
                x0 = x - int(taillex / 2)
                if x0 < 0:
                    x0 = 0

                x1 = x + int(taillex / 2)
                if x1 > self.taillecarte - 1:
                    x1 = self.taillecarte - 1

                y0 = y - int(tailley / 2)
                if y0 < 0:
                    y0 = 0

                y1 = y + int(tailley / 2)
                if y1 > self.taillecarte - 1:
                    y1 = self.taillecarte - 1

                taillex = x1 - x0
                tailley = y1 - y0

                id = get_prochain_id()
                newregion = Region(self, id, x0, y0, taillex, tailley, nomregion)

                dicoreg = {}
                for i in range(tailley):
                    for j in range(taillex):
                        self.cartecase[y0 + i][x0 + j].parent = newregion
                        self.cartecase[y0 + i][x0 + j].montype = nomregion
                        # listereg.append(self.cartecase[y0+i][x0+j])
                        casereg = self.cartecase[y0 + i][x0 + j]
                        casereg.parent = newregion
                        dicoreg[casereg.id] = casereg

                newregion.dicocases = dicoreg
                self.regions[nomregion][id] = newregion

    def creer_population(self, mondict):
        couleurs = [["O", "orange"], ["R", "red"], ["B", "blue"], ["J", "yellow"], ["V", "lightgreen"]]
        quadrants = [[[0, 0], [int(self.aireX / 2), int(self.aireY / 2)]],
                     [[int(self.aireX / 2), 0], [self.aireX, int(self.aireY / 2)]],
                     [[0, int(self.aireY / 2)], [int(self.aireX / 2), self.aireY]],
                     [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]],
                     [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]]]
        nquad = 5
        bord = 50
        x = 1700
        y = 1800
        for i in mondict:
            id = get_prochain_id()
            coul = couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad = random.choice(range(nquad))
            nquad -= 1
            quad = quadrants.pop(choixquad)

            n = 1
            while n:
                #x = random.randrange(quad[0][0] + bord, quad[1][0] - bord)
                #y = random.randrange(quad[0][1] + bord, quad[1][1] - bord)
                #X1 += 100 #SS
                x += random.randrange(100, 200)
                case = self.trouver_case(x, y)
                if case.montype == "plaine":
                    self.joueurs[i] = Joueur(self, id, i, coul, x, y)
                    n = 0

    def deplacer(self):
        for i in self.joueurs:
            self.joueurs[i].deplacer()

    # Fonction pour le jour et la nuit (en construction. so far ça fonctionne) YOAN
    def determiner_jour_nuit(self):
        t = int(time.time())
        if (t - self.debut) % DAY == 0 and self.daylight is True:
            self.daylight = False  # self.daylight = False = c'est la nuit
            self.parent.vue.textmessageimportant.delete(1.0, 'end')
            self.parent.vue.textmessageimportant.insert('end', "C'est la nuit")
        elif (t - self.debut) % NIGHT == 0 and self.daylight is False:
            self.daylight = True  # self.daylight = True = c'est le jour
            for i in self.joueurs:
                self.joueurs[i].doubler_soul_usine()
            self.parent.vue.textmessageimportant.delete(1.0, 'end')
            self.parent.vue.textmessageimportant.insert('end', "C'est le jour")

    def jouer_prochain_coup(self, cadrecourant):
        self.ressourcemorte = []
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER
        if cadrecourant in self.actionsafaire:
            for i in self.actionsafaire[cadrecourant]:
                self.joueurs[i[0]].actions[i[1]](i[2])
        ##################################################################

        if self.countHumain < 15:##ajout lex pour incrementer des humains
            self.countHumain = 35
            n = self.countHumain
            while n:
                x = random.randrange(self.aireX)
                y = random.randrange(self.aireY)
                case = self.trouver_case(x, y)
                if case.montype == "plaine":
                    id = get_prochain_id()
                    monhumain = Humain(self, id, x, y)
                    self.biotopes["humain"][id] = monhumain
                    self.listebiotopes.append(monhumain)
                    n -= 1

        # demander aux objets de s'activer
        for i in self.biotopes["humain"].keys():
            self.biotopes["humain"][i].deplacer()
            #self.biotopes["humain"][i].jouerprochainCoup()

        humainMort = None ## pour enlever les daim mort de la liste
        for i in self.biotopes["humain"].keys():
            if self.biotopes["humain"][i].etat == "mort":
                humainMort = self.biotopes["humain"][i].id
        if humainMort != None:
            self.biotopes["humain"].pop(humainMort)


        for i in self.biotopes["brume"].keys():
            self.biotopes["brume"][i].jouer_prochain_coup()

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
            # appelé ici pour l'instant. probablement un meilleur endroit pour l'appeler
            self.determiner_jour_nuit()

        if self.daylight is False:
            if self.indice_dico_couleur < 8:
                if cadrecourant % 5 == 0:
                    self.indice_dico_couleur += 1
                    self.parent.vue.canevas.configure(bg=TEMPS_COULEUR[self.indice_dico_couleur])

        if self.daylight is True:
            if self.indice_dico_couleur > 0:
                if cadrecourant % 5 == 0:
                    self.indice_dico_couleur -= 1
                    self.parent.vue.canevas.configure(bg=TEMPS_COULEUR[self.indice_dico_couleur])

        self.faire_action_partie()

    def faire_action_partie(self):
        if self.delaiprochaineaction == 0:
            self.produire_action()
            self.delaiprochaineaction = random.randrange(10, 20)
        else:
            self.delaiprochaineaction -= 1

    def produire_action(self):
        typeressource = Grave.typeressource
        n = 1
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                img = typeressource[0]
                grave = Grave(self, id, img, x, y, "grave")
                self.biotopes["grave"][id] = grave
                n -= 1
                self.parent.afficher_bio(grave)

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
        if ress.img == "grave_full":
            self.graveempty.append(ress)
            self.ressourcemorte.append(ress)

    #SS attaquer batiment
    def eliminer_batiment(self, batiment, type, joueur):
        if batiment.id in self.joueurs[joueur.nom].batiments[type]:
            self.batimentmort.append(batiment)

    def choix(self): ##Alex pour proposer un choix de retour des ames
        self.parent.choix()

    #############################################################################    
    # ATTENTION : NE PAS TOUCHER                 
    def ajouter_actions_a_faire(self, actionsrecues):
        for i in actionsrecues:
            cadrecle = i[0]
            if (self.parent.cadrejeu - 1) > int(cadrecle):
                print("PEUX PAS")
            action = ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle] = action
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
