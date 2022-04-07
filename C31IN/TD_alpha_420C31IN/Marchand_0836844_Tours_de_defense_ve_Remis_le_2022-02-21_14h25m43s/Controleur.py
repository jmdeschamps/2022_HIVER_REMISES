import Modele
import Vue
from tkinter import *


class Controleur:
    def __init__(self):
        self.modele = Modele.Modele(self)
        self.vue = Vue.Vue(self)
        self.demarrer_jeu()
        self.jouer_partie()
        self.vue.root.mainloop()

    def demarrer_jeu(self):
        self.modele.demarrer_partie()
        self.vue.creer_interface()

    def jouer_partie(self):
        self.modele.jouer()
        self.vue.afficher_partie()
        if not self.modele.partie.partie_terminee:
            self.vue.root.after(30, self.jouer_partie)

    def creer_tour(self, x, y):
        if self.modele.partie.activer_placer:
            tour = self.modele.partie.creer_tour(x, y)
            if tour is not None:
                self.vue.afficher_tour(tour)
            self.modele.partie.activer_placer = False

    def placer_tour(self, type_tour):
        self.modele.partie.placer_tour(type_tour)
        print(self.modele.partie.type_tour)

    def fin_partie(self):
        if self.modele.partie.partie_gagnee:
            self.vue.afficher_partie_gagnee()
        else:
            self.vue.afficher_fin_partie()

    def redemarrer(self, evt):
        self.modele.demarrer_partie()
        self.vue.redemarrer_interface()
        self.jouer_partie()


if __name__ == '__main__':
    c = Controleur()
