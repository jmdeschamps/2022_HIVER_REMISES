import Daleks_Vue
import Daleks_Objets


class Controleur():

    def __init__(self):
        self.modele = Daleks_Objets.Jeu()
        self.vue = Daleks_Vue.Vue()

        self.actions = {
            "P": self.demarrer_niveau,
            "S": self.voir_score,
            "O": self.choisir_option,
        }

        self.options = {
            "H": self.vue.affiche_menu_hauteur,
            "L": self.vue.affiche_menu_largeur,
        }

    def afficher_menu_initial(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse.upper() in 'POS':
            self.actions[reponse.upper()]()
        else:
            print("OUPS")
        return None


    def demarrer_niveau(self):
        self.modele.demarrer_niveau()
        while self.modele.niveaucourant.docteur.etat:
            direction = self.vue.afficher_niveau(self.modele.niveaucourant)
            self.modele.niveau_qui_roule(direction)

        return None

    def choisir_option(self):
        reponse = self.vue.affiche_menu_options()
        if reponse.upper() in 'LH':
            action = self.options[reponse.upper()]()
            if reponse.upper() == "L":
                self.modele.changer_option_largeur(action)
                self.afficher_menu_initial()
            elif reponse.upper() == "H":
                self.modele.changer_option_hauteur(action)
                self.afficher_menu_initial()
        else:
            print("OUPS")


    def voir_score(self):
        print("Score")
        return None


if __name__ == '__main__':
    c = Controleur()
    c.afficher_menu_initial()

    print("FIN DE PARTIE")
