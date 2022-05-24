import copy
import math
import random
import numpy as np

from CorpsCeleste import Etoile
from Id import get_prochain_id
from CapsuleInformation import CapsuleInformation
from Ressource import Energie
from Projectile import Projectile
from helper import Helper as hlp, Helper


'''
Les sous-classes de Vaisseau possède des listes en variable statique
de leurs upgrades potentiels selon leur niveau. La fonction accorder_niveau() est appelé
pour appliquer les changements aux vaisseaux.
'''
class Vaisseau:
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.ang = 0
        self.etoile_mere = self.parent.parent.joueurs[self.proprietaire].etoile_mere
        self.cible = 0
        self.niveau = 1
        self.energie = 100
        self.energie_max = 100
        self.consommation_energie = 1
        self.degat = 1
        self.taille = 5
        self.vitesse = 7
        self.hp = 100
        self.max_hp = 100
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {
            "Etoile": self.arriver_etoile,
            "PorteVers": self.arriver_porte,
        }
        self.limite_capsule = 1
        self.nombre_capsule_information = 0
        self.capsules = []
        self.projectiles = []
        self.est_cible_pour_attaque = False
        self.type_vaisseau = "Vaisseau"
        self.succes_de_degaine = .3
        self.theta = 0
        self.vitesse_rotation = 100  # < is fast
        self.dtheta = (2 * math.pi) / self.vitesse_rotation
        self.distance_minimale_pour_attaquer = 100
        self.reaction_defensive = 6

    def initialiser_valeurs(self):
        self.energie = self.energie_max
        self.hp = self.max_hp

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.est_cible_pour_attaque:
            if hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) <= self.distance_minimale_pour_attaquer:
                chance = random.random()
                if chance < .25:
                    self.x += self.reaction_defensive
                    self.y -= self.reaction_defensive
                elif chance < .5:
                    self.x += self.reaction_defensive
                    self.y += self.reaction_defensive
                elif chance < .75:
                    self.x -= self.reaction_defensive
                    self.y += self.reaction_defensive
                else:
                    self.x -= self.reaction_defensive
                    self.y -= self.reaction_defensive

                # défensive toujours à 100% occurence
                if self.cible != "Etoile":
                    projectile1 = Projectile(self, self.cible, True)
                    projectile2 = Projectile(self, self.cible, True)
                    self.projectiles.append(projectile1)
                    self.projectiles.append(projectile2)

                self.est_cible_pour_attaque \
                    = False if self.parent.parent.joueurs[self.__cible.proprietaire].isIa is True else True

        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):
        ##enlever energie au joueur lors du deplacement
        # if self.parent.energie.quantite > 0:
        #     self.parent.energie.quantite -= self.consommation_energie

            if self.cible != 0:
                x = self.cible.x
                y = self.cible.y
                self.x, self.y = hlp.getAngledPoint(
                    self.angle_cible, self.vitesse, self.x, self.y)
                if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                    type_obj = type(self.cible).__name__
                    rep = self.arriver[type_obj]()
                    return rep

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id,
             self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
            self.acquerir_capsule(self.cible)

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
        return ["PorteVers", cible]

    def acquerir_capsule(self, contenu):
        if len(self.capsules) < self.limite_capsule:
            self.capsules.append(CapsuleInformation(self, contenu))

    def verifier_tech(self):
        for tech in self.parent.technologies:
            if tech.nom == "Rage de vivre":
                tech.effet(self)


