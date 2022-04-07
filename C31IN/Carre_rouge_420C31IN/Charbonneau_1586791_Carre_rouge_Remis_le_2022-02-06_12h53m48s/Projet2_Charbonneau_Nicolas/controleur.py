from jeu import Jeu
from vue import Vue


class Controleur():
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def jouer(self):
        if not self.modele.partie_courante.est_termine:
            self.modele.incrementer_vitesse()
            self.modele.deplacer_sentinelles()
            self.vue.afficher_objets()
            self.modele.verifier_collision()
            self.modele.verifier_sortie()
            self.vue.root.after(40, self.jouer)
        else:
            self.modele.arreter_chrono()
            self.modele.calculer_points()
            self.vue.afficher_menu_fin_partie()

    def demarrer_chrono(self):
        self.modele.demarrer_chrono()

    def deplacer_pion(self, x, y):
        self.modele.deplacer_pion(x, y)

    def retour_vers_menu(self):
        self.vue.enlever_menu_jeu()
        self.vue.enlever_menu_fin_partie()
        self.modele.reinitialiser_objets()
        self.modele.partie_courante.est_termine = False
        self.vue.afficher_menu_principal()

    def rejouer(self):
        self.vue.enlever_menu_jeu()
        self.vue.enlever_menu_fin_partie()
        self.reinitialiser_objets()
        self.modele.partie_courante.est_termine = False
        self.vue.afficher_menu_jeu()

    def reinitialiser_objets(self):
        self.modele.reinitialiser_objets()

    def ajouter_score(self, duree):
        self.modele.ajouter_score(duree)

    def sauvegarder_session(self, nom):
        self.modele.sauvegarder_session(nom)

    def supprimer_session(self):
        self.modele.supprimer_session()

    def lire_scores(self):
        donnees = self.modele.lire_scores()
        return donnees

    def trier_scores(self):
        donnees = self.modele.trier_scores()
        return donnees

    def effacer_scores(self):
        self.modele.effacer_scores()

    def sauvegarder_options(self, choix_sentinelles, choix_pion, choix_jeu, choix_difficulte):
        self.modele.sauvegarder_options(choix_sentinelles, choix_pion, choix_jeu, choix_difficulte)

    def sortir_menu_session(self):
        self.vue.enlever_menu_session()
        self.vue.afficher_menu_principal()

    def sortir_menu_scores(self):
        self.vue.enlever_menu_scores()
        self.vue.afficher_menu_principal()