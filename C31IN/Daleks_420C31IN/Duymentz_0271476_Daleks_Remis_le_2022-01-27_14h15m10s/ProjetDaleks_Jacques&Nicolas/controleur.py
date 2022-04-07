from jeu import Jeu
from vue import Vue
import sys


class Controleur():

    def __init__(self):
        self.modele = Jeu()
        self.vue = Vue()
        self.actions_menu_initial = {
            "p": self.demarrer_partie,
            "o": self.choisir_options,
            "s": self.voir_scores,
            "x": self.quitter_jeu
        }
        self.afficher_menu_initial()

    def afficher_menu_initial(self):
        est_valide = False
        while not est_valide:
            reponse = self.vue.afficher_menu_initial()
            if reponse in 'posx':
                self.actions_menu_initial[reponse]()
                est_valide = True
            else:
                self.vue.afficher_message_erreur(1)

    def demarrer_partie(self):
        self.modele.demarrer_partie()
        self.vue.afficher_partie(self.modele.partie_courante)
        self.jouer()

    def jouer(self):
        est_mort = False
        while not est_mort:
            self.modele.partie_courante.trouver_positions_occupees()
            self.afficher_menu_jeu()
            self.vue.afficher_partie(self.modele.partie_courante)
            for dalek in self.modele.partie_courante.daleks:
                est_mort = self.modele.jouer_tour_dalek(dalek)
                self.vue.afficher_partie(self.modele.partie_courante)
                if est_mort:
                    self.afficher_menu_fin_partie()
                    break
            self.modele.partie_courante.retirer_daleks_morts()
            if not self.modele.partie_courante.daleks:
                self.modele.changer_niveau()
                self.vue.afficher_partie(self.modele.partie_courante)

    def choisir_options(self):
        est_valide = False
        while not est_valide:
            options_jeu = {}
            reponse = self.vue.afficher_menu_options()
            if int(reponse[0]) >= 8 and int(reponse[1]) >= 6 and len(reponse[2]) == 1 and reponse[2] in "123":
                options_jeu['largeur'] = int(reponse[0])
                options_jeu['hauteur'] = int(reponse[1])
                options_jeu['difficulte'] = int(reponse[2])
                self.modele.changer_options(options_jeu)
                self.afficher_menu_initial()
                est_valide = True
            else:
                self.vue.afficher_message_erreur(2)

    def voir_scores(self):
        liste_scores = self.modele.lire_scores()
        est_valide = False
        while not est_valide:
            reponse = self.vue.afficher_menu_scores()
            if reponse == 'o':
                liste_scores = self.modele.trier_scores(liste_scores)
                est_valide = True
            else:
                if reponse != 'n':
                    self.vue.afficher_message_erreur(1)
                else:
                    est_valide = True
        est_valide = False
        while not est_valide:
            reponse = self.vue.afficher_scores(liste_scores)
            if reponse == 'o':
                self.afficher_menu_initial()
                est_valide = True
            elif reponse == 'n':
                self.quitter_jeu()
            else:
                self.vue.afficher_message_erreur(1)

    def afficher_menu_jeu(self):
        est_valide = False
        while not est_valide:
            nbr_zappeurs = self.modele.partie_courante.nbr_zappeurs
            reponse = self.vue.afficher_menu_jeu(nbr_zappeurs)
            if reponse in 'qweasdzxc':
                est_valide = self.modele.partie_courante.actions_menu_jeu[reponse](reponse)
                if not est_valide:
                    self.vue.afficher_message_erreur(3)
            elif reponse == 't':
                est_valide = self.modele.partie_courante.actions_menu_jeu[reponse]()
                if not est_valide:
                    self.vue.afficher_message_erreur(3)
            elif reponse == 'y':
                est_valide = self.modele.partie_courante.actions_menu_jeu[reponse]()
                if not est_valide:
                    self.vue.afficher_message_erreur(4)
            else:
                self.vue.afficher_message_erreur(1)

    def afficher_menu_fin_partie(self):
        reponse = self.vue.afficher_menu_fin_partie()
        if reponse is not None:
            self.modele.ecrire_score(reponse)
        self.afficher_menu_initial()

    def quitter_jeu(self):
        self.vue.afficher_message_aurevoir()
        sys.exit()