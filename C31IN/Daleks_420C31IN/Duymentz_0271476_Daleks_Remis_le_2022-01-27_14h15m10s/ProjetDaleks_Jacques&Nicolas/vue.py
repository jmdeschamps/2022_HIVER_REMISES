import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class Vue:

    def __init__(self):
        pass

    def afficher_menu_initial(self):
        cls()
        print("Bienvenue aux DALEKS")
        print("Choix: p -> Partie, s -> Scores, o -> Options, x -> Quitter")
        reponse = input("Votre réponse ici : ")
        return reponse

    def afficher_menu_scores(self):
        cls()
        print("SCORES")
        print("Voulez-vous trier les scores en ordre croissant ? (o/n)")
        return input("Votre choix : ")

    def afficher_scores(self, liste_scores):
        for i in liste_scores:
            colonnes = i.split(",")
            print("Nom : " + colonnes[0] + "\n      Score : " + colonnes[1] + " crédits cosmiques")
        print("\nVoulez-vous retourner au menu principal ? (o/n)")
        return input("Votre choix : ")

    def afficher_menu_options(self):
        cls()
        print("OPTIONS")
        liste_options = []
        print("Choisir la largeur de la grille (8 et plus)")
        liste_options.append(input("Largeur désirée : "))
        print("Choisir la hauteur de la grille (6 et plus)")
        liste_options.append(input("Hauteur désirée : "))
        print("Choisir la difficulté de téléportation")
        print("1 -> facile, 2 -> ordinaire, 3 -> difficile")
        liste_options.append(input("Difficulté désirée : "))
        return liste_options

    def afficher_partie(self, partie):
        cls()
        print("Partie courante")
        map_visuelle = []
        for i in range(partie.hauteur):
            ligne = []
            for j in range(partie.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)
        map_visuelle[partie.docteur.y][partie.docteur.x] = "D"
        for i in partie.daleks:
            if not i.est_mort:
                map_visuelle[i.y][i.x] = "X"
        for i in partie.ferrailles:
            map_visuelle[i.y][i.x] = "0"
        for i in map_visuelle:
            print(i)

    def afficher_menu_jeu(self, nbr_zappeurs):
        print("C'est à votre tour !\n")
        print("Vous avez " + str(nbr_zappeurs) + " zappeur(s)")
        print("Veuillez choisir parmi les options suivantes : ")
        print("\tq w e")
        print("\ta   d\t==> pour se déplacer vers la direction sélectionnée")
        print("\tz x c")
        print("\ts ==> pour passer son tour")
        print("\tt ==> pour se téléporter")
        print("\ty ==> pour utiliser le zappeur")
        reponse = input("Votre choix : ")
        return reponse

    def afficher_menu_fin_partie(self):
        print("GAME OVER")
        print("Voulez-vous sauvegarder votre score ? (o/n)")
        choix = input("Votre choix : ")
        if choix == 'o':
            return input("Votre nom : ")
        else:
            return None

    def afficher_message_erreur(self, no_erreur):
        if no_erreur == 1:
            print("Erreur. Mauvaise touche.")
        elif no_erreur == 2:
            print("Erreur. Une ou plusieurs options mal sélectionnées. Veuillez recommencer.")
        elif no_erreur == 3:
            print("Erreur. Case occupée ou en dehors de la grille.")
        elif no_erreur == 4:
            print("Erreur. Vous n'avez plus de zappeur.")
        elif no_erreur == 5:
            print("")
        elif no_erreur == 6:
            print("")

    def afficher_message_aurevoir(self):
        print("Au revoir !")