class Cargo(Vaisseau):
    # une [] dans dans le tuple statique 'niveaux' correspond à des attributs
    # dans cet ordre = energie_max, consommation_energie, vitesse, max_hp, degat,
    # limite_capsule, vitesse_extraction, slot_energie_capacite, slot_ressource_capacite
    niveaux = ([250, 1.5, 10.0, 115, 7, 1, 80, 80, 70],  # VITESSE DE PRÉSENTATION (10.0 == 1.0 (3ième))
               [275, 1.2, 1.2, 140, 10, 1, 60, 100, 85],
               [300, 1.0, 1.5, 175, 12, 2, 40, 130, 100])

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.taille = 6
        self.type = "Cargo"
        self.slot_energie_capacite = 0  # limite
        self.slot_energie = Energie(0)  # réservoir - toujours garder un objet Ressource qu'on modifie
        self.vitesse_extraction = 0  # < : + rapide temps de traitement d'extraction
        self.slot_ressource = None
        self.slot_ressource_capacite = 0  # limite quantité ressource
        self.cible_pour_extraction = None  # différence: la cible venant tout juste d'être extraite
        self.cible_en_cours_extraction = None  # différence: si la cible a encore des ressources pouvant être extraites
        self.temps_fin_traitement_extraction_energie = None
        self.est_cible_pour_attaque = False
        self.type_vaisseau = "Cargo"
        self.degat = 1
        self.accorder_niveau()
        self.verifier_tech()
        self.initialiser_valeurs()

    def accorder_niveau(self):
        valeurs_niveau = Cargo.niveaux[self.niveau - 1]
        self.energie_max = valeurs_niveau[0]
        self.consommation_energie = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.max_hp = valeurs_niveau[3]
        self.degat = valeurs_niveau[4]
        self.limite_capsule = valeurs_niveau[5]
        self.vitesse_extraction = valeurs_niveau[6]
        self.slot_energie_capacite = valeurs_niveau[7]
        self.slot_ressource_capacite = valeurs_niveau[8]

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.est_cible_pour_attaque:
            if hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) <= self.distance_minimale_pour_attaquer:
                chance = random.random()
                if chance < .25:
                    self.x += self.reaction_defensive
                    self.y -= self.reaction_defensive
                elif chance < .5:
                    self.x += self.reaction_defensive
                    self.y += self.reaction_defensive
                elif chance < .75:
                    self.x -= self.reaction_defensive
                    self.y += self.reaction_defensive
                else:
                    self.x -= self.reaction_defensive
                    self.y -= self.reaction_defensive

                # défensive toujours à 100% occurence
                if self.cible != "Etoile":
                    projectile1 = Projectile(self, self.cible, True)
                    projectile2 = Projectile(self, self.cible, True)
                    self.projectiles.append(projectile1)
                    self.projectiles.append(projectile2)

                self.est_cible_pour_attaque \
                    = False if self.parent.parent.joueurs[self.__cible.proprietaire].isIa is True else True

        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

        if self.cible_pour_extraction is None:
            if self.cible_en_cours_extraction is not None:
                self.parent.ciblerflotte([self.id, self.cible_en_cours_extraction.id, "Etoile"])
                self.cible_en_cours_extraction = None
        else:
            self.operer_extraction(self.parent.parent.parent.cadrejeu)

    def avancer(self):
        # if self.parent.energie.quantite > 0:
        #     self.parent.energie.quantite -= self.consommation_energie

            if self.cible != 0:
                x = self.cible.x
                y = self.cible.y
                self.x, self.y = hlp.getAngledPoint(
                    self.angle_cible, self.vitesse, self.x, self.y)
                if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                    type_obj = type(self.cible).__name__
                    rep = self.arriver[type_obj]()
                    return rep

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id,
             self.cible.proprietaire])

        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
            self.acquerir_capsule(self.cible)

        if self.cible.proprietaire == self.proprietaire:
            # Cargo est seul type vaisseau capable d'extraire energie + ressource depuis étoile
            # pour opérer extraction; étoile doit appartenir au joueur (self.cible.proprietaire == self.proprietaire)
            if self.slot_energie.quantite > 0 or self.slot_ressource is not None and self.slot_ressource.quantite > 0:
                self.deposer_extraction()  # Cargo se dirige automatiquement vers étoile mère
            else:
                self.cible_pour_extraction = self.verif_extraction_possible()

        cible = self.cible
        self.cible = 0

        return ["Etoile", cible]

    def verif_extraction_possible(self):
        cargo_peut_accumuler_energie = self.slot_energie.quantite < self.slot_energie_capacite
        cargo_peut_accumuler_ressource = \
            self.slot_ressource is not None and self.slot_ressource.quantite < self.slot_ressource_capacite
        etoile_contient_minimum_energie = self.cible.energie.quantite > 0

        etoile_contient_minimum_ressource = \
            self.cible.ressource.quantite > 0 if self.cible.ressource is not None else False

        if cargo_peut_accumuler_energie and etoile_contient_minimum_energie \
                or cargo_peut_accumuler_ressource and etoile_contient_minimum_ressource:
            return self.cible

        return None

    def operer_extraction(self, cadrejeu):
        if self.temps_fin_traitement_extraction_energie is None:
            self.temps_fin_traitement_extraction_energie = cadrejeu + self.vitesse_extraction

        if cadrejeu >= self.temps_fin_traitement_extraction_energie:
            print("Début de l'opération d'extraction")
            # ENERGIE
            # s'il reste de l'énergie sur l'étoile et que la capacité n'est pas atteinte
            if self.cible_pour_extraction.energie.quantite > 0:
                if self.slot_energie.quantite < self.slot_energie_capacite:
                    # le cargo peut emmagasiner de l'énergie
                    capacite_possible = self.slot_energie_capacite - self.slot_energie.quantite

                    # l'étoile a autant ou plus d'énergie que le cargo peut en charger
                    if capacite_possible <= self.cible_pour_extraction.energie.quantite:
                        # étoile fourni assez d'énergie
                        self.slot_energie.quantite += capacite_possible  # transfert d'énergie se fait d'un coup sec
                        self.cible_pour_extraction.energie.retrait_quantite(capacite_possible)

                        if capacite_possible < self.cible_pour_extraction.energie.quantite:
                            # on s'attend ici à ce que le Cargo revient pour finir la job
                            self.cible_en_cours_extraction = self.cible_pour_extraction
                    else:  # l'étoile a moins d'énergie que ce que le cargo peut charger
                        energie_restante = self.cible_pour_extraction.energie.quantite
                        # transfert d'énergie se fait d'un coup sec
                        self.slot_energie.quantite += \
                            self.cible_pour_extraction.energie.retrait_quantite(energie_restante)
            else:
                pass

            # RESSOURCE
            if self.cible_pour_extraction.ressource is not None:
                if self.cible_pour_extraction.ressource.quantite > 0:
                    if self.slot_ressource is None:
                        etoile_contient_ressource_au_dessus_capacite = \
                            self.cible_pour_extraction.ressource.quantite > self.slot_ressource_capacite
                        etoile_contient_autant_ressource_que_cargo_peut_posseder = \
                            self.cible_pour_extraction.ressource.quantite == self.slot_ressource_capacite
                        etoile_contient_moins_ressource_que_capacite_cargo = \
                            self.cible_pour_extraction.ressource.quantite < self.slot_ressource_capacite

                        if etoile_contient_ressource_au_dessus_capacite:  # >
                            quantite_extraite = \
                                self.cible_pour_extraction.ressource.retrait_quantite(self.slot_ressource_capacite)
                            self.slot_ressource = copy.deepcopy(self.cible_pour_extraction.ressource)
                            self.slot_ressource.set_quantite(quantite_extraite)
                            # on s'attend ici à ce que le Cargo revient pour finir la job
                            self.cible_en_cours_extraction = self.cible_pour_extraction
                        elif etoile_contient_autant_ressource_que_cargo_peut_posseder \
                                or etoile_contient_moins_ressource_que_capacite_cargo:  # == || <
                            self.slot_ressource = copy.deepcopy(self.cible_pour_extraction.ressource)
                            self.cible_pour_extraction.ressource = None
                    else:
                        pass

            cargo_doit_cibler_etoile_mere_pour_retour = self.__verifier_si_cargo_doit_retourner_vers_etoile_mere(
                self.cible_pour_extraction
            )

            if cargo_doit_cibler_etoile_mere_pour_retour:
                self.__cibler_etoile_mere_pour_retour_depot_ressource()

    def __verifier_si_cargo_doit_retourner_vers_etoile_mere(self, etoile):
        aucune_energie_restante_sur_etoile = etoile.energie is None or etoile.energie.quantite == 0
        aucune_ressource_restante_sur_etoile = etoile.ressource is None or etoile.ressource.quantite == 0
        pleine_capacite_quantite_energie \
            = self.slot_energie.quantite == self.slot_energie_capacite
        pleine_capacite_quantite_ressource \
            = self.slot_ressource_capacite == self.slot_ressource_capacite

        if aucune_energie_restante_sur_etoile or pleine_capacite_quantite_energie \
                and aucune_ressource_restante_sur_etoile or pleine_capacite_quantite_ressource:
            return True
        else:
            return False

    def __cibler_etoile_mere_pour_retour_depot_ressource(self):  # complétion de opération extraction
        self.cible = self.etoile_mere  # étoile mère devient la cible du Cargo

        self.parent.ciblerflotte([self.id, self.etoile_mere.id, "Etoile"])

        self.cible_pour_extraction = None
        self.temps_fin_traitement_extraction_energie = None

    def deposer_extraction(self):
        joueur = self.parent.parent.joueurs[self.proprietaire]

        quantite_depot_energie = self.slot_energie.quantite
        joueur.energie.ajout_quantite(quantite_depot_energie)
        self.slot_energie.quantite = 0

        if self.slot_ressource is not None:
            quantite_depot_ressource = self.slot_ressource.quantite
            joueur.ressources_possession[self.slot_ressource.nom].ajout_quantite(quantite_depot_ressource)
            self.slot_ressource = None


