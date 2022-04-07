import random

def zappeur(partie):

    position_Zappeur = [partie.docteur.y+1, partie.docteur.x+1][partie.docteur.y -1, partie.docteur.x-1],
    [partie.docteur.y+1, partie.docteur.x-1][partie.docteur.y-1, partie.docteur.x+1]
    [partie.docteur.y, partie.docteur.x] [partie.docteur.y, partie.docteur.x] [partie.docteur.y, partie.docteur.x] [partie.docteur.y, partie.docteur.x]

    for i in partie.daleks:
        if i in position_Zappeur:
            partie.daleks.remove(i)
            partie.points +=1


    return partie



def deplacement_dalek(partie):
    memoire = []
    dalek_detruire = []

    for i in partie.daleks:
        if i.x > partie.docteur.x:
            i.x -= 1
        elif i.x == partie.docteur.x:
            i.x = partie.docteur.x
        else:
            i.x += 1
        if i.y > partie.docteur.y:
            i.y -= 1
        elif i.y == partie.docteur.y:
            i.y = partie.docteur.y
        else:
            i.y += 1

        if i.x < 0:
            i.x = 0
        if i.y < 0:
            i.y = 0
        if i.x > partie.largeur - 1:
            i.x = partie.largeur - 1
        if i.y > partie.hauteur - 1:
            i.y = partie.hauteur - 1

        if [i.x, i.y] in memoire or [i.x, i.y] in partie.feraille:
            dalek_detruire.append(i)
            print("collision")

        memoire.append([i.x, i.y])



    print(partie.feraille)

    for i in dalek_detruire:
        if i in partie.daleks:
            partie.feraille.append(i)
            partie.daleks = list(filter(i.__ne__, partie.daleks))



    return memoire


def deplacement_docteur(partie, reponse):
    if reponse == "w":
        partie.docteur.y -= 1
    elif reponse == "s":
        partie.docteur.y += 1
    elif reponse == "a":
        partie.docteur.x -= 1
    elif reponse == "d":
        partie.docteur.x += 1

    elif reponse == "q":
        partie.docteur.y -= 1
        partie.docteur.x -= 1
    elif reponse == "e":
        partie.docteur.y -= 1
        partie.docteur.x += 1
    elif reponse == "x":
        partie.docteur.y += 1
        partie.docteur.x += 1
    elif reponse == "z":
        partie.docteur.y += 1
        partie.docteur.x -= 1
    elif reponse == "m":
        partie = zappeur(partie)

    elif reponse == "t":
        partie.docteur.x = random.randrange(partie.largeur - 1)
        partie.docteur.y = random.randrange(partie.hauteur - 1)

    if partie.docteur.x < 0:
        partie.docteur.x = 0
    if partie.docteur.y < 0:
        partie.docteur.y = 0
    if partie.docteur.x > partie.largeur - 1:
        partie.docteur.x = partie.largeur - 1
    if partie.docteur.y > partie.hauteur - 1:
        partie.docteur.y = partie.hauteur - 1

    return partie


def afficher_menu_action(partie):
    print("Choisissez une action : ")
    print("Choix a-> Aller vers la gauche, d-> Aller vers la droite, w-> Aller vers le haut, s-> Aller vers "
          "le bas")
    print("q : (0,1)-> Diagonale haut gauche, e-> diagonale haut droit, z-> diagonale bas gauche, x-> diagonale"
          " bas gauche")
    print("m-> Zapper, n-> Teleporter")
    reponse = (input("Votre choix :"))
    deplacement_dalek(partie)
    partie_a_jour = deplacement_docteur(partie, reponse)
    return partie_a_jour

    #     dictionnaire_choix = {
    #         "w": self.deplacement_docteur,
    #         "s": self.deplacement_docteur,
    #         "a": self.deplacement_docteur,
    #         "d": self.deplacement_docteur, }
    #
    #     if reponse in dictionnaire_choix.keys():
    #         return dictionnaire_choix[reponse](partie, reponse)


class Vue():
    def __init__(self):
        pass

    def afficher_menu_initial(self):
        print("BIENVENU AUX DALEKS")
        print("Choix p-> Partie, s-> Score, o-> Options")
        reponse = input("Votre reponse ici: ")
        return reponse

    def afficher_menu_option(self):
        print("Options de DALEKS")
        reponse = int(input("Nouvelle largeur: "))
        return reponse

    def afficher_partie(self, partie):

        print("Partie courante")
        map_visuelle = []
        for i in range(partie.hauteur):  # i dans 8
            ligne = []
            for j in range(partie.largeur):  # j dans
                ligne.append("-")
            map_visuelle.append(ligne)
        map_visuelle[partie.docteur.y][partie.docteur.x] = "D"

        for i in partie.daleks:
            map_visuelle[i.y][i.x] = "W"

        for i in partie.feraille:
            map_visuelle[i.y][i.x] = "X"

        # Coordonnées de tous les joueurs

        z = 0
        print("Docteur :", partie.docteur.x, ",", partie.docteur.y)
        for i in partie.daleks:
            print("Dalek ", z, " = (", i.x, ",", i.y, ")")
            z += 1
            if partie.docteur.x == i.x and partie.docteur.y == i.y:
                partie.docteur.alive = False
                print("Le Docteur n'a pas pu vaincre les Daleks! Exterminate!")

        while partie.docteur.alive:
            for i in map_visuelle:
                print(i)
            self.afficher_partie(afficher_menu_action(partie))


if __name__ == '__main__':
    print("JE SUIS LA VUEEEEEEE")
