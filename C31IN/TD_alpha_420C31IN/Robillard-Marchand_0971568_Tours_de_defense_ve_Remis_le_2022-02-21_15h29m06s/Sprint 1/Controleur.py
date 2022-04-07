import Vue
import Modele

class Controleur:
    def __init__(self):
        self.modele = Modele.Modele(self)
        self.nouvelle_partie()
        self.vue = Vue.Vue(self)
        self.partie_en_cours = False
        self.paused = False
        self.vue.root.mainloop()

    def ouvrir_jeu(self):
        self.vue.creer_menu()

    def nouvelle_partie(self, choix_map=1):
        self.modele.nouvelle_partie(choix_map)

    def nouvelle_vague(self):
        self.modele.nouvelle_vague()

    def acheter_tour(self, type_tour, pos_x, pos_y):
        return self.modele.acheter_tour(type_tour, pos_x, pos_y)

    def lancer_vague(self):
        if not self.partie_en_cours:
            self.partie_en_cours = True
            self.paused = False
            self.jouer_tour()
        if not self.paused:
            self.nouvelle_vague()

    def pause(self):
        if not self.paused:
            self.paused = True
        elif self.paused:
            self.paused = False
            self.jouer_tour()


    def jouer_tour(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.vue.afficher_ressources()
            self.vue.update_dynamique()
            if not self.paused:
                self.vue.root.after(50, self.jouer_tour)


if __name__ == '__main__':
    c = Controleur()