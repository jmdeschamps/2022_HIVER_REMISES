import ast
import math
import random

from Id import *
from helper import Helper as hlp
from math import floor


class Batiment:
    def __init__(self, etoile, type, prix_or, prix_argent, prix_bronze, joueur, id):
        self.etoile = etoile
        self.type = type
        self.prix_or = prix_or
        self.prix_argent = prix_argent
        self.prix_bronze = prix_bronze
        self.niveau = 1
        self.joueur = joueur
        self.id = id
        self.cooldown = 0


class TourDefensive(Batiment):
    # PRIX INITIAL
    prix_or = 100
    prix_argent = 200
    prix_bronze = 300

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "Tour defensive", 100, 200, 300, joueur, id)
        self.consommation_energie = 2
        self.rayon_de_vision = 250
        self.projectile = None
        self.cible = None
        self.angle_cible = None
        self.degat = 5

    def jouer_prochain_coup(self):
        self.regarder_autour()
        if self.cible is not None:
            self.angle_cible = hlp.calcAngle(self.etoile.x, self.etoile.y, self.cible.x, self.cible.y)
            self.attaquer_ennemi(self.cible)
        if self.cooldown >= 75:
            self.joueur.ressources["hydrogene"] -= self.consommation_energie
            self.cooldown = 0
        self.cooldown += 1

    def regarder_autour(self):
        modele = self.joueur.parent
        for i in modele.joueurs.keys():
            i = modele.joueurs[i]
            if i.nom != self.joueur.nom:
                try:
                    for k in i.flotte:
                        for j in i.flotte[k]:
                            j = i.flotte[k][j]
                            if j not in self.joueur.visible:
                                distance = hlp.calcDistance(self.etoile.x, self.etoile.y, j.x, j.y)
                                if distance < self.rayon_de_vision:
                                    self.joueur.visible.append(j)
                                    if self.cible is None:
                                        self.cible = j
                            else:
                                distance = hlp.calcDistance(self.etoile.x, self.etoile.y, j.x, j.y)
                                if distance < self.rayon_de_vision:
                                    if self.cible is None:
                                        self.cible = j
                except:
                    pass

    def attaquer_ennemi(self, cible):
        if self.projectile is None:
            self.projectile = ProjectileTour(self.etoile.x, self.etoile.y, self.cible, self.degat, 10, self)
        rep = self.projectile.tirer_projectile()
        if self.projectile.cible_atteinte:
            self.projectile = None
        if rep:
            try:
                modele = self.joueur.parent
                for i in modele.joueurs.keys():
                    i = modele.joueurs[i]
                    if self.cible in i.visible:
                        i.visible.remove(self.cible)
                self.cible = None
            except:
                pass
        return rep


class Usine(Batiment):
    # PRIX INITIAL
    prix_or = 250
    prix_argent = 400
    prix_bronze = 600

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "usine", 250, 400, 600, joueur, id)
        self.consommation_energie = 2
        if self.joueur.foreuse:
            self.cooldown_min = 25
        else:
            self.cooldown_min = 75

    def jouer_prochain_coup(self):
        if self.cooldown >= self.cooldown_min:
            if self.etoile.ressources_humaines["population"] >= 100 and \
                    self.joueur.ressources["hydrogene"] >= self.consommation_energie:
                facteur_pop = floor(self.etoile.ressources_humaines["population"] / 100)
                if self.etoile.ressources_extraites["or"] >= (self.niveau + facteur_pop):
                    self.etoile.ressources_extraites["or"] -= (self.niveau + facteur_pop)
                    self.joueur.ressources["or"] += (self.niveau + facteur_pop)
                if self.etoile.ressources_extraites["argent"] >= (self.niveau + facteur_pop):
                    self.etoile.ressources_extraites["argent"] -= (self.niveau + facteur_pop)
                    self.joueur.ressources["argent"] += (self.niveau + facteur_pop)
                if self.etoile.ressources_extraites["bronze"] >= (self.niveau + facteur_pop):
                    self.etoile.ressources_extraites["bronze"] -= (self.niveau + facteur_pop)
                    self.joueur.ressources["bronze"] += (self.niveau + facteur_pop)
                if self.etoile.ressources_extraites["hydrogene"] >= (self.niveau + facteur_pop):
                    self.etoile.ressources_extraites["hydrogene"] -= (self.niveau + facteur_pop)
                    self.joueur.ressources["hydrogene"] += (self.niveau + facteur_pop)
                self.joueur.ressources["hydrogene"] -= self.consommation_energie
            self.cooldown = 0
        self.cooldown += 1


class Mine(Batiment):
    # PRIX INITIAL
    prix_or = 50
    prix_argent = 75
    prix_bronze = 100

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "mine", 50, 75, 100, joueur, id)
        self.liste_ressources = ["or", "argent", "bronze", "hydrogene"]
        self.consommation_energie = 10
        if self.joueur.foreuse:
            self.cooldown_min = 133
        else:
            self.cooldown_min = 400

    def jouer_prochain_coup(self, joueur=None):
        if self.cooldown >= self.cooldown_min:
            if self.etoile.ressources_humaines["population"] >= 50 and \
                    self.joueur.ressources["hydrogene"] >= self.consommation_energie:
                facteur_pop = floor(self.etoile.ressources_humaines["population"] / 100)
                if facteur_pop <= 1:
                    facteur_pop = 1
                ratio_ressources = {"or": 50, "argent": 200, "bronze": 300, "hydrogene": 200}
                for i in self.liste_ressources:
                    self.etoile.ressources_totales[i] -= ratio_ressources[i] * (self.niveau + facteur_pop)
                    self.etoile.ressources_extraites[i] += ratio_ressources[i] * (self.niveau + facteur_pop)
                    # print(i + str(self.etoile.ressources_extraites[i]))
                self.joueur.ressources["hydrogene"] -= self.consommation_energie
            self.cooldown = 0
        self.cooldown += 1


class Residence(Batiment):
    # PRIX INITIAL
    prix_or = 25
    prix_argent = 50
    prix_bronze = 75

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "residence", 25, 50, 75, joueur, id)
        self.consommation_energie = 10

    def jouer_prochain_coup(self):
        if self.cooldown >= 750:
            if self.joueur.ressources["hydrogene"] >= self.consommation_energie:
                facteur_pop = floor(self.etoile.ressources_humaines["population"] / 100)
                if facteur_pop <= 1:
                    facteur_pop = 1
                self.etoile.ressources_humaines["population"] += 3 * (self.niveau + facteur_pop)
                self.joueur.ressources["hydrogene"] -= self.consommation_energie
            self.cooldown = 0
        self.cooldown += 1


