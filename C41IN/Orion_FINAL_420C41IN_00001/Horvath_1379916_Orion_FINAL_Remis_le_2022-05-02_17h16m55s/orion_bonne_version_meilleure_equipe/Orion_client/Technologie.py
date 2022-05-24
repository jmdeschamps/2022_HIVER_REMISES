from Ressource import *
from Annonce import *
from helper import Helper as hlp
import Vaisseau
import Batiment
import copy

'''
Ce module est structuré de la manière suivante:
- Superclasse Technologie
    + La fct statique technologies_possibles() liste l'ensemble des technologies du jeu.
- Sous-classes génériques TechRessource et TechVaisseau
    + TechRessource : technologies qui améliore la génération passive de ressources.
    + TechVaisseau : technologies qui augmente de niveau un type de vaisseau.
- Classes spécifiques pour technologies avec effets distincts
'''


class Technologie:
    def __init__(self, nom, cout_science, description, prerequis_ressource=None, prerequis_tech=None):
        self.joueur = None
        self.nom = nom
        self.cout_science = cout_science
        self.prerequis_ressource = prerequis_ressource
        self.prerequis_tech = prerequis_tech
        self.description = description

        # prerequis_tech : liste de Strings avec noms de technologies
        # prerequis_ressource : list d'objets de type Ressource

    def verif_acquerir(self, joueur):
        cout_ressource = []
        for tech in joueur.technologies:
            if self.nom == tech.nom:
                joueur.annonce = Annonce("Vous possédez déjà cette technologie!")
                return False
        if self.prerequis_ressource is not None:
            for ressource in self.prerequis_ressource:
                if isinstance(ressource, Energie):
                    if joueur.energie.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez d'énergie.")
                        return False
                elif isinstance(ressource, Nourriture):
                    if joueur.nourriture.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez de nourriture.")
                        return False
                elif isinstance(ressource, Eau):
                    if joueur.eau.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez d'eau.")
                        return False
                elif isinstance(ressource, Fer):
                    if joueur.fer.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez de fer.")
                        return False
                elif isinstance(ressource, Titanium):
                    if joueur.titanium.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez de titanium.")
                        return False
                elif isinstance(ressource, Cuivre):
                    if joueur.cuivre.quantite > ressource.quantite:
                        cout_ressource.append(ressource)
                    else:
                        joueur.annonce = Annonce("Pas assez de cuivre.")
                        return False
        if self.prerequis_tech is not None:
            nbr_match = 0
            for tech in joueur.technologies:
                if tech.nom in self.prerequis_tech:
                    nbr_match += 1
            if nbr_match != len(self.prerequis_tech):
                joueur.annonce = Annonce("Vous ne possédez pas les technologies préalables.")
                return False
        if joueur.science < self.cout_science:
            joueur.annonce = Annonce("Pas assez de science.")
            return False
        else:
            # le joueur répond aux prérequis, on applique les changements
            joueur.science -= self.cout_science
            for ressource in cout_ressource:
                if isinstance(ressource, Energie):
                    joueur.energie.retrait_quantite(ressource.quantite)
                elif isinstance(ressource, Eau):
                    joueur.eau.retrait_quantite(ressource.quantite)
                elif isinstance(ressource, Fer):
                    joueur.fer.retrait_quantite(ressource.quantite)
                elif isinstance(ressource, Titanium):
                    joueur.titanium.retrait_quantite(ressource.quantite)
                elif isinstance(ressource, Cuivre):
                    joueur.cuivre.retrait_quantite(ressource.quantite)
        return True

    # on ajoute la Technologie dans la liste des technologies de joueur
    def acquerir(self, joueur):
        tech = copy.deepcopy(self)
        tech.joueur = joueur
        joueur.annonce = Annonce(f"Vous avez acquis la technologie {self.nom}")
        joueur.technologies.append(tech)
        tech.effet_immediat()
        tech.effet()

    def effet_immediat(self):
        pass

    def effet(self):
        pass

    @staticmethod
    def technologies_possibles():
        t = {}

        # CHEMIN EXPLOITATION
        t["Ferme II"] = TechRessource("Ferme II", 120, "Ferme", 2,
                                      Technologie.description_ressource
                                      (Batiment.Ferme, 2, "Nourriture", 10, "Eau", 3, "Eau", 40),
                                      "nourriture", 10, "eau", 3, [Eau(40)])
        t["Conservation I"] = TechConservation("Conservation I", 215, "Limite de stockage de nourriture: 1000.", 1000,
                                               None, ["Ferme II"])
        t["Ferme III"] = TechRessource("Ferme III", 120, "Ferme", 3,
                                       Technologie.description_ressource
                                       (Batiment.Ferme, 2, "Nourriture", 16, "Eau", 5, "Eau", 120),
                                       "nourriture", 16, "eau", 5, [Eau(120)])
        t["Conservation II"] = TechConservation("Conservation II", 215, "Limite de stockage de nourriture: 1000.", 2500,
                                               None, ["Ferme III"])
        t["Jardin d'Eden"] = Technologie("Jardin d'Eden", 850, "La nourriture n'est plus un problème.", [Nourriture(1000)],
                                     ["Conservation II"])

        t["Cargo II"] = TechVaisseau("Cargo II", 180, Technologie.description_vaisseau(Vaisseau.Cargo, 2), "Cargo", 2)
        t["Cargo III"] = TechVaisseau("Cargo III", 470, Technologie.description_vaisseau(Vaisseau.Cargo, 3), "Cargo", 3)
        t["Raffinerie II"] = TechBatiment("Raffinerie II", 240, Technologie.description_batiment(Batiment.Raffinerie, 2), "Raffinerie", 2, [Fer(325)], ["Cargo II"])
        t["Raffinerie III"] = TechBatiment("Raffinerie III", 500, Technologie.description_batiment(Batiment.Raffinerie, 2), "Raffinerie", 2, [Fer(750)], ["Cargo III"])
        t["Usine II"] = Technologie("Usine II", 275, "Construisez des vaisseaux supérieurs.", [Fer(240)],
                                     ["Autocratie"])
        t["Usine III"] = Technologie("Usine III", 275, "Construisez des vaisseaux de qualité exceptionnelle.", [Fer(515)],
                                    ["Usine II"])

        # CHEMIN DIPLOMATIE
        t["Autocratie"] = TechAutocratie()
        t["Democratie"] = TechDemocratie()
        t["Figure: Politicien I"] = Technologie("Figure: Politicien I", 100, "Recrutez de jeunes politiciens.", [Nourriture(30)], None)
        t["Alliances"] = Technologie("Alliances", 125, "Forgez des alliances stratégiques.", None,
                                     ["Intrication Quantique", "Politicien I"])
        t["Figure: Politicien II"] = Technologie("Figure: Politicien II", 220, "Recrutez des politiciens d'expérience.", [Nourriture(30)], ["Alliances"])
        t["Marche Cosmique"] = Technologie("Marche Cosmique", 225,
                                           "Manipulez l'offre et la demande à l'échelle cosmique.", None,
                                           ["Intrication Quantique"])
        t["Figure: Marchand I"] = Technologie("Figure: Marchand I", 150, "Recrutez des marchands rusés.",
                                                [Nourriture(120)], ["Marche Cosmique"])
        t["Bazaar Eternel"] = Technologie("Bazaar Eternel", 150, "Déployez le bazaar le plus reconnu dans l'univers.",
                                              [Nourriture(1200)], ["Figure: Marchand I"])

        # CHEMIN EXPLORATION
        t["Satellite: Vision I"] = Technologie("Satellite: Vision I", 80,
                                               "Ouvrez les capsules d'information à distance de ces satellites.",
                                               [Titanium(20)])
        t["Intrication Quantique"] = Technologie("Intrication Quantique", 300,
                                                 "Accédez au Marché Cosmique et au Sénat Intergalactique.")
        t["Satellite: Vision II"] = Technologie("Satellite: Vision II", 280,
                                                "Ouvrez les capsules d'information à distance de ces satellites.",
                                                [Titanium(20)])
        t["Figure: Scientifique I"] = Technologie("Figure: Scientifique I", 100,
                                                  "Recrutez des scientifiques d'expérience.", [Eau(25)])
        t["Figure: Scientifique II"] = Technologie("Figure: Scientifique II", 400,
                                                   "Recrutez des scientifiques de grand renom.", [Eau(75)],
                                                   ["Laboratoire II"])
        t["Scout II"] = TechVaisseau("Scout II", 125, Technologie.description_vaisseau(Vaisseau.Scout, 2), "Scout", 2,
                                     [Fer(120)])
        t["Scout III"] = TechVaisseau("Scout III", 375, Technologie.description_vaisseau(Vaisseau.Scout, 3), "Scout", 3,
                                      [Fer(425)])
        t["Pyramide d'Argent"] = Technologie("Pyramide d'Argent", 1250,
                                             "Faites la découverte d'une Merveille : Pyramide d'Argent.", [Eau(250)],
                                             ["Scout III"])
        t["Colonisateur I"] = TechVaisseau("Colonisateur I", 140,
                                           Technologie.description_vaisseau(Vaisseau.Colonisateur, 2), "Colonisateur",
                                           2, [Fer(250)])
        t["Laboratoire II"] = Technologie("Laboratoire II", 345, "Menez des expériences inédites.", [Nourriture(440)],
                                     ["Figure: Scientifique I"])
        t["Laboratoire III"] = Technologie("Laboratoire III", 750, "Propulsez la science de votre civilisation vers des sommets inespérés.", [Nourriture(715)],
                                    ["Figure: Scientifique II"])
        t["Grande Universite"] = Technologie("Grande Universite", 1500, "Merveille: Soyez la civilisation la plus érudite de l'univers.", [Nourriture(1215)],
                                    ["Laboratoire III"])

        # CHEMIN MILITAIRE
        t["Satellite: Defense I"] = TechSatDefensif("Satellite: Defense I", 270, [Cuivre(215)], None, 1)
        t["Figure: General I"] = Technologie("Figure: General I", 85, "Recrutez des généraux d'expérience", [Eau(100)],
                                             ["Colonisateur I"])
        t["Figure: General II"] = Technologie("Figure: General II", 285, "Recrutez des généraux redoutables.", [Eau(200)],
                                             ["Destroyer I"])
        t["Destroyer I"] = TechVaisseau("Destroyer I", 400, Technologie.description_vaisseau(Vaisseau.Destroyer, 1),
                                        "Destroyer", 1, [Fer(500)], ["Figure: General I"])
        t["Destroyer II"] = TechVaisseau("Destroyer II", 800, Technologie.description_vaisseau(Vaisseau.Destroyer, 2),
                                        "Destroyer", 1, [Fer(800)], ["Figure: General II"])
        t["Satellite: Defense II"] = TechSatDefensif("Satellite: Defense II", 500, [Cuivre(625)], ["Figure: General I"],
                                                     2)
        t["Spacefighter I"] = TechVaisseau("Spacefighter I", 210,
                                           Technologie.description_vaisseau(Vaisseau.Spacefighter, 1), "Spacefighter",
                                           1, [Fer(250)])
        t["Rage de Vivre"] = TechRageDeVivre()
        t["Spacefighter II"] = TechVaisseau("Spacefighter II", 500,
                                            Technologie.description_vaisseau(Vaisseau.Spacefighter, 2), "Spacefighter",
                                            2, [Titanium(125)], ["Rage de Vivre"])
        t["Flotte Renforcee"] = TechFlotteRenforcee()

        return t

    @staticmethod
    def description_ressource(type_infrastructure, niveau, ressource_generee, qte_generee, ressource_entretient,
                              cout_entretient, ressource_acquisition, cout_acquisition):
        description = \
            f"Amélioration niveau {niveau} de {type_infrastructure.__name__}:\n" \
            f"Génère: {qte_generee} {ressource_generee}.\n" \
            f"Coût d'entretient: {cout_entretient} {ressource_entretient}.\n" \
            f"Coût d'acquisition: {cout_acquisition} {ressource_acquisition}.\n"
        return description

    @staticmethod
    def description_vaisseau(type_vaisseau, niveau):
        description = \
            f"Amélioration niveau {niveau} du {type_vaisseau.__name__}:\n" \
            f"{type_vaisseau.niveaux[niveau - 1][0]} Énergie maximum.\n" \
            f"{type_vaisseau.niveaux[niveau - 1][1]} Consommation d'énergie.\n" \
            f"{type_vaisseau.niveaux[niveau - 1][2]} Vitesse.\n" \
            f"{type_vaisseau.niveaux[niveau - 1][3]} HP Maximum.\n" \
            f"{type_vaisseau.niveaux[niveau - 1][4]} Dégâts.\n" \
            f"{type_vaisseau.niveaux[niveau - 1][5]} Caspule(s) maximum.\n"
        if type_vaisseau is Vaisseau.Cargo:
            description += \
                f"{type_vaisseau.niveaux[niveau - 1][6]} Vitesse d'extraction.\n" \
                f"{type_vaisseau.niveaux[niveau - 1][7]} Énergie emmagasinée.\n" \
                f"{type_vaisseau.niveaux[niveau - 1][8]} Ressource emmagasinée.\n"
        return description

    @staticmethod
    def description_batiment(type_batiment, niveau):
        description = \
            f"Amélioration niveau {niveau} du {type_batiment.__name__}:\n"
        if type_batiment is Batiment.Raffinerie:
            description += \
                f"Capacité de stockage de minéraux: {type_batiment.niveaux[niveau - 1]}.\n"
        return description


