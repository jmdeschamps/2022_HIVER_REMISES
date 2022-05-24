# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
# Jessica Chan, Mathieu Mailloux, Pierre-Olivier Parisien, Jacques Duymentz, Pierre Long Nguyen
import random
import math
import helper
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
        self.ressources = {"nourriture": self.taille * 1000 * random.randrange(1, 2),
                           "combustible": self.taille * 2000 * random.randrange(1, 2),
                           "materiaux": self.taille * 2000 * random.randrange(1, 2)}

        self.capacite_population = self.taille*1000
        self.alimentation = {"niv1": 0, "niv2": 0, "niv3": 0}
        self.science = {"niv1": 0, "niv2": 0, "niv3": 0}
        self.industrie = {"niv1": 0, "niv2": 0, "niv3": 0}
        self.habitation = {"niv1": 0, "niv2": 0, "niv3": 0}
        self.parc_immobilier = {"Alimentation": self.alimentation, "Science": self.science, "Industrie": self.industrie, "Habitation": self.habitation}

class Batiments():
    cout_construction = 100
    niveau = 1
    equipage = 100
    def __init__(self):
        pass
    def ameliorationBatiment(self):
        self.niveau += 1

class Alimentation(Batiments):
    cout_construction_m = 80
    cout_construction_p = 100
    niveau = 1
    bonus = 0.01
    def __init__(self):
        super().__init__()
        # ajoute l'augmentation de ressource / tour de jeu

class Science(Batiments):
    cout_construction_m = 100
    cout_construction_p = 100
    niveau = 1
    bonus = 10

    def __init__(self):
        super().__init__()
        # augment la quantité de science / tour de jeu

class Industrie(Batiments):
    cout_construction_m = 120
    cout_construction_p = 100
    niveau = 1
    bonus = 10

    def __init__(self):
        super().__init__()

class Habitation(Batiments):
    cout_construction_m = 80
    niveau = 1
    bonus = 10
    equipage = 0
    def __init__(self, parent):
        super().__init__()
        # augmente la limite de population
        self.parent = parent
        # self.parent.ressources["population"] += 100
        self.parent.population_inactive += 100

class Vaisseau():
    def __init__(self, parent, nom, x, y, mon_type="inconnu"):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.cout = 1
        self.x = x
        self.y = y
        self.rayon_vision = 80  # ...
        self.bonus_vision = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 1
        self.cible = 0
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte}
        # "Zone_attaque":self.arriver_zone_attaque}
        #self.espace_cargo = 0
        #self.chargement = 0
        self.retour_prevu = False
        self.revenu = False
        self.equipage = 10
        self.consommation_carburant = 2
        self.etoiles_visitees = []
        self.trous_visites = []
        self.mon_type = mon_type
        self.sante = 100

        # self.ressource_cible = self.parent.

    def jouer_prochain_coup(self, trouver_nouveau=0): # 0 est False

        if self.cible != 0:
            return self.avancer()

        elif self.mon_type == "Cargo":
            if self.cible_a_miner and self.ordre_de_miner:
                self.ordre_minage(self.parent.ressource_choisi)
            elif self.retour_prevu:
                self.acquerir_cible(self.parent.etoilemere, "Etoile")
                self.retour_prevu = False

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
        if self.mon_type == "Cargo":
            self.ordre_de_miner = True

    def avancer(self):
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                type_obj = type(self.cible).__name__
                rep = self.arriver[type_obj]()

                # Consomation du carburant en fonction de la distance parcourue (l'espace se deplace vers la droite)
                self.parent.ressources["combustible"] -= round(self.consommation_carburant * hlp.calcDistance(self.x, self.y, x, y))
                return rep

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])

        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire

            if len(self.parent.etoiles_controlees) >= 50:         # parent du vaisseau est le joueur

                self.parent.parent.executer_finpartie(self)  # vaisseau, joeur, partie self=vaisseau
                return 0
            #Recalcule de la capacite de population

            self.parent.population_limite = self.parent.etoilemere.capacite_population
            for i in self.parent.etoiles_controlees:
                self.parent.population_limite += i.capacite_population
            self.etoiles_visitees.append(self.cible)

        # devient pret pour miner les ressources de l'etoile conquise
        if self.mon_type == "Cargo":
            self.bonus_technologique_cargo()
            if self.cible.proprietaire == self.proprietaire:
                if self.cible != self.parent.etoilemere:
                    self.cible_a_miner = self.cible

        if self.cible == self.parent.etoilemere:
            self.revenu = True
            for i in self.etoiles_visitees:
                self.parent.etoiles_connues.append(i)
            for i in self.trous_visites:
                self.parent.trous_connus.append(i)
            self.etoiles_visitees = []
            self.trous_visites = []
            self.ordre_dechargement(self.parent.ressource_choisi)

            for etoile in self.parent.etoiles_controlees:
                self.parent.parent.parent.lister_planetes_conquises("Etoile", etoile.id)

        cible = self.cible
        self.cible = 0
        return ["Etoile", cible]

    def ordre_dechargement(self, ressource="combustible"):
        if self.mon_type == "Cargo" and self.parent.joueur_Active:
            # Decharge les ressource dans l'etoile mere
            self.parent.ressources[ressource] += self.chargement
            self.chargement = 0
            self.espace_cargo = self.max_capacite
        if self.parent.ressources["nourriture"] >= 1000000:
            self.parent.parent.executer_finpartie(self)

    def ordre_minage(self, ressource="combustible"):

        if self.ordre_de_miner:
            if self.espace_cargo > 0 and self.cible_a_miner.ressources[ressource] > 0:
                self.chargement += 50 + self.bonus_cargo
                self.espace_cargo -= 50 + self.bonus_cargo
                self.cible_a_miner.ressources[ressource] -= 50 + self.bonus_cargo

            else:
                self.ordre_de_miner = False

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
            self.trous_visites.append(cible)
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
            self.trous_visites.append(cible)
        self.cible = 0
        return ["Porte_de_ver", cible]

