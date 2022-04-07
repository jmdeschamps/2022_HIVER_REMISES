import Square_Modele
import Square_Vue
import time

class SquareController:
    def __init__(self):
        self.partie_en_cours = False
        self.premiere_partie=True
        self.modele = Square_Modele.Jeu(self)
        self.vue = Square_Vue.Jeu_Vue(self)
        self.vue.root.mainloop()

    def nouvelle_partie(self):
        self.modele.nouvelle_partie()
        self.vue.nouvelle_partie()
        self.premiere_partie = False

    def debuter_partie(self):
        self.modele.partie.debut = time.time()
        self.partie_en_cours = True
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.partie.jouer_tour()
            self.modele.partie.bouger_sentinelles()
            self.vue.afficher_partie()
            self.vue.root.after(40, self.jouer_partie)

    def recibler_joueur(self, x, y):
        self.modele.partie.recibler_joueur(x, y)

    def fin_partie(self):
        self.partie_en_cours = False
        self.vue.fin_partie()

if __name__ == '__main__':
    controller = SquareController()
    print("Fini")