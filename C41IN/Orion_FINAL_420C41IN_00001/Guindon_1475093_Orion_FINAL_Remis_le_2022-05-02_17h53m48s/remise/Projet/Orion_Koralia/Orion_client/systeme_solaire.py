import random
from Id import *
from vaisseau import *
import sys
from skillcheck import *


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
        self.cooldown_bebe_max = 1000
        self.cooldown_bebe = self.cooldown_bebe_max
        self.ressources = {
            "moral": 50,
            "defense_art": 0,
            "nourriture": random.randrange(1000,100000),
            "or": random.randrange(1000,100000),
            "fer": random.randrange(1000,100000),
            "cuivre": random.randrange(1000,100000),
            "titanite": random.randrange(1000,100000),
            "uranium": random.randrange(1000,100000),
            "hydrogene": random.randrange(1000,100000),
            "azote": random.randrange(1000,100000),
            "xenon": random.randrange(1000,100000),
            "energie": random.randrange(1000,100000),
            "population": 0,
            "specialiste": 0,
            "artefact": self.parent.getRandomArtefact()
        }
        self.habitable = False
        self.infrastructures = {Mine: [],
                                Musee: [],
                                Ecole: [],
                                Barraques: [],
                                Usine: [],
                                Ferme: [],
                                UsineTraitementGaz: [],
                                CentraleNucleaire: []
                                }
        self.batiment_en_cours = None
        self.livraison_en_attente = False
        self.limite_infrastructures = 5
        self.rayon_fog = 400
        self.eventsGenerator = SSEventsGenerator(self)
        self.cle_evenement_en_cours = ""
        self.delai_entre_event = 0
        self.delai_entre_event_max = 500

    def get_proprietaire(self):
        prop = None
        if self.proprietaire != "":
            prop = self.parent.joueurs[self.proprietaire]
        return prop
    
    def get_fog(self):
        return self.rayon_fog + self.get_proprietaire().bonus["vue_planete"]
    
    def tick(self):
        self.productions()
        self.nourrir_population()
        self.faire_bebes()
        self.tick_event()
        self.finir_batiment()

    def construire_batiment(self, type_batiment):
        nom_classe = getattr(sys.modules[__name__], type_batiment)
        if len(self.infrastructures[nom_classe]) < (self.limite_infrastructures+self.get_proprietaire().bonus["limite_construction"]):
            fonds_manquants = {}
            assez_riche = True
            for key in nom_classe.cost.keys():
                if self.ressources[key] < nom_classe.cost[key]:
                    assez_riche = False
                    fonds_manquants[key] = (int)((nom_classe.cost[key]-self.ressources[key])/1000)+1
            if assez_riche:
                for key in nom_classe.cost.keys():
                    self.ressources[key] -= nom_classe.cost[key]
                batiment = nom_classe(self)
                self.infrastructures[nom_classe].append(batiment)
            else:
                livraison_en_cours = self.get_proprietaire().livraison(fonds_manquants, self)
                if livraison_en_cours:
                    self.parent.parent.vue.creer_boite_information("Livraison", "Roger s'en vient vous livrer les ressources nécessaires, veuillez reconstruire plus tard.", self.proprietaire)
                    self.batiment_en_cours.append(nom_classe)
                    self.livraison_en_attente = True
        else:
            self.parent.parent.vue.creer_boite_information("Maximum Atteint","Vous avez atteint la limite pour ce type de bâtiment", self.proprietaire)

    def finir_batiment(self):
        if self.batiment_en_cours is not None and self.livraison_en_attente is not None:
            self.construire_batiment(self.batiment_en_cours[0])

    def remplirCargo(self, commande):
        matiere_premiere = commande
        fonds_manquants = ""
        assez_riche = True
        for key in matiere_premiere.keys():
            if self.ressources[key] < matiere_premiere[key]:
                assez_riche = False
                fonds_manquants += str((int)((matiere_premiere[key]-self.ressources[key])/1000)+1)+" "+key+", "
        if assez_riche:
            for key in matiere_premiere.keys():
                self.ressources[key] -= matiere_premiere[key]
            return commande
        else:
            self.parent.parent.vue.creer_boite_information("Fonds insuffisants","T'es pauvre, il te manque: "+ fonds_manquants+ "!", self.proprietaire)
            return {}

    def tick_event(self):
        if self.cle_evenement_en_cours != "":
            self.eventsGenerator.events[self.cle_evenement_en_cours].tick()
        else:
            self.delai_entre_event += 1
            if self.delai_entre_event >= self.delai_entre_event_max:
                self.delai_entre_event = 0
                self.cle_evenement_en_cours = self.eventsGenerator.event_generation()


    def productions(self):
        if self.get_proprietaire():
            for key in self.infrastructures.keys():
                qte_batiment = len(self.infrastructures[key])
                if qte_batiment > 0:
                    for batiment in self.infrastructures[key]:
                        production = batiment.production()
                        if len(production) > 0:
                            for ressource in production:
                                ressource_produite, quantite_produite = ressource
                                if ressource_produite == "defense_art":
                                    if self.ressources[ressource_produite] + quantite_produite <=60:
                                        self.ressources[ressource_produite] += quantite_produite
                                else:
                                    self.ressources[ressource_produite] += quantite_produite


    def nourrir_population(self):
        self.ressources["nourriture"] -= self.ressources["population"]
        if self.ressources["nourriture"] <= 0:
            self.ressources["nourriture"] = 0
            self.ressources["moral"] -= 0.0001*self.ressources["population"]

    def faire_bebes(self):
        if self.ressources["moral"] >= 30:
            self.cooldown_bebe -= 1
            if self.cooldown_bebe == 0:
                self.ressources["population"] += 1
                self.cooldown_bebe = self.cooldown_bebe_max

    def produire_bien(self, bien_a_produire):
        matiere_premiere = bien_a_produire[1]
        batiment = bien_a_produire[3]
        fonds_manquants = ""
        assez_riche = True
        for key in matiere_premiere.keys():
            if self.ressources[key] < matiere_premiere[key]:
                assez_riche = False
                if key == "specialiste":
                    fonds_manquants += str(matiere_premiere[key] - self.ressources[key]) + " " + key + ", "
                else:
                    fonds_manquants += str((int)((matiere_premiere[key]-self.ressources[key])/1000)+1)+" "+key+", "
        if assez_riche and len(self.infrastructures[batiment]) > 0:
            for key in matiere_premiere.keys():
                self.ressources[key] -= matiere_premiere[key]
            batiment_base = self.infrastructures[batiment][0]
            for batiment in self.infrastructures[batiment]:
                if len(batiment.ligne_production) < len(batiment_base.ligne_production):
                    batiment_base = batiment
            batiment_base.lancer_production(bien_a_produire)
            return True
        else:
            if not assez_riche:
                titre = "Fonds insuffisants"
                message = "T'es pauvre, il te manque: "+fonds_manquants+"!"
            else:
                titre = "Batiment manquant"
                message = "Vous devez posséder un.e " + batiment.__name__ + " pour produire ce bien!"
            self.parent.parent.vue.creer_boite_information(titre, message, self.proprietaire)
       
    def retourner_infrasctructure(self):
        infrasctures = {}
        for key in self.infrastructures.keys():
            nbr_infrasctructures = len(self.infrastructures[key])
            nom_classe = key.__name__
            infrasctures.update({nom_classe: nbr_infrasctructures})
        return infrasctures

    def retourner_ressources(self):
        res ={}
        for key in self.ressources.keys():
            nbr_res = self.ressources[key]
            nom_classe = key
            res.update({nom_classe: nbr_res})
        return res
     


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
            bonus_joueur = self.parent.get_proprietaire().bonus[self.type_batiment]
            bonus_moral = self.parent.ressources["moral"] / 100
            bonus_population = (self.parent.ressources["population"]/100)+1 if self.parent.ressources["population"] > 0 else 0
            for ressource_possible in self.ressources:
                ressource_produite = ressource_possible
                qte_produite = self.production_base * bonus_joueur * bonus_moral * bonus_population
                production.append([ressource_produite, qte_produite])
        return production

    def lancer_production(self,bien_a_produire):
        self.ligne_production.append(bien_a_produire)

    def progresser(self, bonus_travailleurs=1):
        progres = []
        if len(self.ligne_production) > 0:
            if self.delai_actuel == 0:
                self.delai_total = self.ligne_production[0][2]
                self.delai_actuel = 0
            consommation = self.consommation()
            if self.parent.ressources["energie"] >= consommation:
                self.parent.ressources["energie"] -= consommation
                bonus_joueur = self.parent.get_proprietaire().bonus[self.type_batiment]
                bonus_moral = self.parent.ressources["moral"] / 100
                progression_total = self.production_base * bonus_joueur * bonus_moral * bonus_travailleurs
                self.delai_actuel += progression_total
                if self.delai_actuel >= self.delai_total:
                    self.delai_actuel = 0
                    self.delai_total = 0
                    tableau_bien = self.ligne_production.pop(0)
                    progres = self.finir_progression(tableau_bien)
        return progres

    def consommation(self):
        malus_joueur = self.parent.get_proprietaire().malus[self.type_batiment]
        consommation = self.consommation_base * malus_joueur
        return consommation


