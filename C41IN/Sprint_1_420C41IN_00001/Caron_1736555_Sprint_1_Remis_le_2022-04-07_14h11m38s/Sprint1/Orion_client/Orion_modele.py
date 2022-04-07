# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import ast
from systeme_solaire import *
from map import *
from vaisseau import *
from skillcheck import *
import random


class Joueur():

    def __init__(self, parent, nom, systeme_mere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.systeme_mere = systeme_mere
        self.systeme_mere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []  # le log des systemes visiter
        self.systemes_controlees = [systeme_mere]
        self.flotte = {"Vaisseau": {},
                       "Cargo": {}}
        self.actions = {"creerbien": self.creer_bien,
                        "ciblerflotte": self.ciblerflotte,
                        "conquete": self.conquete
                        }
        # ressources de départ
        self.ressources = {"moral": 50,
                           "nourriture": 150,
                           "or": 10000000,
                           "fer": 55,
                           "cuivre": 86,
                           "titanite": 140971,
                           "uranium": 593,
                           "hydrogene": 35,
                           "azote": 23,
                           "xenon": 2358,
                           "energie": 2023,
                           "population": "On est tous des rebelles"
                           }
        self.bonus = {
            "conquete": 25,
            "voyage": 20  # chance de se faire attaquer en voyagant
        }

        self.bien_production = {
            "Vaisseau": [Vaisseau, {"titanite": 50, "fer": 25, "hydrogene": 5}, 20],
            "Cargo": [Cargo, {"titanite": 50, "fer": 25, "hydrogene": 5}, 20]
        }

    def creer_bien(self, params):
        type = self.bien_production[params[0]]
        self.systeme_mere.produire_bien(type)

    def conquete(self, params):
        joueur, idorigine, idvaisseau, idcible, type_cible = params
        data = [idorigine, idcible, type_cible]
        self.ciblerflotte(data)
        self.avancer_flotte()

        if cible.proprietaire == "":  # si la planète n'est pas habité
            defendant = None
        else:  # si la planète n'est pas habité
            defendant = cible

        # skillcheck = SkillCheck(joueur, defendant)
        # if skillcheck.gagnant_versus == joueur:
        # cible.proprietaire = self.nom  # victoire
        # else:
        # pass  # defaite

    def ciblerflotte(self, cibles):
        id_original, id_destination, type_cible = cibles
        original = None
        for type_vaisseaux in self.flotte.keys():
            if id_original in self.flotte[type_vaisseaux]:
                original = self.flotte[type_vaisseaux][id_original]

        if original:
            if type_cible == "SystemeSolaire":
                for systeme in self.parent.systemes:
                    if systeme.id == id_destination:
                        original.acquerir_cible(systeme, type_cible)
                        return
            elif type_cible == "Porte_de_ver":
                cible = None
                for vers in self.parent.trou_de_vers:
                    if vers.porte_a.id == id_destination:
                        cible = vers.porte_a
                    elif vers.porte_b.id == id_destination:
                        cible = vers.porte_b
                    if cible:
                        original.acquerir_cible(cible, type_cible)
                        return

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        for type_vaisseau in self.flotte:
            for vaisseau in self.flotte[type_vaisseau]:
                vaisseau = self.flotte[type_vaisseau][vaisseau]
                reponse = vaisseau.jouer_prochain_coup(chercher_nouveau)
                if reponse:
                    if reponse[0] == "SystemeSolaire":
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoilescontrolees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        self.systemes_controlees.append(reponse[1])
                        self.parent.parent.afficher_systemes(self.nom, reponse[1])
                    elif reponse[0] == "Porte_de_ver":
                        pass

    def get_usines(self):
        usines = self.systeme_mere.infrastructures[Usine]
        return usines


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, systeme_mere, couleur):
        Joueur.__init__(self, parent, nom, systeme_mere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20
        self.systeme_mere.proprietaire = self.nom
        self.systeme_mere.infrastructures[Usine].append(Usine(self, "usine"))

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creer_bien(["Vaisseau"])
            cible = random.choice(self.parent.systemes)
            if v != None:
                v.acquerir_cible(cible, "SystemeSolaire")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1


# ---------------------------------------------------------------------------------------------#

class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_systeme = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.systemes = []
        self.systemes_occupees = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creer_systemes()
        self.creer_joueurs(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

    def creer_systemes(self):
        bordure = 10
        for i in range(self.nb_systeme):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.systemes.append(SystemeSolaire(self, x, y))

    def creer_joueurs(self, joueurs, ias):
        np = len(joueurs) + ias
        systemes_temp = []
        while np:
            p = random.choice(self.systemes)
            if p not in systemes_temp:
                systemes_temp.append(p)
                np -= 1
        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            systeme = systemes_temp.pop(0)
            self.systemes_occupees.append(systeme)
            self.joueurs[i] = Joueur(self, i, systeme, couleurs.pop(0))
            systeme.infrastructures[Usine].append(Usine(systeme, "usine"))
            systeme.proprietaire = self.joueurs[i].nom
            #Ajoute 5 planètes autour de la planète d'origine
            x = systeme.x
            y = systeme.y
            dist = 500
            for e in range(5):
                x1 = random.randrange(x - dist, x + dist)
                y1 = random.randrange(y - dist, y + dist)
                self.systemes.append(SystemeSolaire(self, x1, y1))


        # IA- creation des ias
        couleursia = ["orange", "green", "cyan",
                      "SeaGreen1", "turquoise1", "firebrick1"]
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), systemes_temp.pop(0), couleursia.pop(0))

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet représentant le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for i in self.joueurs:
            self.joueurs[i].jouer_prochain_coup()

        # NOTE si le modele (qui représente l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()

    #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, actionsrecues):
        cadrecle = None
        for i in actionsrecues:
            cadrecle = i[0]
            if cadrecle:
                if (self.parent.cadrejeu - 1) > int(cadrecle):
                    print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                action = ast.literal_eval(i[1])

                if cadrecle not in self.actions_a_faire.keys():
                    self.actions_a_faire[cadrecle] = action
                else:
                    self.actions_a_faire[cadrecle].append(action)
    # NE PAS TOUCHER - FIN
##############################################################################

    def productions(self):
        for systeme in self.systemes_occupees:
            systeme.productions()
