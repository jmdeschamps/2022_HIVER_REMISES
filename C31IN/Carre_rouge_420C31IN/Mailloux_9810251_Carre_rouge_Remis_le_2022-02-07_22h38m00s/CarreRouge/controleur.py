import time

import vue
import modele

class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = modele.Modele(self)
        self.vue = vue.Vue(self)
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.partie_en_cours = 1
        self.jouer_partie()

    def replacer_jeu(self):
        self.vue.rebind()
        self.vue.scores_update()
        self.modele.replacer_jeu()
        self.vue.afficher_partie()
        self.modele.pret = True

    def jouer_partie(self):
        if self.partie_en_cours and self.modele.pret:
            self.modele.jouer_tour()
            self.vue.root.after(40, self.jouer_partie)
        for i in self.modele.liste_sentinelles:
            i.deplacer_sentinelle()
            i.verifier_capture()
        self.vue.afficher_partie()

if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")