class TechRessource(Technologie):
    def __init__(self, nom, cout_science, type_infrastructure, niveau, description, generation, generation_valeur,
                 cout_entretien, entretien_valeur,
                 prerequis_tech=None, prerequis_ressource=None):
        Technologie.__init__(self, nom, cout_science, description, prerequis_tech, prerequis_ressource)
        self.type_infrastructure = type_infrastructure
        self.niveau = niveau
        self.generation = generation
        self.generation_valeur = generation_valeur
        self.cout_entretien = cout_entretien
        self.entretien_valeur = entretien_valeur

    def effet(self):
        self.joueur.niveaux[self.type_infrastructure] = self.niveau
        self.joueur.generation_passive[self.generation] += self.generation_valeur
        self.joueur.cout_passif[self.cout_entretien] += self.entretien_valeur


class TechConservation(Technologie):
    def __init__(self, nom, cout_science, description, limite_nourriture, prerequis_ressource=None,
                 prerequis_tech=None):
        Technologie.__init__(self, nom, cout_science, description, prerequis_ressource, prerequis_tech)
        self.limite_nourriture = limite_nourriture

    def effet_immediat(self):
        self.joueur.limite_nourriture = self.limite_nourriture


class TechVaisseau(Technologie):
    def __init__(self, nom, cout_science, description, type_vaisseau, niveau, prerequis_tech=None,
                 prerequis_ressource=None):
        Technologie.__init__(self, nom, cout_science, description, prerequis_tech, prerequis_ressource)
        self.type_vaisseau = type_vaisseau
        self.niveau = niveau

    def effet(self):
        # pour les futurs vaisseaux
        self.joueur.niveaux[self.type_vaisseau] = self.niveau

        # pour les vaisseaux actuels
        if self.joueur.flotte[self.type_vaisseau] is not None:
            for vaisseau in self.joueur.flotte[self.type_vaisseau]:
                vaisseau.niveau = self.niveau
                vaisseau.accorder_niveau()


