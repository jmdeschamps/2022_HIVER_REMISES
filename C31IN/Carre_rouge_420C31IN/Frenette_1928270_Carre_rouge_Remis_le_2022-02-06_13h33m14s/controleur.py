import vue
import Modele
import time


class Controleur():
    def __init__(self):
        self.partie_en_cours=0
        self.modele =Modele.Modele(self)
        self.vue = vue.Vue(self)
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.partie_en_cours.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.partie_en_cours.debut = time.time()
        self.partie_en_cours =1
        self.modele.pion.isCollision =False
        self.jouer_partie()

    def reset_partie(self):
        self.modele.reset_partie()


    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.partie_en_cours.jouer_tour()
            for i in self.modele.sentinelles:
                i.move()

        self.vue.afficher_partie()

        if (self.modele.pion.isCollision):
            self.reset_partie()

        if self.partie_en_cours:
            self.vue.root.after(40, self.jouer_partie)









if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
