class Vue():
    def __init__(self):
        pass

    def afficher_menu_initial(self):
        print("Bienvenue aux Daleks !")
        print("Choix : p -> pour commencer une partie, s -> pour afficher le score et o -> pour afficher les options")
        reponse = input("Votre reponse ici : ")
        return reponse

    def afficher_menu_option(self):
        print("Options des Daleks !")
        reponse = int(input("Nouvelle largeur  : "))
        return reponse

    def afficher_partie(self,partie):
        print("Partie Courante")
        map_visuelle = []
        for i in range(partie.hauteur):
            ligne = []
            for j in range(partie.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)
        map_visuelle[partie.docteur.y][partie.docteur.x] = "D"

        for i in partie.liste_daleks:
            map_visuelle[i.y][i.x] = "W"

        for i in partie.liste_ferraille:
            map_visuelle[i.y][i.x] = "X"

        for i in map_visuelle:
            print(i)

    def afficher_action_joueur(self):
        print("Utiliser le numpad pour choisir votre direction, t : pour la teleportation et z : pour utiliser le zappeur")
        print("utiliser le numpad")
        action_choisie = input("Action desiree ici : ")
        return action_choisie

if __name__ == '__main__':
    print("je suis la vue")