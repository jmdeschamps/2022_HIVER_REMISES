## - Encoding: UTF-8 -*-

import ast

import json
import random
from helper import Helper
from RTS_divers import *
import math
import time


# Choses dont les nom est à changer: Maison => Village
#                                     Abri => Ferme
#                              or et aurus => gold
#                                     mana => pv
#                                   parent => $nom_de_l'objet
class SiteConstruction():
    def __init__(self, parent, id, x, y, sorte, case):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.case = case
        self.sorte = sorte
        self.delai = Partie.valeurs[self.sorte]["delai"]
        self.or_par_seconde = 0
        self.zone_controle = []

    def decremente_delai(self):
        self.delai -= 1


class Batiment():
    def __init__(self, parent, id, x, y, case):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.case = case
        self.image = None
        self.montype = None
        # carte batiment n'est plus utiliser
        self.cartebatiment = []
        self.mana = 200
        self.zone_controle = []
        self.or_par_seconde = 0

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            self.parent.annoncer_mort_batiment(self)
            return 1


class Usineballiste(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype


class Maison(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype


class Abri(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.or_par_seconde = 0.5


class Caserne(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype, case):
        Batiment.__init__(self, parent, id, x, y, case)
        self.image = couleur[0] + "_" + montype
        self.montype = montype


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
    typeressource = ['arbre0grand',
                     'arbre0petit',
                     'arbre1grand',
                     'arbre2grand',
                     'arbresapin0grand',
                     'arbresapin0petit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 30


# À réutiliser plus tard, mais pas utile maintenant
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


class Ouvrier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.champvision = 400
        self.vitesse = 20
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "construirebatiment": self.construire_batiment,
                                 }

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def construire_batiment(self):
        self.cible.decremente_delai()
        if self.cible.delai <= 0:
            case = self.parent.partie.trouver_case(self.cible.x, self.cible.y)
            batiment = self.parent.partie.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte, case)
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

    # def deplacer(self,pos):
    #     self.position_visee = pos
    #     self.actioncourante = "bouger"
    #
    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme [object redacted]
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


    ## PAS UTILISER POUR LE MOMENT          
    def scanner_alentour(self):
        dicojoueurs = self.parent.controleur.joueurs
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


class Joueur:
    classespersos = {"ouvrier": Ouvrier,
                     "soldat": Soldat}
    ressources = {"Azteque": {"Or": 200},
                  "Congolaise": {"arbre": 200,
                                 "roche": 200,
                                 "Or": 888888888},
                  }

    def __init__(self, partie, id, nom, couleur, x, y):
        # un référence à object partie
        self.partie = partie

        # le nom du joueur
        self.nom = nom

        # un identifieur unique
        self.id = id

        # le x y de la premier maison du
        # joueur en px
        self.x = x
        self.y = y

        # la couleur que les bâtiment et les
        # perso du joueur seront
        self.couleur = couleur

        # la list de message de chat envoyer
        # par le joueur
        self.monchat = []

        # indique qu’il y a de nouveau
        # message
        self.chatneuf = 0

        # un conteur de tick qui se reset a chaque seconde
        # il sert a ajouter de l'or a toute les seconde
        self.cycle_delai = 0

        # la quantiter d'or du joueur
        self.Or = 200
        self.persos = {"ouvrier": {},
                       "soldat": {}}

        self.batiments = {"maison": {},
                          "abri": {},
                          "caserne": {},
                          "usineballiste": {},
                          "siteconstruction": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner}
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
        ennemi = self.partie.joueurs[nomjoueur].persos[sorte][idperso]
        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)
                    # j.attaquer(ennemi)

    def abandonner(self, param):
        # ajouter parametre nom de l'Abandonneux, et si c'est moi, envoyer une action
        # quitter au serveur et faire destroy
        msg = param[0]
        self.partie.montrer_msg_general(msg)

    def chatter(self, param):
        txt, envoyeur, receveur = param
        self.partie.joueurs[envoyeur].monchat.append(txt)
        self.partie.joueurs[receveur].monchat.append(txt)
        self.partie.joueurs[envoyeur].chatneuf = 1
        self.partie.joueurs[receveur].chatneuf = 1

    def avertir_ressource_mort(self, type, ress):
        for i in self.persos["ouvrier"]:
            self.persos["ouvrier"][i].abandonner_ressource(ress)  # ajouer libereressource
        self.partie.eliminer_ressource(type, ress)

    def chasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.partie.biotopes[typeress][idress],
                                                           typeress, "ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.partie.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        case = self.partie.trouver_case(x, y)
        self.batiments["maison"][idmaison] = Maison(self, idmaison, self.couleur, x, y, "maison", case)

        case = self.batiments["maison"][idmaison].case
        case.montype = "batiment"
        max = len(self.partie.cartecase) - 1  # 55
        min = 0
        print(case.x, case.y)

        # Affectation de la zone de controle
        for x in range(case.x - 2, case.x + 3):
            if x < min:
                x = min
            elif x > max:
                x = max
            for y in range(case.y - 2, case.y + 3):
                if y < min:
                    y = min
                elif y > max:
                    y = max
                if self.partie.cartecase[y][x] not in self.batiments["maison"][idmaison].zone_controle:
                    self.batiments["maison"][idmaison].zone_controle.append(self.partie.cartecase[y][x])

        print(self.batiments["maison"][idmaison].zone_controle)

    def construire_batiment(self, param):
        perso, sorte, pos = param
        id = get_prochain_id()
        case = self.partie.trouver_case(pos[0], pos[1])
        fail = 1

        for i in self.batiments:
            if i == "siteconstruction":
                pass
            else:
                for j in self.batiments[i]:
                    if case in self.batiments[i][j].zone_controle:
                        # payer batiment
                        vals = Partie.valeurs[sorte]
                        self.Or -= vals["Or"]

                        siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte, case)
                        self.batiments["siteconstruction"][id] = siteconstruction
                        for i in perso:
                            self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
                            # self.persos["ouvrier"][i].construire_batiment(siteconstruction)
                        fail = 0
        if fail:
            print("Vous ne contrôlez pas cette zone")

    def installer_batiment(self, batiment):
        # self.batiments['siteconstruction'].pop(batiment.id)
        self.partie.installer_batiment(self.nom, batiment)

    # transmet à tous ses persos de jouer
    def jouer_prochain_coup(self):
        for j in self.persos.keys():
            for i in self.persos[j].keys():
                self.persos[j][i].jouer_prochain_coup()

        self.cycle_delai += 1
        if self.cycle_delai >= 25:
            self.cycle_delai = 0
            for list_de_batiments in self.batiments.values():
                for batiment in list_de_batiments.values():
                    self.Or += batiment.or_par_seconde

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


