## - Encoding: UTF-8 -*-

import ast

import json
import random
from helper import Helper
from RTS_divers import *
from RTS_batiments import *
import math
import time

from navigation import *
from RTS_valeurs import *
from RTS_persos import *

from typing import List

# Choses dont les nom est à changer: Maison => Village
#                                     Abri => Ferme
#                              or et aurus => gold
#                                     mana => life
#                                   parent => $nom_de_l'objet

# À réutiliser plus tard, mais pas utile maintenant


#######################  LE MODELE est la partie #######################
class Partie():
    def __init__(self, controleur, mondict: List[str]):
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
        self.classesbatiments = {"Village": Village,
                                 "Caserne": Caserne,
                                 "Ferme": Ferme,
                                 "Scierie": Scierie,
                                 "pecherie": Pecherie,
                                 "mine": Mine,
                                 "tour": Tour}
        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat}
        self.ressourcemorte = []
        self.batimentmort = []
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
        self.creer_population(mondict)

    # calc et affiche le nombre total de bâtiment et de perso
    def calc_stats(self):
        total = 0
        for i in self.joueurs:
            total += self.joueurs[i].get_stats()
        for i in self.biotopes:
            total += len(self.biotopes[i])
        self.montrer_msg_general(str(total))

    def montrer_msg_general(self, txt):
        self.msggeneral = txt

    # afficher le batiment et ajoute la zone de controle
    def installer_batiment(self, nomjoueur, batiment):
        # --------------------------------------------Raphael-----------------------------------------------------------
        case = batiment.case
        case.montype = "batiment"
        max = len(self.cartecase) - 1  # 55
        min = 0
        range_min = 1
        range_max = 2
        print(case.x, case.y)

        # Affectation de la zone de controle
        if batiment.montype == "Village":  # Si maison agrandie la ZdC à 2 cases de large
            range_min = 2
            range_max = 3

        for x in range(case.x - range_min, case.x + range_max):  # Se promène dans les cases autour du batiment (x)
            if x < min:  # empêche de sortir de la map et d'avoir une erreur
                x = min
            elif x > max:
                x = max
            for y in range(case.y - range_min, case.y + range_max):  # Se promène dans les cases autour du batiment (y)
                if y < min:  # empêche de sortir de la map et d'avoir une erreur
                    y = min
                elif y > max:
                    y = max
                if self.cartecase[y][
                    x] not in batiment.zone_controle:  # Si la case n'est pas dans la ZdC: ajoute la case
                    batiment.zone_controle.append(self.cartecase[y][x])

        self.controleur.afficher_batiment(nomjoueur, batiment)

        print(batiment.zone_controle)

    def ajouter_batiment_mort(self, batiment):
        caseX = batiment.case.x
        caseY = batiment.case.y
        self.cartecase[caseY][caseX].montype = batiment.caseinitiale
        self.batimentmort.append(batiment)

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
        self.batimentmort = []
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
            self.cartecase.append(t1)
            for j in range(taille):
                id = get_prochain_id()
                t1.append(Caseregion(self, self.cartecase, id, j, i))

    def trouver_case(self, x, y):
        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)

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


class Region():
    def __init__(self, partie: Partie, id, x:int , y:int, taillex:int, tailley:int, montype):
        self.partie = partie
        self.id = id
        self.debutx = x
        self.taillex = taillex
        self.debuty = y
        self.tailley = tailley
        self.montype = montype
        self.dicocases = {}


