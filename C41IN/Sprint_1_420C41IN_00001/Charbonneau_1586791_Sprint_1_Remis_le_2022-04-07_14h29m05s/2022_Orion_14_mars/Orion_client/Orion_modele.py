import ast
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


class Usine(Batiment):
    # PRIX INITIAL
    prix_or = 250
    prix_argent = 400
    prix_bronze = 600

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "usine", 250, 400, 600, joueur, id)

    def jouer_prochain_coup(self):
        if self.cooldown >= 100:
            if self.etoile.ressources_extraites["or"] >= 1:
                self.etoile.ressources_extraites["or"] -= self.niveau
                self.joueur.ressources["or"] += self.niveau
            if self.etoile.ressources_extraites["argent"] >= 1:
                self.etoile.ressources_extraites["argent"] -= self.niveau
                self.joueur.ressources["argent"] += self.niveau
            if self.etoile.ressources_extraites["bronze"] >= 1:
                self.etoile.ressources_extraites["bronze"] -= self.niveau
                self.joueur.ressources["bronze"] += self.niveau
            if self.etoile.ressources_extraites["hydrogene"] >= 1:
                self.etoile.ressources_extraites["hydrogene"] -= self.niveau
                self.joueur.ressources["hydrogene"] += self.niveau
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

    def jouer_prochain_coup(self, joueur=None):
        if self.cooldown >= 500:
            ratio_ressources = {"or": 5, "argent": 20, "bronze": 50, "hydrogene": 20}
            for i in self.liste_ressources:
                self.etoile.ressources_totales[i] -= ratio_ressources[i] * self.niveau
                self.etoile.ressources_extraites[i] += ratio_ressources[i] * self.niveau
                # print(i + str(self.etoile.ressources_extraites[i]))
            self.cooldown = 0
        self.cooldown += 1


class Residence(Batiment):
    # PRIX INITIAL
    prix_or = 25
    prix_argent = 50
    prix_bronze = 75

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "residence", 25, 50, 75, joueur, id)

    def jouer_prochain_coup(self, joueur=None):
        if self.cooldown >= 500:
            self.etoile.ressources_humaines["population"] += 20 * self.niveau
            self.cooldown = 0
        self.cooldown += 1


class Ferme(Batiment):
    prix_or = 10
    prix_argent = 20
    prix_bronze = 30

    def __init__(self, etoile, joueur, id):
        Batiment.__init__(self, etoile, "ferme", 10, 20, 30, joueur, id)

    def jouer_prochain_coup(self, joueur=None):
        pass

    # def activite_batiment(self):
    #     if self.cooldown != 0:
    #         self.cooldown -=Mine créée pour l'étoile1
    #     else:
    #         self.etoile.ressources["or"] += 1
    #         self.etoile.ressources["pierre"] += 1
    #         self.etoile.ressources["bois"] += 1


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
        self.generer_ressources()

    def generer_ressources(self, multiple=1):
        valeur = random.randrange(2, 5) * 1000 * multiple
        self.ressources_totales["or"] = valeur
        self.ressources_totales["argent"] = valeur * 2
        self.ressources_totales["bronze"] = valeur * 3
        self.ressources_totales["hydrogene"] = valeur


class Projectile:
    def __init__(self, x, y, cible):
        self.x = x
        self.y = y
        self.degat = 25
        self.cible = cible
        self.vitesse = 10
        self.cible_atteinte = False

    def tirer_projectile(self, angle):
        self.x, self.y = hlp.getAngledPoint(angle, self.vitesse, self.x, self.y)
        distance = hlp.calcDistance(self.x, self.y, self.cible.x, self.cible.y)
        if distance <= self.vitesse:
            self.cible_atteinte = True
            self.cible.recevoir_degat(self.degat)