class Ferme(Batiment):
    prix_or = 10
    prix_argent = 20
    prix_bronze = 30

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "ferme", 10, 20, 30, joueur, id)
        self.consommation_energie = 1

    def jouer_prochain_coup(self):
        if self.cooldown >= 200:
            if self.joueur.ressources["hydrogene"] >= self.consommation_energie:
                facteur_pop = floor(self.etoile.ressources_humaines["population"] / 100)
                if facteur_pop <= 1:
                    facteur_pop = 1
                self.etoile.ressources_humaines["nourriture"] += 2 * (self.niveau + facteur_pop)
                self.joueur.ressources["hydrogene"] -= self.consommation_energie
            self.cooldown = 0
        self.cooldown += 1


class Porte_de_vers:
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


class Trou_de_vers:
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant
        # l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup()
        self.porte_b.jouer_prochain_coup()


class Etoile:
    def __init__(self, parent, x, y):
        self.points_vie = 150
        self.points_vie_max = 150
        self.id = get_prochain_id()
        self.parent = parent
        self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.batiments = []
        self.prix_batiments = {"Ferme": {"or": 10, "argent": 20, "bronze": 30},
                               "Residence": {"or": 25, "argent": 50, "bronze": 75},
                               "Mine": {"or": 50, "argent": 75, "bronze": 100},
                               "Usine": {"or": 250, "argent": 400, "bronze": 600}
                               }
        self.ressources_totales = {
            "or": 0, "argent": 0, "bronze": 0, "hydrogene": 0
        }
        self.ressources_extraites = {
            "or": 0, "argent": 0, "bronze": 0,
            "hydrogene": 0
        }
        self.ressources_humaines = {
            "population": 0, "nourriture": 0
        }
        self.cooldown_reduction_nourriture = 0
        self.generer_ressources()

    def generer_ressources(self, multiple=1):
        valeur = random.randrange(2, 5) * 1000 * multiple
        self.ressources_totales["or"] = valeur
        self.ressources_totales["argent"] = valeur * 2
        self.ressources_totales["bronze"] = valeur * 3
        self.ressources_totales["hydrogene"] = valeur

    def reduire_nourriture(self):
        quantite = floor(self.ressources_humaines["population"] / 10)
        if self.ressources_humaines["nourriture"] >= quantite:
            self.ressources_humaines["nourriture"] -= quantite
        else:
            self.ressources_humaines["population"] -= quantite / 2


class Projectile:

    def __init__(self, x, y, cible, munitions_enflammees, paralysant):

        self.x = x
        self.y = y
        self.degat = 25
        self.munitions_enflammees = munitions_enflammees
        self.cible = cible
        self.vitesse = 10
        self.cible_atteinte = False
        self.paralysant = paralysant

    def tirer_projectile(self, angle):
        self.x, self.y = hlp.getAngledPoint(angle, self.vitesse, self.x, self.y)
        distance = hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
        if distance <= self.vitesse:
            self.cible_atteinte = True
            print("cible atteinte")

            rep = self.cible.recevoir_degat(self.degat, self.munitions_enflammees, self.paralysant)
            return rep

    def attaquer_planete(self, angle):
        distance = hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
        if distance > self.vitesse:
            distance = self.vitesse
        self.x, self.y = hlp.getAngledPoint(angle, distance, self.x, self.y)
        if distance <= 1:
            self.cible_atteinte = True
            print("cible atteinte")
            degat = self.degat
            if self.cible.points_vie < self.degat:
                degat = self.cible.points_vie
            self.cible.points_vie -= degat
            return


class ProjectileTour:
    def __init__(self, x, y, cible, degat, vitesse, parent):
        self.x = x
        self.y = y
        self.degat = degat
        self.vitesse = vitesse
        self.cible = cible
        self.cible_atteinte = False
        self.progress_cooldown = 0
        self.cooldown = 0
        self.parent = parent
        self.couleurs_rgb = [125, 0, 200]
        self.couleurs_hex = ""

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def tirer_projectile(self):
        angle = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
        distance = hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
        rep = False
        if distance > self.vitesse:
            distance = self.vitesse
        else:
            if self.progress_cooldown >= 10:
                rep = self.cible.recevoir_degat(self.degat, False, False)
                if rep:
                    self.cible_atteinte = True
                self.progress_cooldown = 0
            self.progress_cooldown += 1
        self.couleurs_rgb[2] += 4
        if self.couleurs_rgb[2] > 250:
            self.couleurs_rgb[2] = 100
        self.couleurs_hex = self.rgb_to_hex(self.couleurs_rgb)
        self.x, self.y = hlp.getAngledPoint(angle, distance, self.x, self.y)
        if self.cooldown >= 70:
            self.cible_atteinte = True
            print("cible atteinte")
            self.cooldown = 0
        self.cooldown += 1
        return rep


