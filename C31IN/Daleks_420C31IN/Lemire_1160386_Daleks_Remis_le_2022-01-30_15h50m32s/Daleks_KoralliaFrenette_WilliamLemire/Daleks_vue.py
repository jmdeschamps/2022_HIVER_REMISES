import os

class Vue():
    def __init__(self):
        pass

    def afficher_menu_option(self):
        print("Options des Daleks")
        reponses = {"hauteur": int(input("Nouvelle hauteur: ")),
                    "largeur": int(input("Nouvelle largeur: ")),
                    "nbDalek": int(input("Nombre de daleks: "))}

        return reponses

    def afficher_menu_initial(self):
        print("Bienvenue aux Daleks")
        print("p: Partie, s: Score, o: Options")
        reponse = input("Votre réponse ici: ")
        return reponse

    def afficher_partie(self, partie):
        os.system('cls')
        print("Partie courante, niveau #", partie.niveau)

        map_visuelle = []
        for i in range(partie.hauteur):
            ligne = []
            for j in range(partie.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)
        for i in partie.daleks:
            map_visuelle[i.y][i.x] = "w"
        for i in partie.ferailles:
            map_visuelle[i.y][i.x] ="F"
        if map_visuelle[partie.docteur.y][partie.docteur.x] == "w":
            map_visuelle[partie.docteur.y][partie.docteur.x] = "X"
        else:
            map_visuelle[partie.docteur.y][partie.docteur.x] = "☻"

        for i in map_visuelle:
            print(i)

    def afficher_menu_jeu(self, partie):
        print("__________MENU JEU_________")
        print("   |  PESEZ UNE TOUCHE  |  ")
        print("             ▲             ")
        print("  7    ┌     8     ┐    9  ")
        print("◄ 4    |     ■     |    6 ►")
        print("  1    └     2     ┘    3  ")
        print("             ▼             ")
        print("t: TÉLÉPORTEUR   z: ZAPPEUR")
        print("NOMBRE DE ZAPPEURS: " + str(partie.nb_zappeur))


    def afficher_scores(self,score):
        print("__________MENU JEU_________")
        print("*                          .")
        print("               .          .                        .       |       .")
        print("                                                         --*--")
        print("                              _________                    |")
        print("         .               _|_ /_   _")
        print("         _______       _  |  |_| |      .")
        print("              | \  _  |_")
        print("              |_/ |_|      .                                  .")
        print("          _____  ____  _________    _____ _____________")
        print("          \    \/    \/         \__/     V     ____    | ")
        print("           \      _      /|      __      |    |____|   |         .")
        print("   .        \____/ \___/  |_____|  |_____|_____________|")
        print("                                                         ")
        print("             .                          .")
        print("                                     Exterminate!")
        print("                                    /")
        print("                                ___")
        print("                        D>=G==='   '.")
        print("                              |======|")
        print("                              |======|")
        print("                          )--/]IIIIII]")
        print("                              |_______|")
        print("                              C O O O D")
        print("                             C O  O  O D")
        print("                            C  O  O  O  D")
        print("                            C__O__O__O__D")
        print("                           [_____________]")
        print("                                                                  ")
        print("                           MEILLEUR SCORE:" +str(score))


    def afficher_level_up(self):
        print(" ██        █████████ ██     ██ █████████ ██        ")
        print(" ██        ██        ██     ██ ██        ██        ")
        print(" ██        ██        ██     ██ ██        ██        ")
        print(" ██        ███████   ██     ██ ███████   ██        ")
        print(" ██        ██         ██   ██  ██        ██        ")
        print(" ██        ██          ██ ██   ██        ██        ")
        print(" █████████ █████████    ███    █████████ █████████ ")
        print("                                                   ")
        print("                  ██     ██ ████████               ")
        print("                  ██     ██ ██     ██              ")
        print("                  ██     ██ ██     ██              ")
        print("                  ██     ██ ███████                ")
        print("                  ██     ██ ██                     ")
        print("                  ██     ██ ██                     ")
        print("                   ███████  ██                     ")
        print("                                                   ")

    def afficher_touche_invalide(self):
        print("                                                                        ")
        print("█████████  ███████  ██     ██  ███████  ██     ██ █████████             ")
        print("    ██    ██     ██ ██     ██ ██     ██ ██     ██ ██                    ")
        print("    ██    ██     ██ ██     ██ ██        ██     ██ ██                    ")
        print("    ██    ██     ██ ██     ██ ██        █████████ ███████               ")
        print("    ██    ██     ██ ██     ██ ██        ██     ██ ██                    ")
        print("    ██    ██     ██ ██     ██ ██     ██ ██     ██ ██                    ")
        print("    ██     ███████   ███████   ███████  ██     ██ █████████             ")
        print("                                                                        ")
        print(" ████ ██     ██ ██     ██    ███    ██        ████ ████████  █████████  ") 
        print("  ██  ███    ██ ██     ██   ██ ██   ██         ██  ██     ██ ██         ")
        print("  ██  ████   ██ ██     ██  ██   ██  ██         ██  ██     ██ ██         ")
        print("  ██  ██ ██  ██ ██     ██ ██     ██ ██         ██  ██     ██ ███████    ")
        print("  ██  ██   ████  ██   ██  █████████ ██         ██  ██     ██ ██         ")
        print("  ██  ██    ███   ██ ██   ██     ██ ██         ██  ██     ██ ██         ")
        print(" ████ ██     ██    ███    ██     ██ █████████ ████ ████████  █████████  ")
        print("                                                                        ")

    def afficher_menu_gameover(self,score):
        print("  ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  ")
        print(" ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒")
        print("▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒")
        print("░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ")
        print("░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒")
        print(" ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░")
        print("  ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░")
        print("░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ ")
        print("      ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     ")
        print("                                     Exterminate!")
        print("                                    /")
        print("                                ___")
        print("                        D>=G==='   '.")
        print("                              |======|")
        print("                              |======|")
        print("                          )--/]IIIIII]")
        print("                              |_______|")
        print("                              C O O O D")
        print("                             C O  O  O D")
        print("                            C  O  O  O  D")
        print("                            C__O__O__O__D")
        print("                           [_____________]")
        print("                           score "+ str(score)                                      )
       


    def gérer_déplacement(self, direction):
        deplacement = {
            "7": [-1, -1],
            "8": [0, -1],
            "9": [1, -1],
            "4": [-1, 0],
            "6": [1, 0],
            "1": [-1, 1],
            "2": [0, 1],
            "3": [1, 1]
        }
        if direction in deplacement.keys():
            return deplacement[direction]
        else:
            return False


if __name__ == '__main__':
    print("Je suis la vue")