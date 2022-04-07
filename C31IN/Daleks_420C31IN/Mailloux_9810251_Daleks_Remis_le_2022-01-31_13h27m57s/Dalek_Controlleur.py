import Dalek_Modele
import Dalek_Vue

class Controleur ():
    def __init__(self):
        self.modele = Dalek_Modele.Jeu(self)
        self.vue = Dalek_Vue.Vue(self)
        self.actions = {"p": self.demarrer_partie,
                        "o": self.choisir_option,
                        "s": self.afficher_scores,
                        "q": self.quitter_jeu}
        self.afficher_bienvenue()
        self.afficher_menu_initial()

    def afficher_bienvenue(self):
        self.vue.afficher_bienvenue()

    # def afficher_mort(self):
    #     self.vue.afficher_mort()
    #     self.afficher_menu_initial()

    def afficher_menu_initial(self):
        reponse = ""
        while not reponse:
            reponse = self.vue.afficher_menu_initial()
            if reponse not in self.actions.keys():
                print("RATÉ")
            else:
                self.actions[reponse]()

    def demarrer_partie(self):
        difficultes = ["d", "i", "e"]
        reponse = self.vue.afficher_options_difficulte()
        while reponse not in difficultes:
            print("Choix non valide")
            reponse = self.vue.afficher_options_difficulte()
        self.modele.demarrer_partie(reponse)
        self.modele.jouer(self)

    def choisir_option(self):
        reponses = self.vue.afficher_menu_options()
        largeur = reponses[0]
        hauteur = reponses[1]
        self.modele.changer_options(largeur, hauteur)
        self.afficher_menu_initial()

    def afficher_partie(self):
        self.vue.afficher_partie(self.modele.partie_courante)

    def afficher_scores(self):
        self.vue.afficher_scores(self.modele.high_score)
        self.afficher_menu_initial()

    def quitter_jeu(self):
        with open("./high_scores.txt", "w") as f:
            string_score = ""
            for i in self.modele.high_score:
                string_score += str(i)
                string_score += "\n"
            print(string_score)
            f.write(string_score)
        print("Au Revoir!")

if __name__ == '__main__':
    c = Controleur()