class Vaisseau:

    def __init__(self, parent, nom, x, y):
        self.cooldown_stack_enflammees = 0
        self.liste_etoile_photo = []
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.bouclier_max = 100
        self.couleur_initiale = parent.couleur
        if self.parent.rayon_infini:
            self.rayon_de_tir = parent.parent.largeur
        else:
            self.rayon_de_tir = 100
        if self.parent.techno_bouclier:
            self.bouclier = 100
        else:
            self.bouclier = 0

        self.munitions_enflammees = self.parent.munitions_enflammees
        self.stack_enflammees = 0
        self.cooldown_stack_enflammees = 0

        if self.parent.paralysant:
            self.paralysant = True
        else:
            self.paralysant = False
        self.compteur_paralysant = 0
        self.delai_paralysant = 0

        self.x = x
        self.y = y
        self.vie_max = 100
        self.vie_actuelle = self.vie_max
        self.niveau = 1
        self.degat = 10
        self.espace_cargo = 0
        self.carburant = 50
        self.carburant_max = 100
        self.cooldown_remplissage = 0
        self.en_remplissage = 0
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.cout_en_carburant_par_frame = 0.08
        self.type_cible = None
        self.angle_cible = 0
        self.distance = 0
        self.vitesse_tir = 50
        self.tir_delai = 0
        self.rayon_de_vision = 300
        self.liste_projectiles = []
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte,
                        }
        self.a_conquerit_etoile = False
        self.liste_etoile_photo = []

    def devier(self, force, angle):
        self.x, self.y = hlp.getAngledPoint(angle, force, self.x, self.y)

    def manipulation(self):
        self.parent.manipulation(self)

    def ajouter_bouclier(self):
        self.bouclier = 100 * self.niveau
        self.bouclier_max = self.bouclier

    def ameliorer_vaisseau(self):
        pass

    def recevoir_degat(self, degat, munitions_enflammees=False, paralysant=False):
        if munitions_enflammees:
            self.stack_enflammees += 1
            print("+1 stack")
            degat += degat * 0.10 * self.stack_enflammees
        degat_subi = (self.bouclier - degat)
        if degat_subi < 0:
            self.vie_actuelle -= abs(degat_subi)
            self.bouclier = 0
        else:
            self.bouclier -= degat
        print(self.vie_actuelle)
        if paralysant:
            self.compteur_paralysant = 100
        if self.vie_actuelle <= 0:
            self.parent.tuer_flotte(self)
            return True

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.compteur_paralysant > 0:
            self.compteur_paralysant -= 1
        if self.delai_paralysant > 0:
            self.delai_paralysant -= 1
        self.verifier_autour()
        if self.parent.techno_bouclier:
            self.recharger_bouclier()
        self.tir_delai += 1

        if self.cooldown_stack_enflammees % 10 == 0:
            degat = 2 * self.stack_enflammees
            self.vie_actuelle -= degat
            if self.vie_actuelle <= 0:
                self.parent.tuer_flotte(self)
        if self.cooldown_stack_enflammees >= 120:
            self.stack_enflammees -= 1 if self.stack_enflammees > 0 else 0
            self.cooldown_stack_enflammees = 0
        self.cooldown_stack_enflammees += 1
        if self.en_remplissage == 1:
            self.remplir_carburant()
        elif self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            a_verifier = True
            cible = None
            while a_verifier:
                cible = random.choice(self.parent.parent.etoiles)
                a_verifier = False
                for joueur in self.parent.parent.joueurs:
                    if joueur != self.parent.nom:
                        if self.parent.parent.joueurs[joueur].etoilemere.id == cible.id:
                            a_verifier = True
            self.acquerir_cible(cible, "Etoile")

    def assez_carburant_aller_retour(self):
        distance = hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y) * 2
        temps_en_frame = distance / self.vitesse
        cout_total = temps_en_frame * self.cout_en_carburant_par_frame
        if cout_total <= self.carburant:
            return True
        else:
            return False

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):
        self.carburant -= self.cout_en_carburant_par_frame
        if self.carburant >= 0:
            if self.compteur_paralysant <= 0:
                if self.cible != 0:
                    x = self.cible.x
                    y = self.cible.y

                    self.angle_cible = hlp.calcAngle(self.x, self.y, x, y)

                    if self.type_cible == "Flotte":
                        if hlp.calcDistance(self.x, self.y, x, y) > 25:
                            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)

                        if hlp.calcDistance(self.x, self.y, x, y) <= self.rayon_de_tir:
                            if self.attaquer_ennemi():
                                return

                        if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse and self.cible.vie_actuelle <= 0:
                            self.x = x
                            self.y = y
                            self.cible = 0
                            return
                    elif self.type_cible == "Etoile" and self.cible.proprietaire != self.proprietaire and self.cible.proprietaire != "":
                        if not self.a_conquerit_etoile:
                            if hlp.calcDistance(self.x, self.y, x, y) > 25:
                                self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)

                            if hlp.calcDistance(self.x, self.y, x, y) <= self.rayon_de_tir:
                                self.attaquer_planete()

                            if self.cible.points_vie <= 0:
                                self.a_conquerit_etoile = True
                                self.cible.points_vie = self.cible.points_vie_max
                        else:
                            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
                            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                                type_obj = type(self.cible).__name__
                                rep = self.arriver[type_obj]()
                                return rep
                    elif self.type_cible == "Etoile" or self.type_cible == "Porte_de_ver":
                        self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
                        if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                            type_obj = type(self.cible).__name__
                            rep = self.arriver[type_obj]()
                            return rep

        else:
            self.carburant = 0

    def arriver_etoile(self):

        if self.cible in self.parent.etoilescontrolees:
            self.remplir_carburant()
        else:
            self.a_conquerit_etoile = True
            for i in self.cible.batiments:
                i.joueur = self.parent

        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire:
            rng = random.randint(1, 7)
            if rng == 1:
                self.parent.ajouter_artefact()

            self.cible.proprietaire = self.proprietaire
            if self.cible in self.parent.parent.joueurs[self.parent.parent.parent.vue.mon_nom].visible:
                self.parent.parent.parent.afficher_etoile(self.cible.proprietaire, self.cible)
        else:
            self.cible.proprietaire = self.proprietaire
            self.parent.parent.afficher_etoile(self.cible.proprietaire, self.cible)
        cible = self.cible
        if isinstance(self, Cargo):
            if self.en_retour == 0:
                self.collecter_ressources()
                self.en_retour = 1
            else:
                self.decharger_cargo()
                self.en_retour = 0
        else:
            self.cible = 0
        return ["Etoile", cible]

    def remplir_carburant(self):
        if self.en_remplissage == 0 and self.carburant <= self.carburant_max:
            self.en_remplissage = 1
        if self.en_remplissage == 1:
            self.cooldown_remplissage += 1
            if self.cooldown_remplissage >= 50:
                if self.parent.ressources["hydrogene"] >= 50:
                    if self.carburant_max - self.carburant >= 50:
                        quantite = 50
                    else:
                        quantite = self.carburant_max - self.carburant

                else:
                    quantite = self.parent.ressources["hydrogene"]
                    if self.carburant_max - self.carburant < quantite:
                        quantite = self.carburant_max - self.carburant
                quantite = floor(quantite)
                self.parent.ressources["hydrogene"] -= quantite
                self.carburant += quantite
                self.cooldown_remplissage = 0
            if self.carburant_max - self.carburant <= 1:
                self.carburant = self.carburant_max
            if self.parent.ressources["hydrogene"] == 0 or self.carburant == self.carburant_max:
                self.en_remplissage = 0

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id])
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

    def attaquer_ennemi(self):
        if self.tir_delai >= self.vitesse_tir:
            self.tir_delai = 0
            self.liste_projectiles.append(
                Projectile(self.x, self.y, self.cible, self.munitions_enflammees, self.paralysant
                if self.delai_paralysant <= 0 else False))
            if self.paralysant:
                self.delai_paralysant = 200

        if self.liste_projectiles:
            for i in self.liste_projectiles:
                rep = i.tirer_projectile(self.angle_cible)

                if i.cible_atteinte:
                    self.liste_projectiles.remove(i)
                if rep:
                    try:
                        self.parent.visible.remove(self.cible)
                    except:
                        pass
                    self.cible = 0
                    return rep

    def attaquer_planete(self):
        if self.tir_delai >= self.vitesse_tir:
            self.tir_delai = 0
            self.liste_projectiles.append(Projectile(self.x, self.y, self.cible, False, False))

        if self.liste_projectiles:
            for i in self.liste_projectiles:
                i.attaquer_planete(self.angle_cible)

                if i.cible_atteinte:
                    self.liste_projectiles.remove(i)
                # if rep:
                #     self.parent.visible.remove(self.cible)

                return self.cible.points_vie <= 0

    def verifier_autour(self):
        for i in self.parent.parent.etoiles:
            if self.parent.coque_etoile:
                distance = hlp.calcDistance(self.x, self.y, i.x, i.y)
                if distance < self.rayon_de_vision:
                    self.carburant += 0.3
                    if i not in self.liste_etoile_photo:
                        self.liste_etoile_photo.append(i)
                    self.carburant += 0.05 * len(self.liste_etoile_photo)
                    self.parent.parent.parent.vue.afficher_rechargement(self.x, self.y, self.liste_etoile_photo)
                    if self.carburant >= self.carburant_max:
                        self.carburant = self.carburant_max
                else:
                    if i in self.liste_etoile_photo:
                        self.liste_etoile_photo.remove(i)

            if i not in self.parent.etoilescontrolees and i not in self.parent.visible:
                distance = hlp.calcDistance(self.x, self.y, i.x, i.y)
                if distance < self.rayon_de_vision:
                    self.parent.visible.append(i)
                    if i.proprietaire != "":
                        self.parent.parent.parent.afficher_etoile(i.proprietaire, i)
        modele = self.parent.parent
        for i in modele.joueurs.keys():
            i = modele.joueurs[i]

            if i.nom != modele.parent.vue.mon_nom:
                for k in i.flotte:
                    for j in i.flotte[k]:
                        j = i.flotte[k][j]
                        if j not in self.parent.visible:
                            distance = hlp.calcDistance(self.x, self.y, j.x, j.y)
                            if distance < self.rayon_de_vision:
                                self.parent.visible.append(j)

    def recharger_bouclier(self):
        if self.bouclier < self.bouclier_max:
            self.bouclier += 0.4
            if self.bouclier > self.bouclier_max:
                self.bouclier = self.bouclier_max