class Caseregion:
    def __init__(self, partie, carte_case, id, x, y):
        self.partie = partie
        self.carte_case = carte_case
        self.id = id
        self.adjacent = set([])
        self.montype = "plaine"
        self.ressources = {}
        self.x = x
        self.y = y

        # FAB: code pour pathfinding ------------------------------------------
        if self.x >= 1:
            case = self.carte_case[y][x - 1]
            case.adjacent.add((self, 1))
            self.adjacent.add((case, 1))
        if self.y >= 1:
            case = self.carte_case[y - 1][x]
            case.adjacent.add((self, 1))
            self.adjacent.add((case, 1))
        if self.x >= 1 and self.y >= 1:
            case = self.carte_case[y - 1][x - 1]
            case.adjacent.add((self, math.sqrt(2)))
            self.adjacent.add((case, math.sqrt(2)))

    # fab todo to doc
    def pathfinding(self, pos_x, pos_y, target_x, target_y):
        start = self
        goal = self.partie.trouver_case(target_x, target_y)

        return A_Star(self.carte_case, start, goal, pos_x, pos_y)

    # fab todo to doc
    def get_ajacent(self):
        return filter(lambda case: case[0].montype != "eau", self.adjacent)

    # fab todo to doc
    def centre(self):
        x = self.x * self.partie.taillecase
        y = self.y * self.partie.taillecase
        return x, y

    # fab todo to doc
    def caculate_waypoint(self, from_x, from_y):
        x1 = self.centre()[0] + (self.partie.taillecase / 2)
        x0 = self.centre()[0] - (self.partie.taillecase / 2)

        y1 = self.centre()[1] + (self.partie.taillecase / 2)
        y0 = self.centre()[1] - (self.partie.taillecase / 2)

        if from_x > x1:
            to_x = x1
        elif from_x < x0:
            to_x = x0
        else:
            to_x = from_x

        if from_y > y1:
            to_y = y1
        elif from_y < y0:
            to_y = y0
        else:
            to_y = from_y

        return to_x, to_y

    # fab todo to doc
    def h(self, target_x, target_y):
        x, y = self.centre()
        return Helper.calcDistance(x, y, target_x, target_y)


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

        self.batiments = {"Village": {},
                          "Ferme": {},
                          "Caserne": {},
                          "Tour": {},
                          "siteconstruction": {},
                          "Scierie": {},
                          "Pecherie": {},
                          "Mine": {}
                          }

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        }
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)

    # return la somme des batiment et des perso du joueur
    def get_stats(self):
        total = 0
        for i in self.persos:
            total += len(self.persos[i])
        for i in self.batiments:
            total += len(self.batiments[i])
        return total

    # supprime le perso
    def annoncer_mort(self, perso):
        mort = False
        for id in self.persos[perso.montype]:
            if perso.id == id:
                mort = True
        if mort:
            self.persos[perso.montype].pop(perso.id)

    # supprime le batiment
    def annoncer_mort_batiment(self, batiment):
        mort = False
        for id in self.batiments[batiment.montype]:
            if batiment.id == id:
                mort = True
        if mort:
            self.partie.ajouter_batiment_mort(batiment)
            self.batiments[batiment.montype].pop(batiment.id)

    # apple la fonction attaquer du perso concerné
    def attaquer(self, param):
        attaquants, attaque = param
        nomjoueur, idperso, sorte = attaque
        ennemi = self.partie.joueurs[nomjoueur].persos[sorte][idperso]
        for perso in self.persos.keys():
            for attaquant in attaquants:
                if attaquant in self.persos[perso]:
                    self.persos[perso][attaquant].attaquer(ennemi)

    # ajouter un msg de chat
    def chatter(self, param):
        txt, envoyeur, receveur = param
        self.partie.joueurs[envoyeur].monchat.append(txt)
        self.partie.joueurs[receveur].monchat.append(txt)
        self.partie.joueurs[envoyeur].chatneuf = 1
        self.partie.joueurs[receveur].chatneuf = 1

    # apple la méthode deplacer des perso concerné
    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    # creer le village initial
    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        case = self.partie.trouver_case(x, y)
        self.batiments["Village"][idmaison] = Village(self, idmaison, self.couleur, x, y, "Village", case)

        case = self.batiments["Village"][idmaison].case
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
                if self.partie.cartecase[y][x] not in self.batiments["Village"][idmaison].zone_controle:
                    self.batiments["Village"][idmaison].zone_controle.append(self.partie.cartecase[y][x])

        print(self.batiments["Village"][idmaison].zone_controle)

    # ROBB: methode verifie si la construction se trouve dans la zone de controle
    def verification_zone_controle(self, case):
        for type_batiment, batiment_list in self.batiments.items():
            if type_batiment != "siteconstruction":
                for batiment in batiment_list.values():
                    if case in batiment.zone_controle:
                        return True
        return False

    # FAB: methode qui verifi si on a asser d'or et qui retire l'or
    def paiement_batiment(self, sorte):
        vals = valeurs[sorte]
        if self.Or >= vals["Or"]:
            self.Or -= vals["Or"]
            return True
        return False

    def verif_type_case_zdc(self, type_case:str, case):  # ROBB: zdc = ZONE DE CONTROLE
        for x in range(case.x - 1, case.x + 2):
            for y in range(case.y - 1, case.y + 2):
                case_verifiee = self.partie.cartecase[y][x]
                if case_verifiee is not case:
                    if case_verifiee.montype == type_case:
                        return True
        return False

    def check_cases(self, sorte, case, perso, pos):
        if self.verif_type_case_zdc(batiments_ressources[sorte]['ressources'], case):
            if self.verification_zone_controle(case):
                if self.paiement_batiment(sorte):
                    siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte, case)
                    self.batiments["siteconstruction"][id] = siteconstruction
                    for i in perso:
                        print("id", i)
                        self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
                return

    def construire_batiment(self, param):
        persos, sorte, pos = param
        id = get_prochain_id()
        case = self.partie.trouver_case(pos[0], pos[1])  # ROBB: METHODE TROUVE POS CAS EXACT BASEE SUR PIXEL
        if case.montype != "batiment":
            # ROBB: SCIERIE aide a voir si foret autour pour or(currency)
            if sorte in batiments_ressources.keys():
                self.check_cases(sorte, case, persos, pos)
            else:
                if self.verification_zone_controle(case):
                    # ROBB: verification si joueur peut se permettre batiment avec balance courante d'or
                    if self.paiement_batiment(sorte):
                        siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte, case)
                        self.batiments["siteconstruction"][id] = siteconstruction
                        for perso in persos:
                            self.persos["ouvrier"][perso].construire_site_construction(siteconstruction)
                            break
                        return

    def installer_batiment(self, batiment):
        self.partie.installer_batiment(self.nom, batiment)

    # transmet à tous ses persos de jouer
    def jouer_prochain_coup(self):
        for j in self.persos.keys():
            for i in self.persos[j].keys():
                self.persos[j][i].jouer_prochain_coup()

        for i in self.batiments["Tour"].keys():
            self.batiments["Tour"][i].jouer_prochain_coup()

        self.cycle_delai += 1
        if self.cycle_delai >= 25:
            self.cycle_delai = 0
            for list_de_batiments in self.batiments.values():
                for batiment in list_de_batiments.values():
                    self.Or += batiment.or_par_seconde

    def creer_perso(self, param):
        sorteperso, batimentsource, idbatiment, pos = param
        if self.Or < valeurs[sorteperso]["Or"]:
            pass
        else:
            id = get_prochain_id()
            batiment = self.batiments[batimentsource][idbatiment]

            x = batiment.x + 100 + (random.randrange(50) - 15)
            y = batiment.y + (random.randrange(50) - 15)

            self.Or -= valeurs[sorteperso]["Or"]

            self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                           sorteperso)