class Mine(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "mine", ["fer", "or", "cuivre", "titanite", "uranium"])
        self.production_base = 10
        self.consommation_base = 1


class Musee(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "musee", ["moral"])
        self.production_base = 0.001
        self.consommation_base = 1


class Barraques(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "barraques", ["defense_art"])
        self.production_base = 1
        self.consommation_base = 1



class Ferme(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "ferme", ["nourriture"])
        self.production_base = 30
        self.consommation_base = 0


class UsineTraitementGaz(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "usineTraitementGaz", ["hydrogene", "azote", "xenon"])
        self.production_base = 10
        self.consommation_base = 1


class CentraleNucleaire(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "centraleNucleaire", ["energie"])
        self.production_base = 10
        self.consommation_base = 0


class Usine(Infrastructure):
    cost = {"fer": 15000,
            "or" : 13000
            }
    def __init__(self, parent):
        super().__init__(parent, "usine", ["progression"])
        self.production_base = 1
        self.consommation_base = 1
        self.id = get_prochain_id()
        self.ligne_production = []
        self.delai_total = 0
        self.delai_actuel = 0

    # Fonction qui dit progresse au lieu de produire
    def production(self):
        bonus_population = (self.parent.ressources["population"] / 100) + 1
        return self.progresser(bonus_population)

    # Fonction qui s'adapte au type de produits possible pour ce bâtiment
    def finir_progression(self, tableau_bien):
        production = []
        bien = tableau_bien[0]
        if isinstance(bien, str):
            production.append([bien, 1])
        elif bien == Vaisseau or bien == Cargo or bien == Combat:
            type_vaisseau = None
            vaisseau = None
            if bien == Cargo:
                vaisseau = Cargo(self.parent.get_proprietaire(),
                                 self.parent.proprietaire, self.parent.x + 10, self.parent.y)
                type_vaisseau = "Cargo"
            elif bien == Vaisseau:
                vaisseau = Vaisseau(self.parent.get_proprietaire(),
                                    self.parent.proprietaire, self.parent.x + 10, self.parent.y)
                type_vaisseau = "Vaisseau"
            elif bien == Combat:
                vaisseau = Combat(self.parent.get_proprietaire(),
                                    self.parent.proprietaire, self.parent.x + 10, self.parent.y)
                type_vaisseau = "Combat"
            self.parent.get_proprietaire().flotte[type_vaisseau][
                vaisseau.id] = vaisseau
        return production

