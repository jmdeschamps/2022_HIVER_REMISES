import Daleks_Vue
import random
import os


class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 9
        self.hauteur = 9
        self.difficulte = 0
        self.partie_courante = None

    def demarrer_partie(self):
        self.partie_courante = Partie(self)

    def jouer(self):
        # Tant que la partie n'est pas terminée
        while self.partie_courante.fin_de_partie is False:
            dalek_transmute = []
            decision_legale = False
            while decision_legale is False:
                os.system('cls')
                self.parent.vue.afficher_partie(self.partie_courante)
                reponse = self.parent.vue.afficher_menu_jeu(self.partie_courante.msg_erreur)
                if reponse in 'wsadqezc ':
                    decision_legale = self.partie_courante.docteur.deplacer(reponse,self.partie_courante.tas_de_ferraille)
                elif reponse == 't':
                    decision_legale = self.partie_courante.docteur.teleporter()
                elif reponse == 'p':
                    decision_legale = self.partie_courante.docteur.zapper(self.partie_courante.daleks, dalek_transmute)
                else:
                    self.partie_courante.msg_erreur = "Saisissez une commande valide."

            # Déplacement des Daleks non-zappés
            for dalek in self.partie_courante.daleks:
                if dalek not in dalek_transmute:
                    if dalek.deplacer(self.partie_courante.docteur.x, self.partie_courante.docteur.y):
                        self.partie_courante.fin_de_partie = True

            # Collision des Daleks ensemble
            for i in self.partie_courante.daleks:
                for j in self.partie_courante.daleks:
                    if i is not j:
                        if i.x == j.x and i.y == j.y:
                            dalek_transmute.append(i)

            # Collision des Daleks avec un tas de ferraille
            for i in self.partie_courante.daleks:
                for j in self.partie_courante.tas_de_ferraille:
                    if i not in dalek_transmute:
                        if i.x == j.x and i.y == j.y:
                            dalek_transmute.append(i)

            # Transmutation des Daleks concernés en ferraille
            for i in dalek_transmute:
                self.partie_courante.tas_de_ferraille.append(TasFerraille(i.x, i.y))
                if i in self.partie_courante.daleks:
                    self.partie_courante.daleks.remove(i)
                    self.partie_courante.score += i.worth

            # S'il n'y a plus de Daleks, on crée un nouveau niveau
            if not len(self.partie_courante.daleks):
                self.partie_courante.creer_niveau()

        self.parent.nouveau_score(self.partie_courante.score)

    def changer_option(self, largeur=9, hauteur=9, difficulte=0):
        self.largeur = largeur
        self.hauteur = hauteur
        self.difficulte = difficulte


class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.difficulte = self.parent.difficulte
        self.niveau = 0
        self.daleks_par_niveau = 5
        self.daleks = []
        self.tas_de_ferraille = []
        self.docteur = Docteur(self, self.largeur-1, self.hauteur-1, int(self.largeur / 2), int(self.hauteur / 2))
        self.fin_de_partie = False
        self.creer_niveau()
        self.score = 0
        self.msg_erreur = None

    def creer_niveau(self):
        self.niveau += 1
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.docteur.nbr_zapper += 1
        self.tas_de_ferraille.clear()
        nb_daleks = self.daleks_par_niveau * self.niveau
        pos_valides = [[self.docteur.x, self.docteur.y]]

        while nb_daleks:
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x, y] not in pos_valides:
                pos_valides.append([x, y])
                nb_daleks -= 1

        pos_valides.pop(0)
        for i in pos_valides:
            self.daleks.append(Dalek(i))


