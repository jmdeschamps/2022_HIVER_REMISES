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
        self.mana=200

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


class Maison(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.tier = 1
        self.minerais =     {"cuivre" : 0,
                             "etain" : 0,
                             "fer" : 0,
                             "argent" : 0,
                             "metalnoir" : 0,
                             "bois" : 0,
                             "boisfin" : 0,
                             "boisdebase" : 0,
                             "boisancien" : 0,
                             "framboises" : 0,
                             "bleuets" : 0,
                             "viande" : 0,
                             "miel" : 0,
                             "carottes" : 0,
                             "navets" : 0,
                             "herbes" : 0,
                             "champignons" : 0,
                             "poisson" : 0,
                             "farineorge" : 0,
                             "roche" : 0,
                             "obsidienne" : 0,
                             "silex" : 0,
                             "ramuredurci" : 0,
                             "cuirdedaim" : 0,
                             "fragmentsdos" : 0,
                             "entrailles" : 0,
                             "charbon" : 0,
                             "grainescarrotte" : 0,
                             "grainesnavet" : 0,
                             "grainesoignon" : 0,
                             "lingotcuivre": 0,
                             "lingotetain": 0,
                             "lingotfer": 0,
                             "lingotbronze": 0,
                             "lingotargent": 0,
                             "lingotnoir": 0,
                             "hachettedesilex": 0,
                             "canneapeche": 0,
                             "viandegrillee": 0,
                             "poissongrillee": 0,
                             "viandesechee": 0,
                             "marmelade": 0,
                             "repasbifteck": 0,
                             "ragout": 0,
                             "soupecarotte": 0
                             }
        self.recettespossible = ["lingotcuivre", "lingotetain"]


# Création de la classe Forge qui est une sous classe de Batiment
class Forge(Batiment):
    def __init__(self, parent, id,couleur,x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.hp = 75
        self.defense = 5
        self.prixConstruction = {"cuivre": 6,
                                 "charbon": 4,
                                 "bois": 30,
                                 "pierre": 10}

        self.armes = {"baton": 0,
                      "epieu": 0,
                      "masse": 0,
                      "epee": 0,
                      "hache": 0}

        self.armures = {"armureCuir": 0,
                         "armureTroll": 0,
                         "armureBronze": 0,
                         "armureAcier": 0,
                         "armureArgent": 0,
                         "armureLin": 0}

        self.outils = {"hacheSilex": 0,
                       "piocheRamure": 0,
                       "hacheBronze": 0,
                       "piocheBronze": 0,
                       "hacheFer": 0,
                       "piocheFer": 0}


class Fournaise(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0
        self.arret = False
        self.prixConstruction = {"lingot": 6}

        self.inventaire = {"bois": 0}

    def convertireBoisCharbon(self):
        pass


class Abri():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class Caserne():
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0

class NPC():
    def __init__(self, parent, id, spawnX, spawnY, playerID, currentQuest):
        self.id = id
        self.x = spawnX
        self.y = spawnY
        self.nomimg = "npcTemp"
        self.montype = "npc"
        self.etat = ""
        self.playerID = playerID
        self.currentQuest = currentQuest
        self.questInProgress = False



class Quete():
    def __init__(self, id, name, playerID, questText, isCompleted, objType):
        self.id = id
        self.name = name
        self.playerID = playerID
        self.questText = questText
        self.isCompleted = isCompleted
        self.objType = objType


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
        self.valeur = 40
        self.position_visee = None
        self.angle = None
        self.dir = "GB"
        self.img = self.nomimg + self.dir
        self.vitesse = 2
        self.brouter = 50

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
                self.position_visee=None
        else:
            if self.etat == "vivant":
                self.brouter -= 1
                if self.brouter <= 0:
                    self.trouver_cible()
                    self.brouter = random.randrange(25) + 20

    def trouver_cible(self):
        n = 1
        while n:
            x = (random.randrange(200) - 100) + self.x
            y = (random.randrange(200) - 100) + self.y
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


class Framboises(Biotope):
    typeressource = ['framboisesgros',
                     'framboisespetit']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 1

class Bleuets(Biotope):
    typeressource = ['bleuetsgros',
                     'bleuetspetit']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 1

class Champignons(Biotope):
    typeressource = ['champignonsgros',
                     'champignonspetit']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 1

class Marais(Biotope):
    typeressource = ['marais1',
                     'marais2',
                     'marais3']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100


class Eau(Biotope):
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
            self.spritelen = 6 #len(self.parent.parent.vue.gifs["poissons"])
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

class Cuivre(Biotope):
    typeressource = ['cuivre1 grand',
                     'cuivre1petit',
                     'cuivre2grand',
                     'cuivre2petit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100

class Bois(Biotope):
    typeressource = ['arbre0grand',
                     'arbre0petit',
                     'arbre1grand',
                     'arbre2grand',
                     'arbresapin0grand',
                     'arbresapin0petit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 30




class Fleche():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.taille = 20
        self.force=10
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
            rep=self.cibleennemi.recevoircoup(self.force)
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
        self.vitesse = 5
        self.angle = None
        self.etats_et_actions={"bouger": self.bouger,
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

    def deplacer(self,pos):
        self.position_visee = pos
        self.actioncourante = "bouger"

    def bouger(self):
        if self.position_visee:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le daim
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
                if self.actioncourante=="bouger":
                    self.actioncourante=None
                return "rendu"
            else:
                return dist



    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee =[self.cible.x,self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.image = self.image[:-1] + self.dir
        else:

            self.position_visee =None

    def test_etat_du_sol(self,x1, y1):
        ######## SINON TROUVER VOIE DE CONTOURNEMENT
        # ici oncalcule sur quelle case on circule
        casex = x1 / self.parent.parent.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.parent.taillecase
        if casey != int(casey):
            casey = int(casey) + 1
        #####AJOUTER TEST DE LIMITE
        case=self.parent.parent.trouver_case(x1,y1)
        #
        # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
        if case.montype != "plaine":
            # test pour être sur que de n'est 9 (9=batiment)
            if case.montype != "batiment":
                print("marche dans ",case.montype )
            else:
                print("marche dans batiment")

    def test_etat_du_sol1(self,x1, y1):
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

class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20


class Archer(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Chevalier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Druide(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Ingenieur(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Ballista(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "DH"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible=None
        self.angle=None
        self.distancefeumax = 30
        self.distancefeu = 30
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
        self.position_visee=[x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.distancefeu:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"

    def attaquerennemi(self):
        if self.delaifeu==0:
            id = get_prochain_id()
            fleche=Fleche(self,id,self.ciblennemi)
            self.delaifeu=self.delaifeumax
        for i in self.fleches:
            rep=i.bouger()
        if rep:
            rep = self.cibleennemi.recevoir_coup(self.force)
            self.fleches.remove(rep)


class Ouvrier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.activite=None # sedeplacer, cueillir, chasser, pecher, construire, reparer, attaquer, fuir, promener,explorer,chercher
        self.typeressource = None
        self.quota = 20
        self.ramassage = 0
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = random.randrange(100) + 300
        self.champchasse = 120
        self.javelots = []
        self.vitesse = random.randrange(5) + 5
        self.etats_et_actions={"bouger": self.bouger,
                               "ciblersiteconstruction": self.cibler_site_construction,
                               "ciblerproie": self.cibler_proie,
                               "ciblerennemi": None,
                               "attaquerennemi": None,
                               "construirebatiment": self.construire_batiment,
                               "ramasserressource": self.ramasser,
                               "ciblerressource": self.cibler_ressource,
                               "retourbatimentmere": self.retour_batiment_mere,
                               "validerjavelot": self.valider_javelot,
                               }

    def chasser_ramasser(self,objetcible,sontype,actiontype):
        self.cible=objetcible
        self.typeressource=sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante=actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "daim" or self.typeressource == "eau":
                    self.parent.ressources["viande"] += self.ramassage
                else:
                    self.parent.ressources[self.typeressource] += self.ramassage
                self.ramassage = 0
                if self.cible.valeur<1:
                    rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                    self.cibler(rep)
                if self.cible:
                    self.cibler(self.cible)
                    if self.cible.montype=="daim":
                        self.actioncourante= "ciblerproie"
                    else:
                        self.actioncourante="ciblerressource"
                else:
                    self.actioncourante = None
        else:
            pass

    def cibler_ressource(self):
        reponse=self.bouger()
        if reponse == "rendu":
            self.actioncourante="ramasserressource"

    def cibler_site_construction(self):
        reponse=self.bouger()
        if reponse == "rendu":

            self.actioncourante="construirebatiment"


    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse=self.bouger()
        if reponse == "rendu":
            if self.typeressource == "daim" or self.typeressource == "eau":
                self.actioncourante="ramasserressource"
        elif reponse <= self.champchasse and self.cible.etat=="vivant":
            self.actioncourante = "validerjavelot"

    def valider_javelot(self):
        self.lancer_javelot(self.cible)
        for i in self.javelots:
                i.bouger()

    def ramasser(self):
        self.ramassage += 1
        self.cible.valeur -= 1
        if self.cible.valeur == 0  or self.ramassage == self.quota:
            self.actioncourante = "retourbatimentmere"
            self.position_visee=[self.batimentmere.x, self.batimentmere.y]
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
        if self.cible.delai<1:
            batiment = self.parent.parent.classesbatiments[self.cible.sorte](self,self.cible.id, self.parent.couleur,
                                                                       self.cible.x, self.cible.y, self.cible.sorte)

            self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

            sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)
            print(sitecons)

            self.parent.installer_batiment(batiment)
            if self.cible.sorte=="maison":
                self.batimentmere=batiment
            self.cible=None
            self.actioncourante=None


    def construire_site_construction(self,site_construction):
        self.cibler(site_construction)
        self.actioncourante="ciblersiteconstruction"
        #pass #monte le batiment par etapes on pourrait montrer l'anavancement de la construciton

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def lancer_javelot(self, proie):
        if self.javelots == []:
            id = get_prochain_id()
            self.javelots.append(Javelot(self, id, proie))

    def chercher_nouvelle_ressource(self, type, idreg):
        print("Je cherche nouvelle ressource")
        if type != "framboises" and type != "bleuets" and type != "champignons" and type != "daim":
            reg = self.parent.parent.regions[type]
            if idreg in reg:
                regspec = self.parent.parent.regions[type][idreg]
                n = len(regspec.dicocases)
                while n > 0:
                    clecase = list(regspec.dicocases.keys())
                    case = regspec.dicocases[random.choice(clecase)]
                    n -= 1
                    if case.ressources:
                        clecase2 = list(case.ressources.keys())
                        newress = case.ressources[random.choice(clecase2)]
                        if newress.montype == type:
                            return newress
                return None
        else:
            nb=len(self.parent.parent.biotopes[type])
            for i in range(nb):
                rep=random.choice(list(self.parent.parent.biotopes[type].keys()))
                obj=self.parent.parent.biotopes[type][rep]
                if obj != self.cible:
                    distance = Helper.calcDistance(self.x, self.y, obj.x, obj.y)
                    if distance<=self.champvision:
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
                self.position_visee=[self.batimentmere.x,self.batimentmere.y]

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
                     "chevalier": Chevalier,
                     "druide": Druide,
                     "ballista": Ballista,
                     "ingenieur": Ingenieur}

    def __init__(self, parent, id, nom, couleur, x, y):
        self.parent = parent
        self.nom = nom
        self.id = id
        self.x = x
        self.y = y
        self.couleur = couleur
        self.monchat = []
        self.chatneuf = 0
        self.ressourcemorte = []
        self.ressources = {"viande": 200,
                           "framboises": 50,
                           "bleuets": 50,
                           "champignons": 50,
                           "bois": 200,
                           "boisdebase": 200,
                           "boisfin": 200,
                           "roche": 200,
                           "silex": 200,
                           "cuivre": 50,
                           "etain": 50,
                           "fer": 50,
                           "charbon":0}
        self.persos = {"ouvrier": {},
                       "soldat": {},
                       "archer": {},
                       "chevalier": {},
                       "druide": {},
                       "ingenieur": {},
                       "ballista": {}}

        self.batiments = {"maison": {},
                          "abri": {},
                          "caserne": {},
                          "usineballiste": {},
                          "siteconstruction": {},
                          "forge": {},
                          "fournaise": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner,
                        "convertirbois":self.convertir_bois,
                        "creerarmes": self.creer_armes,
                        "creerarmures": self.creer_armures,
                        "creeroutils": self.creer_outils
                        }
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)
    def get_stats(self):
        total=0
        for i in self.persos:
            total+= len(self.persos[i])
        for i in self.batiments:
            total+= len(self.batiments[i])
        return total

    def annoncer_mort(self, perso):
        self.persos[perso.montype].pop(perso.id)
    def annoncer_mort_batiment(self, perso):
        self.batiments[perso.montype].pop(perso.id)

    def attaquer(self, param):
        attaquants, attaque = param
        nomjoueur, idperso, sorte = attaque
        ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)
                    # j.attaquer(ennemi)

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
                                                           typeress,"ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress,"ciblerressource")

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        self.batiments["maison"][idmaison] = Maison(self, idmaison, self.couleur, x, y, "maison")

    def construire_batiment(self, param):
        perso, sorte, pos = param
        id = get_prochain_id()
        # payer batiment
        vals = Partie.valeurs
        for k, val in self.ressources.items():
            self.ressources[k] = val - vals[sorte][k]

        siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte)
        self.batiments["siteconstruction"][id] = siteconstruction
        for i in perso:
            self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
            #self.persos["ouvrier"][i].construire_batiment(siteconstruction)

    def installer_batiment(self, batiment):
        # self.batiments['siteconstruction'].pop(batiment.id)
        self.parent.installer_batiment(self.nom,batiment)

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
        batiment = self.batiments[batimentsource][idbatiment]

        x = batiment.x + 100 + (random.randrange(50) - 15)
        y = batiment.y + (random.randrange(50) - 15)

        self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                       sorteperso)

    def convertir_bois(self, param):
        nbDebois = self.parent.joueurs.keys()
        for i in nbDebois:
            total = self.parent.joueurs[i].ressources["bois"]
        if total > 0:
            self.parent.joueurs[i].ressources["charbon"] += 1
        self.parent.joueurs[i].ressources["bois"] -= 10

    def creer_perso(self, param):
        sorteperso, batimentsource, idbatiment, pos = param
        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]

        x = batiment.x + 100 + (random.randrange(50) - 15)
        y = batiment.y + (random.randrange(50) - 15)

        self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                       sorteperso)

    def creer_armes(self, param):
        batimentsource, idbatiment, pos = param
        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]
        listeArmes = ["baton", "epieu", "masse", "epee", "hache"]
        choixArme = random.choice(listeArmes)

        print(choixArme)

    def creer_armures(self, param):
        batimentsource, idbatiment, pos = param
        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]
        listeArmures = ["armurecuir", "arumureTroll", "armureBronze", "arumureAcier", "arumureArgent", "arumureLin"]
        choixArmure = random.choice(listeArmures)

        print(choixArmure)

    def creer_outils(self,param):
        batimentsource, idbatiment, pos = param
        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]
        listeOutils = ["hacheSilex","piocheRamure","hacheBronze","piocheBronze","hacheFer","piocheFer"]
        choixOutil = random.choice(listeOutils)

        print(choixOutil)


#######################  LE MODELE est la partie #######################
class Partie():
    valeurs = {"maison": {"viande": 0,
                          "bois": 20,
                          "roche": 20,
                          "cuivre": 0,
                          "framboises": 0,
                          "bleuets": 0,
                          "champignons": 0,
                          "boisdebase": 0,
                          "boisfin": 0,
                          "etain": 0,
                          "fer": 0,
                          "silex": 0,
                          "charbon":0,
                          "delai":50,},
               "abri": {"viande": 0,
                        "bois": 10,
                        "roche": 5,
                        "cuivre": 0,
                        "framboises": 0,
                        "bleuets": 0,
                        "champignons": 0,
                        "boisdebase": 0,
                        "boisfin": 0,
                        "etain": 0,
                        "fer": 0,
                        "silex": 0,
                        "charbon": 0,
                        "delai":30},
               "caserne": {"viande": 0,
                           "bois": 10,
                           "roche": 5,
                           "cuivre": 0,
                           "framboises": 0,
                           "bleuets": 0,
                           "champignons": 0,
                           "boisdebase": 0,
                           "boisfin": 0,
                           "etain": 0,
                           "fer": 0,
                           "silex": 0,
                           "charbon": 0,
                           "delai":60},
               "usineballiste": {"viande": 0,
                                 "bois": 10,
                                 "roche": 5,
                                 "cuivre": 0,
                                 "framboises": 0,
                                 "bleuets": 0,
                                 "champignons": 0,
                                 "boisdebase": 0,
                                 "boisfin": 0,
                                 "etain": 0,
                                 "fer": 0,
                                 "silex": 0,
                                 "charbon": 0,
                                 "delai":80},
               "forge" : {"viande": 0,
                          "bois": 30,
                          "roche": 10,
                          "framboises": 0,
                          "bleuets": 0,
                          "champignons": 0,
                          "boisdebase": 0,
                          "boisfin": 0,
                          "etain": 0,
                          "fer": 0,
                          "silex": 0,
                          "cuivre": 0,
                          "charbon": 0,
                          "delai": 30},

               "fournaise": {"viande": 0,
                             "bois": 10,
                             "roche": 5,
                             "cuivre": 0,
                             "framboises": 0,
                             "bleuets": 0,
                             "champignons": 0,
                             "boisdebase": 0,
                             "boisfin": 0,
                             "etain": 0,
                             "fer": 0,
                             "silex": 0,
                             "charbon": 0,
                             "delai": 80}
               }

    recettes = {            "lingotcuivre":    {"cuivre": 1,
                                   "charbon": 2},
                            "lingotetain":      {"etain": 1,
                                                 "charbon": 2},
                            "lingotfer":        {"fer": 1,
                                                 "charbon": 2},
                            "lingotbronze":     {"lingotcuivre": 2,
                                                 "lingotetain": 1},
                            "lingotargent":     {"argent": 1,
                                                 "charbon": 2},
                            "lingotnoir":       {"metalnoir": 1,
                                                  "charbon": 2},
                            "armuredecuir":     {"cuir": 6},
                            "armuredetroll":    {"cuirdetroll": 15,
                                                 "fragmentdos": 6},
                            "armuredebronze":   {"lingotbronze": 15,
                                                 "cuir": 3},
                            "armuredacier":     {"lingotfer": 15,
                                                 "charbon": 15},
                            "armuredargent":    {"lingotargent": 15,
                                                 "fourruredeloup": 3},
                            "armuredelin":      {"lin": 30,
                                                 "lingotnoir": 6},
                            "baton":            {"bois": 10},
                            "epieudebronze":    {"lingotbronze": 10,
                                                 "bois": 5},
                            "massuedefer":      {"lingotfer": 10,
                                                 "boisdebase": 5},
                            "epeedargent":      {"lingotargent": 10,
                                                 "boisfin": 5},
                            "hachedaciernoir":  {"lingotnoir": 10,
                                                 "boisancien": 5},
                            "hachettedesilex": {"silex": 5,
                                                 "bois": 5},
                            "arc":             {"bois": 10,
                                                 "cuir": 2},
                            "arccomposite":    {"boisfin": 10,
                                                 "boisdebase": 10},
                            "arcdechasseur":   {"boisfin": 10,
                                                 "lingotfer": 10,
                                                 "cuir": 2},
                            "canneapeche":     {"bois": 10},
                            "piochederamure":  {"ramuredurci": 1,
                                                 "bois": 5},
                            "hachettedebronze":{"lingotbronze": 10,
                                                 "boisdebase": 5},
                            "piochedebronze":  {"lingotbronze": 10,
                                                 "boisdebase": 5},
                            "hachettedacier":  {"lingotfer": 10,
                                                 "charbon": 10,
                                                 "boisfin": 5},
                            "piochedefer":     {"lingotfer": 10,
                                                 "boisfin": 5},
                            "viandegrillee":   {"viande": 1},
                            "poissongrillee":  {"poisson": 1},
                            "viandesechee":    {"viande": 1,
                                                 "miel": 1},
                            "marmelade":       {"framboise": 4,
                                                 "bleuet": 2},
                            "repasbifteck":    {"viande": 1,
                                                 "carotte": 1,
                                                 "herbes": 1},
                            "ragout":          {"viande": 1,
                                                 "navet": 1,
                                                 "carotte": 3},
                            "soupecarotte":    {"carotte": 1,
                                                 "champignon": 3},
                            "tourtiere":       {"viande": 2,
                                                 "herbes": 3,
                                                 "farineorge": 3},
                            "wrapthon":        {"poisson": 2,
                                                 "oignon": 1,
                                                 "farineorge": 2},
                            "soupeoignon":     {"farineorge": 1,
                                                 "oignon": 3},
                            "saucisse":        {"entraille": 1,
                                                 "viande": 2,
                                                 "herbes": 1},
                            "hydromelresispoison": {"miel": 10,
                                                     "charbon": 10,
                                                     "herbes": 5},
                            "hydromelresisfroid":  {"miel": 10,
                                                     "entraille": 5,
                                                     "herbes": 2},
                            "hydromelvie":         {"miel": 10,
                                                     "framboise": 5,
                                                     "bleuets": 2}
                            }

    def __init__(self, parent, mondict):
        self.parent = parent
        self.actionsafaire = {}
        self.debut=int(time.time())
        self.aireX = 4000
        self.aireY = 4000
        # Decoupage de la surface
        self.taillecase = 20
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()

        self.delaiprochaineaction = 20

        self.joueurs = {}
        ###  reference vers les classes appropriées
        self.classesbatiments = {"maison": Maison,
                                 "caserne": Caserne,
                                 "abri": Abri,
                                 "usineballiste": Usineballiste,
                                 "forge":Forge,
                                 "fournaise": Fournaise}
        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat,
                              "archer": Archer,
                              "chevalier": Chevalier,
                              "druide": Druide}
        self.ressourcemorte = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.biotopes = {"daim": {},
                         "bois": {},
                         "roche": {},
                         "cuivre": {},
                         "eau": {},
                         "marais": {},
                         "framboises": {},
                         "bleuets": {},
                         "champignons": {}
                         }

        self.regions = {}
        self.regionstypes = [["bois", 50, 20, 5, "forest green"],
                             ["eau", 10, 20, 12, "light blue"],
                             ["marais", 3, 8, 8, "DarkSeaGreen3"],
                             ["roche", 8, 3, 6, "gray60"],
                             ["cuivre", 8, 3, 6, "DarkOrange3"]]
        self.creer_regions()
        self.creer_biotopes()
        self.creer_population(mondict)

    def calc_stats(self):
        total=0
        for i in self.joueurs:
            total+=self.joueurs[i].get_stats()
        for i in self.biotopes:
            total+=len(self.biotopes[i])
        self.montrer_msg_general(str(total))

    def trouver_valeurs(self):
        vals=Partie.valeurs
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

        self.creer_biotope("bois", "bois", Bois)
        self.creer_biotope("roche", "roche", Roche)
        self.creer_biotope("cuivre", "cuivre", Cuivre)
        self.creer_biotope("eau", "eau", Eau)
        self.creer_biotope("marais", "marais", Marais)

    def creer_biotope(self, region, ressource, typeclasse):  # creation des forets
        typeressource = typeclasse.typeressource

        for cleregion in self.regions[region].keys():
            listecases = self.regions[region][cleregion].dicocases
            # for listecase in self.regions[region]:
            #nressource = random.randrange(int(len(listecases) / 3)) + int((len(listecases) / 5))
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
        for i in mondict:
            id = get_prochain_id()
            coul = couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad = random.choice(range(nquad))
            nquad -= 1
            quad = quadrants.pop(choixquad)

            n = 1
            while n:
                x = random.randrange(quad[0][0] + bord, quad[1][0] - bord)
                y = random.randrange(quad[0][1] + bord, quad[1][1] - bord)
                case = self.trouver_case(x, y)
                if case.montype == "plaine":
                    self.joueurs[i] = Joueur(self, id, i, coul, x, y)
                    n = 0

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

        for i in self.biotopes["eau"].keys():
            self.biotopes["eau"][i].jouer_prochain_coup()

        # demander aux objets de s'activer
        for i in self.joueurs.keys():
            self.joueurs[i].jouer_prochain_coup()

        if self.msggeneral and "cadre" not in self.msggeneral:
            self.msggeneralcompteur += 1
            if self.msggeneralcompteur == self.msggeneraldelai:
                self.msggeneral = ""
                self.msggeneralcompteur = 0
        else:
            t=int(time.time())
            msg="cadre: "+str(cadrecourant)+" - secs: "+str(t-self.debut)
            self.msggeneral=msg

        self.renouveler_ressources_naturelles()

    def renouveler_ressources_naturelles(self):
        if self.delaiprochaineaction == 0:
            self.generer_ressource(Framboises, "framboises")
            self.generer_ressource(Bleuets, "bleuets")
            self.generer_ressource(Champignons, "champignons")
            self.delaiprochaineaction = 200
        else:
            self.delaiprochaineaction -= 1

    def generer_ressource(self, ressource, nom_ressource):
        typeressource = ressource.typeressource
        n = 1
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                img = random.choice(typeressource)
                cette_ressource = ressource(self, id, img, x, y, nom_ressource)
                self.biotopes[nom_ressource][id] = cette_ressource
                n -= 1
                self.parent.afficher_bio(cette_ressource)

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
        if ress not in self.ressourcemorte:
            self.ressourcemorte.append(ress)

    #############################################################################    
    # ATTENTION : NE PAS TOUCHER                 
    def ajouter_actions_a_faire(self, actionsrecues):
        for i in actionsrecues:
            cadrecle = i[0]
            if (self.parent.cadrejeu-1)> int(cadrecle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            action = ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle] = action
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
