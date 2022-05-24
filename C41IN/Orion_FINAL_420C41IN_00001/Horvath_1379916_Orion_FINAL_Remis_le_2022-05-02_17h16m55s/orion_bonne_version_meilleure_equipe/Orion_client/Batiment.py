from Id import get_prochain_id
from Projectile import *
from helper import *
from Ressource import *
from Annonce import *
import random

class Infrastructure:
    def __init__(self, parent, nom, etoile, prerequis_tech = None):
        self.id = get_prochain_id()
        self.parent = parent
        self.etoile = etoile
        self.proprietaire = nom
        self.prerequis_ressource = []
        self.prerequis_tech = prerequis_tech
        self.cout_science = 0
        self.couts_ressources = []

    def verification_creation(self):
        if self.prerequis_ressource is not None:
            for ressource in self.prerequis_ressource:
                if isinstance(ressource, Energie):
                    if self.parent.energie.quantite >= ressource.quantite:
                        self.couts_ressources.append(ressource)
                    else:
                        self.parent.annonce = Annonce("Il manque " + str(ressource.quantite - self.parent.energie.quantite) + " Energie")
                        return False
                elif isinstance(ressource, Eau):
                    if self.parent.eau.quantite >= ressource.quantite:
                        self.couts_ressources.append(ressource)
                    else:
                        self.parent.annonce = Annonce("Il manque " + str(ressource.quantite - self.parent.eau.quantite )+ " Eau")
                        return False
                elif isinstance(ressource, Fer):
                    if self.parent.fer.quantite >= ressource.quantite:
                        self.couts_ressources.append(ressource)
                    else:
                        self.parent.annonce = Annonce("Il manque " + str(ressource.quantite - self.parent.fer.quantite )+ " Fer")
                        return False
                elif isinstance(ressource, Titanium):
                    if self.parent.titanium.quantite >= ressource.quantite:
                        self.couts_ressources.append(ressource)
                    else:
                        self.parent.annonce = Annonce("Il manque " + str(ressource.quantite - self.parent.titanium.quantite )+ " Titanium")
                        return False
                elif isinstance(ressource, Cuivre):
                    if self.parent.cuivre.quantite >= ressource.quantite:
                        self.couts_ressources.append(ressource)
                    else:
                        self.parent.annonce = Annonce("Il manque " + str(ressource.quantite - self.parent.cuivre.quantite )+ " Cuivre")
                        return False

        if self.prerequis_tech is not None:
            nbr_match = 0
            for tech in self.parent.technologies:
                if tech.nom in self.prerequis_tech:
                    nbr_match += 1
            if nbr_match != len(self.prerequis_tech):
                return False

        # le joueur répond aux prérequis, on applique les changements
        for ress in self.couts_ressources:
            if isinstance(ress, Energie):
                self.parent.energie.retrait_quantite(ress.quantite)
            elif isinstance(ress, Eau):
                self.parent.eau.retrait_quantite(ress.quantite)
            elif isinstance(ress, Fer):
                self.parent.fer.retrait_quantite(ress.quantite)
            elif isinstance(ress, Titanium):
                self.parent.titanium.retrait_quantite(ress.quantite)
            elif isinstance(ress, Cuivre):
                self.parent.cuivre.retrait_quantite(ress.quantite)
        return True


class Batiment(Infrastructure):
    def __init__(self, parent, nom, etoile):
        Infrastructure.__init__(self, parent, nom, etoile)
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.nom_batiment = ""


class Satellite(Infrastructure):
    def __init__(self, parent, nom, etoile):
        Infrastructure.__init__(self, parent, nom, etoile)
        # tableau_satellite_ecran = [] ajouter dans joueur
        self.id = get_prochain_id()
        self.parent = parent
        self.x = etoile.x
        self.y = etoile.y
        self.xc = etoile.x
        self.yc = etoile.y
        self.theta = 0
        self.time = 200
        self.dtheta = (2 * math.pi) / self.time
        self.rayon = 15
        self.degat = 1
        self.vie = 0
        self.taille = 3
        self.rayon_verification = 70
        self.vitesse = 0
        self.projectiles = []
        self.deplacement_sur_planete = True
        self.cible_vaisseau = None
        self.detruit = False
        self.niveau = 0
        self.hp = 60
        # self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def deplacerSatellite(self):
        self.theta += self.dtheta
        self.x = self.rayon * math.cos(self.theta) + self.xc
        self.y = self.rayon * math.sin(self.theta) + self.yc

class SatKamikaze(Satellite):
    def __init__(self, parent, nom, etoile):
        Satellite.__init__(self, parent, nom, etoile)
        self.degat = 3
        self.rayon = 65
        self.rayon_verification = 300
        self.vitesse = 3
        self.prerequis_ressource = [Cuivre(50),Energie(20),Fer(30)]

    def verification_range_kamikaze(self):

        objets_joueurs = list()
        for nom_joueur in self.parent.parent.joueurs.keys():
            objets_joueurs.append(self.parent.parent.joueurs[nom_joueur])

        for f in objets_joueurs:
            for i in f.flotte:
                for k in f.flotte[i]:
                    vaisseau = f.flotte[i][k]
                    if self.proprietaire != vaisseau.proprietaire:
                        distance = Helper.calcDistance(vaisseau.x, vaisseau.y, self.x, self.y)
                        somme_rayon = vaisseau.taille + self.rayon_verification

                        if distance < somme_rayon:
                            self.cible_vaisseau = vaisseau
                            self.deplacement_sur_planete = False
                            self.vitesse = 8

    def suivre_vaisseau(self):
        distance_projectile = Helper.calcDistance(self.x, self.y, self.cible_vaisseau.x, self.cible_vaisseau.y)
        angle_projectile = Helper.calcAngle(self.x, self.y, self.cible_vaisseau.x, self.cible_vaisseau.y)
        cible_projectile = Helper.getAngledPoint(angle_projectile, self.vitesse, self.x, self.y)

        self.x = cible_projectile[0]
        self.y = cible_projectile[1]

        if distance_projectile < 30:  # variable qui determine le rayon de la cible pour touche
            self.detruit = True
            if self.cible_vaisseau.hp > 0:
                self.cible_vaisseau.hp -= self.degat
                #self.cible_vaisseau.parent.compteur -= 1
                self.parent.tuer_satellite(self)