class Cargo(Vaisseau):
    cout = 150
    equipage = 80
    def __init__(self, parent, nom, x, y, mon_type):
        Vaisseau.__init__(self, parent, nom, x, y, mon_type)
        self.max_capacite = 2500
        self.espace_cargo = self.max_capacite
        self.chargement = 0
        self.type_chargement = ""
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
        self.cible = 0
        self.ang = 0
        self.rayon_vision = 50
        self.consommation_carburant = 4
        self.cout = 50
        self.equipage = 50
        self.cooldown_recolte = 500
        self.ordre_de_miner = True
        self.cible_a_miner = None
        self.sante = 100
        self.bonus_cargo = 0

    def bonus_technologique_cargo(self):
        self.bonus_cargo = 0
        for etoile in self.parent.etoiles_controlees:
            self.bonus_cargo += etoile.parc_immobilier["Industrie"]["niv1"] + 2 * etoile.parc_immobilier["Industrie"]["niv2"] \
                + 5 * etoile.parc_immobilier["Industrie"]["niv3"]
        return self.bonus_cargo

class Explorateur(Vaisseau):
    cout = 100
    equipage = 20
    def __init__(self, parent, nom, x, y, mon_type):
        Vaisseau.__init__(self, parent, nom, x, y, mon_type)
        self.energie = 200
        self.taille = 5
        self.vitesse = 4
        self.cible = 0
        self.ang = 0
        self.consommation_carburant = 1
        self.cout = Explorateur.cout
        self.equipage = Explorateur.equipage
        self.sante = 100

class Chasseur(Vaisseau):
    cout = 280
    equipage = 250
    def __init__(self, parent, nom, x, y, mon_type):
        Vaisseau.__init__(self, parent, nom, x, y, mon_type)
        self.x = x
        self.y = y
        self.energie = 1000
        self.taille = 6
        self.vitesse = 3
        self.cible = 0
        self.ang = 0
        self.rayon_vision = 50
        self.rayon_attaque = 100
        self.consomation_carburant = 2
        self.cout = Chasseur.cout
        self.equipage = Chasseur.equipage
        self.sante = 100
        self.ma_flotte = None
        self.max_cooldown = 100
        self.cooldown = 0
        self.autre_vaisseau = None

    def detecter_vaisseau_ennemi(self):
        mon_nom = self.parent.parent.parent.mon_nom
        self.ma_flotte = self.parent.flotte


        for nom_joueur in self.parent.parent.joueurs.keys():
            if nom_joueur != mon_nom:
                for type_vaisseau in self.parent.parent.joueurs[nom_joueur].flotte.keys():
                    for id_vaiss in self.parent.parent.joueurs[nom_joueur].flotte[type_vaisseau]:
                        autre_vaiss = self.parent.parent.joueurs[nom_joueur].flotte[type_vaisseau][id_vaiss]
                        distance = math.sqrt(math.pow(self.x-autre_vaiss.x, 2) + math.pow(self.y-autre_vaiss.y, 2))
                        if distance < self.rayon_attaque:
                            # self.attaque(autre_vaiss)
                            self.autre_vaisseau = autre_vaiss
                            self.attaque()

    def attaque(self):
        if self.cooldown == 0:
            self.parent.parent.missiles.append(Missile(self, self.autre_vaisseau))
            self.cooldown = self.max_cooldown
        else:
            self.cooldown -= 1
    # self.jouer_prochain_coup()
    #
    #
    # def jouer_prochain_coup(self):
    #     if self.cooldown == 0:
    #         self.parent.parent.missiles.append(Missile(self, self.autre_vaisseau))
    #         self.cooldown = self.max_cooldown
    #     else:
    #         self.cooldown -= 1


