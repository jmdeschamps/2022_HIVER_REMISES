# Le main est le fichier qui a été donné à l'excécutable.
# Un contrôleur contrôle le logiciel, le main sert à créer mon contrôleur.
# Pass indique un place holder
# Toutes les méthodes d'une classe ont comme paramètre self
# Python enhancement Proposals : pep #8 = standard conventionnel des pythonistas; Classa start by maj, variable by min.
# Objet devrait être noms
# méthdes devraient être des verbes
# aller voir pep sur les hint
# tuple parenthèse, liste immuables; on ne peut pas le changer, on peut le créer, le lire mais n'est pas modifiable
import random

import Daleks_Vue


class Jeu():
    def __init__(self):
        self.partiecourante = None
        self.largeur = 8
        self.hauteur = 6

    def demarrer_partie(self):
        self.partiecourante = Partie(self)

    def changer_option(self, largeur=8, hauteur=6):
        self.largeur = largeur


class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.nivo = 0
        self.daleks_par_nivo = 5
        self.daleks = []
        self.feraille = []
        self.points = 0

        self.docteur = Docteur(int(self.largeur / 2), int(self.hauteur / 2))

        self.creer_niveau()

    def creer_niveau(self):
        self.nivo += 1
        nb_daleks = self.nivo * self.daleks_par_nivo
        positions = [[self.docteur.y, self.docteur.x]]

        while nb_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)

            if [y, x] not in positions:
                positions.append([x, y])
                nb_daleks -= 1

        positions.pop(0)
        for i in positions:
            self.daleks.append(Dalek(i[0], i[1]))


class Docteur():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True


class Dalek():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Feraille():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Controleur():
    def __init__(self):
        self.modele = Jeu()
        self.vue = Daleks_Vue.Vue()
        self.actions = {"p": self.demarrer_partie,
                        "o": self.choisir_option,
                        "s": self.voir_score,
                        "e": self.effacer_score,
                        }
        self.afficher_menu_initial()

    def effacer_score(self):
        print("Effacer")

    def afficher_menu_initial(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse in self.actions.keys():
            self.actions[reponse]()

        else:
            print("RATÉ")

    def demarrer_partie(self):
        self.modele.demarrer_partie()
        self.vue.afficher_partie(self.modele.partiecourante)

    def voir_score(self):
        print("SCORE")

    def choisir_option(self):
        reponse = self.vue.afficher_menu_option()
        self.modele.changer_option(largeur=reponse)
        self.afficher_menu_initial()


# if =>on met le premier objet qu'on testait et on le met dans une liste de morts, à la fin il nous reste la liste
# des morts et on fait un for pour les retirer de la liste principale de daleks.

if __name__ == '__main__':
    c = Controleur()

    print("FIN DE DALEKS")
