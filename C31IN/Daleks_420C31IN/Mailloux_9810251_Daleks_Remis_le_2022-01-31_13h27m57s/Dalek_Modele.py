import random
import os

class Jeu():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 8
        self.hauteur = 8
        self.partie_courante = None
        self.high_score = []
        self.chemin_scores = "./high_scores.txt"
        self.charger_scores()

    def charger_scores(self):
        if os.path.isfile(self.chemin_scores):
            with open(self.chemin_scores, 'r') as f:
                for i in f.read().splitlines():
                    self.high_score.append(int(i))
                self.high_score.sort()

    def demarrer_partie(self, difficulte):
        self.partie_courante = Partie(self, difficulte)
        self.partie_courante.creer_niveau()


    def changer_options(self, largeur=12, hauteur=12):
        self.largeur = largeur
        self.hauteur = hauteur

    def jouer(self, parent):
        self.parent = parent
        jouer = True
        while jouer:
            while self.partie_courante.docteur.en_vie and len(self.partie_courante.daleks) > 0:
                self.parent.vue.afficher_partie(self.partie_courante)
                action = self.parent.vue.afficher_actions_docteur()
                if action in self.partie_courante.docteur.actions:
                    self.partie_courante.tour(action)
                else:
                    print("Action invalide")
            if self.partie_courante.docteur.en_vie and len(self.partie_courante.daleks) == 0:
                self.partie_courante.augmenter_niveau()
                input("Bravo, vous avez survécu à cette vague."
                      "Appuyez sur une touche pour passer au prochain niveau")
            else:
                print("Vous êtes mort...")
                print(f"Vous avez fait un score de {self.partie_courante.score}")
                self.high_score.append(self.partie_courante.score)
                jouer = False
        self.parent.afficher_menu_initial()


class Partie():
    def __init__(self, parent, difficulte):
        self.parent = parent
        self.score = 0
        self.niveau = 0
        self.densite = 0.35
        self.nb_daleks_par_niveau = 5
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.docteur = Docteur(self)
        self.daleks = []
        self.ferrailles = []
        self.difficulte = difficulte

    def creer_niveau(self):
        self.docteur.x = int(self.largeur / 2)
        self.docteur.y = int(self.hauteur / 2)
        self.niveau += 1
        nb_daleks = self.niveau * self.nb_daleks_par_niveau
        positions = [[self.docteur.x, self.docteur.y]]

        if nb_daleks > (self.largeur * self.hauteur)*self.densite:
            self.largeur += 1
            self.hauteur += 1

        while nb_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x, y] not in positions:
                positions.append([x, y])
                nb_daleks -= 1
        positions.pop(0)
        for i in positions:
            self.daleks.append(Dalek(self, i[0], i[1]))

    def augmenter_niveau(self):
        self.densite += 0.015
        self.daleks = []
        self.ferrailles = []
        self.docteur.nb_zapper += 1
        self.creer_niveau()

    def tour(self, action):
        self.deplacer_docteur(action)
        self.deplacer_daleks()
        self.verifier_collisions()
        self.verifier_vie_docteur()

    def deplacer_daleks(self):
        for dalek in self.daleks:
            dalek.deplacer_dalek()

        for i in self.daleks:
            if i.x == self.docteur.x and i.y == self.docteur.y:
                self.docteur.en_vie = False

    def verifier_collisions(self):
        daleks_morts = []

        # Vérifier daleks qui entrent en collision avec ferraille
        for i in self.daleks:
            for j in self.ferrailles:
                if i.x == j.x and i.y == j.y:
                    daleks_morts.append(i)
                    self.score += 5

        #Vérifier daleks qui entrent en collision entre eux
        for i in self.daleks:
            for j in self.daleks:
                if i != j and (i.x == j.x and i.y == j.y):
                    if i not in daleks_morts:
                        daleks_morts.append(i)
                        self.score += 5

        #Retirer les daleks et fabriquer une ferraille si nécessaire
        for i in daleks_morts:
            self.daleks.remove(i)
            inexistant = 1
            for j in self.ferrailles:
                if i.x == j.x and i.y == j.y:
                    inexistant = 0
            if inexistant:
                self.ferrailles.append(Ferraille(self, i.x, i.y))

    def deplacer_docteur(self, action):
        if action not in self.docteur.actions:
            self.parent.vue.afficher_erreur()
            self.deplacer_docteur()
        else:
            self.docteur.actions[action]()

    def verifier_vie_docteur(self):
        for i in self.daleks:
            if i.x == self.docteur.x and i.y == self.docteur.y:
                self.docteur.en_vie = False


