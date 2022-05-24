import random
from Id import *


class SkillCheck:
    def __init__(self, joueur, activite, opposant=None, planete=None):
        self.joueur = joueur
        self.opposant = opposant
        self.planete = planete
        self.activite = activite
        self.domination_check = 50  # savoir si on joueur domine l'autre ou pas
        self.seuil_reussite_auto = 80
        self.resultat_event = None
        self.gagnant_versus = None
        self.skill_check()

    def skill_check(self):
        if self.opposant is None:
            self.skill_check_evenement()
        else:
            self.skill_check_versus()

    def skill_check_evenement(self):
        bonus_joueur = self.joueur.bonus.get(self.activite)
        if bonus_joueur >= self.seuil_reussite_auto:
            self.resultat_event = True
        else:
            nbr = random.randint(1, 100)
            if 1 <= nbr <= bonus_joueur:
                self.resultat_event = True
            else:
                self.resultat_event = False

    def skill_check_versus(self):
        bonus_joueur = self.joueur.bonus.get(self.activite)
        if self.planete:
            bonus_opposant = self.planete.ressources["defense_art"] + self.planete.defense_nat
        else:
            bonus_opposant = self.opposant.bonus.get(self.activite)

        if abs(bonus_joueur - bonus_opposant) >= self.domination_check:
            self.gagnant_versus = self.joueur if bonus_joueur > bonus_opposant else self.opposant
        else:
            nbr_joueur = random.randrange(bonus_joueur, 100)
            nbr_opposant = random.randrange(bonus_opposant, 100)

            if nbr_joueur < nbr_opposant:
                self.gagnant_versus = self.joueur
            elif nbr_joueur > nbr_opposant:
                self.gagnant_versus = self.opposant
            else:
                self.skill_check_versus()


class SystemeSolaireEvent:
    def __init__(self, parent, probabilite, duree, threshold, choix, message):
        self.id = get_prochain_id()
        self.parent = parent
        self.probabilite = probabilite
        self.threshold = threshold
        self.systeme = self.parent.systeme
        self.choix = choix
        self.delai_max = 12
        self.duree_initiale = duree
        self.isActive = False
        self.duree = duree
        self.delai = 0
        self.consequence = None
        self.recherches_ajouter = False
        self.message = message
        self.option_choisit = None

    def tick(self):
        if self.isActive:
            self.tick_ressources()

    def ajout_recherches(self, option_choisit):
        if self.choix[option_choisit][0] is not None:
            for key in self.choix[option_choisit][0].keys():
                pass  # def debloquerRecherche(self, nom):

    def tick_ressources(self):
        if self.option_choisit is not None:
            self.delai += 1
            if self.duree > 0:
                self.duree = self.duree - 1
                if self.delai >= self.delai_max:
                    self.delai = 0
                    for key in self.choix[self.option_choisit][1].keys():
                        self.systeme.ressources[key] += self.choix[self.option_choisit][1][key]
        else:
            self.isActive = False
            self.recherches_ajouter = False
            self.systeme.cle_evenement_en_cours = ""
            self.duree = self.duree_initiale
            self.delai = 0


class SSEventsGenerator:
    def __init__(self, systeme):
        self.id = get_prochain_id()
        self.systeme = systeme
        self.modele = self.systeme.parent
        self.vue = self.modele.parent.vue
        self.ressources = systeme.ressources
        self.is_evenement_actif = False
        self.is_evement_choisit = False
        self.evenement_en_cours = None
        self.events = {
            "rebellion": SystemeSolaireEvent(self, 0.3, 900,
                                             self.ressources.get("moral") == 0,
                                             {
                                                 0: [None, {"defense_art": -1, "population": -1}],  # Non
                                                 1: [None, {"defense_art": -1, "population": -1}]  # Oui
                                             },
                                             "Le peuple ont décidé de se rebeller, voulez-vous être hostile?"),
            "epidemie": SystemeSolaireEvent(self, 0.005, 20000,
                                            self.ressources.get("nourriture") < 10000,
                                            {
                                                0: [None, {"popoulation": -1, "or": -1000}],
                                                1: None
                                            },
                                            "Il y a une épidémie!"),
            "blackout": SystemeSolaireEvent(self, 0.2, 600,
                                            self.ressources.get("energie") < 1000,
                                            {
                                                0: [None, {"defense_art": -1}],
                                                1: None
                                            },
                                            "Il y a un blackout sur la planète au complet"),
            "fête de la marmotte": SystemeSolaireEvent(self, 1, 250,
                                                       self.ressources.get("moral") > 60,
                                                       {
                                                           0: [None, {"defense_art": +1, "population": +1}],
                                                           1: None
                                                       },
                                                       "C'est la fête de la marmotte!! Le peuple célèbre l'arrivé d'Éric la marmotte"),

            "bombe nucléaire": SystemeSolaireEvent(self, 1, 1,
                                                   self.ressources.get("moral") < 0,
                                                   {
                                                       0: [None, {"defense_art": -10, "population": -10000}],
                                                       1: None
                                                   },
                                                   "Un bombe nucléaire a tombé sur une des planètes."),
            "empereur Jean-Marc a fait une bonne blague": SystemeSolaireEvent(self, 0.00001, 1, True,
                                                                              {
                                                                                  0: [None, {"population": -100000}],
                                                                                  1: [None, {"moral": 2}]  # Oui
                                                                              },
                                                                              "L'empereur Jean-Marc a fait une bonne blague, VOUS DEVEZ RIRE!! Est-ce qu'elle était drôle?"),
            "catastrophe naturelle": SystemeSolaireEvent(self, 0.005, 1, True,
                                                         {
                                                             0: [None, {"defense_nat": -10, "population": -100}],
                                                             1: None
                                                         },
                                                         "Il y a eu une catastrophe naturel!! ")

        }

    def event_generation(self):
        cle_evenement_en_cours = ""
        cles_events_activees = self.check_thresholds()
        if not self.is_evement_choisit:
            if len(cles_events_activees) > 0:
                cle_evenement_en_cours = self.choisir_event(cles_events_activees)
                self.is_evement_choisit = True
                self.evenement_en_cours = self.events.get(cle_evenement_en_cours)
                if not self.is_evenement_actif:
                    self.message()
                    self.is_evenement_actif = True

        return cle_evenement_en_cours

    def message(self):
        if self.systeme.get_proprietaire() is not None:
            if self.evenement_en_cours.choix[1] is None:
                self.evenement_en_cours.option_choisit = self.vue.creer_boite_information(
                    "Evenement sur : " + self.systeme.id,
                    self.evenement_en_cours.message, self.systeme.get_proprietaire())
            else:
                self.evenement_en_cours.option_choisit = self.vue.creer_boite_information(
                    "Evenement sur : " + self.systeme.id,
                    self.evenement_en_cours.message, self.systeme.get_proprietaire(), 1)
        else:
            self.evenement_en_cours.option_choisit = 0

    def check_thresholds(self):
        tableau_cles_events = []
        for key in self.events.keys():
            event = self.events.get(key)
            if event.threshold:
                tableau_cles_events.append(key)
        return tableau_cles_events

    def choisir_event(self, tableau_events):
        nombre = random.randrange(0, len(tableau_events))
        return tableau_events[nombre]

    def evenement_est_en_cours(self, cle):
        event = self.events.get(cle)
        if random.randrange(0, 1) < event.probabilite:
            event.isActive = True
        return event.isActive

    def modifier_events_positifs(self, prob):
        for key in self.events.keys():
            for options in self.events[key].choix:
                for consequence in options[1]:
                    if consequence > 0:
                        self.events[key].probabilite += prob
