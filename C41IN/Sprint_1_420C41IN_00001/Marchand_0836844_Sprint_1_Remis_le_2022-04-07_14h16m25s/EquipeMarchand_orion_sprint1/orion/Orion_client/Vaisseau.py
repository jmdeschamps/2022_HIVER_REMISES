import copy
import random

from CorpsCeleste import Etoile
from Id import get_prochain_id
from CapsuleInformation import CapsuleInformation
from Ressource import Energie
from helper import Helper as hlp


class Vaisseau:
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.type = None
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.ang = 0
        self.espace_cargo = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {"Etoile": self.arriver_etoile,
                        # "PlaneteMere": self.arriver_planete,
                        "Porte_de_vers": self.arriver_porte}
        self.limite_capsule = 1
        self.capsules = []
        self.hp = 0
        self.attaque = 1


    def jouer_prochain_coup(self, trouver_nouveau=0):
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
        return ["Porte_de_ver", cible]

    def acquerir_capsule(self, contenu):
        if len(self.capsules) < self.limite_capsule:
            self.capsules.append(CapsuleInformation(self, contenu))

    # vérifier planète maison la plus proche pour retour pour dépôt de ressources
    def verifier_retour(self, localisation_actuelle):
        etoiles_controlees = self.parent.etoiles_controlees
        distances_etoiles = []
        for etoile in etoiles_controlees:
            distances_etoiles.append(
                [
                    hlp.calcDistance(
                        etoile.x,
                        etoile.y,
                        localisation_actuelle.x,
                        localisation_actuelle.y
                    ),
                    etoile
                ]
            )

        distances = []
        etoiles = []
        indexes = []
        for index, distance_etoile in enumerate(distances_etoiles):
            distances.append(distance_etoile[0])
            etoiles.append(distance_etoile[1])
            indexes.append(index)

        aggregat = []
        for distance_par_etoile in zip(distances, etoiles):
            aggregat.append(distance_par_etoile)

        distance_moindre = min(distances)
        for information in aggregat:
            if information[0] == distance_moindre:
                print("Planète la plus proche:", information[1])
                return information[1]  # retourner la planète la plus proche