class Dalek():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def deplacer_dalek(self):
        if self.x > self.parent.docteur.x:
            self.x -= 1
        elif self.x < self.parent.docteur.x:
            self.x += 1
        if self.y > self.parent.docteur.y:
            self.y -= 1
        elif self.y < self.parent.docteur.y:
            self.y += 1


class Ferraille():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y


class Docteur():
    def __init__(self, parent, x=1, y=1):
        self.partie = parent
        self.x = x
        self.y = y
        self.arrive = []
        self.en_vie = True
        self.nb_zapper = 1
        self.actions = {"5": self.immobile,
                        "8": self.monter,
                        "7": self.monter_gauche,
                        "9": self.monter_droite,
                        "2": self.descendre,
                        "1": self.descendre_gauche,
                        "3": self.descendre_droite,
                        "4": self.gauche,
                        "6": self.droite,
                        "t": self.teleporter,
                        "z": self.zapper
                        }


    def monter_gauche(self):
        if self.x >= 1:
            self.x -= 1
        if self.y >= 1:
            self.y -= 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.descendre_droite()
        self.partie.verifier_vie_docteur()

    def monter_droite(self):
        if self.x <= self.partie.largeur - 2:
            self.x += 1
        if self.y >= 1:
            self.y -= 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.descendre_gauche()
        self.partie.verifier_vie_docteur()

    def descendre_gauche(self):
        if self.x >= 1:
            self.x -= 1
        if self.y <= self.partie.hauteur - 2:
            self.y += 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.monter_droite()
        self.partie.verifier_vie_docteur()

    def descendre_droite(self):
        if self.x <= self.partie.largeur - 2:
            self.x += 1
        if self.y <= self.partie.hauteur - 2:
            self.y += 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.monter_gauche()
        self.partie.verifier_vie_docteur()

    def monter(self):
        if self.y >= 1:
            self.y -= 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.descendre()
        self.partie.verifier_vie_docteur()

    def descendre(self):
        if self.y <= self.partie.hauteur - 2:
            self.y += 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.monter()
        self.partie.verifier_vie_docteur()

    def gauche(self):
        if self.x >= 1:
            self.x -= 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.droite()
        self.partie.verifier_vie_docteur()

    def droite(self):
        if self.x <= self.partie.largeur - 2:
            self.x += 1
        for i in self.partie.ferrailles:
            if i.x == self.x and i.y == self.y:
                self.gauche()
        self.partie.verifier_vie_docteur()

    def immobile(self):
        self.x = self.x
        self.y = self.y
        self.partie.verifier_vie_docteur()

    def zapper(self):
        if self.nb_zapper == 0:
            print("Vous n'avez plus de zapper")

        while self.nb_zapper > 0:
            daleks_morts = []
            self.nb_zapper -= 1
            for i in self.partie.daleks:
                if abs(i.x - self.x) <= 1 and abs(i.y - self.y) <= 1:
                    daleks_morts.append(i)
            for i in daleks_morts:
                self.partie.daleks.remove(i)
                self.partie.score += 5
                self.partie.ferrailles.append(Ferraille(self, i.x, i.y))

    def teleporter(self):
        existant = True
        compteur_loop = 0
        while (existant and compteur_loop < self.partie.largeur * self.partie.hauteur):
            compteur = 0
            x = random.randrange(self.partie.largeur)
            y = random.randrange(self.partie.hauteur)
            for i in self.partie.ferrailles:
                if i.x == x and i.y == y:
                    compteur += 1
            if self.partie.difficulte == 'd':
                for i in self.partie.daleks:
                    if abs(i.x - x) <= 1 and abs(i.y - y) <= 1:
                        compteur += 1
            elif self.partie.difficulte == 'i':
                for i in self.partie.daleks:
                    if i.x == x and i.y == y:
                        compteur += 1
            if compteur > 0:
                existant = True
            else:
                existant = False
            self.partie.verifier_vie_docteur()
            compteur_loop += 1
        self.x = x
        self.y = y