class Docteur:
    def __init__(self, parent, max_x, max_y, x=1, y=1):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.nbr_zapper = 0
        self.parent = parent

    def deplacer(self, touche, tas_de_ferraille):
        direction_x = 0
        direction_y = 0

        if touche == 'w' and self.y:
            direction_y = -1
        elif touche == 's' and self.y is not self.max_y:
            direction_y = 1
        elif touche == 'a' and self.x:
            direction_x = -1
        elif touche == 'd' and self.x is not self.max_x:
            direction_x = 1
        elif touche == 'q' and self.x and self.y:
            direction_y = -1
            direction_x = -1
        elif touche == 'e' and self.x is not self.max_x and self.y:
            direction_y = -1
            direction_x = 1
        elif touche == 'z' and self.x and self.y is not self.max_y:
            direction_y = 1
            direction_x = -1
        elif touche == 'c' and self.x is not self.max_x and self.y is not self.max_y:
            direction_y = 1
            direction_x = 1
        elif touche == ' ':
            print("Vous attendez")
        else:
            self.parent.msg_erreur = "Mouvement impossible, recommencez."
            return False

        for tas in tas_de_ferraille:
            if self.x + direction_x == tas.x and self.y + direction_y == tas.y:
                self.parent.msg_erreur = "Impossible de se déplacer sur un tas de ferraille."
                return False

        self.x += direction_x
        self.y += direction_y
        self.parent.msg_erreur = None
        return True

    def teleporter(self):
        teleportation_valide = False
        positions_non_valides = []

        while not teleportation_valide:
            teleportation_x = random.randrange(self.parent.largeur)
            teleportation_y = random.randrange(self.parent.hauteur)
            # Position est valide jusqu'à preuve du contraire
            position_valide = True

            if [teleportation_x, teleportation_y] in positions_non_valides:
                position_valide = False

            if position_valide:
                # S'assurer qu'on ne reste pas à la même place
                if teleportation_x is self.x and teleportation_y is self.y:
                    position_valide = False

            if position_valide:
                # Si difficulté facile, Daleks ne doivent pas se trouver à 2 cases et moins de la téléportation
                if self.parent.difficulte == 0:
                    for dalek in self.parent.daleks:
                        if (teleportation_x - 2) <= dalek.x <= (teleportation_x + 2):
                            if (teleportation_y - 2) <= dalek.y <= (teleportation_y + 2):
                                position_valide = False
                # Si difficulté moyenne, Daleks ne doivent pas se trouver à l'endroit de la téléportation
                elif self.parent.difficulte == 1:
                    for dalek in self.parent.daleks:
                        if dalek.x is teleportation_x and dalek.y is teleportation_y:
                            position_valide = False
                # Si difficulté difficile, la nouvelle position est toujours valide vis-à-vis des Daleks

            # Vérifier qu'il n'y a aucune ferraille à la nouvelle position
            if position_valide:
                if self.parent.tas_de_ferraille:
                    for tas in self.parent.tas_de_ferraille:
                        if teleportation_x is tas.x and teleportation_y is tas.y:
                            position_valide = False

            teleportation_valide = position_valide

            if teleportation_valide is False:
                if ([teleportation_x, teleportation_y]) not in positions_non_valides:
                    positions_non_valides.append([teleportation_x, teleportation_y])
                    if len(positions_non_valides) == self.parent.largeur * self.parent.hauteur:
                        self.parent.msg_erreur = "Impossible de se téléporter, " \
                                                 "car aucune position valide en accord avec la difficulté choisie."
                        return False

        self.x = teleportation_x
        self.y = teleportation_y
        return True

    def zapper(self, daleks, transmute_list):
        if self.nbr_zapper > 0:
            for dalek in daleks:
                if abs(dalek.x-self.x) <= 1 and abs(dalek.y-self.y) <= 1:
                    transmute_list.append(dalek)
            self.nbr_zapper -= 1
            self.parent.msg_erreur = None
            return True
        else:
            self.parent.msg_erreur = "Aucune charge de zapper."
            return False


class Dalek:
    def __init__(self, pos):
        pos_x, pos_y = pos
        self.x = pos_x
        self.y = pos_y
        self.worth = 5

    def deplacer(self, docteur_x, docteur_y):
        if docteur_x > self.x:
            self.x += 1
        elif docteur_x < self.x:
            self.x -= 1
        if docteur_y > self.y:
            self.y += 1
        elif docteur_y < self.y:
            self.y -= 1

        return self.x == docteur_x and self.y == docteur_y


class TasFerraille:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Daleks_Vue.Vue()
        self.actions_menu_initial = {
            "p": self.demarrer_partie,
            "o": self.choisir_option,
            "s": self.voir_score,
            "m": self.voir_manuel,
            "q": self.quitter
        }
        self.liste_scores = []
        self.quitter_logiciel = False
        self.afficher_menu_initial()

    def afficher_menu_initial(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse in self.actions_menu_initial.keys():
            self.actions_menu_initial[reponse]()
        else:
            print("Saisissez une commande valide.")

    def demarrer_partie(self):
        self.modele.demarrer_partie()
        self.jouer()

    def jouer(self):
        self.modele.jouer()

    def nouveau_score(self, score):
        nom = self.vue.nouveau_score(score)
        with open('score.txt', 'a') as f:
            f.write(f"{score} {nom}\n")

    # Menu d'options du jeu
    def choisir_option(self):
        nouvelle_largeur, nouvelle_hauteur, nouvelle_difficulte = self.vue.afficher_menu_option()
        self.modele.changer_option(largeur=nouvelle_largeur, hauteur=nouvelle_hauteur, difficulte=nouvelle_difficulte)
        self.afficher_menu_initial()

    # Affichage des High Scores
    def voir_score(self):
        self.liste_scores.clear()

        # Création d'un fichier vide si les scores sont inexistants
        if not os.path.exists('score.txt'):
            with open('score.txt', 'w'):
                pass

        with open('score.txt', 'r') as f:
            for line in f:
                score_entree = line.split()
                score_valeur, score_nom = score_entree
                self.liste_scores.append([int(score_valeur), score_nom.strip()])

        self.vue.afficher_score(sorted(self.liste_scores, key=lambda x: x[0], reverse=True))
        self.afficher_menu_initial()

    def voir_manuel(self):
        self.vue.afficher_manuel()

    def quitter(self):
        self.quitter_logiciel = True


if __name__ == '__main__':
    quitter_logiciel = False
    while not quitter_logiciel:
        c = Controleur()
        quitter_logiciel = c.quitter_logiciel
        