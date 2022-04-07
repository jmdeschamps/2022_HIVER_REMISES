import random
import daleks_vue

class Jeu():
    def __init__(self):
        self.largeur = 5 #pour les options. on va transferer cette donnée à Partie() par la suite
        self.hauteur = 6
        self.partie_courante = None

    def demarrer_partie(self):
        self.partie_courante = Partie(self)

    def fin_partie(self):
        self.partie_courante = None


    def changer_option(self, largeur=8, hauteur = 6):
        self.largeur=largeur

class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.niveau = 0
        self.nombre_daleks_par_niveau = 5
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.docteur = Docteur(int(self.largeur/2), int(self.hauteur/2))
        self.liste_daleks = []
        self.creer_niveau()
        self.liste_ferraille = []
        self.liste_daleks_morts= []

    def creer_niveau(self):
        self.niveau += 1
        nb_daleks = self.niveau * self.nombre_daleks_par_niveau
        position = [[self.docteur.x , self.docteur.y]]
        while nb_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x, y] not in position:
                position.append([x, y])
                nb_daleks -= 1

        position.pop(0)
        for i in position:
            self.liste_daleks.append(Daleks(i[0], i[1]))

    def fin_niveau(self):
        for i in self.liste_daleks:
            if i.x == self.docteur.x and i.y == self.docteur.y:
                print("Le bon Docteur ne peut etre extermine, voulez-vous reesayer ? Appuyer sur 'c' ")
        if self.liste_daleks_morts == self.niveau * self.nombre_daleks_par_niveau :
            print("Niveau reussi, appuyer sur 'c' pour le prochain continuer")
            self.niveau +1

    def collision(self):
        inexistent = 0
        for i in self.liste_daleks:
            for j in self.liste_daleks:
                if i != j:
                    if i.x == j.x and i.y == j.y:
                        if i not in self.liste_daleks_morts:
                            self.liste_daleks_morts.append(i)
                            self.liste_daleks_morts.append(j)

        for i in self.liste_daleks_morts:
            if i in self.liste_daleks:
                self.liste_daleks.remove(i)
                inexistent = 1

            for j in self.liste_ferraille:
                if i.x == j.x and i.y == j.y:
                    inexistent = 0
            if inexistent:
                self.liste_ferraille.append(Ferraille(i.x, i.y))

    def mouvement_daleks(self):
        for i in range(len(self.liste_daleks)):
            self.distance_x = abs(self.liste_daleks[i].x - self.docteur.x)
            self.distance_y = abs(self.liste_daleks[i].y - self.docteur.y)
            if self.distance_x > self.distance_y:
                if self.liste_daleks[i].x > self.docteur.x:
                    self.liste_daleks[i].x -= 1
                else:
                    self.liste_daleks[i].x += 1
            elif self.distance_x < self.distance_y:
                if self.liste_daleks[i].y > self.docteur.y:
                    self.liste_daleks[i].y -= 1
                else:
                    self.liste_daleks[i].y += 1
            else :
               if self.liste_daleks[i].x > self.docteur.x:
                   if self.liste_daleks[i].y > self.docteur.y:
                       self.liste_daleks[i].x -= 1
                       self.liste_daleks[i].y -= 1
                   else:
                       self.liste_daleks[i].x -= 1
                       self.liste_daleks[i].y += 1
               else:
                   if self.liste_daleks[i].y > self.docteur.y:
                       self.liste_daleks[i].x += 1
                       self.liste_daleks[i].y -= 1
                   else:
                       self.liste_daleks[i].x += 1
                       self.liste_daleks[i].y += 1

    def zapper(self):
        for i in self.liste_daleks:

            if i.x == self.docteur.x:
                if i.y == self.docteur.y + 1:
                    self.liste_daleks_morts.append(i)
                if i.y == self.docteur.y - 1:
                    self.liste_daleks_morts.append(i)

            if i.x == self.docteur.x - 1:
                if i.y == self.docteur.y:
                    self.liste_daleks_morts.append(i)
                if i.y == self.docteur.y + 1:
                    self.liste_daleks_morts.append(i)
                if i.y == self.docteur.y - 1:
                    self.liste_daleks_morts.append(i)

            if i.x == self.docteur.x + 1:
                if i.y == self.docteur.y:
                    self.liste_daleks_morts.append(i)
                if i.y == self.docteur.y + 1:
                    self.liste_daleks_morts.append(i)
                if i.y == self.docteur.y - 1:
                    self.liste_daleks_morts.append(i)

        for i in self.liste_daleks_morts:
            if i in self.liste_daleks:
                self.liste_daleks.remove(i)

    def teleportation(self):
        x = random.randrange(0,self.largeur)
        y = random.randrange(0, self.hauteur)
        position_libre = 1
        for i in self.liste_daleks:
            if i.x == x and i.y == y:
                position_libre = 0

        while position_libre == 0:
            x = random.randrange(0, self.largeur)
            y = random.randrange(0, self.hauteur)
            position_libre = 1
            for i in self.liste_daleks:
                if i.x == x and i.y == y:
                    position_libre = 0

        self.docteur.x = x
        self.docteur.y = y


