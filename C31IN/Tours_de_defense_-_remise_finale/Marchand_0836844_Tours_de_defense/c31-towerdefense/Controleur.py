import Modele
import Vue
from tkinter import *


class Controleur:
    def __init__(self):
        self.modele = Modele.Modele(self)
        self.vue = Vue.Vue(self)
        self.vue.root.mainloop()

    def demarrer_jeu(self):
        self.modele.demarrer_partie()

    def nouvelle_partie(self, evt):
        self.demarrer_jeu()
        self.vue.changer_cadre("jeu")
        self.jouer_partie()

    def jouer_partie(self):
        if not self.modele.partie.partie_terminee:
            self.modele.jouer()
            self.vue.afficher_partie()
            self.vue.root.after(30, self.jouer_partie)

    def faire_acheter(self, type_tour):
        return self.modele.partie.faire_acheter(type_tour)

    def faire_upgrade_tour(self, type_tour):
        self.modele.partie.faire_upgrade_tour(type_tour)

    def creer_tour(self, x, y, type_tour):
        tour = self.modele.partie.creer_tour(x, y, type_tour)
        if tour is not None:
            self.vue.afficher_tour(tour)

    def placer_tour(self, type_tour):
        self.modele.partie.placer_tour(type_tour)

    def fin_partie(self):
        if self.modele.partie.partie_gagnee:
            self.vue.afficher_partie_gagnee()
        elif self.modele.partie.partie_terminee:
            self.vue.afficher_fin_partie()
        self.vue.nouveau_score()

    def game_over(self, evt):
        self.vue.redemarrer_interface()
        self.modele.demarrer_partie()
        self.jouer_partie()

    def redemarrer(self, evt):
        self.pause("redemarrer")
        self.vue.redemarrer_interface()
        self.modele.demarrer_partie()

    def pause(self, evt):
        self.modele.partie.pause()
        self.vue.pause(evt)
        self.jouer_partie()

    def creer_annonce(self, annonce, type):
        self.modele.partie.nouvelle_annonce(annonce, type)

    def utiliser_antidepresseur(self, evt):
        self.modele.partie.utiliser_antidepresseur()


# note: fonction pour le button redémarer différente,car les fonctions jouer s'addionnaient créant a chaque fois une vitesse plus forte des creep.pour empêche cela il faudrait mettre
# la variable partie terminer a true mais cela applerais le processus de game-over. il est donc plus simple de tout simplement créer une autre fonction représentant un autre cas d'utilisation.


if __name__ == '__main__':
    c = Controleur()
