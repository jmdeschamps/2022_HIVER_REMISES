from vaisseau import *
from systeme_solaire import *
from Orion_modele import *


class RechercheManager:
    artefacts_trouvables = {
        0: "Arsenal de la Crevette-Mante",
        1: "L'Anneau de la Licorne Rose Sacrée",
        2: "Le Fantasmagorique Recueil des Corrections des Daleks",
        3: "Statuette du dieu Mythique Mharssel Lythallyenh",
        4: "360 no scope full cool yolo swag Edgelord",
        5: "Relique de la Sanctus Ordo C'est Beau",
        6: "Migrating Coconuts",
        7: "Le Fameux Modem Hell-X",
        8: "The Mondoshawans's Sixth Element",
        9: "42",
    }

    @staticmethod
    def getRandomArtefact():
        artefact = ""
        resultat = random.randrange(0, 100)
        pourcentage_chance = 10
        if resultat >= (100-pourcentage_chance):
            artefact = RechercheManager.artefacts_trouvables[random.randrange(0, len(RechercheManager.artefacts_trouvables))]
        return artefact

    def __init__(self, joueur):
        self.joueur = joueur
        self.dictionnaire = {
            "Nanotechnologie": {
                "production": [self, {"cuivre": 50000, "or": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 0,
                "fonction": self.reduireCoutRecherches,
                "params": [0.15],
                "Description": "Réduis les coûts des recherches et débloque plusieurs autres recherches"
            },
            "Robotique Avancée": {
                "production": [self, {"fer": 50000, "or": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Nanotechnologie"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["ecole"], 0.5, 0.5],
                "Description": "Augmente l'efficacité de l'école et des recherches"
            },
            "Culture Hydroponique": {
                "production": [self, {"nourriture": 50000, "azote": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["ferme"], 0.5, 0.5],
                "Description": "Augmente la production des fermes"
            },
            "Mineur Robotisé": {
                "production": [self, {"nourriture": 50000, "or": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Robotique Avancée"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["mine"], 0.5, 0.5],
                "Description": "Augmente la production des mines"
            },
            "Extraction de Gaz Exotique": {
                "production": [self, {"azote": 50000, "energie": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Nanotechnologie"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["usineTraitementGaz"], 0.5, 0.5],
                "Description": "Augmente la production des Usines à traitements des Gaz"
            },
            "Fusion Nucléaire": {
                "production": [self, {"uranium": 50000, "xenon": 100000, "specialiste": 1}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Nanotechnologie"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["centraleNucleaire"], 0.5, 0.5],
                "Description": "Augmente la production de la centrale nucléaire"
            },
            "Physique Quantique": {
                "production": [self, {"nourriture": 500000, "cuivre": 500000, "hydrogene": 500000, "specialiste": 5}, 100, Ecole],
                "type": "Age",
                "prerequis": ["Nanotechnologie"],
                "ere_requise": 0,
                "fonction": self.avancerAge,
                "params": ["Physique Quantique", "Age Quantiques"],
                "Description": "Permet de passer à l'âge quantique"
            }, ###########################################################
            "Communications Quantiques": {
                "production": [self, {"energie": 100000, "hydrogene": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 1,
                "fonction": self.debloquerElement,
                "params": ["log_instant", True],
                "Description": "Permet à l'explorateur de communiquer instantanément avec la planète mère"
            },
            "Explorateur Auto-Suffisant": {
                "production": [self, {"cuivre": 100000, "xenon": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Communications Quantiques"],
                "ere_requise": 1,
                "fonction": self.debloquerElement,
                "params": ["planete_a_planete", True],
                "Description": "Permet à l'explorateur de se promener de planète à planète sans devoir revenir à la planète mère"
            },
            "Invention: Vaisseau de combat": {
                "production": [self, {"fer": 100000, "titanite": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 1,
                "fonction": self.debloquerBien,
                "params": ["Combat", [Combat, {"fer": 50000, "titanite": 25000, "hydrogene": 5000}, 20, Usine]],
                "Description": "Nouveau vaisseau qui permet de conquérir des planètes"
            },
            "Sondes Minérales Nanite": {
                "production": [self, {"xenon": 100000, "or": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Geothermal Tracking"],
                "ere_requise": 1,
                "fonction": self.augmenterProductionRessources,
                "params": [["mine"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des mines"
            },
            "Algorithmes d'Assemblage": {
                "production": [self, {"cuivre": 100000, "or": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Robotique Avancée"],
                "ere_requise": 1,
                "fonction": self.augmenterProductionRessources,
                "params": [["usine"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des usines"
            },
            "Histoire SocioCulturelle": {
                "production": [self, {"nourriture": 100000, "titanite": 200000, "specialiste": 5}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 1,
                "fonction": self.augmenterProductionRessources,
                "params": [["musee"], 0.5, 0.5],
                "Description": "Augmente l'efficacité du musée"
            },
            "Expansion Stellaire": {
                "production": [self, {"nourriture": 1000000, "cuivre": 1000000, "azote": 1000000, "specialiste": 10}, 100, Ecole],
                "type": "Age",
                "prerequis": ["Explorateur Auto-Suffisant", "Invention: Vaisseau de combat"],
                "ere_requise": 1,
                "fonction": self.avancerAge,
                "params": ["Expansion Stellaire", "Age Stellaire"],
                "Description": "Permet de passer à l'âge Stellaire"
            }, ##################################################
            "Standardisation de l'Explorateur": {
                "production": [self, {"fer": 200000, "azote": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Algorithmes d'Assemblage"],
                "ere_requise": 2,
                "fonction": self.reduireCoutsProduction,
                "params": ["Vaisseau", 0.25],
                "Description": "Réduis les couts de production du vaisseau d'exploration"
            },
            "Commande Militaire Centralisée": {
                "production": [self, {"nourriture": 200000, "or": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 2,
                "fonction": self.augmenterProductionRessources,
                "params": [["barraques"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des barraques militaires"
            },
            "Cultures Transgéniques": {
                "production": [self, {"nourriture": 200000, "azote": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Culture Hydroponique"],
                "ere_requise": 2,
                "fonction": self.augmenterProductionRessources,
                "params": [["ferme"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des fermes"
            },
            "Propulseurs Ioniques": {
                "production": [self, {"xenon": 200000, "hydrogene": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Standardisation de l'Explorateur"],
                "ere_requise": 2,
                "fonction": self.ameliorerBonus,
                "params": ["vitesse_explorateur", 3],
                "Description": "Améliore la vitesse des vaisseaux d'exploration"
            },
            "Invention: Vaisseau de Cargaison": {
                "production": [self, {"fer": 200000, "uranium": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 2,
                "fonction": self.debloquerBien,
                "params": ["Cargo", [Cargo, {"fer": 200000, "titanite": 25000, "hydrogene": 5000}, 20, Usine]],
                "Description": "Débloque le vaisseau de cargo"
            },
            "Urbanisme Contrôlé": {
                "production": [self, {"or": 200000, "titanite": 400000, "specialiste": 10}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 2,
                "fonction": self.ameliorerBonus,
                "params": ["limite_construction", 5],
                "Description": "Augmente la limite de nombre de batiment de chaque sorte que l'on peut construire sur une planète"
            },
            "Empire Galactique": {
                "production": [self, {"nourriture": 2000000, "cuivre": 2000000, "azote": 2000000, "specialiste": 20}, 100, Ecole],
                "type": "Age",
                "prerequis": ["Invention: Vaisseau de Cargaison", "Propulseurs Ioniques"],
                "ere_requise": 2,
                "fonction": self.avancerAge,
                "params": ["Empire Galactique", "Age Galactique"],
                "Description": "Permet de passer à l'âge Galactique"
            }, ###############################################
            "Ingénierie Modulaire": {
                "production": [self, {"cuivre": 400000, "xenon": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 3,
                "fonction": self.reduireCoutsProduction,
                "params": ["Cargo", 0.25],
                "Description": "Réduis les coûts de production des vaisseau de cargo"
            },
            "Spatioport": {
                "production": [self, {"hydrogene": 400000, "fer": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 3,
                "fonction": self.reduireCoutsProduction,
                "params": ["Combat", 0.25],
                "Description": "Réduis les coûts de production des vaisseaux de guerre"
            },
            "Capteurs Gravitiques": {
                "production": [self, {"uranium": 400000, "xenon": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 3,
                "fonction": self.ameliorerBonus,
                "params": ["vue_planete", 200],
                "Description": "Augmente la vision des planètes"
            },
            "Supraconductivité Appliquée": {
                "production": [self, {"cuivre": 400000, "or": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Fusion Nucléaire"],
                "ere_requise": 3,
                "fonction": self.augmenterProductionRessources,
                "params": [["centraleNucleaire"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des Centrales nucléaires"
            },
            "Bio-Réacteur": {
                "production": [self, {"nourriture": 400000, "azote": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Extraction de Gaz Exotique"],
                "ere_requise": 3,
                "fonction": self.augmenterProductionRessources,
                "params": [["usineTraitementGaz"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des usines de traitement des gaz"
            },
            "Consumérisme Prédictif": {
                "production": [self, {"or": 400000, "titanite": 800000, "specialiste": 20}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Algorithmes d'Assemblage"],
                "ere_requise": 3,
                "fonction": self.augmenterProductionRessources,
                "params": [["usine"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des usines"
            },
            "Unification InterGalactique": {
                "production": [self, {"nourriture": 4000000, "cuivre": 4000000, "azote": 4000000, "specialiste": 50}, 100, Ecole],
                "type": "Age",
                "prerequis": ["Capteurs Gravitiques"],
                "ere_requise": 3,
                "fonction": self.avancerAge,
                "params": ["Unification InterGalactique", "Age InterGalactique"],
                "Description": "Permet d'avancer à l'âge InterGalactique"
            }, ################################################
            "Initiative de Recherche Interplanétaire": {
                "production": [self, {"nourriture": 750000, "or": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 4,
                "fonction": self.reduireCoutRecherches,
                "params": [0.15],
                "Description": "Réduis le coût des recherches"
            },
            "Logistique Interstellaire": {
                "production": [self, {"nourriture": 750000, "energie": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 4,
                "fonction": self.ameliorerBonus,
                "params": ["vitesse_cargo", 0.5],
                "Description": "Augmente la vitesse des vaisseau de cargo"
            },
            "Architecture Adaptative": {
                "production": [self, {"energie": 750000, "xenon": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Urbanisme Contrôlé"],
                "ere_requise": 4,
                "fonction": self.ameliorerBonus,
                "params": ["limite_construction", 5],
                "Description": "Augmente la limite de nombre de batiment de chaque sorte que l'on peut construire sur une planète"
            },
            "Xenobiology": {
                "production": [self, {"nourriture": 750000, "azote": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Robotique Avancée"],
                "ere_requise": 4,
                "fonction": self.augmenterProductionRessources,
                "params": [["ecole"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des écoles et leurs recherches"
            },
            "Holo-divertissement": {
                "production": [self, {"xenon": 750000, "titanite": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Histoire SocioCulturelle"],
                "ere_requise": 4,
                "fonction": self.augmenterProductionRessources,
                "params": [["musee"], 0.5, 0.5],
                "Description": "Augmente l'efficacité des musées"
            },
            "Capteurs Subspatiaux": {
                "production": [self, {"uranium": 750000, "xenon": 1500000, "specialiste": 50}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Capteurs Gravitiques"],
                "ere_requise": 4,
                "fonction": self.ameliorerBonus,
                "params": ["vue_planete", 500],
                "Description": "Augmente la vision des planètes"
            },
            "Conquête Cosmique": {
                "production": [self, {"nourriture": 8000000, "cuivre": 8000000, "azote": 8000000, "specialiste": 100}, 100, Ecole],
                "type": "Age",
                "prerequis": ["Capteurs Subspatiaux", "Initiative de Recherche Interplanétaire"],
                "ere_requise": 4,
                "fonction": self.avancerAge,
                "params": ["Conquête Cosmique", "Age Cosmique"],
                "Description": "Avance vers l'âge cosmique"
            }, #####################################################
            "Vaisseau de Guerre": {
                "production": [self, {"fer": 1000000, "uranium": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Spatioport"],
                "ere_requise": 5,
                "fonction": self.debloquerElement,
                "params": ["abilite_conquete_enemie", True],
                "Description": "Permet désormais d'envahir des planète contrôlées par d'autres joueurs"
            },
            "Satellite Hyperspatiaux": {
                "production": [self, {"fer": 1000000, "hydrogene": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Capteurs Subspatiaux"],
                "ere_requise": 5,
                "fonction": self.ameliorerBonus,
                "params": ["vue_planete", 1000],
                "Description": "Augmente la vision des planètes"
            },
            "Bouclier Planétaire": {
                "production": [self, {"energie": 1000000, "uranium": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Commande Militaire Centralisée"],
                "ere_requise": 5,
                "fonction": self.augmenterProductionRessources,
                "params": [["barraques"], 0.5, 0.5],
                "Description": "Augmente les défenses de la planète"
            },
            "Architecture Idyllique": {
                "production": [self, {"or": 1000000, "titanite": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Architecture Adaptative"],
                "ere_requise": 5,
                "fonction": self.ameliorerBonus,
                "params": ["limite_construction", 5],
                "Description": "Augmente la limite de nombre de batiment de chaque sorte que l'on peut construire sur une planète"
            },
            "Moteur à l'Anti-Matière": {
                "production": [self, {"azote": 1000000, "hydrogene": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": [],
                "ere_requise": 5,
                "fonction": self.ameliorerBonus,
                "params": ["vitesse_guerre", 2],
                "Description": "Augmente la vitesse des vaisseau de guerre"
            },
            "Tactiques d'Invasion Planétaire": {
                "production": [self, {"nourriture": 1000000, "or": 2000000, "specialiste": 100}, 100, Ecole],
                "type": "Recherche",
                "prerequis": ["Vaisseau de Guerre"],
                "ere_requise": 5,
                "fonction": self.ameliorerBonus,
                "params": ["conquete", 20],
                "Description": "Améliore les chances de conquérir des planètes"
            }, ########################################
            "Arsenal de la Crevette-Mante": {
                "production": [self, {"fer": 50000, "xenon": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.ameliorerBonus,
                "params": ["conquete", 5]
            },
            "L'Anneau de la Licorne Rose Sacrée": {
                "production": [self, {"nourriture": 50000, "titanite": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.ameliorerBonus,
                "params": ["limite_construction", 5]
            },
            "Le Fantasmagorique Recueil des Corrections des Daleks": {
                "production": [self, {"or": 50000, "energie": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.reduireCoutRecherches,
                "params": [0.05]
            },
            "360 no scope full cool yolo swag Edgelord": {
                "production": [self, {"titanite": 50000, "xenon": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.ameliorerBonus,
                "params": ["vue_planete", 400]
            },
            "Statuette du dieu Mythique Mharssel Lythallyenh": {
                "production": [self, {"specialiste": 30}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.ressourcesBonus,
                "params": [["nourriture", "or", "fer", "cuivre", "titanite", "uranium", "hydrogene", "azote", "xenon", "energie"], 5000000]
            },
            "Relique de la Sanctus Ordo C'est Beau": {
                "production": [self, {"or": 50000, "titanite": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["mine","musee","ecole","barraques","usine","ferme","usineTraitementGaz","centraleNucleaire"], 0.3, 0]
            },
            "Migrating Coconuts": {
                "production": [self, {"nourriture": 50000, "uranium": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.ameliorerBonus,
                "params": ["vitesse_cargo", 0.5]
            },
            "Le Fameux Modem Hell-X": {
                "production": [self, {"cuivre": 50000, "azote": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.debloquerElement,
                "params": ["log_instant", True]
            },
            "The Mondoshawans's Sixth Element": {
                "production": [self, {"hydrogene": 50000, "xenon": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.augmenterProductionRessources,
                "params": [["mine","musee","ecole","barraques","usine","ferme","usineTraitementGaz","centraleNucleaire"], 0.5, 0]
            },
            "42": {
                "production": [self, {"nourriture": 50000, "or": 10000, "specialiste": 15}, 5000, Ecole],
                "type": "Artefact",
                "prerequis": ["Trouver?"],
                "ere_requise": 0,
                "fonction": self.reduireCoutRecherches,
                "params": [0.05]
            },
        }

    def getRecherches(self, recherches_completee, artefacts_possedes, ere_joueur):
        resultat = {}
        for key in self.dictionnaire.keys():
            liste_prerequis = self.dictionnaire[key]["prerequis"]
            append = True
            if len(liste_prerequis) > 0:
                for prerequis in liste_prerequis:
                    if prerequis not in recherches_completee and prerequis not in artefacts_possedes:
                        append = False
            if ere_joueur < self.dictionnaire[key]["ere_requise"]:
                append = False
            if key in recherches_completee or key in artefacts_possedes:
                append = False
            if append:
                resultat[key] = self.dictionnaire[key]
        return resultat

    def debloquerRecherche(self, nom):
        parametres = self.dictionnaire[nom]["params"]
        if self.dictionnaire[nom]["fonction"] is not None:
            self.dictionnaire[nom]["fonction"](self.joueur, parametres)

    def reduireCoutsProduction(self, joueur, params):
        bien = params[0]
        reduction = params[1]
        cout_actuel = joueur.bien_production[bien][1]
        for ressource in cout_actuel:
            cout_actuel[ressource] -= cout_actuel[ressource]*reduction

    def debloquerElement(self, joueur, params):
        joueur.bonus[params[0]] = True

    def debloquerBien(self, joueur, params):
        cleBien = params[0]
        production = params[1]
        joueur.bien_production[cleBien] = production
        print(joueur.bien_production)

    def augmenterProductionRessources(self, joueur, params):
        batiments = params[0]
        bonus = params[1]
        malus = params[2]
        for batiment in batiments:
            joueur.bonus[batiment] += bonus
            joueur.malus[batiment] += malus

    def ameliorerBonus(self, joueur, params):
        type_bonus = params[0]
        bonus = params[1]
        joueur.bonus[type_bonus] += bonus

    def avancerAge(self, joueur, params):
        joueur.ere_actuelle += 1
        joueur.age = params[1]
        self.dictionnaire[params[0]]["prerequis"] = ["Débloqué!"]

    def ajouter_artefact(self, artefact):
        self.dictionnaire[artefact]["prerequis"] = []

    def reduireCoutRecherches(self, joueur, params):
        reduction = params[0]
        for recherche in self.dictionnaire:
            for key in self.dictionnaire[recherche]["production"][1]:
                if key != "specialiste":
                    cost = self.dictionnaire[recherche]["production"][1][key]
                    cost -= cost*reduction

    def ressourcesBonus(self, joueur, params):
        ressources = params[0]
        quantite = params[1]
        ressourcesPlanete = joueur.systeme_mere.ressources
        for key in ressourcesPlanete:
            if key in ressources:
                ressourcesPlanete[key] += quantite