class Cargo(Vaisseau):
    # PRIX INITIAL
    prix_or = 15
    prix_argent = 40
    prix_bronze = 100

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 300
        # self.energie = 500
        self.carburant = 500
        self.carburant_max = 500
        if self.parent.techno_bouclier:
            self.bouclier = 100
        else:
            self.bouclier = 0
        self.taille = 6
        self.vitesse = 1
        self.prix_or = Cargo.prix_or * self.niveau
        self.prix_argent = Cargo.prix_argent * self.niveau
        self.prix_bronze = Cargo.prix_bronze * self.niveau

        self.cible = 0
        self.ang = 0
        self.cargo_actuel = 0
        self.ressources_transportees = {
            "or": 0, "argent": 0, "bronze": 0,
            "hydrogene": 0
        }
        self.etoile_a_collecter = None
        self.en_chargement = 0
        self.en_dechargement = 0
        self.en_retour = 0
        self.compteur_chargement = 0
        self.compteur_dechargement = 0
        self.index_ressources = 0
        self.a_conquerit_etoile = False

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.compteur_paralysant > 0:
            self.compteur_paralysant -= 1
        if self.delai_paralysant > 0:
            self.delai_paralysant -= 1
        if self.cooldown_stack_enflammees % 10 == 0:
            self.vie_actuelle -= 2 * self.stack_enflammees
        if self.cooldown_stack_enflammees >= 120:
            self.stack_enflammees -= 1 if self.stack_enflammees > 0 else 0
            self.cooldown_stack_enflammees = 0
        self.cooldown_stack_enflammees += 1
        self.verifier_autour()
        if self.parent.techno_bouclier:
            self.recharger_bouclier()
        if self.en_remplissage == 1:
            self.remplir_carburant()
        elif self.cible != 0 and self.en_chargement == 0 and self.en_dechargement == 0:
            return self.avancer()
        elif self.cible != 0 and self.en_chargement == 1:
            self.collecter_ressources()
        elif self.cible != 0 and self.en_dechargement == 1:
            self.decharger_cargo()
        elif trouver_nouveau:
            a_verifier = True
            cible = None
            while a_verifier:
                cible = random.choice(self.parent.parent.etoiles)
                a_verifier = False
                for joueur in self.parent.parent.joueurs:
                    if joueur != self.parent.nom:
                        if self.parent.parent.joueurs[joueur].etoilemere.id == cible.id:
                            a_verifier = True
            self.acquerir_cible(cible, "Etoile")

    def collecter_ressources(self):
        chargement_termine = True
        doit_collecter = True
        for i in self.cible.batiments:
            if isinstance(i, Usine):
                doit_collecter = False
                break
        if doit_collecter:
            self.etoile_a_collecter = self.cible
            if self.en_chargement == 0:
                self.en_chargement = 1
            if self.compteur_chargement >= 35:
                liste_ressources = ['or', 'argent', 'bronze', 'hydrogene']
                if self.index_ressources >= 4:
                    self.index_ressources = 0
                quantite = 0
                if self.cargo_actuel <= self.cargo:
                    if self.cargo_actuel <= self.cargo - 100*self.niveau:
                        if self.cible.ressources_extraites[liste_ressources[self.index_ressources]] >= 100*self.niveau:
                            quantite = 100*self.niveau
                        else:
                            quantite = self.cible.ressources_extraites[liste_ressources[self.index_ressources]]
                    else:
                        quantite = self.cargo - self.cargo_actuel
                        if self.cible.ressources_extraites[liste_ressources[self.index_ressources]] >= quantite:
                            pass
                        else:
                            quantite = self.cible.ressources_extraites[liste_ressources[self.index_ressources]]
                    self.cible.ressources_extraites[liste_ressources[self.index_ressources]] -= quantite
                    self.ressources_transportees[liste_ressources[self.index_ressources]] += quantite
                    self.cargo_actuel += quantite
                    print("en chargement de " + str(quantite) + str(liste_ressources[self.index_ressources]))
                    self.index_ressources += 1
                chargement_termine = True
                for i in liste_ressources:
                    if self.cible.ressources_extraites[i] >= 50:
                        chargement_termine = False
                # if self.cargo_actuel >= self.cargo or chargement_termine:
                if self.cargo_actuel >= self.cargo:
                    self.en_chargement = 0
                    self.index_ressources = 0
                    print("chargement termine")
                    self.cibler_usine()
                self.compteur_chargement = 0
        else:
            self.cible = 0

        self.compteur_chargement += 1

    def decharger_cargo(self):
        if self.en_dechargement == 0:
            self.en_dechargement = 1
        if self.compteur_dechargement >= 50:
            liste_ressources = ['or', 'argent', 'bronze', 'hydrogene']
            quantite = 0
            quantite = self.ressources_transportees[liste_ressources[self.index_ressources]]
            self.cible.ressources_extraites[liste_ressources[self.index_ressources]] += quantite
            self.ressources_transportees[liste_ressources[self.index_ressources]] -= quantite
            self.cargo_actuel -= quantite
            print("en dechargement de " + str(quantite) + str(liste_ressources[self.index_ressources]))
            self.index_ressources += 1
            self.compteur_dechargement = 0
            if self.cargo_actuel == 0:
                self.en_dechargement = 0
                self.index_ressources = 0
                print("dechargement complété")
                self.effectuer_transport(self.etoile_a_collecter)
        self.compteur_dechargement += 1

    def cibler_usine(self):
        etoile_ciblee = None
        distance_cible = None
        distance = 0
        for i in self.parent.etoilescontrolees:
            for j in i.batiments:
                if isinstance(j, Usine):
                    distance = hlp.calcDistance(self.x, self.y, i.x, i.y)
                    if distance_cible is None:
                        distance_cible = distance
                        etoile_ciblee = i
                    if distance < distance_cible:
                        distance_cible = distance
                        etoile_ciblee = i
                    break
        self.effectuer_transport(etoile_ciblee)

    def effectuer_transport(self, etoile=None):
        ids = [self.id, etoile.id, "Etoile"]
        self.parent.ciblerflotte(ids)

    def ameliorer_vaisseau(self):
        self.niveau += 1
        if self.niveau < 4:
            self.cargo *= 2
            self.vitesse *= 1.5
            self.degat *= 1.2
            self.vie_max *= 2
            if self.bouclier > 0:
                self.bouclier *= 1.5
                self.bouclier_max *= 1.5