class TechBatiment(Technologie):
    def __init__(self, nom, cout_science, description, type_batiment, niveau, prerequis_tech=None, prerequis_ressource=None):
        Technologie.__init__(self, nom, cout_science, description, prerequis_tech, prerequis_ressource)
        self.type_batiment = type_batiment
        self.niveau = niveau

    def effet(self):
        # pour les futurs bâtiments
        self.joueur.niveaux[self.type_batiment] = self.niveau

        # pour les bâtiments actuels
        for etoile in self.joueur.etoiles_controlees:
            if self.joueur.etoiles_controlees.batiment[self.type_batiment] is not None:
                for batiment in self.joueur.etoiles_controlees.batiment[self.type_batiment]:
                    batiment.niveau = self.niveau
                    batiment.accorder_niveau()


class TechAutocratie(Technologie):
    def __init__(self, nom="Autocratie", cout_science=75):
        Technologie.__init__(self, nom, cout_science, None)
        self.description = "Gouvernez d'une main de fer votre civilisation.\nEntretien nourriture -5."

    def effet(self):
        self.joueur.cout_passif["nourriture"] = hlp.clamp(self.joueur.cout_passif["nourriture"] - 5, 0, 9999)


class TechDemocratie(Technologie):
    def __init__(self, nom="Démocratie", cout_science=140):
        Technologie.__init__(self, nom, cout_science, None)
        self.description = "C'est au peuple de décider.\nGénération de moral +0.5."

    def effet(self):
        self.joueur.generation_passive["moral"] += 0.5


