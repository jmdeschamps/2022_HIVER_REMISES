import os


class Vue:
    def __init__(self):
        pass

    def afficher_menu_initial(self):
        os.system('cls')
        print("   __                   _                ___      _      _        ")
        print("   \ \  ___ _   _    __| | ___  ___     /   \__ _| | ___| | _____ ")
        print("    \ \/ _ \ | | |  / _` |/ _ \/ __|   / /\ / _` | |/ _ \ |/ / __|")
        print(" /\_/ /  __/ |_| | | (_| |  __/\__ \  / /_// (_| | |  __/   <\__ \\")
        print(" \___/ \___|\__,_|  \__,_|\___||___/ /___,' \__,_|_|\___|_|\_\___/")
        print("******************************************************************")
        print("\t\tDéric Marchand & Karl Robillard-Marchand")
        print()
        print()
        print()
        print("\tp-> Partie  s-> Score  o-> Options  m-> Manuel  q-> Quitter")
        print()
        reponse = input("\t\t\tCHOISISSEZ: ")
        return reponse

    def afficher_partie(self, partie):
        print(f"Niveau: {partie.niveau}     Score: {partie.score}     Zappers: {partie.docteur.nbr_zapper}")
        map_visuelle = []
        for i in range(partie.hauteur):
            ligne = []
            for j in range(partie.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)

        map_visuelle[partie.docteur.y][partie.docteur.x] = "D"

        for i in partie.daleks: # liste d'objets Dalek dans la partie courante
            map_visuelle[i.y][i.x] = "W"

        for i in partie.tas_de_ferraille: # liste d'objets Tas de ferraille dans la partie courante
            map_visuelle[i.y][i.x] = "X"

        # On imprime à la console tous les éléments de la liste
        for i in map_visuelle:
            print(i)

    def afficher_menu_jeu(self, msg_erreur = None):
        if msg_erreur is not None:
            print(f"ATTENTION: {msg_erreur}")
        print("À vous d'agir.")
        print("w-> HAUT  a-> GAUCHE  q-> HAUT-GAUCHE e-> HAUT-DROITE")
        print("s-> BAS  d-> DROITE  z-> BAS-GAUCHE  c-> BAS-DROITE")
        print("Espace-> ATTENDRE  |  t-> TÉLÉPORTER  |  p-> ZAPPER")
        reponse = input("Action: ")
        return reponse

    def afficher_menu_option(self):
        os.system('cls')
        print("OPTIONS")
        print("-------")
        reponse = []
        reponse.append(int(input("Largeur initiale du monde: ")))
        reponse.append(int(input("Hauteur initiale du monde: ")))
        print("0-> FACILE  1-> MOYEN  2-> DIFFICILE")
        reponse.append(int(input("Difficulté: ")))
        return reponse

    def afficher_score(self, liste_scores):
        retour_principal = False
        while not retour_principal:
            os.system('cls')
            print("TABLEAU DES SCORES")
            print("------------------")
            for score in liste_scores:
                print(f"{score[0]:<20}{score[1]}")
            print()
            touche = input("'b' pour retourner au menu principal: ")
            if touche == 'b':
                retour_principal = True

    def nouveau_score(self, score):
        os.system('cls')
        print(f"Vous avez récolté {score} crédits cosmiques!")
        nom = input("Veuillez saisir votre nom: ")
        return nom

    def afficher_manuel(self):
        retour_principal = False
        while not retour_principal:
            os.system('cls')
            with open('LISEZMOI.txt', 'r') as f:
                for line in f:
                   print(line, end='')
            print()
            touche = input("'b' pour retourner au menu principal: ")
            if touche == 'b':
                retour_principal = True