class Docteur():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Daleks():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ferraille():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Controleur():
    def __init__(self):
        self.modele = Jeu()
        self.vue = daleks_vue.Vue()
        self.action = {"p" : self.demarrer_partie,
                       "o" : self.choisir_option,
                       "s" : self.voir_score,
                       }

        self.directions = {"8": self.direction_haut,
                           "2": self.direction_bas,
                           "4": self.direction_gauche,
                           "6": self.direction_droite,
                           "7": self.direction_gauche_haut,
                           "9": self.direction_droite_haute,
                           "1": self.direction_gauche_bas,
                           "3": self.direction_droite_bas,
                           "5": self.direction_sur_place
                           }
        self.afficher_menu_inital()

    def afficher_menu_inital(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse in self.action.keys():
            self.action[reponse]()


    def demarrer_partie(self):
        self.modele.demarrer_partie()
        self.vue.afficher_partie(self.modele.partie_courante)

    def fin_partie(self):
        self.modele.fin_partie()
        self.vue.afficher_partie(self.modele.partie_courante)

    def choisir_option(self):
        reponse = self.vue.afficher_menu_option()
        self.modele.changer_option(largeur=reponse)
        self.afficher_menu_inital()


        print("OPTION")

    def voir_score(self):
        print("SCORE")

    def entrer_direction(self):
        action_choisie = self.vue.afficher_action_joueur()

        if action_choisie == "z":
            self.modele.partie_courante.zapper()

        self.modele.partie_courante.mouvement_daleks()
        self.modele.partie_courante.collision()

        if action_choisie == "t":
            self.modele.partie_courante.teleportation()

        if action_choisie != "z" and action_choisie != "t":
            if action_choisie in '824679135':
                self.directions[action_choisie]()
            else:
                print("choix invalide")

        self.vue.afficher_partie(self.modele.partie_courante)

    def direction_haut(self):
        if (self.modele.partie_courante.docteur.y <= 0):
            self.modele.partie_courante.docteur.y = 0
            print("Le docteur ne prend jamais la fuite!")
        else:
            self.modele.partie_courante.docteur.y -= 1

    def direction_bas(self):
        if (self.modele.partie_courante.docteur.y >= self.modele.hauteur ):
            self.modele.partie_courante.docteur.y = self.modele.hauteur
            print("Le docteur ne prend jamais la fuite!")
        else:
            self.modele.partie_courante.docteur.y+=1

    def direction_gauche(self):
        if (self.modele.partie_courante.docteur.y <=0):
            self.modele.partie_courante.docteur.y = 0
            print("Le docteur ne prend jamais la fuite!")
        else:
            self.modele.partie_courante.docteur.x -= 1

    def direction_droite(self):
        self.modele.partie_courante.docteur.x += 1
        self.vue.afficher_partie(self.modele.partie_courante)

    def direction_gauche_haut(self):
        self.modele.partie_courante.docteur.x -= 1
        self.modele.partie_courante.docteur.y -= 1

    def direction_droite_haute(self):
        self.modele.partie_courante.docteur.x += 1
        self.modele.partie_courante.docteur.y -= 1

    def direction_gauche_bas(self):
        self.modele.partie_courante.docteur.x -= 1
        self.modele.partie_courante.docteur.y += 1

    def direction_droite_bas(self):
        self.modele.partie_courante.docteur.x += 1
        self.modele.partie_courante.docteur.y += 1

    def direction_sur_place(self):
        pass


if __name__ == '__main__':
    c = Controleur()

    while(True):
        c.entrer_direction()