class Scout(Vaisseau):
    # une [] dans dans le tuple statique 'niveaux' correspond à des attributs
    # dans cet ordre = energie_max, consommation_energie, vitesse, max_hp, degat, limite_capsule
    niveaux = ([200, 1, 10.2, 75, 5, 2],  # VITESSE DE PRÉSENTATION (10.2 == 1.2 (3ième))
               [215, 0.8, 1.4, 85, 7, 3],
               [225, 0.5, 1.6, 100, 8, 4])

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.taille = 3
        self.type = "Scout"
        self.accorder_niveau()
        self.verifier_tech()
        self.initialiser_valeurs()

    def accorder_niveau(self):
        valeurs_niveau = Scout.niveaux[self.niveau - 1]
        self.energie_max = valeurs_niveau[0]
        self.consommation_energie = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.max_hp = valeurs_niveau[3]
        self.degat = valeurs_niveau[4]
        self.limite_capsule = valeurs_niveau[5]


class Spacefighter(Vaisseau):
    # une [] dans dans le tuple statique 'niveaux' correspond à des attributs
    # dans cet ordre = energie_max, consommation_energie, vitesse, max_hp, degat, limite_capsule
    niveaux = ([210, 1.2, 10.3, 100, 10, 1],  # VITESSE DE PRÉSENTATION (10.3 == 1.3 (3ième))
               [230, 1, 1.6, 125, 15, 1],
               [250, 0.8, 1.9, 150, 20, 1])

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.taille = 4
        self.type = "Spacefighter"
        self.actions = {
            "Vaisseau": self.attaquer_adversaire,
            "Cargo": self.attaquer_adversaire,
            "Scout": self.attaquer_adversaire,
            "Destroyer": self.attaquer_adversaire,
            "Colonisateur": self.attaquer_adversaire,
            "Spacefighter": self.attaquer_adversaire,
            "Etoile": self.se_positionner
        }
        self.types_vaisseaux_cibles = [
            "Vaisseau", "Cargo", "Scout"
            , "Destroyer", "Colonisateur", "Spacefighter"
        ]
        self.projectiles = []
        self.dans_rayon_attaque = False
        self.en_zone_attaque = False
        self.est_attaque = False
        self.succes_de_degaine = .5
        self.est_cible_pour_attaque = False
        self.type_vaisseau = "Spacefighter"
        self.degat = 3
        self.accorder_niveau()
        self.verifier_tech()
        self.initialiser_valeurs()

    def accorder_niveau(self):
        valeurs_niveau = Spacefighter.niveaux[self.niveau - 1]
        self.energie_max = valeurs_niveau[0]
        self.consommation_energie = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.max_hp = valeurs_niveau[3]
        self.degat = valeurs_niveau[4]
        self.limite_capsule = valeurs_niveau[5]

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible if cible is not self else 0
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.est_cible_pour_attaque:
            if hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) <= self.distance_minimale_pour_attaquer:
                chance = random.random()
                if chance < .25:
                    self.x += self.reaction_defensive
                    self.y -= self.reaction_defensive
                elif chance < .5:
                    self.x += self.reaction_defensive
                    self.y += self.reaction_defensive
                elif chance < .75:
                    self.x -= self.reaction_defensive
                    self.y += self.reaction_defensive
                else:
                    self.x -= self.reaction_defensive
                    self.y -= self.reaction_defensive

                # défensive toujours à 100% occurence
                if self.cible != "Etoile":
                    projectile1 = Projectile(self, self.cible, True)
                    projectile2 = Projectile(self, self.cible, True)
                    self.projectiles.append(projectile1)
                    self.projectiles.append(projectile2)

                self.est_cible_pour_attaque \
                    = False if self.parent.parent.joueurs[self.__cible.proprietaire].isIa is True else True

        if self.cible != 0:
            return self.avancer()

    def avancer(self):
        self.x, self.y = hlp.getAngledPoint(
            hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
            , self.vitesse
            , self.x
            , self.y
        )

        if type(self.cible).__name__ != "Etoile":
            if hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) <= self.distance_minimale_pour_attaquer:
                if self.theta == 0:
                    self.theta = Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y) * 100

                self.x = self.distance_minimale_pour_attaquer * math.cos(self.theta) + self.cible.x
                self.y = self.distance_minimale_pour_attaquer * math.sin(self.theta) + self.cible.y

                self.theta += self.dtheta

                self.en_zone_attaque = True
                type_obj = type(self.cible).__name__
                rep = self.actions[type_obj]()
                return rep
        else:
            if hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) <= self.distance_minimale_pour_attaquer:
                type_obj = type(self.cible).__name__
                rep = self.actions[type_obj]()
                return rep

    def attaquer_adversaire(self):
        self.parent.log.append(
            [
                "En train d'attaquer une cible :"
                , self.parent.parent.cadre_courant
                , "Flotte"
                , self.id
                , self.cible.id
                , self.cible.proprietaire
            ]
        )

        if self.est_cible_pour_attaque is False and self.cible != "Etoile":
            if random.random() < self.succes_de_degaine:
                projectile = Projectile(self, self.cible)
                self.projectiles.append(projectile)

        return ["Flotte", self.cible]

    def se_positionner(self):
        self.parent.log.append(
            [
                "Arrivé :"
                , self.parent.parent.cadre_courant
                , "Etoile"
                , self.id
                , self.cible.id
                , self.cible.proprietaire
            ]
        )

        cible = self.cible
        self.cible = 0

        return ["Etoile", cible]