class Vaisseau:

    def __init__(self, parent, nom, x, y):
        self.rayon_de_tir = 10
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.vie_max = 100
        self.vie_actuelle = self.vie_max

        self.espace_cargo = 0
        self.carburant = 100
        self.carburant_max = 100
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.cout_en_carburant_par_frame = 0.08
        self.type_cible = None
        self.angle_cible = 0
        self.distance = 0
        self.vitesse_tir = 50
        self.tir_delai = 0
        self.rayon_de_tir = 100
        self.rayon_de_vision = 300
        self.liste_projectiles = []
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte,
                        }

    def recevoir_degat(self, degat):
        self.vie_actuelle -= degat
        if self.vie_actuelle <= 0:
            self.parent.tuer_flotte(self)

    def jouer_prochain_coup(self, trouver_nouveau=0):
        self.tir_delai += 1
        self.verifier_autour()
        if self.cible != 0:
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
        if self.assez_carburant_aller_retour():
            print("assez de carburant")
        else:
            print("ca va mal finir si tu va là")

    def avancer(self):
        self.carburant -= self.cout_en_carburant_par_frame
        if self.carburant >= 0:

            if self.cible != 0:
                x = self.cible.x
                y = self.cible.y

                self.angle_cible = hlp.calcAngle(self.x, self.y, x, y)

                if self.type_cible == "Flotte":
                    if hlp.calcDistance(self.x, self.y, x, y) > 10:
                        self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)

                    if hlp.calcDistance(self.x, self.y, x, y) <= self.rayon_de_tir:
                        self.attaquer_ennemi()

                    if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse and self.cible.vie_actuelle < 0:
                        self.x = x
                        self.y = y
                        self.cible = 0
                        return
                elif self.type_cible == "Etoile":
                    self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
                    if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                        type_obj = type(self.cible).__name__
                        rep = self.arriver[type_obj]()
                        return rep


        else:
            self.carburant = 0

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
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
            self.liste_projectiles.append(Projectile(self.x, self.y, self.cible))

        if self.liste_projectiles:
            for i in self.liste_projectiles:
                i.tirer_projectile(self.angle_cible)
                if i.cible_atteinte:
                    self.liste_projectiles.remove(i)

    def verifier_autour(self):
        for i in self.parent.parent.etoiles:
            if i not in self.parent.etoilescontrolees:
                distance = hlp.calcDistance(self.x, self.y, i.x, i.y)
                if distance < self.rayon_de_vision:
                    self.parent.visible.append(i)
                    if i.proprietaire != "":
                        self.parent.parent.parent.afficher_etoile(i.proprietaire, i)


class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        # self.energie = 500
        self.carburant = 500
        self.carburant_max = 500
        self.taille = 6
        self.vitesse = 1
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

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0 and self.en_chargement == 0 and self.en_dechargement == 0:
            return self.avancer()
        elif self.cible != 0 and self.en_chargement == 1:
            self.collecter_ressources()
        elif self.cible != 0 and self.en_dechargement == 1:
            self.decharger_cargo()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
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
                    if self.cargo_actuel <= self.cargo - 100:
                        if self.cible.ressources_extraites[liste_ressources[self.index_ressources]] >= 100:
                            quantite = 100
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


class Explorateur(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.vitesse = 2
        self.degat = 15
        self.carburant = 200
        self.carburant_max = 200
        self.nouvelle_exploration = False
        self.en_exploration = False

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
        self.tir_delai += 1
        if self.cible != 0:
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
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.vitesse = 1.5
        self.degat = 15
        self.carburant = 90
        self.carburant_max = 90


class Joueur:
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.batiments.append(Usine(self.etoilemere, self, 0))
        self.etoilemere.proprietaire = self.nom
        self.etoilemere.generer_ressources(2)
        self.couleur = couleur
        self.log = []
        self.etoilescontrolees = [etoilemere]
        self.flotte = {"Explorateur": {},
                       "Cargo": {},
                       "Combattant": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte,
                        "creerbatiment": self.creerbatiment,
                        "augmenterniveaubatiment": self.augmenterniveaubatiment,
                        "detruirebatiment": self.detruirebatiment,
                        "explorer_inconnu": self.explorer_inconnu}
        self.ressources = {
            "population": 100, "nourriture": 200,
            "or": 200, "argent": 200, "bronze": 200, "hydrogene": 200
        }
        self.visible = []
        self.visible.extend(self.etoilescontrolees)
        self.id_batiment = 1

    def tuer_flotte(self, vaisseau):
        if vaisseau.id in self.flotte["Explorateur"]:
            self.flotte["Explorateur"].pop(vaisseau.id)
        elif vaisseau.id in self.flotte["Cargo"]:
            self.flotte["Cargo"].pop(vaisseau.id)

    def explorer_inconnu(self, vaisseau_id):
        type_vaisseau = "Explorateur"
        vaisseau = self.flotte[type_vaisseau][vaisseau_id[0]]
        vaisseau.explorer_inconnu()

    def creervaisseau(self, params):
        type_vaisseau = params[0]
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        elif type_vaisseau == "Explorateur":
            v = Explorateur(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        elif type_vaisseau == "Combattant":
            v = Combattant(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)

        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(type_vaisseau, v.id)
        return v

    def ressources_necessaires(self, type=None, batiment=None):
        qte_or = self.ressources["or"]
        qte_argent = self.ressources["argent"]
        qte_bronze = self.ressources["bronze"]
        if batiment is not None:
            return (batiment.prix_or <= qte_or and
                    batiment.prix_argent <= qte_argent and
                    batiment.prix_bronze <= qte_bronze)
        else:
            if type == "Ferme":
                return (Ferme.prix_or <= qte_or and
                        Ferme.prix_argent <= qte_argent and
                        Ferme.prix_bronze <= qte_bronze)
            if type == "Residence":
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
        for i in self.etoilescontrolees:
            for j in i.batiments:
                j.jouer_prochain_coup()

    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                if j.vie_actuelle < 0:
                    pass
                else:
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


class Modele:
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

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
##############################################################################
