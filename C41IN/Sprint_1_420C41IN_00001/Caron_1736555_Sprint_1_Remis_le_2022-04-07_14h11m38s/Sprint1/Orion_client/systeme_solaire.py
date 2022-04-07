import random
from Id import *
from vaisseau import *


class SystemeSolaire:
    def __init__(self, parent, x, y):
        self.id = get_prochain_id()
        self.parent = parent
        self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.espaces_construction = self.taille
        self.defense_nat = random.randrange(1, 30)

        self.ressources = {"moral": 50,
                           "defense_art": 999,
                           "nourriture": 999,
                           "or": 999,
                           "fer": 999,
                           "cuivre": 999,
                           "titanite": 999,
                           "uranium": 999,
                           "hydrogene": 999,
                           "azote": 999,
                           "xenon": 999,
                           "energie": 999
                           }
        self.population = 0
        self.habitable = False
        self.infrastructures = {Mine: [Mine(self, "mine")],
                                Musee: [],
                                Ecole: [],
                                Barraques: [],
                                Usine: [],
                                Ferme: [],
                                UsineTraitementGaz: [],
                                CentraleNucleaire: []
                                }

    def construire(self, categorie):
        # Faut trouver une façon de transformer String en nom de classe. Donc construit l'objet dont le nom de la classe est équivalent
        # la string passé en categorie
        categorie = ""
        nouveau_batiment = self.infrastructures[categorie](self, categorie)
        inventaire_batiments = self.infrastructures[categorie]
        inventaire_batiments.append(nouveau_batiment)

    def productions(self):
        if self.parent.joueurs[self.proprietaire]:
            for key in self.infrastructures.keys():
                qte_batiment = len(self.infrastructures[key])
                if qte_batiment > 0:
                    for batiment in self.infrastructures[key]:
                        production = batiment.production()
                        if len(production) > 0:
                            for ressource in production:
                                ressource_produite, quantite_produite = ressource
                                self.ressources[ressource_produite] += quantite_produite

    def produire_bien(self, bien_a_produire):
        matiere_premiere = bien_a_produire[1]
        assez_riche = True
        for key in matiere_premiere.keys():
            if self.ressources[key] < matiere_premiere[key]:
                assez_riche = False
                break
        if assez_riche:
            for key in matiere_premiere.keys():
                self.ressources[key] -= matiere_premiere[key]
            usine_base = self.infrastructures[Usine][0]
            for usine in self.infrastructures[Usine]:
                if len(usine.ligne_production) < len(usine_base.ligne_production):
                    usine_base = usine
            usine_base.lancer_production(bien_a_produire)


class Infrastructure:
    def __init__(self, parent, type_batiment, ressources):
        self.parent = parent
        self.type_batiment = type_batiment
        self.ressources = ressources
        self.production_base = 0
        self.consommation_base = 0

    def production(self):
        production = []
        consommation = self.consommation()
        if self.parent.ressources["energie"] >= consommation:
            self.parent.ressources["energie"] -= consommation
            #bonus = self.parent.proprietaire.bonus_infrastructures[self.type_batiment]
            bonus = 0
            if bonus:
                bonus_joueur = bonus
            else:
                bonus_joueur = 1
            bonus_moral = self.parent.ressources["moral"] / 100
            for ressource_possible in self.ressources:
                ressource_produite = ressource_possible
                qte_produite = self.production_base * bonus_joueur * bonus_moral
                production.append([ressource_produite, qte_produite])
        return production

    def consommation(self):
        #bonus = self.parent.proprietaire.consommation_infrastructures[self.type_batiment]
        bonus = 0
        if bonus:
            bonus_joueur = bonus
        else:
            bonus_joueur = 1
        consommation = self.consommation_base * bonus_joueur
        return consommation


class Mine(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["fer", "or", "cuivre", "titanite"])
        self.production_base = 10
        self.consommation_base = 0


class Musee(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["moral"])
        self.production_base = 10
        self.consommation_base = 1


class Barraques(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["defense_art"])
        self.production_base = 10
        self.consommation_base = 1


class Ferme(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["nourriture"])
        self.production_base = 10
        self.consommation_base = 0


class UsineTraitementGaz(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["hydrogene", "azote", "xenon"])
        self.production_base = 10
        self.consommation_base = 1


class CentraleNucleaire(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["energie"])
        self.production_base = 10
        self.consommation_base = 0


class Usine(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["progression"])
        self.type_batiment = "usine"
        self.production_base = 1
        self.consommation_base = 1
        self.id = get_prochain_id()
        self.ligne_production = []
        self.pourcentage_production = 0
        self.delai_total = 0
        self.delai_actuel = 0

    def lancer_production(self,bien_a_produire):
       self.ligne_production.append(bien_a_produire)

    def production(self):
        production = []
        if len(self.ligne_production) > 0:
            if self.delai_actuel == 0:
                self.delai_total = self.ligne_production[0][2]
                self.delai_actuel = 0
            consommation = self.consommation()
            if self.parent.ressources["energie"] >= consommation:
               self.parent.ressources["energie"] -= consommation
               #bonus = self.parent.proprietaire.bonus_infrastructures[self.type_batiment]
               bonus = 0
               if bonus:
                    bonus_joueur = bonus
               else:
                   bonus_joueur = 1
               bonus_moral = self.parent.ressources["moral"] / 100
               progression_total = self.production_base * bonus_joueur * bonus_moral
               self.delai_actuel += progression_total
               if self.delai_actuel >= self.delai_total:
                   self.delai_actuel = 0
                   self.delai_total = 0
                   tableau_bien = self.ligne_production.pop(0)
                   bien = tableau_bien[0]
                   if isinstance(bien, str):
                       production.append(bien)
                   elif bien == Vaisseau or bien == Cargo:
                       if bien == Cargo:
                           vaisseau = Cargo(self.parent.parent.joueurs[self.parent.proprietaire], self.parent.proprietaire, self.parent.x + 10, self.parent.y)
                           type_vaisseau = "Vaisseau"
                       else:
                           vaisseau = Vaisseau(self.parent.parent.joueurs[self.parent.proprietaire], self.parent.proprietaire, self.parent.x + 10, self.parent.y)
                           type_vaisseau = "Cargo"
                       self.parent.parent.joueurs[self.parent.proprietaire].flotte[type_vaisseau][vaisseau.id] = vaisseau
        return production


    def consommation(self):
        #bonus = self.parent.proprietaire.consommation_infrastructures[self.type_batiment]
        bonus = 0
        if bonus:
            bonus_joueur = bonus
        else:
            bonus_joueur = 1
        consommation = self.consommation_base * bonus_joueur
        return consommation


class Ecole(Infrastructure):
    def __init__(self, parent, type_batiment):
        super().__init__(parent, type_batiment, ["progression"])
        self.production_base = 10
        self.consommation_base = 1

    def production(self):
        pass
