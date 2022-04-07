import random

class Vue():
    def __init__(self):
        self.touche = {
            "1": [-1, 1],
            "2": [0, 1],
            "3": [1, 1],
            "4": [-1, 0],
            "5": [0, 0],
            "6": [1, 0],
            "7": [-1, -1],
            "8": [0, -1],
            "9": [1, -1],
            "z": [],
            "t": [],
            "r": [],
        }

    def afficher_menu_initial(self):
        print("Bienvenu aux DALEKS")
        print("Choix: p-> Partie, s -> Score, o -> Options")
        reponse = input("Votre reponse ici : ")
        return reponse

    def afficher_menu_option(self):
        print("Options des DALEKS")
        reponse = input("Nouvelle largeur : ")
        return int(reponse)

    def afficher_menu_jeu(self, partie):
        print("Déplacement")
        print("Haut -> 8, Bas -> 2  Gauche -> 4 Droite -> 6, Passif ->5")
        print("Haut-Gauche -> 7, Haut-Droit -> 9  Bas-Gauche -> 1 Bas-Droite -> 3")
        print("Power-Up")
        print("Zapper -> z, Teleporter -> t, Recommencer -> r")
        #print("Score:" + partie.score)
        reponse = input("Votre choix ici : ")


        if reponse in self.touche.keys():
            partie.mouvement_docteur(self.touche[reponse])
        self.afficher_partie(partie)


    def afficher_partie(self, partie):
        print("partie courante")
        map_visuelle = []
        for i in range(partie.hauteur):
            ligne = []
            for j in range(partie.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)
        map_visuelle[partie.docteur.y][partie.docteur.x] = "D"
        for i in partie.daleks:
            map_visuelle[i.y][i.x] = "W"
        for i in map_visuelle:
            print(i)
            #if i == D
                #compteur = 1
        self.afficher_menu_jeu(partie)

if __name__ == '__main__':
    print("slaut")