class Destroyer(Vaisseau):
    # une [] dans dans le tuple statique 'niveaux' correspond à des attributs
    # dans cet ordre = energie_max, consommation_energie, vitesse, max_hp, degat, limite_capsule
    niveaux = ([275, 3, 6.8, 220, 20, 1],  # VITESSE DE PRÉSENTATION (06.8 == 0.8 (3ième))
               [300, 2.5, 1, 275, 30, 1],
               [350, 2.3, 1.1, 350, 40, 2])

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.taille = 4
        self.type = "Destroyer";
        self.accorder_niveau()
        self.verifier_tech()
        self.initialiser_valeurs()

    def accorder_niveau(self):
        valeurs_niveau = Destroyer.niveaux[self.niveau - 1]
        self.energie_max = valeurs_niveau[0]
        self.consommation_energie = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.max_hp = valeurs_niveau[3]
        self.degat = valeurs_niveau[4]
        self.limite_capsule = valeurs_niveau[5]


class Colonisateur(Vaisseau):
    # une [] dans dans le tuple statique 'niveaux' correspond à des attributs
    # dans cet ordre = energie_max, consommation_energie, vitesse, max_hp, degat, limite_capsule
    niveaux = ([400, 5.0, 05.7, 185, 7, 2],  # VITESSE DE PRÉSENTATION (05.7 == 0.7 (3ième))
               [500, 4.5, 0.8, 220, 9, 2],
               [600, 4.0, 1.0, 280, 12, 3])

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.taille = 4
        self.type = "Colonisateur";
        self.vitesse_colonisation = 300
        self.accorder_niveau()
        self.verifier_tech()
        self.initialiser_valeurs()

    def accorder_niveau(self):
        valeurs_niveau = Colonisateur.niveaux[self.niveau - 1]
        self.energie_max = valeurs_niveau[0]
        self.consommation_energie = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.max_hp = valeurs_niveau[3]
        self.degat = valeurs_niveau[4]
        self.limite_capsule = valeurs_niveau[5]
