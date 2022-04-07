import Vue
import Modele

class Controleur:
    def __init__(self):
        self.modele = Modele.Modele(self)
        self.vue = Vue.Vue(self)
        self.ouvrir_jeu()
        self.partie_en_cours = False
        self.paused = False
        self.vue.root.mainloop()

    def acheter_tour(self, type_tour, pos_x, pos_y):
        return self.modele.acheter_tour(type_tour, pos_x, pos_y)

    def jouer_tour(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.vue.afficher_ressources()
            self.vue.update_dynamique()
            if not self.paused:
                self.vue.root.after(50, self.jouer_tour)

    def lancer_vague(self):
        if not self.partie_en_cours:
            self.partie_en_cours = True
            self.paused = False
            self.jouer_tour()
        if not self.paused:
            self.nouvelle_vague()

    def nouvelle_partie(self, choix):
        if self.vue.niveau.get():
            self.modele.changer_difficultes(self.vue.niveau.get())
        self.modele.nouvelle_partie(choix)

    def nouvelle_vague(self):
        self.modele.nouvelle_vague()

    def ouvrir_jeu(self):
        self.vue.accueil()

    def pause(self):
        if not self.paused:
            self.paused = True
        elif self.paused:
            self.paused = False
            self.jouer_tour()

    def upgrade_tour(self, id_tour, upgrade):
        self.modele.upgrade_tour(id_tour, upgrade)

    def vendre_tour(self, id_tour):
        self.modele.vendre_tour(id_tour)

    def terminer_partie(self, succes, score, inscrire):
        self.vue.fin_partie(succes, score, inscrire)

    def inscrire_nouv_score(self, nom):
        self.modele.partie.inscire_nouv_score(nom, self.modele.partie.score_final)



if __name__ == '__main__':
    c = Controleur()