#######################  LE MODELE est la partie #######################
class Partie():
    valeurs = {"maison": {
                          "Or": 20,
                          "delai": 50},
               "abri": {
                        "Or": 10,
                        "delai": 30},
               "caserne": {
                           "Or": 1,
                           "delai": 60},
               "usineballiste": {
                                 "Or": 1,
                                 "delai": 80},

               "ouvrier": {
                   "Or": 20,
               }

               }

    def __init__(self, controleur, mondict):
        self.controleur = controleur
        self.actionsafaire = {}
        self.debut = int(time.time())
        self.aireX = 4032
        self.aireY = 4032
        # Decoupage de la surface
        self.taillecase = 72
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()

        self.delaiprochaineaction = 20

        self.joueurs = {}
        ###  reference vers les classes appropriées
        self.classesbatiments = {"maison": Maison,
                                 "caserne": Caserne,
                                 "abri": Abri,
                                 "usineballiste": Usineballiste}
        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat}
        self.ressourcemorte = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.biotopes = {"arbre": {},
                         "roche": {},
                         "eau": {}}

        self.regions = {}
        self.regionstypes = [["arbre", 10, 7, 5, "forest green"],
                             ["eau", 3, 20, 12, "light blue"],
                             ["roche", 8, 5, 6, "gray60"], ]
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
        # x1, y1, x2, y2 =

        # cartebatiment = self.get_carte_bbox(x1, y1, x2, y2)
        # for i in cartebatiment:
        #    self.cartecase[i[1]][i[0]].montype = "batiment"
        # batiment.cartebatiment = cartebatiment
        # print(cartebatiment)

        case = batiment.case
        case.montype = "batiment"
        max = len(self.cartecase) - 1  # 55
        min = 0
        range_min = 1
        range_max = 2
        print(case.x, case.y)

        # Affectation de la zone de controle
        if batiment.montype == "maison":
            range_min = 2
            range_max = 3

        for x in range(case.x - range_min, case.x + range_max):
            if x < min:
                x = min
            elif x > max:
                x = max
            for y in range(case.y - range_min, case.y + range_max):
                if y < min:
                    y = min
                elif y > max:
                    y = max
                if self.cartecase[y][x] not in batiment.zone_controle:
                    batiment.zone_controle.append(self.cartecase[y][x])

        self.controleur.afficher_batiment(nomjoueur, batiment)

        print(batiment.zone_controle)

    def creer_biotopes(self):
        # self.creer_biotope("arbre", "arbre", Arbre)
        # self.creer_biotope("roche", "roche", Roche)
        self.creer_biotope("eau", "eau", Eau)

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
                # x = random.randrange(self.taillecase)
                # y = random.randrange(self.taillecase)
                # xa = (pos.x * self.taillecase) + x
                # ya = (pos.y * self.taillecase) + y

                # styleress = random.choice(typeressource)
                # id = get_prochain_id()
                # objet = typeclasse(self, id, styleress, xa, ya, ressource, cleregion, pos.id)
                # pos.ressources[id] = objet
                # self.biotopes[ressource][id] = (objet)
                # self.listebiotopes.append(objet)
                # pos.montype = ressource
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
                        self.cartecase[y0 + i][x0 + j].controleur = newregion
                        self.cartecase[y0 + i][x0 + j].montype = nomregion
                        # listereg.append(self.cartecase[y0+i][x0+j])
                        casereg = self.cartecase[y0 + i][x0 + j]
                        casereg.controleur = newregion
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
            t = int(time.time())
            msg = "cadre: " + str(cadrecourant) + " - secs: " + str(t - self.debut)
            self.msggeneral = msg

        self.faire_action_partie()

    def faire_action_partie(self):
        if self.delaiprochaineaction == 0:
            # self.produire_action()
            self.delaiprochaineaction = random.randrange(20, 30)
        else:
            self.delaiprochaineaction -= 1

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

        # if x < 0:
        #    x = 0
        # if y < 0:
        #    y = 0

        # if x > (self.aireX - 1):
        #    x = self.aireX - 1
        # if y > (self.aireY - 1):
        #    y = self.aireY - 1

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        # if cx != 0 and x % self.taillecase > 0:
        #    cx += 1

        # if cy != 0 and y % self.taillecase > 0:
        #    cy += 1

        # possible d'etre dans une case trop loin
        # if cx == self.taillecarte:
        #    cx -= 1
        # if cy == self.taillecarte:
        #    cy -= 1
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
            if (self.controleur.cadrejeu - 1) > int(cadrecle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            action = ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle] = action
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