class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.taille = 6
        self.vitesse = 10
        self.hp = 200
        self.slot_energie_capacite = 100  # limite
        self.slot_energie = Energie(0)  # réservoir - toujours garder un objet Ressource qu'on modifie
        self.vitesse_extraction = 20  # < : + rapide temps de traitement d'extraction
        self.slot_ressources = {}
        self.extraction = None
        self.temps_fin_traitement_extraction_energie = None
        self.etat = {
            "EXTRACTION": self.extraire_energie
        }

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")
        if self.extraction is not None:
            self.etat["EXTRACTION"](self.parent.parent.parent.cadrejeu)

    def avancer(self):
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
            # pour en extraire les ressources, incluant Etoile, étoile doit appartenir au joueur
            if self.slot_energie.quantite > 0: # il faut ajouter ici la condition de savoir si l'étoile d'arrivée contient une infrastructure de dépôt
                self.depot_ressource()
                print("depôt des ressources")
            else:
                self.extraction = self.verif_extraction_possible()

        cible = self.cible
        self.cible = 0

        print(self.capsules)
        # seulement après exploitation de ressources, déterminer planète la plus proche pour un retour
        # self.verifier_retour(cible)

        return ["Etoile", cible]

    def verif_extraction_possible(self):
        resultat = None
        if self.slot_energie.quantite < self.slot_energie_capacite and self.cible.energie.quantite > 0:
            resultat = self.cible
        return self.cible
        # cargo_extraction_energie_confirmee = self.extraire_energie(self.cible)
        # cargo_exploitation_confirme = self.exploite_etoile_ressource(self.cible)

    def extraire_energie(self, cadrejeu):
        print(self.extraction.energie.quantite)
        if self.temps_fin_traitement_extraction_energie is None:
            self.temps_fin_traitement_extraction_energie = cadrejeu + self.vitesse_extraction
        if cadrejeu >= self.temps_fin_traitement_extraction_energie:
            # s'il reste de l'énergie sur l'étoile et que la capacité n'est pas atteinte
            if self.extraction.energie.quantite > 0 and self.slot_energie.quantite < self.slot_energie_capacite:
                capacite_possible = self.slot_energie_capacite - self.slot_energie.quantite
                # l'étoile a autant ou plus d'énergie que le cargo peut en charger
                if capacite_possible <= self.extraction.energie.quantite:  # l'étoile fourni assez d'énergie?
                    self.slot_energie.quantite += capacite_possible
                    self.extraction.energie.retrait_quantite(capacite_possible)
                    print(self.extraction.energie.quantite)
                    self.extraction = None
                # l'étoile a moins d'énergie que ce que le cargo peut charger
                else:
                    energie_restante = self.extraction.energie.quantite
                    self.slot_energie.quantite += self.extraction.energie.retrait_quantite(energie_restante)
                    print(self.extraction.energie.quantite)
                    self.extraction = None
            else:
                print("Étoile épuisée ou capacité de chargement atteinte. Veuillez décharger au dépôt le plus près.")
                self.extraction = None

    def depot_ressource(self):
        depot = self.slot_energie.quantite
        self.parent.parent.joueurs[self.proprietaire].energie.ajout_quantite(depot)
        self.slot_energie.quantite = 0

    # Anciennes fonctions d'exploitation de ressource
    # def exploite_etoile_ressource(self, etoile):
    #     if self.capacite >= 0:  # vérifier que Cargo a la capacité de transporter
    #         ressources_sur_lieu = etoile.ressource
    #         self.stock = copy.deepcopy(etoile.ressource)
    #         self.stock.quantite = 0
    #         temps_de_traitement = self.vitesse_de_traitement
    #         while temps_de_traitement >= 0:
    #             temps_de_traitement -= 1
    #             if temps_de_traitement <= 0:
    #                 self.capacite -= 10
    #                 self.stock.quantite += 10
    #                 etoile.ressource.quantite -= 10
    #                 temps_de_traitement = self.vitesse_de_traitement
    #                 if self.capacite <= 0 and etoile.ressource.quantite <= 0:
    #                     break
    #
    #         print("Exploitation complétée")
    #         print("Stock du cargo:", self.stock.nom, " | ", self.stock.quantite)
    #         self.deposer_etoile_ressource(etoile)
    #         return True
    #     else:
    #         print("CAPACITÉ DÉJÀ MAXIMISÉE")
    #         return False
    #
    # def deposer_etoile_ressource(self, etoile):
    #     self.cible = etoile_a_proximite_pour_depot = self.verifier_retour(etoile)
    #     print(self.cible.x, self.cible.y)
    #     self.avancer()  # avance de retour vers etoile_a_proximite

class Scout(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.energie = 200
        self.taille = 3
        self.vitesse = 1.1
        self.cible = 0
        self.nombre_capsule_information = 3
        self.hp = 75

class Spacefighter(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.energie = 300
        self.taille = 4
        self.vitesse = 1
        self.cible = 0
        self.hp = 125

class Destroyer(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.energie = 300
        self.taille = 4
        self.taille = 4
        self.vitesse = 1
        self.cible = 0
        self.hp = 125

class Colonisateur(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.energie = 1000
        self.taille = 10
        self.vitesse = 1
        self.cible = 0
        self.hp = 200

    # def arriver_planete(self):
    #     self.parent.log.append(
    #         ["Arrive:", self.parent.parent.cadre_courant, "Planete", self.id, self.cible.id, self.cible.proprietaire])
    #     if not self.cible.proprietaire:
    #         self.cible.proprietaire = self.proprietaire
    #         self.acquerir_capsule(self.cible)
    #
    #     cible = self.cible
    #     self.cible = 0
    #     # seulement après exploitation de ressources, déterminer planète la plus proche pour un retour
    #     # self.verifier_retour(cible)
    #     return ["Planete", cible]