import Daleks_vue
import Modele


class Controleur():
    def __init__(self):
        self.modele = Modele.Jeu()
        self.vue = Daleks_vue.Vue()

        self.actions = {"p": self.demarrer_partie,
                        "o": self.choisir_option,
                        "s": self.voir_score,
                        }
        self.commandes = {
                "t": self.modele.teleporter_docteur,
                "z": self.modele.zapper,

        }
        while(1):
            self.afficher_menu_initial()
            self.jouer()

    def afficher_menu_initial(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse in self.actions.keys():
            self.actions[reponse]()
        else:
            self.afficher_menu_initial()

    def traiter_commande_docteur(self, reponse):
        if reponse in self.commandes.keys():
            return self.commandes[reponse]()
        else:
            return self.vue.gérer_déplacement(reponse)

    def voir_score(self):
        self.vue.afficher_scores(self.modele.highscore)
        self.afficher_menu_initial()

    def demarrer_partie(self):
        self.modele.demarrer_partie()
        self.modele.game_over = False

    def jouer(self):
        while not self.modele.game_over:
            self.vue.afficher_partie(self.modele.partie_courante)
            self.vue.afficher_menu_jeu(self.modele.partie_courante)
            reponse = input("direction choisie:")
            deplacement = self.traiter_commande_docteur(reponse)

            if deplacement and self.modele.deplacer_docteur(deplacement) == True:
                    self.modele.deplacer_daleks()
                    self.modele.valider_si_doctor_mort()
                    if (not self.modele.game_over):
                        self.modele.est_collision()
                        self.modele.a_frapper_feraille()
                        self.modele.est_meilleur_score()
            else:
                self.vue.afficher_touche_invalide()
            if(len(self.modele.partie_courante.daleks) == 0):
                self.vue.afficher_level_up()
                self.modele.partie_courante.creer_niveau()
        if(self.modele.game_over):
            self.vue.afficher_partie(self.modele.partie_courante)
            self.vue.afficher_menu_gameover(self.modele.partie_courante.scoregame)

    def choisir_option(self):
        reponses = self.vue.afficher_menu_option()
        largeur = reponses.get("largeur")
        hauteur = reponses.get("hauteur")
        nbDalek = reponses.get("nbDalek")
        niveau_difficulter = reponses.get("niveau_difficulter")

        self.modele.changer_option(largeur,hauteur,nbDalek,niveau_difficulter)
        self.afficher_menu_initial()


if __name__ == '__main__':
    c = Controleur()
    print("FIN DALEKS")