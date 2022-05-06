# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import random

import ast
from Id import *
from helper import Helper as hlp


class Porte_de_vers():
    def __init__(self, parent, x, y, couleur, taille):
        self.parent = parent
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.pulsemax = taille
        self.pulse = random.randrange(self.pulsemax)
        self.couleur = couleur

    def jouer_prochain_coup(self):
        self.pulse += 1
        if self.pulse >= self.pulsemax:
            self.pulse = 0

class ruin():
    def __init__(self, parent, x, y):
        def __init__(self, parent, x, y):
            self.id = get_prochain_id()
            self.parent = parent
            self.x = x
            self.y = y
            self.taille = random.randrange(4, 8)
            self.ressources = {"metal": self.taille * 100 * random.randrange(1, 2),
                               "combustible": self.taille * 200 * random.randrange(1, 2),
                               "eau": self.taille * 1000 * random.randrange(1, 2),
                               "materiaux": self.taille * 1000 * random.randrange(1, 2)}

class Trou_de_vers():
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup()
        self.porte_b.jouer_prochain_coup()


class Etoile():
    def __init__(self, parent, x, y):
        self.id = get_prochain_id()
        self.parent = parent
        self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.ressources = {"metal": self.taille * 1000 * random.randrange(1, 2),
                           "combustible": self.taille * 2000 * random.randrange(1, 2),
                           "eau": self.taille * 10000 * random.randrange(1, 2),
                           "materiaux": self.taille * 10000 * random.randrange(1, 2)}

        self.info_rapportee = False


class Vaisseau():
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.cout = 1 # cout a redefinir
        self.x = x
        self.y = y
        self.rayon_vision = 80  # ...
        self.rayon_attaque = 0
        self.espace_cargo = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte, }
        # "Zone_attaque":self.arriver_zone_attaque}

        self.retour_prevu = False

        self.revenu = False

        self.consommation_carburant = 2

        self.etoiles_visitees = []


    def jouer_prochain_coup(self, trouver_nouveau=0): # 0 est False
        if self.cible != 0:
            return self.avancer()

        elif self.cible == 0 and self.retour_prevu:
            cible = self.parent.etoilemere
            self.acquerir_cible(cible, "Etoile")
            self.retour_prevu = False

        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                type_obj = type(self.cible).__name__
                rep = self.arriver[type_obj]()

                #Consomation du carburant en fonction de la distance parcourue (l'espace se deplace vers la droite)
                self.parent.ressources["combustible"] -= round(self.consommation_carburant * hlp.calcDistance(self.x, self.y, x, y))
                print(self.parent.ressources["combustible"])
                print(hlp.calcDistance(self.x, self.y, x, y))
                print(self.consommation_carburant * hlp.calcDistance(self.x, self.y, x, y))
                return rep

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])

        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
            self.etoiles_visitees.append(self.cible)

        if self.cible == self.parent.etoilemere:
            self.revenu = True
            for i in self.etoiles_visitees:
                i.info_rapportee = True

        cible = self.cible

        self.cible = 0

        return ["Etoile", cible]

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]

    # def arriver_zone_attaque(self):
    #     self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant,"Porte", self.id, self.cible.id,])
    #     cible = self.cible
    #     trou=cible.parent
    #     if cible==trou.porte_a:
    #         self.x=trou.porte_b.x+random.randrange(6)+2
    #         self.y=trou.porte_b.y
    #     elif cible==trou.porte_b:
    #         self.x=trou.porte_a.x-random.randrange(6)+2
    #         self.y=trou.porte_a.y
    #     self.cible = 0
    #     return ["Porte_de_ver", cible]


class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargaison = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 7
        self.cible = 0
        self.ang = 0
        self.rayon_vision = 50
        self.rayon_attaque = 0
        self.consommation_carburant = 4
        self.cout = 50


