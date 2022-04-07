
class Vue():
    def __init__(self):
        pass

    def afficher_menu_initial(self):
        print("Bienvenu aux DALEKS")
        print("Choix : P-> Partie , S-> Score, O-> Options")
        reponse = input("Votre reponse ici : ")

        return reponse

    def afficher_niveau(self,niveau):
        print("Partie courante")
        map_visuelle = []
        for i in range(niveau.hauteur):
            ligne = []
            for j in range(niveau.largeur):
                ligne.append("-")
            map_visuelle.append(ligne)
        map_visuelle[niveau.docteur.y][niveau.docteur.x] = "D"
        for i in niveau.dalek_list:
            map_visuelle[i.y][i.x] = "W"
        for j in niveau.ferailles_list:
            map_visuelle[j.y][j.x] = "#"
        for i in map_visuelle:
            print(i)

        direction = self.afficher_menu_directions()
        return direction

    def afficher_menu_directions(self):
        print("Utilisez les touches de déplacement: ")
        print("Q  W   E")
        print("A  S   D")
        print("Z  X   C")
        print("K : Zap")
        print("L : Teleport")
        deplacement = input("Votre action : ")
        return deplacement.lower()

    def affiche_menu_options(self):
        print("Options des DALEKS")
        reponse = input("Largeur = L ou Hauteur = H : ")
        return reponse.upper()

    def affiche_menu_largeur(self):
        print("Options des DALEKS")
        reponse = input("Nouvelle largeur : ")
        return int(reponse)

    def affiche_menu_hauteur(self):
        print("Options des DALEKS")
        reponse = input("Nouvelle hauteur : ")
        return int(reponse)