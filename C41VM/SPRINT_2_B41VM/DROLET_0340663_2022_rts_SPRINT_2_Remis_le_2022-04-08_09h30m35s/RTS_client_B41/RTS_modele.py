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
        self.mana = 200

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort_batiment(self)
            return 1


class Maison(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.tier = 1
        self.ressources = {"metal": 1000,
                           "bois": 1000,
                           "nourriture": 1000,
                           "pierre": 1000
                           }


class Forge(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.hp = 75
        self.defense = 5
        self.prixConstruction = {"cuivre": 6,
                                 "charbon": 4,
                                 "bois": 30,
                                 "pierre": 10}

class Ferme(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype):
        Batiment.__init__(self,parent,id,x,y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.valeur = 5

class Fournaise(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0
        self.arret = False
        self.prixConstruction = {"lingot": 6}


class Caserne(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class NPC:
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

class Stele:
    def __init__(self,parent,joueur,id,rune,x,y):
        self.parent = parent
        self.joueur = joueur #ImageTk.PhotoImage(Image.open("image"))'stele0' # à changer
        self.rune = rune
        self.id = id
        self.tempsA = int(time.time())
        self.x = x
        self.y = y

    def incrementerPoints(self):
        if self.rune >= 1:
            self.joueur.nbPointsRune += 20

    def incrementerRune(self):
        if self.rune < 4:
            self.rune += 1

    def incrementerPointsSec(self):
        tempsB = int(time.time())

        if self.tempsA != tempsB:
            self.joueur.nbPointsRune += (1 * self.rune)
            self.tempsA = tempsB


class Daim:
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
            case = self.parent.trouver_case(x1, y1)
            if case.montype != "plaine":
                pass
            self.x, self.y = x1, y1
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.cible = None
                self.position_visee = None
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

            if case.montype == "plaine" or case.montype == "foretnoire" or case.montype == "prairie":
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


class Biotope:
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
        self.valeur = 10.0


class Bleuets(Biotope):
    typeressource = ['bleuetsgros',
                     'bleuetspetit']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 20.0


class Champignons(Biotope):
    typeressource = ['champignonsgros',
                     'champignonspetit']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 15.0


class Caillous(Biotope):
    typeressource = ['caillous1',
                     'caillous2',
                     'caillous3']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100.0


class Pierre(Biotope):
    typeressource = ['pierre1']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 200.0


class Rocher(Biotope):
    typeressource = ['rocher1',
                     'rocher2']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 300.0


class Pin(Biotope):
    typeressource = ['pin']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 40.0


class Sapin(Biotope):
    typeressource = ['sapin']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 35.0


class Hetre(Biotope):
    typeressource = ['hetre']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 10.0


class Bouleau(Biotope):
    typeressource = ['bouleau']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 15.0


class Fleche:
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


class Javelot:
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
        self.vie = 100
        self.force = 5
        self.champvision = 100
        self.vitesse = 5
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
        self.vie -= force
        print("Ouch")
        if self.vie < 1:
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


class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20


class Archer(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "D"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible = None
        self.angle = None
        self.distancefeumax = 50
        self.distancefeu = 50
        self.delaifeu = 0
        self.delaifeumax = 30
        self.fleches = []
        self.cibleennemi = None

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
            fleche = Fleche(self, id, self.cibleennemi)
            self.fleches.append(fleche)
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
        self.ramassage = 0
        self.qteramassage = 1
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = 100
        self.champvisionmax = 800
        self.champchasse = 120
        self.delailoop = 25
        self.delaianim = self.delailoop / 5
        self.javelots = []
        self.vitesse = 5 + self.parent.chaussureniveau
        self.etats_et_actions = {"bouger": self.bouger,
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

    def chasser_ramasser(self, objetcible, sontype, actiontype):
        self.cible = objetcible
        self.typeressource = sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "daim" or self.typeressource == "framboises" or self.typeressource == "bleuets" or self.typeressource == "champignons" or self.typeressource == "ferme":
                    self.parent.mamaison.ressources["nourriture"] += self.ramassage
                elif self.typeressource == "hetre" or self.typeressource == "bouleau" or self.typeressource == "sapin" or self.typeressource == "pin":
                    self.parent.mamaison.ressources["bois"] += self.ramassage
                elif self.typeressource == "caillous" or self.typeressource == "pierre" or self.typeressource == "rocher":
                    self.parent.mamaison.ressources["pierre"] += self.ramassage
                else:
                    self.parent.mamaison.ressources[self.typeressource] += self.ramassage
                self.ramassage = 0
                if self.cible.valeur == 0:
                    if self.cible.montype == "ferme":
                        ravpossible = self.ravitaille_ferme(self.cible)
                        if ravpossible:
                            self.actioncourante = "ciblerressource"
                        else:
                            self.actioncourante = None
                    else:
                        rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
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

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        if reponse == "rendu":
            if self.typeressource == "daim" or self.typeressource == "eau":
                self.actioncourante = "ramasserressource"
        elif reponse <= self.champchasse and self.cible.etat == "vivant":
            self.actioncourante = "validerjavelot"

    def valider_javelot(self):
        self.lancer_javelot(self.cible)
        for i in self.javelots:
            i.bouger()

    def ramasser(self):
        if self.delailoop == 25:
            self.ramassage += self.qteramassage
            self.cible.valeur -= self.qteramassage
        print("valeur: ", self.cible.valeur)
        if self.cible.valeur == 0 or self.ramassage >= self.quota:
            self.actioncourante = "retourbatimentmere"
            self.position_visee = [self.batimentmere.x, self.batimentmere.y]
            if self.cible.valeur <= 0:
                if self.cible.montype != "ferme":
                    self.parent.avertir_ressource_mort(self.typeressource, self.cible)
                if self.cible.montype == "daim":
                    self.parent.ndaims -= 1
                elif self.cible.montype == "framboises" or self.cible.montype == "champignons" or self.cible.montype == "bleuets":
                    self.parent.nbuissons -= 1
            self.ramassage = int(self.ramassage)
        else:
            if self.delaianim == 5:
                self.y -= 5
            elif self.delaianim == 1:
                self.y += 5
            if self.delaianim > 0:
                self.delaianim -= 1
        self.delailoop -= 1
        if self.delailoop == 0:
            self.delailoop = 25
            self.delaianim = self.delailoop / 5

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
            if self.cible.sorte == "maison":
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

    def chercher_nouvelle_ressource(self, type, idreg):
        print("Je cherche nouvelle ressource")
        nb = len(self.parent.parent.biotopes[type])
        vision = self.champvision
        chercheressource = True
        while chercheressource:
            for i in range(nb):
                rep = random.choice(list(self.parent.parent.biotopes[type].keys()))
                obj = self.parent.parent.biotopes[type][rep]
                if obj != self.cible:
                    distance = Helper.calcDistance(self.x, self.y, obj.x, obj.y)
                    if distance <= vision:
                        chercheressource = False
                        return obj
            # si l'ouvrier ne trouve pas de la même ressource dans son champs de vision, il l'aggrandi jusqu'à un max.
            # Ca fait en sorte qu'il prendra les ressources plus près de lui en premier, règle générale.
            if chercheressource and vision < self.champvisionmax:
                vision += 50
            else:
                chercheressource = False
        print("Je n'ai pas trouvé de nouvelles ressources près de ma maison")
        return None

    def ravitaille_ferme(self, cible):
        print("Je tente de ravitailler la ferme")
        fermecible = cible
        if self.parent.mamaison.ressources["bois"] > 25:
            fermecible.valeur = 100
            self.parent.mamaison.ressources["bois"] -= 25
            return True
        else:
            print("ressources insuffisantes")
            return False

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
        self.ressources = {}
        self.x = x
        self.y = y
        self.montype = self.definirtyperegion(x,y)

    def definirtyperegion(self, x, y):
        if ((0 <= x < 20) or (60 < x <= 80)) and ((0 <= y < 20) or (60 < y <= 80)):
            return "plaine"
        elif (25 < x <= 55) and (25 < y <= 55):
            return "prairie"
        else:
            return "foretnoire"

class Joueur():
    classespersos = {"ouvrier": Ouvrier,
                     "soldat": Soldat,
                     "archer": Archer, }

    def __init__(self, parent, id, nom, couleur, x, y,nbPointsRune):
        self.parent = parent
        self.nom = nom
        self.id = id
        self.x = x
        self.y = y
        self.nbPointsRune = nbPointsRune
        self.couleur = couleur
        self.monchat = []
        self.stele = None
        self.chatneuf = 0
        self.ressourcemorte = []
        self.ressources = {}
        self.mamaison = None
        self.persos = {"ouvrier": {},
                       "soldat": {},
                       "archer": {},
                       "chevalier": {},
                       "druide": {},
                       "ingenieur": {},
                       "ballista": {}}

        self.batiments = {"maison": {},
                          "caserne": {},
                          "siteconstruction": {},
                          "forge": {},
                          "fournaise": {},
                          "ferme":{}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner,
                        "convertirpierre": self.convertir_pierre,
                        "creerarmes": self.creer_armes,
                        "creerarmures": self.creer_armures,
                        "creeroutils": self.creer_outils
                        }
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)

        self.nbuissons = self.parent.nbuissons
        self.ndaims = self.parent.ndaims

        self.outilsniveau = 0
        self.chaussureniveau = 0
        self.armesniveau = 0
        self.arumureniveau = 0

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
                                                           typeress, "ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        if typeress == "ferme":
                            self.persos[j][i].chasser_ramasser(self.batiments[typeress][idress],
                                                               typeress, "ciblerressource")
                        else:
                            self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        self.batiments["maison"][idmaison] = Maison(self, idmaison, self.couleur, x, y, "maison")
        self.mamaison = self.batiments["maison"][idmaison]

    def construire_batiment(self, param):
        perso, sorte, pos = param
        id = get_prochain_id()
        # payer batiment
        vals = Partie.valeurs
        for k, val in self.mamaison.ressources.items():
            if (self.mamaison.ressources[k] > 0 ):
                ok = True
                self.mamaison.ressources[k] = val - vals[sorte][k]
            else:
                ok = False
                break

        if (ok):
            siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte)
            self.batiments["siteconstruction"][id] = siteconstruction
            for i in perso:
                self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
                # self.persos["ouvrier"][i].construire_batiment(siteconstruction)

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
        batiment = self.batiments[batimentsource][idbatiment]

        x = batiment.x + 100 + (random.randrange(50) - 15)
        y = batiment.y + (random.randrange(50) - 15)

        self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                       sorteperso)

    def convertir_pierre(self, param):

        # n = self.parent.joueurs.keys()
        # for i in n:
        #     if i == self.nom:
        #         clemaison = self.parent.joueurs[i].batiments["maison"].keys()
        #         cle = list(clemaison)[0]
        #         maison = self.parent.joueurs[i].batiments["maison"][cle]
        nbressource = self.mamaison.ressources["pierre"]

        if nbressource >= 10:
            self.mamaison.ressources["metal"] += 1
            self.mamaison.ressources["pierre"] -= 10

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

    def creer_outils(self, param):
        batimentsource, idbatiment, pos = param
        id = get_prochain_id()
        batiment = self.batiments[batimentsource][idbatiment]
        listeOutils = ["hacheSilex", "piocheRamure", "hacheBronze", "piocheBronze", "hacheFer", "piocheFer"]
        choixOutil = random.choice(listeOutils)

        print(choixOutil)

    def upgrade(self, upgradetype):
        clemaison = self.batiments["maison"].keys()
        cle = list(clemaison)[0]
        maison = self.batiments["maison"][cle]

        if upgradetype == "Chaussure":
            maison.ressources["metal"] -= 1
            self.chaussureniveau += 1
        if upgradetype == "Armes":
            maison.ressources["metal"] -= 1
            self.armesniveau += 1
        if upgradetype == "Outils":
            maison.ressources["metal"] -= 1
            self.outilsniveau += 1
        if upgradetype == "Armures":
            maison.ressources["metal"] -= 1
            self.outilsniveau += 1

        for i in self.persos:
            for j in self.persos[i]:
                p = self.persos[i][j]
                p.vitesse = 5 + self.chaussureniveau
                p.force += self.armesniveau
                p.vie += (10 * self.arumureniveau)

                if p.montype == "ouvrier":
                    p.quota = 20 + (3 * self.outilsniveau)





#######################  LE MODELE est la partie #######################
class Partie():

    def cout(self, ressouces):
        nbressource = self.mamaison.ressources



    valeurs = {"maison": {"nourriture": 0,
                          "bois": 50,
                          "pierre": 0,
                          "metal": 0,
                          "delai": 10
                          },
               "caserne": {"nourriture": 0,
                           "bois": 50,
                           "pierre": 0,
                           "metal": 0,
                           "delai": 10
                           },
               "forge": {"nourriture": 0,
                         "bois": 50,
                         "pierre": 20,
                         "metal": 10,
                         "delai": 10
                         },
               "fournaise": {"nourriture": 0,
                             "bois": 50,
                             "pierre": 25,
                             "metal": 0,
                             "delai": 10
                             },
               "ferme":        {"nourriture": 0,
                             "bois": 50,
                             "pierre": 25,
                             "metal": 0,
                             "delai": 10
                             }
               }

    def __init__(self, parent, mondict):
        self.parent = parent
        self.actionsafaire = {}
        self.debut = int(time.time())
        self.aireX = 4000
        self.aireY = 4000
        # Decoupage de la surface
        self.taillecase = 50
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()

        self.delaiprochaineaction = 20

        self.nbuissons = 0
        self.maxbuissons = 20
        self.ndaims = 0
        self.maxdaims = 20

        self.joueurs = {}
        ###  reference vers les classes appropriées
        self.classesbatiments = {"maison": Maison,
                                 "caserne": Caserne,
                                 "forge": Forge,
                                 "fournaise": Fournaise,
                                 "ferme":Ferme}
        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat,
                              "archer": Archer}
        self.ressourcemorte = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.biotopes = {"daim": {},
                         "hetre": {},
                         "bouleau": {},
                         "pin": {},
                         "sapin": {},
                         "caillous": {},
                         "pierre": {},
                         "rocher": {},
                         "framboises": {},
                         "bleuets": {},
                         "champignons": {}
                         }

        self.regions = {}
        self.regionstypes = [["hetre", 20, 2, 1, "forest green"],
                             ["bouleau", 20, 2, 1, "forest green"],
                             ["pin", 100, 4, 2, "forest green"],
                             ["sapin", 75, 4, 2, "forest green"],
                             ["caillous", 15, 2, 1, "gray60"],
                             ["pierre", 15, 2, 1, "gray60"],
                             ["rocher", 15, 2, 1, "gray60"]
                             ]
        self.creer_regions()
        self.creer_biotopes()
        self.creer_population(mondict)

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
        # creer des daims éparpillés
        while self.ndaims < self.maxdaims:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine" or case.montype == "foretnoire" or case.montype == "prairie":
                id = get_prochain_id()
                mondaim = Daim(self, id, x, y)
                self.biotopes["daim"][id] = mondaim
                self.listebiotopes.append(mondaim)
                self.ndaims += 1

        self.creer_biotope("hetre", "hetre", Hetre)
        self.creer_biotope("pin", "pin", Pin)
        self.creer_biotope("sapin", "sapin", Sapin)
        self.creer_biotope("bouleau", "bouleau", Bouleau)
        self.creer_biotope("caillous", "caillous", Caillous)
        self.creer_biotope("pierre", "pierre", Pierre)
        self.creer_biotope("rocher", "rocher", Rocher)

    def creer_biotope(self, region, ressource, typeclasse):  # creation des forets
        typeressource = typeclasse.typeressource

        for cleregion in self.regions[region].keys():
            listecases = self.regions[region][cleregion].dicocases
            # for listecase in self.regions[region]:
            # nressource = random.randrange(int(len(listecases) / 3)) + int((len(listecases) / 5))
            if region == "sapin" or region == "pin":
                nressource = random.randrange(10, 30)
            else:
                nressource = random.randrange(1, 3)

            while nressource:
                # placer les ressources plus ou moins dans les bons biomes (types)
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
            nbrregion = reg[1]
            minregion = reg[2]
            randregion = reg[3]
            x = 0
            y = 0
            self.regions[nomregion] = {}
            for k in range(nbrregion):

                # placer la pierre dans la région "prairie"
                if nomregion == "pierre" or nomregion == "caillous" or nomregion == "rocher":
                    pasuneprairie = True
                    while pasuneprairie:
                        x = random.randrange(self.taillecarte)
                        y = random.randrange(self.taillecarte)
                        case = self.cartecase[y][x]
                        if case.montype == "prairie":
                            pasuneprairie = False

                # placer les conifères dans la foret noire
                elif nomregion == "pin" or nomregion == "sapin":
                    pasuneforet = True
                    while pasuneforet:
                        x = random.randrange(self.taillecarte)
                        y = random.randrange(self.taillecarte)
                        case = self.cartecase[y][x]
                        if case.montype == "foretnoire":
                            pasuneforet = False

                # on place le reste
                else:
                    pasuneplaine = True
                    while pasuneplaine:
                        x = random.randrange(self.taillecarte)
                        y = random.randrange(self.taillecarte)
                        case = self.cartecase[y][x]
                        if case.montype == "plaine":
                            pasuneplaine = False

                # calcule la largeur (x) et hauteur(y) de la region
                taillex = random.randrange(randregion) + minregion
                tailley = random.randrange(randregion) + minregion

                # vérifie que la region ne déborde pas vers l'extérieur du jeu
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
                        casereg = self.cartecase[y0 + i][x0 + j]
                        casereg.parent = newregion
                        dicoreg[casereg.id] = casereg

                newregion.dicocases = dicoreg
                self.regions[nomregion][id] = newregion

    def creer_population(self, mondict):
        couleurs = [["O", "orange"], ["R", "red"], ["B", "blue"], ["J", "yellow"], ["V", "lightgreen"]]
        # quadrants = [[[0, 0], [int(self.aireX / 2), int(self.aireY / 2)]],
        #              [[int(self.aireX / 2), 0], [self.aireX, int(self.aireY / 2)]],
        #              [[0, int(self.aireY / 2)], [int(self.aireX / 2), self.aireY]],
        #              [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]],
        #              [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]]]
        xQuadrants = int(self.aireX) / 6
        yQuadrants = int(self.aireY) / 6
        quadrants = [[xQuadrants, yQuadrants], [int(self.aireX - xQuadrants), yQuadrants],
                     [xQuadrants, int(self.aireY - yQuadrants)],
                     [int(self.aireX - xQuadrants), int(self.aireY - yQuadrants)]]
        tableauOrdreMap = [0, 1, 2, 3]
        b = 0
        for i in mondict:
            id = get_prochain_id()
            coul = couleurs.pop()
            # placer les joueurs dans des quandrants differents
            j = random.choice(tableauOrdreMap)
            tableauOrdreMap.remove(j)
            rune = 1
            runePoints = 0
            x = quadrants[j][b]
            y = quadrants[j][b + 1]
            self.joueurs[i] = Joueur(self, id, i, coul, x, y,runePoints)
            id = get_prochain_id()
            self.joueurs[i].stele = Stele(self,self.joueurs[i],id,rune,x+100,y+100)



    def deplacer(self):
        for i in self.joueurs:
            self.joueurs[i].deplacer()

    def jouer_prochain_coup(self, cadrecourant):
        self.ressourcemorte = []
        t = int(time.time())
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

        # demander aux objets de s'activer
        for i in self.joueurs.keys():
            self.joueurs[i].jouer_prochain_coup()
            self.joueurs[i].stele.incrementerPointsSec()

        if self.msggeneral and "cadre" not in self.msggeneral:
            self.msggeneralcompteur += 1
            if self.msggeneralcompteur == self.msggeneraldelai:
                self.msggeneral = ""
                self.msggeneralcompteur = 0
        else:
            msg = "cadre: " + str(cadrecourant) + " - secs: " + str(t - self.debut)
            self.msggeneral = msg

        self.renouveler_ressources_naturelles()

    def renouveler_ressources_naturelles(self):
        if self.delaiprochaineaction == 0:
            if self.nbuissons < self.maxbuissons:
                self.generer_buissons()
            if self.ndaims < self.maxdaims:
                self.generer_daims()
            self.delaiprochaineaction = 20
        else:
            self.delaiprochaineaction -= 1

    def generer_buissons(self):
        # On regénère les buissons si il y en a moins que le max sur la carte
        x = random.randrange(self.aireX)
        y = random.randrange(self.aireY)
        case = self.trouver_case(x, y)

            #Si la case est de type "prairie", la boucle while se répète sans incrémenter
        if case.montype == "plaine":
            if random.randrange(2) < 1:
                ressource = Champignons
                nom_ressource = "champignons"
            else:
                ressource = Framboises
                nom_ressource = "framboises"
            id = get_prochain_id()
            img = random.choice(ressource.typeressource)
            cette_ressource = ressource(self, id, img, x, y, nom_ressource)
            self.biotopes[nom_ressource][id] = cette_ressource
            self.nbuissons += 1
            print(self.nbuissons, " (+framboises)")
            self.parent.afficher_bio(cette_ressource)
        elif case.montype == "foretnoire":
            if random.randrange(2) < 1:
                ressource = Champignons
                nom_ressource = "champignons"
            else:
                ressource = Bleuets
                nom_ressource = "bleuets"
            id = get_prochain_id()
            img = random.choice(ressource.typeressource)
            cette_ressource = ressource(self, id, img, x, y, nom_ressource)
            self.biotopes[nom_ressource][id] = cette_ressource
            self.nbuissons += 1
            print(self.nbuissons, " (+bleuets)")
            self.parent.afficher_bio(cette_ressource)

    def generer_daims(self):
        # On ramene le nombre de daims au max si il y en a moins sur la carte
        x = random.randrange(self.aireX)
        y = random.randrange(self.aireY)
        case = self.trouver_case(x, y)
        if case.montype == "plaine" or case.montype == "foretnoire" or case.montype == "prairie":
            id = get_prochain_id()
            mondaim = Daim(self, id, x, y)
            self.biotopes["daim"][id] = mondaim
            self.listebiotopes.append(mondaim)
            self.ndaims += 1
            print(self.ndaims, " (+daim)")

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
            if (self.parent.cadrejeu - 1) > int(cadrecle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            action = ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle] = action
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