class Eclaireur(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargaison = 100
        self.energie = 200
        self.taille = 5
        self.vitesse = 20
        self.cible = 0
        self.ang = 0
        self.rayon_attaque = 0
        self.consommation_carburant = 1
        self.cout = 10


class Chasseur(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargaison = 0
        self.energie = 1000
        self.taille = 5.5
        self.vitesse = 12
        self.cible = 0
        self.ang = 0
        self.rayon_vision = 50
        self.rayon_attaque = 50
        self.consomation_carburant = 2
        self.cout = 200

class Joueur():
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.info_rapportee = True
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.etoilescontrolees = [etoilemere]
        self.flotte = {"Vaisseau": {},
                       "Cargo": {}, "Eclaireur": {}, "Chasseur": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte}
        self.ressources = {"metal": 10000,
                           "combustible": 10000,
                           "eau": 10000,

                           "materiaux": 10001,
                           "population": 2}
        self.taux_croissance = 2

        # A definir la regle de croissance de la population
    def croissance_population(self):
        self.ressources["population"] += self.taux_croissance

        #"materiaux": 10001}
        self.batiments = {"creeralimentation": self.creer_alimentation,
                          "creerscience": self.creer_science,
                          "creerindustrie": self.creer_industrie
                          }

    def creer_alimentation(self):
        pass

    def creer_science(self):
        pass

    def creer_industrie(self):
        pass


    def creervaisseau(self, params):
        type_vaisseau = params[0]
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        elif type_vaisseau == "Eclaireur":
            v = Eclaireur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        elif type_vaisseau == "Chasseur":
            v = Chasseur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        else:
            v = Vaisseau(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)  # A effacer plus tard

        # Si suffisament de ressources - Payer cout du vaisseau
        if self.ressources["metal"] >= v.cout:
            self.ressources["metal"] -= v.cout
            # Ajoute le vaisseau dans la flotte
            self.flotte[type_vaisseau][v.id] = v

            if self.nom == self.parent.parent.mon_nom:
                self.parent.parent.lister_objet(type_vaisseau, v.id)
        else:
            return None
        return v

    def ciblerflotte(self, params):
        idori, iddesti, type_cible, retour_prevu = params
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

                # implémentatio du retour_prevu
                ori.retour_prevu = retour_prevu

        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:# =joueur.modele.etoiles???
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return

            elif type_cible == "Porte_de_ver":
                cible = None
                for j in self.parent.trou_de_vers:
                    if j.porte_a.id == iddesti:
                        cible = j.porte_a
                    elif j.porte_b.id == iddesti:
                        cible = j.porte_b
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return
            # elif type_cible == "Ruin": # Pierre - en progression
            #     for j in self.parent.ruin:
            #         if j.id == iddesti:
            #             ori.acquerir_cible(j, type_cible)
            #             return

            elif type_cible == "Vaisseau_etranger":
                print("Voulez-vous attaquer le vaisseau étranger ?")
                pass

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile":
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoilescontrolees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        self.etoilescontrolees.append(rep[1])
                        self.parent.parent.afficher_etoile(self.nom, rep[1])
                        print("ici")

                    elif rep[0] == "Porte_de_ver":
                        pass
                    elif rep[0] == "blablabla":
                        pass


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoilemere, couleur):
        Joueur.__init__(self, parent, nom, etoilemere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Vaisseau"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1

class Batiments():
    cout_construction = 10 #materiaux
    niveau = 1
    def __init__(self):
        pass

class Alimentation(Batiments):
    cout_construction = 8
    niveau = 1
    def __init__(self):
        super().__init__()

class Science(Batiments):
    cout_construction = 10
    niveau = 1
    def __init__(self):
        super().__init__()

class Industrie(Batiments):
    cout_construction = 12
    niveau = 1
    def __init__(self):
        super().__init__()


class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.ruin = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)
        # Pour le cout de construction dans la vue
        self.batiment_alimentation = Alimentation
        self.batiment_science = Science
        self.batiment_industrie = Industrie

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creer_ruin(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure

    def creeretoiles(self, joueurs, ias=0):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.etoiles.append(Etoile(self, x, y))
        # nombre de joueur et d'IA
        np = len(joueurs) + ias
        etoile_occupee = []
        while np:
            p = random.choice(self.etoiles)
            if p not in etoile_occupee:
                etoile_occupee.append(p)
                self.etoiles.remove(p)
                np -= 1

        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            etoile = etoile_occupee.pop(0)
            etoile.taille = 8
            etoile.ressources = {"metal": etoile.taille * 1000,
                                 "combustible": etoile.taille * 2000,
                                 "eau": etoile.taille * 10000,
                                 "materiaux": etoile.taille * 10000}
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