class Ecole(Infrastructure):
    cost = {"fer": 15000,
            "or": 13000,
            }
    def __init__(self, parent):
        super().__init__(parent, "ecole", ["progression"])
        self.production_base = 10
        self.consommation_base = 1
        self.ligne_production = []
        self.delai_total = 0
        self.delai_actuel = 0

    # Fonction qui dit progresse au lieu de produire
    def production(self):
        bonus_specialiste = (self.parent.ressources["specialiste"] / 100) + 1
        return self.progresser(bonus_specialiste)

    ########## Fonction qui s'adapte au type de produits possible pour ce bâtiment
    def finir_progression(self, tableau_bien):
        joueur_propriétaire = self.parent.get_proprietaire()
        production = []
        classe_produite = tableau_bien[0]
        if tableau_bien[-2] in ["Recherche", "Artefact", "Age"]:
            nom_recherche = tableau_bien[-1]
            self.parent.ressources["specialiste"] += tableau_bien[1]["specialiste"]
            joueur_propriétaire.recherche.debloquerRecherche(nom_recherche)
            joueur_propriétaire.recherches_en_cours.remove(nom_recherche)
            type = tableau_bien[-2]
            if type == "Recherche":
                joueur_propriétaire.recherches_completee.append(nom_recherche)
            elif type == "Artefact":
                joueur_propriétaire.artefacts.append(nom_recherche)
            elif type == "Age":
                joueur_propriétaire.log.append(["Nouvelle Âge: ", nom_recherche])
                self.parent.parent.parent.vue.creer_boite_information("Nouvelle Âge",
                                                               "Vous venez d'entrer dans un nouvel ère pour votre civilisation!", self.parent.proprietaire)
        elif isinstance(classe_produite, str):
            production.append([classe_produite, 1])
        joueur_propriétaire.mise_a_jour_recherches()
        return production