class Explorateur(Vaisseau):
    # PRIX INITIAL
    prix_or = 5
    prix_argent = 10
    prix_bronze = 35

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.vitesse = 2
        self.degat = 15
        self.carburant = 200
        if self.parent.techno_bouclier:
            self.bouclier = 100
        else:
            self.bouclier = 0
        self.carburant_max = 200
        self.prix_amelioration_or = Explorateur.prix_or * self.niveau
        self.prix_amelioration_argent = Explorateur.prix_argent * self.niveau
        self.prix_amelioration_bronze = Explorateur.prix_bronze * self.niveau
        self.nouvelle_exploration = False
        self.en_exploration = False
        self.a_conquerit_etoile = False

    def ameliorer_vaisseau(self):
        self.niveau += 1
        if self.niveau < 4:
            self.vitesse *= 2
            self.carburant_max *= 1.5
            self.degat *= 1.2
            self.vie_max *= 1.2
            if self.bouclier > 0:
                self.bouclier *= 1.2
                self.bouclier_max *= 1.2

    def explorer_inconnu(self):
        self.en_exploration = True
        distance_courte = 1000
        for i in self.parent.parent.etoiles:
            if i not in self.parent.etoilescontrolees:
                distance = hlp.calcDistance(self.x, self.y, i.x, i.y)
                if distance_courte > distance:
                    distance_courte = distance
                    self.cible = i

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.compteur_paralysant > 0:
            self.compteur_paralysant -= 1
        if self.delai_paralysant > 0:
            self.delai_paralysant -= 1
        if self.cooldown_stack_enflammees % 10 == 0:
            if self.stack_enflammees > 0:
                print("stack : " + str(self.stack_enflammees))
            self.vie_actuelle -= 2 * self.stack_enflammees
        if self.cooldown_stack_enflammees >= 120:
            if self.stack_enflammees > 0:
                print(self.stack_enflammees)
            self.stack_enflammees -= 1 if self.stack_enflammees > 0 else 0
            self.cooldown_stack_enflammees = 0
        self.cooldown_stack_enflammees += 1
        self.verifier_autour()
        if self.parent.techno_bouclier:
            self.recharger_bouclier()
        self.tir_delai += 1
        if self.en_remplissage == 1:
            self.remplir_carburant()
        elif self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            a_verifier = True
            cible = None
            while a_verifier:
                cible = random.choice(self.parent.parent.etoiles)
                a_verifier = False
                for joueur in self.parent.parent.joueurs:
                    if joueur != self.parent.nom:
                        if self.parent.parent.joueurs[joueur].etoilemere.id == cible.id:
                            a_verifier = True
            self.acquerir_cible(cible, "Etoile")
        elif self.en_exploration:
            self.explorer_inconnu()


class Combattant(Vaisseau):
    # PRIX INITIAL
    prix_or = 35
    prix_argent = 70
    prix_bronze = 100

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.vitesse = 1.5
        self.degat = 35
        if self.parent.techno_bouclier:
            self.bouclier = 100
        else:
            self.bouclier = 0
        self.prix_amelioration_or = Combattant.prix_or * self.niveau
        self.prix_amelioration_argent = Combattant.prix_argent * self.niveau
        self.prix_amelioration_bronze = Combattant.prix_bronze * self.niveau
        self.carburant = 90
        self.carburant_max = 90
        self.a_conquerit_etoile = False

    def ameliorer_vaisseau(self):
        self.niveau += 1
        if self.niveau < 4:
            self.vitesse *= 1.5
            self.degat *= 2
            self.vie_max *= 1.2
            if self.bouclier > 0:
                self.bouclier *= 1.5
                self.bouclier_max *= 1.5