class SatDefensif(Satellite):
    # degat, rayon, vitesse, cooldown pour tirer
    niveaux = ([10, 45, 2, 30 ],
               [16, 60, 2.4, 25])

    def __init__(self, parent, nom, etoile):
        Satellite.__init__(self, parent, nom, etoile)
        self.nom_batiment = "SatDefensif"
        self.degat = 2
        self.rayon = 45
        self.cooldowntirer = 30
        self.cooldown = 0
        self.vitesse = 2
        self.projectiles = []
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.accorder_niveau()
        self.verifier_tech()
        self.prerequis_ressource = [Cuivre(25), Energie(20)]
        self.hp = 100

    def accorder_niveau(self):
        valeurs_niveau = SatDefensif.niveaux[self.niveau - 1]
        self.degat = valeurs_niveau[0]
        self.rayon = valeurs_niveau[1]
        self.vitesse = valeurs_niveau[2]
        self.cooldowntirer = valeurs_niveau[3]

    def verifier_tech(self):
        for tech in self.parent.technologies:
            if self.niveau == 1:
                if tech.nom == "Satellite: Defense I":
                    tech.effet(self)
                    print("J'existe")
            elif self.niveau == 2:
                if tech.nom == "Satellite: Defense II":
                    tech.effet(self)
                    print("J'existe niveau 2")

    def verification_range_vaisseau(self):
        objets_joueurs = list()
        for nom_joueur in self.parent.parent.joueurs.keys():
            objets_joueurs.append(self.parent.parent.joueurs[nom_joueur])
        for f in objets_joueurs:
            for i in f.flotte:
                for k in f.flotte[i]:
                    vaisseau = f.flotte[i][k]
                    if self.proprietaire != vaisseau.proprietaire:
                        distance = Helper.calcDistance(vaisseau.x, vaisseau.y, self.x, self.y)
                        somme_rayon = vaisseau.taille + self.rayon_verification

                        if distance < somme_rayon:
                            if self.cooldown == 0:
                                ##i.est_cible = True append dans une liste
                                self.tirer_vaisseau(vaisseau)
                                self.cooldown = self.cooldowntirer

                        if self.cooldown > 0:
                            self.cooldown -= 1

    def tirer_vaisseau(self, vaisseau):
        self.projectiles.append(Projectile(self, vaisseau))


class SatVision(Satellite):
    def __init__(self, parent, nom, etoile):
        Satellite.__init__(self, parent, nom, etoile)
        self.rayon = 60
        self.vitesse = 4
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.prerequis_ressource = [Cuivre(25),Energie(10)]

class Merveille(Infrastructure):
    def __init__(self, nom, etoile, parent):
        Infrastructure.__init__(self, nom, etoile, parent)
        self.prerequis_ressource = [Titanium(70), Energie(70),Fer(70),Cuivre(70),Eau(70)]
        self.all_merveille = ["Muraille de Chine","Pyramide d'Egypte","Cite Atlantis","Arche de Noe","Statue de Wil Taupe-Un","Statue de la liberte","Tour Eiffel"]
        self.longueur = len(self.all_merveille)
        self.nom_merveille = self.all_merveille[round(random.randrange(0,self.longueur))]


class FigureImportance(Infrastructure):
    def __init__(self, nom, etoile, parent):
        Infrastructure.__init__(self, nom, etoile, parent)


class Raffinerie(Batiment):
    niveaux = (500, 1000, 2000)

    def __init__(self, nom, etoile, parent):
        Batiment.__init__(self, nom, etoile, parent)
        self.nom_batiment = "Raffinerie"
        self.niveau = 1
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.prerequis_ressource = [Fer(25 * self.niveau), Energie(30 * self.niveau)]
        self.accorder_niveau()

    def accorder_niveau(self):
        valeurs_niveau = Raffinerie.niveaux[self.niveau - 1]
        self.capacite = valeurs_niveau


class Usine(Batiment):
    def __init__(self, nom, etoile, parent):
        Batiment.__init__(self, nom, etoile, parent)
        self.delai = 0
        self.nom_batiment = "Usine"
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.etoile.possede_usine = True
        self.prerequis_ressource = [Fer(50 * self.niveau), Energie(30 * self.niveau)]


class Ferme(Batiment):
    def __init__(self, nom, etoile, parent):
        Batiment.__init__(self, nom, etoile, parent)
        self.nom_batiment = "Ferme"
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.prerequis_ressource = [Eau(25 * self.niveau), Energie(30 * self.niveau)]
        self.generation = 10


class Laboratoire(Batiment):
    def __init__(self, nom, etoile, parent):
        Batiment.__init__(self, nom, etoile, parent)
        self.nom_batiment = "Laboratoire"
        self.niveau = self.parent.niveaux[type(self).__name__]
        self.prerequis_ressource = [Titanium(25 * self.niveau), Energie(30 * self.niveau)]
        self.gen_science = 5
