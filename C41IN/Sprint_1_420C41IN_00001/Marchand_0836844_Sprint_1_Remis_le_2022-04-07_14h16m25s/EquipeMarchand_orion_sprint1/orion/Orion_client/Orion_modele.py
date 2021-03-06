# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import random

import ast
from Id import *
from helper import Helper as hlp
from Joueur import *
from CorpsCeleste import *
from Ressource import *
from Vaisseau import *
from TrouVers import *


class Modele:
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.ressources_pouvant_exister_sur_etoile = {  # "NOM_RESSOURCE": (Initialisateur, taux_rarete)
            Nourriture.nom: (Nourriture(random.randrange(10, 1001)), Nourriture.taux_rarete),
            Eau.nom: (Eau(random.randrange(10, 1001)), Eau.taux_rarete),
            Fer.nom: (Fer(random.randrange(10, 1001)), Fer.taux_rarete),
            Titanium.nom: (Titanium(random.randrange(10, 1001)), Titanium.taux_rarete),
            Cuivre.nom: (Cuivre(random.randrange(10, 1001)), Cuivre.taux_rarete)
        }
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 2)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(TrouVers(x1, y1, x2, y2))

    def creeretoiles(self, joueurs, ias=0):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.etoiles.append(Etoile(self, x, y))
        etoiles_meres_a_distribuer = len(joueurs) + ias
        etoile_occupee = []
        while etoiles_meres_a_distribuer:
            etoile = random.choice(self.etoiles)
            if etoile not in etoile_occupee:
                etoile_occupee.append(etoile)
                #self.etoiles.remove(p)
                etoiles_meres_a_distribuer -= 1

        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            etoile = etoile_occupee.pop(0)
            etoile.habitable = True
            self.joueurs[i] = Joueur(self, i, etoile, couleurs.pop(0))
            x = etoile.x
            y = etoile.y
            dist = 500
            for e in range(5):
                x1 = random.randrange(x - dist, x + dist)
                y1 = random.randrange(y - dist, y + dist)
                self.etoiles.append(Etoile(self, x1, y1))

        # IA- creation des ias
        couleursia = ["orange", "green", "cyan",
                      "SeaGreen1", "turquoise1", "firebrick1"]
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), etoile_occupee.pop(0), couleursia.pop(0))

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demand??e par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet repr??sentant le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for i in self.joueurs:
            self.joueurs[i].jouer_prochain_coup()

        # NOTE si le modele (qui repr??sente l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

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