class Missile():
    def __init__(self, parent, vaisseau):
        self.vaisseau = vaisseau
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.demitaille = 4
        self.cible_atteinte = False
        self.vitesse = 5

    def suivre_vaisseau(self):
        distance = helper.Helper.calcDistance(self.x, self.y, self.vaisseau.x, self.vaisseau.y)
        angle = helper.Helper.calcAngle(self.x, self.y, self.vaisseau.x, self.vaisseau.y)
        point_cible = helper.Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        self.x, self.y = point_cible
        if distance < 5:
            self.cible_atteinte = True
        if self.cible_atteinte:
            if self.vaisseau.sante > 0:
                self.vaisseau.sante -= 5
            else:
                self.vaisseau.sante = 0

    def jouer_prochain_coup(self):
        self.suivre_vaisseau()

class Joueur():
    def __init__(self, parent, nom, etoilemere, couleur):
        self.b = None
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.etoiles_controlees = [etoilemere]
        self.flotte = {"Vaisseau": {},
                       "Cargo": {}, "Explorateur": {}, "Chasseur": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte,
                        "creerbatiment": self.creer_batiment,
                        "choix_ressource": self.choix_ressource,
                        "suivre_ennemi": self.suivre_ennemi}
        self.ressources = {"nourriture": 2000,
                           "combustible": 250,
                           "materiaux": 300,
                           "travailleur": 0}
        self.taux_croissance = 2
        # loop pour population limite des planetes
        self.population_limite = self.etoilemere.capacite_population
        self.population_inactive = self.population_limite-self.ressources["travailleur"]
        self.bonus_batiments_alimentation = 0
        self.vaisseaux_vus = []
        self.vaisseaux_disparus = []
        self.etoiles_connues = []
        self.etoiles_connues.append(etoilemere)
        self.trous_connus = []
        self.ressource_choisi = "combustible"
        self.joueur_Active = True
        self.nourriture_consommee_debase = 0
        self.bonus_rayon_chasseur = 0

    def bonus_batiment_espace_cargo(self):
        if self.etoilemere.parc_immobilier["Industrie"]["niv1"] >= 1:
            for cargo in self.flotte["Cargo"]:
                self.flotte["Cargo"][cargo].vitesse += 0.1
                self.flotte["Cargo"][cargo].sante += 10
        if self.etoilemere.parc_immobilier["Industrie"]["niv2"] >= 1:
            for cargo in self.flotte["Cargo"]:
                self.flotte["Cargo"][cargo].max_capacite += 100
        if self.etoilemere.parc_immobilier["Industrie"]["niv3"] >= 1:
            for cargo in self.flotte["Cargo"]:
                self.flotte["Cargo"][cargo].sante += 200
                self.flotte["Cargo"][cargo].max_capacite += 500


    def bonus_batiment_rayon(self):
        if self.etoilemere.parc_immobilier["Science"]["niv1"] >= 1:
            for chasseur in self.flotte["Chasseur"]:
                self.flotte["Chasseur"][chasseur].vitesse += 0.1
                self.flotte["Chasseur"][chasseur].sante += 15
            for explorateur in self.flotte["Explorateur"]:
                self.flotte["Explorateur"][explorateur].vitesse += 0.2
                self.flotte["Explorateur"][explorateur].sante += 5

        if self.etoilemere.parc_immobilier["Science"]["niv2"] >= 1 and self.etoilemere.parc_immobilier["Science"]["niv3"] == 0:
            for chasseur in self.flotte["Chasseur"]:
                self.flotte["Chasseur"][chasseur].rayon_vision = 150
                self.flotte["Chasseur"][chasseur].rayon_attaque = 150

        if self.etoilemere.parc_immobilier["Science"]["niv3"] == 1:
            for chasseur in self.flotte["Chasseur"]:
                self.flotte["Chasseur"][chasseur].rayon_vision = 250
                self.flotte["Chasseur"][chasseur].rayon_attaque = 200

        if self.etoilemere.parc_immobilier["Science"]["niv3"] >= 3:
            for chasseur in self.flotte["Chasseur"]:
                self.flotte["Chasseur"][chasseur].rayon_vision = 450
                self.flotte["Chasseur"][chasseur].rayon_attaque = 250


    def bonus_batiment_alimentation_taux(self):
        self.bonus_batiments_alimentation = 0
        for etoile in self.etoiles_controlees:
            self.bonus_batiments_alimentation += .02*etoile.parc_immobilier["Alimentation"]["niv1"] + 0.1 * etoile.parc_immobilier["Alimentation"]["niv2"] \
                + 0.5 * etoile.parc_immobilier["Alimentation"]["niv3"]

    def consommation_nourriture(self):
        self.bonus_batiment_alimentation_taux()
        self.nourriture_consommee = self.nourriture_consommee_debase + 0.00005 * self.population_limite
        self.ressources["nourriture"] -= self.nourriture_consommee - self.bonus_batiments_alimentation
        if self.ressources["nourriture"] <= 0:
            self.ressources["travailleur"] -= 0.01
            self.population_limite -= 0.01
            self.population_inactive -= 0.01
            self.ressources["nourriture"] = 0
            if self.population_inactive <= 0 or self.population_limite <= 0:
                self.ressources["travailleur"] = 0
                self.population_limite = 0
                self.population_inactive = 0

    def voir_vaisseaux(self):
        mon_nom = self.nom
        ma_flotte = self.flotte

        for type in ma_flotte.keys():
            for id_vaiss in ma_flotte[type].keys():
                vaiss = ma_flotte[type][id_vaiss]
                for nom_joueur in self.parent.joueurs.keys():
                    if nom_joueur != mon_nom:
                        for type_vaisseau in self.parent.joueurs[nom_joueur].flotte.keys():
                            for id_vaiss in self.parent.joueurs[nom_joueur].flotte[type_vaisseau]:
                                autre_vaiss = self.parent.joueurs[nom_joueur].flotte[type_vaisseau][id_vaiss]
                                distance = math.sqrt(math.pow(vaiss.x - autre_vaiss.x, 2) + math.pow(vaiss.y - autre_vaiss.y, 2))
                                if distance < 2000:
                                    if autre_vaiss not in self.vaisseaux_vus:
                                        self.vaisseaux_vus.append(autre_vaiss)
                                else:
                                    if autre_vaiss in self.vaisseaux_vus:
                                        self.vaisseaux_disparus.append(autre_vaiss)

        for i in self.vaisseaux_disparus:
            if i in self.vaisseaux_vus:
                self.vaisseaux_vus.remove(i)
        self.vaisseaux_disparus = []

    def choix_ressource(self, params):
        type_ressource = params[0]
        if type_ressource == 3:
            self.ressource_choisi = "materiaux"
        elif type_ressource == 2:
            self.ressource_choisi = "combustible"
        else:
            self.ressource_choisi = "nourriture"

    def creer_batiment(self, params):
        type_batiment = params[0]
        if type_batiment == "Alimentation":
            self.b = Alimentation()
        elif type_batiment == "Science":
            self.b = Science()
            self.bonus_batiment_rayon()
        elif type_batiment == "Industrie":
            self.b = Industrie()
            self.bonus_batiment_espace_cargo()
        elif type_batiment == "Habitation":
            self.b = Habitation(self)

        # Verifie si suffisament de ressource et de population
        if self.ressources["materiaux"] >= self.b.cout_construction_m and self.b.equipage <= self.population_inactive:
            self.ressources["materiaux"] -= self.b.cout_construction_m
            if type_batiment != "Habitation":
                self.population_inactive -= self.b.cout_construction_p
                self.ressources["travailleur"] += self.b.equipage
        for i in self.etoiles_controlees:
            if i.id == params[1]:
                batiment = i.parc_immobilier[type_batiment]
                if batiment["niv1"] < 3:
                    batiment["niv1"] += 1
                else:
                    batiment["niv1"] = 0
                    if batiment["niv2"] < 3:
                        batiment["niv2"] += 1
                    else:
                        batiment["niv2"] = 0
                        batiment["niv3"] += 1


        return self.b


    def creervaisseau(self, params):
        type_vaisseau = params[0]
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y, type_vaisseau)
        elif type_vaisseau == "Explorateur":
            v = Explorateur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y, type_vaisseau)
        elif type_vaisseau == "Chasseur":
            v = Chasseur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y, type_vaisseau)
        else:
            v = Vaisseau(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y, type_vaisseau)  # A effacer plus tard

        # Si suffisament de ressources - Payer cout du vaisseau
        if self.ressources["materiaux"] >= v.cout\
                and v.equipage <= self.population_inactive:
            self.ressources["materiaux"] -= v.cout
            self.ressources["travailleur"] += v.equipage
            self.population_inactive -= v.equipage
            # Ajoute le vaisseau dans la flotte
            self.flotte[type_vaisseau][v.id] = v

            if self.nom == self.parent.parent.mon_nom:
                self.parent.parent.lister_objet(type_vaisseau, v.id)
        else:
            return None
        return v

    def suivre_ennemi(self, params):
        nom_joueur, id_ennemi, id_mon_chasseur = params


    def ciblerflotte(self, params):
        idori, iddesti, type_cible, nom_joueur, retour_prevu = params
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

                # implémentatio du retour_prevu
                ori.retour_prevu = retour_prevu

        if ori:
            if type_cible == "Etoile":
                if self.etoilemere.id == iddesti:
                    ori.acquerir_cible(self.etoilemere, type_cible)
                    return
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

    def jouer_prochain_coup(self):
        self.avancer_flotte()

        self.consommation_nourriture()


        self.voir_vaisseaux()


        for i in self.flotte["Chasseur"]:
            self.flotte["Chasseur"][i].detecter_vaisseau_ennemi()


    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile":
                        if rep[1].proprietaire:
                            if rep[1].proprietaire != self.nom:
                                self.parent.joueurs[rep[1].proprietaire].etoiles_controlees.remove(rep[1])

                        if rep[1] not in self.etoiles_controlees:
                            self.etoiles_controlees.append(rep[1])
                            self.parent.parent.afficher_etoile(self.nom, rep[1])


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
        #             self.etoiles_controlees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Vaisseau"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1




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
        self.missiles = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)
        # Pour le cout de construction dans la vue
        self.batiment_alimentation = Alimentation
        self.batiment_science = Science
        self.batiment_industrie = Industrie
        self.batiment_habitation = Habitation
        self.cout_alimentation_m = Alimentation.cout_construction_m
        self.cout_alimentation_p = Alimentation.cout_construction_p
        self.cout_science_m = Science.cout_construction_m
        self.cout_science_p = Science.cout_construction_p
        self.cout_industrie_m = Industrie.cout_construction_m
        self.cout_industrie_p = Industrie.cout_construction_p
        self.cout_habitation_m = Habitation.cout_construction_m
        self.cout_cargo = Cargo.cout
        self.cout_equipage_cargo = Cargo.equipage
        self.cout_chasseur = Chasseur.cout
        self.cout_equipage_chasseur = Chasseur.equipage
        self.cout_explo = Explorateur.cout
        self.cout_equipage_explo = Explorateur.equipage

    def executer_finpartie(self, objet):
        self.parent.partie_en_cours = 0
        self.parent.avertir_findepartie(objet)

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

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
            etoile.ressources = {"nourriture": etoile.taille * 1000,
                                 "combustible": etoile.taille * 2000,
                                 "population": etoile.taille * 1000,
                                 "materiaux": etoile.taille * 1000}
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

        for i in self.missiles:
            i.jouer_prochain_coup()

        to_delete = []
        for missile in self.missiles:
            if missile.cible_atteinte:
                to_delete.append(missile)
        for missile in to_delete:
            self.missiles.remove(missile)


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