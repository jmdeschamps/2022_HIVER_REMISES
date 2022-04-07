import random


class Vue:
    def __init__(self):
        pass


def afficher_partie(jeu):
    print("Partie courante")
    map_visuelle = []  # liste [] fait partie de la classe liste
    for i in range(jeu.hauteur):
        ligne = []

        for j in range(jeu.largeur):
            ligne.append("-")
        map_visuelle.append(ligne)

    map_visuelle[jeu.doctor.y][jeu.doctor.x] = "D"

    for i in jeu.daleks:
        map_visuelle[i.y][i.x] = "X"

    for i in jeu.position_ferraile:
        map_visuelle[i[1]][i[0]] = "W"

    for i in map_visuelle:
        print(i)


def afficher_menu_initial():
    print("Welcome Dalek")
    print("Choix: p-> Game start, s-> Score, o-> Options")
    answer = input("Your answer here: ")
    return answer


def afficher_menu_options():
    print("Options de Dalek")

    answer = input("Nouvelle largeur : ")
    return int(answer)


def afficher_menu_options2():
    answer = input("Nouvelle hauteur : ")
    return int(answer)


def afficher_menu_mouvement():
    print("mouvement du docteur")

    reponse = input("écrire mouvement (GH,H,DH,G,C,D,GB,B,DB,TP) : ")

    dictonnaire_deplacement = {"D": [1, 0],
                               "H": [0, -1],
                               "G": [-1, 0],
                               "B": [0, 1],
                               "GH": [-1, -1],
                               "DH": [1, -1],
                               "GB": [-1, 1],
                               "DB": [1, 1],
                               "C": [0, 0],
                               }

    if reponse in dictonnaire_deplacement.keys():
        return dictonnaire_deplacement[reponse]
    else:
        print("mauvais mouvement, recommencez :")
    afficher_menu_mouvement()


def afficher_option_zapper(zap):
    print("Il vous reste " + str(zap) + " zapper")
    print("voulez-vous zapper ?")

    reponse = input("Y/N :")

    if reponse == "Y":
        return True
    else:
        return False


def afficher_option_tp():
    print("voulez-vous vous téléporter ?!")
    reponse = input("Y/N :")

    if reponse == "Y":
        return True
    else:
        return False


def fin_de_partie(parent):
    print("Fin de partie votre score est de : " + str(parent.score))



if __name__ == '__main__':
    print("I am vue")


def pas_de_zap():
    print("aucun zapper disponible!")
