import os

class Vue():
    def __init__(self, parent):
        self.parent = parent

    def afficher_bienvenue(self):
        print("Bienvenue aux DALEKS")

    def afficher_menu_initial(self):
        print("Choix: p-> Partie, s-> Score, o-> Option, q-> Quitter")
        reponse = input("Votre réponse ici : ")
        return reponse

    def afficher_options_difficulte(self):
        print("Choisissez un niveau de difficulté")
        print("Choix: d -> Débutant, i -> Intermédiaire, e -> Expert")
        reponse = input("Votre réponse ici : ")
        return reponse

    def afficher_menu_options(self):
        reponses = []
        print("Options de DALEKS")
        print("Nouvelle largeur: ")
        largeur = int(input("Votre réponse ici : "))
        reponses.append(largeur)
        print("Nouvelle hauteur: ")
        hauteur = int(input("Votre réponse ici : "))
        reponses.append(hauteur)
        return reponses

    def afficher_partie(self, partie):

        # Fonctionne seulement en console à l'extérieur de PyCharm
        os.system("cls")

        print(f"Partie courante | Score : {partie.score} "
              f"| Niveau : {partie.niveau} "
              f"| Zapper : {partie.docteur.nb_zapper}")
        carte_visuelle = []
        for i in range(partie.hauteur):
            ligne=[]
            for j in range(partie.largeur):
                ligne.append("-")
            carte_visuelle.append(ligne)
        carte_visuelle[partie.docteur.y][partie.docteur.x] = "W"
        for i in partie.daleks:
           carte_visuelle[i.y][i.x] = "D"
        for i in partie.ferrailles:
           carte_visuelle[i.y][i.x] = "F"
        for i in carte_visuelle:
            print(i)

    # def afficher_mort(self):
    #     print("Vous êtes mort, retour au menu principal")

    def afficher_actions_docteur(self):
        print("À vous de jouer")
        print("Utiliser le pavé numérique pour vous déplacer, z-> zapper, t->téléporter")
        action = input("Votre action ici : ")
        return action

    def afficher_scores(self, high_scores):
        high_scores.sort(reverse=True)
        print("HIGH SCORES")
        for i in high_scores:
            i = str(i)
            i = i.rjust(11, '.')
            print(i)

    def afficher_erreur(self):
        print("Choix invalide")
        self.afficher_partie()