class Joueur:
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.foreuse = False
        self.robot = False
        self.xenomorphe = False
        self.etoilemere.batiments.append(Usine(self.etoilemere, self, 0))
        self.etoilemere.proprietaire = self.nom
        self.etoilemere.generer_ressources(2)
        self.couleur = couleur
        self.coque_etoile = False
        self.paralysant = False
        self.techno_bouclier = False
        self.multi_dimension = False
        self.rayon_infini = False
        self.munitions_enflammees = False
        self.generateur_de_trou_noir = False
        self.log = []
        self.artefacts_joueur = []
        self.compteur_robot = 0
        self.temps_procreation = 3000
        self.etoilescontrolees = [etoilemere]

        self.flotte = {"Explorateur": {},
                       "Cargo": {},
                       "Combattant": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte,
                        "creerbatiment": self.creerbatiment,
                        "augmenterniveaubatiment": self.augmenterniveaubatiment,
                        "detruirebatiment": self.detruirebatiment,
                        "explorer_inconnu": self.explorer_inconnu,
                        "ameliorer_vaisseau": self.ameliorer_vaisseau,
                        "manipuler": self.manipuler,
                        "creer_trou_noir": self.creer_trou_noir
                        }
        self.ressources = {
            "population": 100, "nourriture": 200,
            "or": 300, "argent": 400, "bronze": 500, "hydrogene": 500
        }
        self.visible = []
        self.id_batiment = 1

    def manipuler(self, vaisseau_id):
        vaisseau_id = vaisseau_id[0]
        self.xenomorphe = False
        for i in self.parent.joueurs:
            i = self.parent.joueurs[i]
            for j in i.flotte.keys():
                if vaisseau_id in i.flotte[j]:
                    vaisseau = i.flotte[j][vaisseau_id]
                    self.flotte[j][vaisseau_id] = vaisseau
                    if vaisseau in self.visible:
                        self.visible.remove(vaisseau)
                    i.flotte[j].pop(vaisseau_id)
                    vaisseau.proprietaire = self.nom
                    vaisseau.couleur_initiale = i.couleur
                    i.visible.append(vaisseau)

    def creer_trou_noir(self, coord):
        if self.generateur_de_trou_noir:
            x, y = coord
            self.parent.liste_trou_noir.append(TrouNoir(self.parent, x, y))
            self.generateur_de_trou_noir = False

    def ajouter_artefact(self):
        if len(self.parent.artefacts) > 0:
            artefact = random.choice(self.parent.artefacts)

            # self.parent.parent.vue.afficher_artefacts(self)
            self.artefacts_joueur.append(artefact)
            artefact.proprio = self.nom
            self.parent.parent.vue.afficher_message(artefact)
            print(self.artefacts_joueur)
            self.parent.artefacts.remove(artefact)
            self.effet_artefact(artefact)

    def effet_artefact(self, artefact):
        artefact.faire_effet(self)

    def ameliorer_vaisseau(self, vaisseau_id):
        vaisseau = None
        if vaisseau_id in self.flotte["Explorateur"]:
            vaisseau = self.flotte["Explorateur"][vaisseau_id]
        elif vaisseau_id in self.flotte["Cargo"]:
            vaisseau = self.flotte["Cargo"][vaisseau_id]
        elif vaisseau_id in self.flotte["Combattant"]:
            vaisseau = self.flotte["Combattant"][vaisseau_id]

        if vaisseau is not None:
            if self.ressources_necessaires(None, vaisseau):
                vaisseau.ameliorer_vaisseau()

    def tuer_flotte(self, vaisseau):
        modele = self.parent
        for i in modele.joueurs.keys():
            i = modele.joueurs[i]
            if vaisseau in i.visible:
                i.visible.remove(vaisseau)
        if vaisseau.id in self.flotte["Explorateur"]:
            self.flotte["Explorateur"].pop(vaisseau.id)

        elif vaisseau.id in self.flotte["Cargo"]:
            self.flotte["Cargo"].pop(vaisseau.id)

        elif vaisseau.id in self.flotte["Combattant"]:
            self.flotte["Combattant"].pop(vaisseau.id)

    def explorer_inconnu(self, vaisseau_id):
        type_vaisseau = "Explorateur"
        vaisseau = self.flotte[type_vaisseau][vaisseau_id[0]]
        vaisseau.explorer_inconnu()

    def creervaisseau(self, params):
        type_vaisseau = params[0]

        if type_vaisseau == "Cargo":
            if self.ressources_necessaires("Cargo"):
                v = Cargo(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
                self.charger_ressources(v)
                self.flotte[type_vaisseau][v.id] = v

                if self.nom == self.parent.parent.mon_nom:
                    self.parent.parent.lister_objet(type_vaisseau, v.id)
                return v
            else:
                print("Manque de ressources pour construire le Cargo.")

        elif type_vaisseau == "Explorateur":
            if self.ressources_necessaires("Explorateur"):
                v = Explorateur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
                self.charger_ressources(v)
                self.flotte[type_vaisseau][v.id] = v
                if self.nom == self.parent.parent.mon_nom:
                    self.parent.parent.lister_objet(type_vaisseau, v.id)
                return v
            else:
                print("Manque de ressources pour construire l'Explorateur.")

        elif type_vaisseau == "Combattant":
            if self.ressources_necessaires("Combattant"):
                v = Combattant(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
                self.charger_ressources(v)
                self.flotte[type_vaisseau][v.id] = v
                if self.nom == self.parent.parent.mon_nom:
                    self.parent.parent.lister_objet(type_vaisseau, v.id)
                return v
            else:
                print("Manque de ressources pour construire le Combattant.")

    def charger_ressources(self, objet=None):
        self.ressources["or"] -= objet.prix_or
        self.ressources["argent"] -= objet.prix_argent
        self.ressources["bronze"] -= objet.prix_bronze

    def ressources_necessaires(self, type=None, objet=None):
        qte_or = self.ressources["or"]
        qte_argent = self.ressources["argent"]
        qte_bronze = self.ressources["bronze"]
        if objet is not None:
            return (objet.prix_or <= qte_or and
                    objet.prix_argent <= qte_argent and
                    objet.prix_bronze <= qte_bronze)
        else:
            if type == "Tour defensive":
                return (TourDefensive.prix_or <= qte_or and
                        TourDefensive.prix_argent <= qte_argent and
                        TourDefensive.prix_bronze <= qte_bronze)
            elif type == "Ferme":
                return (Ferme.prix_or <= qte_or and
                        Ferme.prix_argent <= qte_argent and
                        Ferme.prix_bronze <= qte_bronze)
            elif type == "Residence":
                return (Ferme.prix_or <= qte_or and
                        Ferme.prix_argent <= qte_argent and
                        Ferme.prix_bronze <= qte_bronze)
            elif type == "Mine":
                return (Mine.prix_or <= qte_or and
                        Mine.prix_argent <= qte_argent and
                        Mine.prix_bronze <= qte_bronze)
            elif type == "Usine":
                return (Usine.prix_or <= qte_or and
                        Usine.prix_argent <= qte_argent and
                        Usine.prix_bronze <= qte_bronze)
            elif type == "Explorateur":
                return (Explorateur.prix_or <= qte_or and
                        Explorateur.prix_argent <= qte_argent and
                        Explorateur.prix_bronze <= qte_bronze)
            elif type == "Cargo":
                return (Cargo.prix_or <= qte_or and
                        Cargo.prix_argent <= qte_argent and
                        Cargo.prix_bronze <= qte_bronze)
            elif type == "Combattant":
                return (Combattant.prix_or <= qte_or and
                        Combattant.prix_argent <= qte_argent and
                        Combattant.prix_bronze <= qte_bronze)

    def creerbatiment(self, infos):
        etoile = infos[1]
        type = infos[0]

        for i in self.etoilescontrolees:
            if i.id == etoile:
                id = self.id_batiment
                self.id_batiment += 1
                if type == "Ferme":
                    i.batiments.append(Ferme(i, self, id))
                    print("Ferme créée pour l'étoile " + str(etoile))
                elif type == "Usine":
                    i.batiments.append(Usine(i, self, id))
                    print("Usine créée pour l'étoile " + str(etoile))
                elif type == "Mine":
                    i.batiments.append(Mine(i, self, id))
                    print("Mine créée pour l'étoile " + str(etoile))
                elif type == "Residence":
                    i.batiments.append(Residence(i, self, id))
                    print("Residence créée pour l'étoile " + str(etoile))
                elif type == "Tour defensive":
                    i.batiments.append(TourDefensive(i, self, id))
                    print("Tour défensive créée pour l'étoile " + str(etoile))
                self.ressources["or"] -= i.batiments[-1].prix_or
                self.ressources["argent"] -= i.batiments[-1].prix_argent
                self.ressources["bronze"] -= i.batiments[-1].prix_bronze
                break

    def detruirebatiment(self, infos):
        batiment_id = infos[0]
        etoile_id = infos[1]
        for etoile in self.etoilescontrolees:
            if etoile.id == etoile_id:
                for i in range(len(etoile.batiments)):
                    if etoile.batiments[i].id == batiment_id:
                        self.ressources["or"] += floor(etoile.batiments[i].prix_or / 2)
                        self.ressources["argent"] += floor(etoile.batiments[i].prix_argent / 2)
                        self.ressources["bronze"] += floor(etoile.batiments[i].prix_bronze / 2)
                        etoile.batiments.pop(i)

    def augmenterniveaubatiment(self, infos):
        batiment_id = infos[0]
        etoile_id = infos[1]
        for i in self.etoilescontrolees:
            if i.id == etoile_id:
                for batiment in i.batiments:
                    if batiment.id == batiment_id:
                        self.ressources["or"] -= batiment.prix_or
                        self.ressources["argent"] -= batiment.prix_argent
                        self.ressources["bronze"] -= batiment.prix_bronze
                        batiment.niveau += 1
                        batiment.prix_bronze *= batiment.niveau
                        batiment.prix_argent *= batiment.niveau
                        batiment.prix_or *= batiment.niveau

    def ciblerflotte(self, ids):
        idori, iddesti, type_cible = ids
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return
                if self.etoilemere.id == iddesti:
                    ori.acquerir_cible(self.etoilemere, type_cible)
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
            elif type_cible == "Flotte":
                modele = self.parent
                for i in modele.joueurs.keys():
                    i = modele.joueurs[i]
                    for j in i.flotte:
                        for k in i.flotte[j]:
                            if k == iddesti:
                                ennemi = i.flotte[j][k]
                                ori.acquerir_cible(ennemi, type_cible)

    def jouer_prochain_coup(self):
        self.avancer_flotte()
        if self.robot:
            self.procreation_robotique()
        population_totale = 0
        for i in self.etoilescontrolees:
            for j in i.batiments:
                j.jouer_prochain_coup()
            i.cooldown_reduction_nourriture += 1
            if i.cooldown_reduction_nourriture >= 250:
                i.reduire_nourriture()
                i.cooldown_reduction_nourriture = 0
            population_totale += i.ressources_humaines["population"]
        population_totale += self.etoilemere.ressources_humaines["population"]
        self.ressources["population"] = population_totale

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

                        if self.nom == self.parent.parent.mon_nom:
                            self.parent.parent.afficher_etoile(self.nom, rep[1])


                    elif rep[0] == "Porte_de_ver":
                        pass

    def procreation_robotique(self):
        self.compteur_robot += 1
        if self.compteur_robot == self.temps_procreation:
            self.compteur_robot = 0
            self.ressources["population"] += math.floor(self.ressources["population"] / 2)


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoilemere, couleur):
        Joueur.__init__(self, parent, nom, etoilemere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20
        self.foreuse = False

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Explorateur"])
            a_verifier = True
            cible = None
            while a_verifier is True:
                cible = random.choice(self.parent.etoiles)
                a_verifier = False
                for joueur in self.parent.joueurs:
                    if joueur != self.nom:
                        if self.parent.joueurs[joueur].etoilemere.id == cible.id:
                            a_verifier = True

            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1


class Artefact:
    def __init__(self):
        self.type = None
        self.description = "artéfact de base"
        self.proprio = None

    def faire_effet(self, parent):
        pass


class CoquePhotovoltaique(Artefact):
    def __init__(self):
        super().__init__()
        self.etat = "actif"
        self.nom = "Coque photovoltique"
        self.description = "Cette technologie permet d'exploiter l'énergie des étoiles environnantes pour remplir le " \
                           "carburant \n des vaisseaux, les rendants presque auto-suffisants dans l'espace."
        self.effet = "Le carburant se recharge à proximité des étoiles."
        self.type = "Énergie"

    def faire_effet(self, parent):
        parent.coque_etoile = True


class Bouclier(Artefact):
    def __init__(self):
        super().__init__()
        self.etat = "passif"
        self.nom = "Bouclier Carbyne"
        self.description = "Artéfact de défense servant à protéger les vaisseaux et les bâtiments d'attaque. Il " \
                           "s'agit de cristaux \n de Carbyne que l'on parsème sur la coque des vaisseaux.  On dit qu'elle " \
                           "est presque indéstructible."
        self.effet = "Bouclier pour chaque vaisseaux/batiments"
        self.type = "Défense"

    def faire_effet(self, parent):
        for k in parent.flotte:
            for j in parent.flotte[k]:
                vaisseau = parent.flotte[k][j]
                vaisseau.ajouter_bouclier()


class InterferenceDeFluxMultidimensionnelle(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Interfereur de flux multidimensionnel"
        self.description = "Cette technologie crée des micro-fissures dimensionnelles permettant d'avoir accès aux " \
                           "informations \n des autres joueurs, leurs ressources, leurs vaisseaux, leurs bâtiments, " \
                           "etc. , et ce, dans toute la galaxie."
        self.effet = "Vision infinie"
        self.type = "Communication"

    def faire_effet(self, parent):
        pass


class ForeuseLuminique(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Foreuse luminique"
        self.description = "Cette technologie permet de forer avec une vitesse quasi-luminique, triplant la vitesse \n" \
                           "d'extraction des minéraux et de production de l'usine."
        self.effet = "Exploitation + Usinage x3"
        self.type = "Exploitation"

    def faire_effet(self, parent):
        parent.foreuse = True
        for etoiles in parent.etoilescontrolees:
            for batiment in etoiles.batiments:
                if isinstance(batiment, Mine) or isinstance(batiment, Usine):
                    batiment.cooldown_min /= 3


class Paralyseur(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Paralyseur"
        self.description = "À chaque 10 secondes, votre prochain projectile gèlera votre adversaire" \
                           "pendant 5 secondes"
        self.effet = "Effet paralysant"
        self.type = "Extermination"

    def faire_effet(self, parent):
        parent.paralysant = True
        for k in parent.flotte:
            for j in parent.flotte[k]:
                vaisseau = parent.flotte[k][j]
                vaisseau.paralysant = True


class RobotReproducteur(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Robot reproducteur"
        self.description = "Donnez à ce robot deux embryons humains et il entamera un procéssus de reproduction " \
                           " \n infini, vous ne manquerez jamais d'êtres humains."
        self.effet = "Population + 5 par cycle"
        self.type = "Reproduction"

    def faire_effet(self, parent):
        parent.robot = True


class ManipulationXenomorphe(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Manipulateur Xenomorphe"
        self.description = "Vous possédez un micro-organisme qui répond à vos ordres, il s'infiltre et prend le " \
                           "contrôle d'un vaisseau ennemi."
        self.effet = "1 vaisseau fait maintenant partie de votre flotte mais l'ennemi ne le sait pas avant d'être " \
                     "attaqué "
        self.type = "Extermination"

    def faire_effet(self, parent):
        parent.xenomorphe = True


class HeritageAncien(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Héritage ancien"
        self.description = "Vous possédez le savoir ancestral d'une population extraterrestre qui dominait autrefois " \
                           "un empire galactique, \n votre gain d'expérience est triplé."
        self.effet = "gain experience x3"
        self.type = "Connaissance"


class TelescopeGigaGalactique(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Téléscope Giga Galactique"
        self.description = "Vous êtes muni d'un téléscope militaire vous permettant de viser des ennemis dans toute \n " \
                           "la galaxie sans pour autant révéler votre position."
        self.effet = "visée infini"
        self.type = "Extermination"

    def faire_effet(self, parent):
        parent.rayon_infini = True
        for k in parent.flotte:
            for j in parent.flotte[k]:
                vaisseau = parent.flotte[k][j]
                vaisseau.rayon_de_tir = parent.parent.largeur * 2


class MunitionEnflammee(Artefact):
    def __init__(self):
        super().__init__()
        self.nom = "Munitions enflammées"
        self.description = "Vous êtes muni de munitions explosives capable d'enflammer la coque d'un vaisseau, " \
                           "il subi des dégats continus "
        self.effet = "munitions enflammées"
        self.type = "Extermination"

    def faire_effet(self, parent):
        parent.munitions_enflammees = True
        for k in parent.flotte:
            for j in parent.flotte[k]:
                vaisseau = parent.flotte[k][j]
                vaisseau.munitions_enflammees = True


class TrouNoir(Porte_de_vers):
    def __init__(self, parent, x, y, couleur="blue", taille=random.randrange(6, 20)):
        super().__init__(parent, x, y, couleur, taille)
        self.x = x
        self.y = y
        self.parent = parent
        self.forces_attraction = [0.5, 1, 1.5, 2]
        self.niveau_attraction = 0
        self.rayon_attraction = 200

    def jouer_prochain_coup(self):
        mod = self.parent
        val = 0

        for joueur in mod.joueurs.keys():
            joueur = mod.joueurs[joueur]
            for type_vaisseau in joueur.flotte.keys():
                try:
                    for identifiant in joueur.flotte[type_vaisseau]:
                        vaisseau = joueur.flotte[type_vaisseau][identifiant]
                        distance = hlp.calcDistance(self.x, self.y, vaisseau.x, vaisseau.y)
                        angle = hlp.calcAngle(vaisseau.x, vaisseau.y, self.x, self.y)

                        # for i in self.rayon_attraction.keys():
                        #     if i[0] < distance < i[1]:
                        #         val = self.rayon_attraction[i]
                        #         break
                        # if val > 0:
                        #     vaisseau.devier(val, angle)

                        pourcentage_distance = distance / self.rayon_attraction
                        if pourcentage_distance < 0.25:
                            val = self.forces_attraction[3]
                            try:

                                vaisseau.recevoir_degat(0.5)
                            except:
                                pass
                        elif pourcentage_distance < 0.50:
                            val = self.forces_attraction[2]
                        elif pourcentage_distance < 0.75:
                            val = self.forces_attraction[1]
                        elif pourcentage_distance < 1:
                            val = self.forces_attraction[0]

                        if val > 0:
                            vaisseau.devier(val, angle)
                except:
                    pass

                    # if self.rayon_attraction >= distance >= self.rayon_attraction - 50:
                    #     vitesse = self.liste_de_vitesse[0]
                    # elif self.rayon_attraction - 51 >= distance >= self.rayon_attraction - 101:
                    #     vitesse = self.liste_de_vitesse[1]
                    # elif self.rayon_attraction - 102 >= distance >= self.rayon_attraction - 152:
                    #     vitesse = self.liste_de_vitesse[2]
                    # elif self.rayon_attraction - 152 >= distance >= 0:
                    #     vitesse = self.liste_de_vitesse[3]

                    # if vitesse > 0:
                    #     vaisseau.x, vaisseau.y = hlp.getAngledPoint(angle, vitesse, vaisseau.x, vaisseau.y)


class GenerateurDeTrouNoir(Artefact):
    def __init__(self):
        super().__init__()
        self.etat = "actif"
        self.nom = "Générateur de trou noir"
        self.description = "Cette technologie permet de générer un trou noir qui attire et détruit les ennemis"
        self.effet = "générer un trou noir lors d'un clic"
        self.type = "Environnement"

    def faire_effet(self, parent):
        parent.generateur_de_trou_noir = True


class Modele:
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 1500
        self.hauteur = 1500
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)
        self.artefacts = []
        self.liste_trou_noir = []
        self.remplir_artefacts()

    def afficher_etoile(self, joueur, cible):
        self.parent.afficher_etoile(joueur, cible)

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
            etoile.ressources_humaines["population"] = 100
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

        if len(self.liste_trou_noir) > 0:
            for i in self.liste_trou_noir:
                i.jouer_prochain_coup()

    def creer_bibittes_spatiales(self, nb_bibittes=0):
        pass

    def reinitialiser_cargo(self, ids):
        for joueur in self.joueurs:
            print(joueur)
            if joueur == ids[0]:
                self.joueurs[joueur].flotte["Cargo"][ids[1]].cible = 0
                self.joueurs[joueur].flotte["Cargo"][ids[1]].etoile_a_collecter = None
                self.joueurs[joueur].flotte["Cargo"][ids[1]].en_chargement = 0
                self.joueurs[joueur].flotte["Cargo"][ids[1]].en_dechargement = 0
                self.joueurs[joueur].flotte["Cargo"][ids[1]].en_retour = 0

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
    def remplir_artefacts(self):

        self.artefacts.append(Bouclier())
        self.artefacts.append(GenerateurDeTrouNoir())
        self.artefacts.append(CoquePhotovoltaique())
        self.artefacts.append(InterferenceDeFluxMultidimensionnelle())
        self.artefacts.append(ForeuseLuminique())
        self.artefacts.append(RobotReproducteur())
        self.artefacts.append(Paralyseur())
        self.artefacts.append(ManipulationXenomorphe())
        self.artefacts.append(HeritageAncien())
        self.artefacts.append(TelescopeGigaGalactique())
        self.artefacts.append(MunitionEnflammee())

##############################################################################
