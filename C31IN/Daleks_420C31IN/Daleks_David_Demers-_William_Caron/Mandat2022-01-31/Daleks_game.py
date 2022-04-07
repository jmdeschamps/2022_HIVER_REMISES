import Vue
import random


class Doctor:
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y
        self.etat = True

    def deplacement(self, deplacement):
        self.x += deplacement[0]
        self.y += deplacement[1]


class Dalek:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Jeu:
    def __init__(self):
        self.largeur = 8
        self.hauteur = 6
        self.partie_courante = None

    def demarrer_partie(self):
        self.partie_courante = Partie(self)

    def change_options(self, largeur=8, hauteur=6):
        self.largeur = largeur
        self.hauteur = hauteur


class Partie:
    def __init__(self, parent):
        self.daleks = []
        self.position_ferraile = []
        self.nombre_dalek_par_niveau = 5
        self.parent = parent
        self.niveau = 0
        self.hauteur = self.parent.hauteur
        self.largeur = self.parent.largeur
        self.doctor = Doctor(int(self.largeur / 2), int(self.hauteur / 2))
        self.creer_niveau()
        self.compteur_zap = self.niveau
        self.score = 0

    def creer_niveau(self):
        self.niveau += 1
        self.position_ferraile.clear()
        nb_daleks = self.niveau * self.nombre_dalek_par_niveau
        position = [[self.doctor.x, self.doctor.y]]
        while nb_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x, y] not in position:
                position.append([x, y])
                nb_daleks -= 1

        position.pop(0)
        for i in position:
            self.daleks.append(Dalek(i[0], i[1]))

    def deplacement_dalek(self):

        for i in self.daleks:
            if i.x < self.doctor.x:
                i.x += 1

            if i.x > self.doctor.x:
                i.x -= 1

            if i.y < self.doctor.y:
                i.y += 1

            if i.y > self.doctor.y:
                i.y -= 1

    def deplacement_docteur(self, deplacement, zapper=False):
        if self.verifiercollisionferraile(deplacement):
            self.doctor.deplacement(deplacement)
        else:
            self.doctor.deplacement([0, 0])

        if zapper:
            self.zapper()

        self.deplacement_dalek()
        self.docteur_en_vie()
        self.collision_daleks()
        self.collision_avec_ferraile()
        self.nouveau_niveau()

    def docteur_en_vie(self):
        for i in self.daleks:
            if i.x == self.doctor.x and i.y == self.doctor.y:
                self.doctor.etat = False

        for i in self.position_ferraile:
            if i == [self.doctor.x, self.doctor.y]:
                self.doctor.etat = False

    def collision_daleks(self):

        positiondalek = []

        for i in self.daleks:
            positiondalek.append([i.x, i.y])

            if positiondalek.count([i.x, i.y]) >= 2:
                positiondalek.remove([i.x, i.y])
                self.position_ferraile.append([i.x, i.y])
                self.daleks.remove(i)

    def collision_avec_ferraile(self):

        for i in self.daleks:
            if [i.x, i.y] in self.position_ferraile:
                self.score += 5
                self.daleks.remove(i)

    def nouveau_niveau(self):

        if not self.daleks and self.doctor.etat:
            self.creer_niveau()
            self.compteur_zap = self.niveau

    def zapper(self):
        if self.compteur_zap > 0:
            self.compteur_zap -= 1
        for i in range(self.doctor.x - 1, self.doctor.x + 2):
            for j in range(self.doctor.y - 1, self.doctor.y + 2):
                for k in self.daleks:
                    if [i, j] == [k.x, k.y]:
                        self.position_ferraile.append([k.x, k.y])
                        self.score += 5
                        self.daleks.remove(k)

    def verifiercollisionferraile(self, deplacment):
        if [self.doctor.x + deplacment[0], self.doctor.y + deplacment[1]] in self.position_ferraile:
            return False
        else:
            return True


class Controleur:
    def __init__(self):
        self.model = Jeu()
        self.vue = Vue  # create une instance de vue with les parentheses
        self.actions = {"p": self.demarrer_partie,
                        "s": self.afficher_score,
                        "o": self.choisir_option,
                        }

        self.show_menu_initial()

    def show_menu_mouvement(self):
        reponse_zap = self.vue.afficher_option_zapper(self.model.partie_courante.compteur_zap)

        if not reponse_zap:
            docteur_deplacement = self.vue.afficher_menu_mouvement()
            self.model.partie_courante.deplacement_docteur(docteur_deplacement)

        else:
            if self.model.partie_courante.compteur_zap > 0:
                self.model.partie_courante.deplacement_docteur([0, 0], reponse_zap)
            elif self.model.partie_courante.compteur_zap == 0:
                self.show_menu_mouvement()
                self.vue.pas_de_zap()

        self.vue.afficher_partie(self.model.partie_courante)

    def show_menu_initial(self):
        answer = self.vue.afficher_menu_initial()
        if answer in self.actions.keys():
            self.actions[answer]()
            while self.model.partie_courante.doctor.etat:
                self.show_menu_mouvement()
            else:

                self.vue.fin_de_partie(self.model.partie_courante)
                self.model.partie_courante.score = 0
                self.show_menu_initial()

        else:
            print("erreur")

    def demarrer_partie(self):
        self.model.demarrer_partie()
        self.vue.afficher_partie(self.model.partie_courante)
        print("PARTIE")

    def afficher_score(self):
        print("SCORE")

    def choisir_option(self):
        reponse = self.vue.afficher_menu_options()
        reponse2 = self.vue.afficher_menu_options2()
        self.model.change_options(largeur=reponse, hauteur=reponse2)
        self.show_menu_initial()
        print("OPTIONS")


if __name__ == '__main__':
    c = Controleur()

    print("Fin de Dalek")
