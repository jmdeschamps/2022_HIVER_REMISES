# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import ast
from systeme_solaire import *
from map import *
from vaisseau import *
from skillcheck import *
import random
from recherche import *


class Joueur:
    def __init__(self, parent, nom, systeme_mere, couleur):
        self.event = "test"
        self.id = get_prochain_id()
        self.parent = parent
        self.est_IA = False
        self.nom = nom
        self.ere_actuelle = 0
        self.age = "Age Contemporain"
        self.systeme_mere = systeme_mere
        self.systeme_mere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []  # le log des systemes visiter
        self.systemes_controlees = [systeme_mere]
        self.flotte = {
            "Vaisseau": {},
            "Cargo": {},
            "Combat": {}
        }
        self.actions = {"creerbien": self.creer_bien,
                        "ciblerflotte": self.ciblerflotte,
                        "construirebatiment": self.construire_batiment,
                        "fairerecherche": self.rechercher
                        }
        self.bonus = {
            "conquete": 50,
            "mine": 1,
            "musee": 1,
            "ecole": 1,
            "barraques": 1,
            "usine": 1,
            "ferme": 1,
            "usineTraitementGaz": 1,
            "centraleNucleaire": 1,
            "log_instant": False,
            'planete_a_planete' : False,
            "vitesse_explorateur": 1,
            "vitesse_cargo": 1,
            "vitesse_guerre": 1,
            "vue_planete": 0,
            "abilite_conquete_enemie": False,
            "limite_construction": 0
        }
        self.malus = {
            "mine": 1,
            "musee": 1,
            "ecole": 1,
            "barraques": 1,
            "usine": 1,
            "ferme": 1,
            "usineTraitementGaz": 1,
            "centraleNucleaire": 1
        }
        self.bien_production = {
            "Vaisseau": [Vaisseau, {"titanite": 50000, "fer": 25000, "hydrogene": 5000}, 20, Usine],
            "Specialiste": ["specialiste", {"nourriture": 100000, "population": 1}, 100, Ecole],
        }
        self.recherche = RechercheManager(self)
        self.recherches_completee = []
        self.artefacts = []
        self.recherches_possibles = {}
        self.recherches_en_cours = []
        self.mise_a_jour_recherches()

    def ajouter_artefact(self, artefact):
        self.recherche.ajouter_artefact(artefact)

    def mise_a_jour_recherches(self):
        if self.systeme_mere.ressources["specialiste"] > 0:
            self.recherches_possibles = self.recherche.getRecherches(self.recherches_completee, self.artefacts,
                                                                     self.ere_actuelle)
            for recherche in self.recherches_en_cours:
                self.recherches_possibles.pop(recherche, None)
        else:
            self.recherches_possibles = {}

    def rechercher(self, params):
        rechercheAProduire = self.recherches_possibles[params[0]]["production"]
        rechercheAProduire.append(self.recherches_possibles[params[0]]["type"])
        rechercheAProduire.append(params[0])  # Fonction ajoute la clé (nom de la recherche spécifique) à la fin du tableau
        if self.systeme_mere.produire_bien(rechercheAProduire):
            self.recherches_en_cours.append(params[0])

    def creer_bien(self, params):
        type = self.bien_production[params[0]]
        self.systeme_mere.produire_bien(type)

    def construire_batiment(self, params):
        type_batiment = params[0]
        systeme = params[1]
        for systemes in self.systemes_controlees:
            if systemes.id == systeme:
                systemes.construire_batiment(type_batiment)

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
                    self.arriver_vaisseau(vaisseau, type_vaisseau, reponse)

    def arriver_vaisseau(self, vaisseau, type_vaisseau, reponse):
        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
        #       quand on l'attribue aux etoilescontrolees
        #       et que ce passe-t-il si l'etoile a un proprietaire ???
        if reponse[0] == "SystemeSolaire":
            cible = reponse[1]
            self.recevoir_log(vaisseau,cible)


            if vaisseau.artefact != "":
                self.ajouter_artefact(vaisseau.artefact)

            if type_vaisseau == "Combat":
                self.arriver_combat(vaisseau, cible, reponse)
            elif type_vaisseau == "Cargo":
                self.arriver_cargo(vaisseau,cible)
            elif type_vaisseau == "Vaisseau":
               self.arriver_explorateur(vaisseau, cible)

    def recevoir_log(self, vaisseau,cible):
        if cible is self.systeme_mere:
            if not self.bonus["log_instant"]:
                for message in vaisseau.log:
                    if not isinstance(self,IA):
                        print(message)
                    self.log.append(message)
                vaisseau.log = []

        self.parent.parent.uptade_log_vue()


    def arriver_combat(self, vaisseau, cible, reponse):
        resultat_conquete = reponse[2]
        if cible.proprietaire != self.nom:
            if resultat_conquete:
                self.conquete(cible)
        if vaisseau.cible is not vaisseau.parent.systeme_mere:
            vaisseau.acquerir_cible(vaisseau.parent.systeme_mere, "SystemeSolaire")
        else:
            vaisseau.cible = 0

    def conquete(self, cible):
        cible.proprietaire = self.nom
        self.systemes_controlees.append(cible)
        self.parent.systemes_occupees.append(cible)  # ajouter le systeme dans le systeme occupé
        self.parent.parent.afficher_systemes(self.nom, cible)

    def arriver_explorateur(self, vaisseau, cible):
        if self.bonus["planete_a_planete"]:
            vaisseau.cible = 0
        else:
            if vaisseau.cible is not vaisseau.parent.systeme_mere:
                vaisseau.acquerir_cible(vaisseau.parent.systeme_mere, "SystemeSolaire")
            else:
                vaisseau.cible = 0


    def arriver_cargo(self, vaisseau, cible):
        if cible.proprietaire is self.nom:
            pass
            # Aller vider ressources planète dans la cible de reponse à l'indice 1
        if vaisseau.cible is not vaisseau.parent.systeme_mere:
            vaisseau.acquerir_cible(vaisseau.parent.systeme_mere, "SystemeSolaire")
        else:
            vaisseau.cible = 0

    def livraison(self, fonds_manquants, systeme):
        if systeme is not self.systeme_mere:
            livreur = None
            for cargo in self.flotte["Cargo"]:
                if cargo.cible == 0:
                    livreur = cargo
            if livreur is not None:
                inventaire = self.systeme_mere.remplirCargo(fonds_manquants)
                if len(inventaire) > 0:
                    for ressource in inventaire.keys():
                        livreur.cargo[ressource] += inventaire[ressource]
                    livreur.livraison_en_cours = True
                    livreur.acquerir_cible(systeme, "SystemSolaire")
                    return true
            else:
                self.parent.parent.vue.creer_boite_information("Livraison", "Roger le livreur est soit occupé, soit inexistant. Créez un Cargo si vous n'en avez pas.", self.nom)
        else:
            self.parent.parent.vue.creer_boite_information("Manque de fonds", "Votre système mère n'a pas les ressources nécessaires pour créer ce que vous tentez de créer.", self.nom)

    def get_tous_evenements_en_cours(self):
        events_en_cours = []
        for systeme in self.systemes_controlees:
            if systeme.cle_evenement_en_cours != "":
                events_en_cours.append(systeme.cle_evenement_en_cours)
        return events_en_cours

# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, systeme_mere, couleur):
        Joueur.__init__(self, parent, nom, systeme_mere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20
        self.systeme_mere.proprietaire = self.nom
        self.systeme_mere.infrastructures[Usine].append(Usine(self.systeme_mere))
        self.est_IA = True

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            if len(self.flotte["Vaisseau"]) == 0:
                self.creer_bien(["Vaisseau"])
            else:
                for v in self.flotte["Vaisseau"]:
                    cible = random.choice(self.parent.systemes)
                    self.flotte["Vaisseau"][v].acquerir_cible(cible, "SystemeSolaire")
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
        self.cheating = True #False
        self.creer_systemes()
        self.creer_joueurs(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def getRandomArtefact(self):
        return RechercheManager.getRandomArtefact()

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
            systeme.infrastructures[Usine].append(Usine(systeme))
            if self.cheating:
                systeme.ressources = {
                    "moral": 100,
                    "defense_art": 0,
                    "nourriture": 50000000000,
                    "or": 50000000000,
                    "fer": 50000000000,
                    "cuivre": 50000000000,
                    "titanite": 50000000000,
                    "uranium": 50000000000,
                    "hydrogene": 50000000000,
                    "azote": 50000000000,
                    "xenon": 50000000000,
                    "energie": 50000000000,
                    "population": 100,
                    "specialiste": 200,
                    "artefact": ""
                }
            else:
                systeme.ressources = {
                    "moral": 50,
                    "defense_art": 0,
                    "nourriture": 50000,
                    "or": 50000,
                    "fer": 50000,
                    "cuivre": 50000,
                    "titanite": 50000,
                    "uranium": 50000,
                    "hydrogene": 50000,
                    "azote": 50000,
                    "xenon": 50000,
                    "energie": 50000,
                    "population": 10,
                    "specialiste": 0,
                    "artefact": ""
                }
            systeme.proprietaire = self.joueurs[i].nom
            # Ajoute 5 planètes autour de la planète d'origine
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
            systeme = systemes_temp.pop(0)
            self.systemes_occupees.append(systeme)
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), systeme, couleursia.pop(0))

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

    def tick(self):
        for systeme in self.systemes_occupees:
            systeme.tick()