class TechRageDeVivre(Technologie):
    def __init__(self, nom="Rage de Vivre", cout_science=100):
        Technologie.__init__(self, nom, cout_science, None)
        self.description = "Chacun de vos vaisseaux reçoit:\n+20 HP.\n+2 Dégât."
        self.prerequis_tech = ["Spacefighter I"]
        self.prerequis_ressource = [Eau(35)]

    def effet_immediat(self):
        for type_vaisseau in self.joueur.flotte:
            for vaisseau in type_vaisseau:
                self.effet(vaisseau)

    def effet(self, vaisseau=None):
        if vaisseau is not None:
            vaisseau.max_hp += 20
            vaisseau.degat += 2


class TechFlotteRenforcee(Technologie):
    def __init__(self, nom="Rage de vivre", cout_science=100):
        Technologie.__init__(self, nom, cout_science, None)
        self.description = "Chacun de vos vaisseaux reçoit:\n+70 HP.\n+10 Dégât."
        self.prerequis_tech = ["Rage de Vivre"]
        self.prerequis_ressource = [Titanium(850)]

    def effet_immediat(self):
        for type_vaisseau in self.joueur.flotte:
            for vaisseau in type_vaisseau:
                self.effet(vaisseau)

    def effet(self, vaisseau=None):
        if vaisseau is not None:
            vaisseau.max_hp += 70
            vaisseau.degat += 5


class TechSatDefensif(Technologie):
    def __init__(self, nom, cout_science, ressource, techs, niveau):
        Technologie.__init__(self, nom, cout_science, None, ressource, techs)
        self.nom = nom
        self.cout_science = cout_science
        self.niveau = niveau
        self.description = f"Vos satellites défensifs ont:\n" \
                           f"Dégâts: {Batiment.SatDefensif.niveaux[self.niveau - 1][0]}.\n" \
                           f"Rayon: {Batiment.SatDefensif.niveaux[self.niveau - 1][1]}.\n" \
                           f"Vitesse: {Batiment.SatDefensif.niveaux[self.niveau - 1][2]}.\n" \
                           f"Cooldown de tir: {Batiment.SatDefensif.niveaux[self.niveau - 1][3]}.\n"
        self.prerequis_tech = techs
        self.prerequis_ressource = ressource

    def effet_immediat(self):
        self.joueur.niveaux["SatDefensif"] = self.niveau
        for batiment in self.joueur.etoiles_controlees.batiment:
            if isinstance(batiment, Batiment.SatDefensif):
                self.effet(batiment)

    def effet(self, satellite=None):
        satellite.niveau = self.joueur.niveaux["SatDefensif"]
        satellite.accorder_niveau()
