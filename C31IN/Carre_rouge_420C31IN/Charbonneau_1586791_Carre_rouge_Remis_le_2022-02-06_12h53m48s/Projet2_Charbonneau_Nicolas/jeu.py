from partie import Partie


class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.largeur_fenetre = 550
        self.hauteur_fenetre = 550
        self.largeur_zone = 450
        self.hauteur_zone = 450
        self.partie_courante = Partie(self)
        self.liste_scores = []
        self.choix_sentinelles = 2
        self.choix_pion = 2
        self.choix_jeu = 2
        self.choix_difficulte = "4"

    def demarrer_chrono(self):
        self.partie_courante.demarrer_chrono()

    def arreter_chrono(self):
        self.partie_courante.arreter_chrono()

    def incrementer_vitesse(self):
        self.partie_courante.incrementer_vitesse()

    def deplacer_pion(self, x, y):
        self.partie_courante.deplacer_pion(x, y)

    def deplacer_sentinelles(self):
        self.partie_courante.deplacer_sentinelles()

    def verifier_collision(self):
        self.partie_courante.verifier_collision()

    def verifier_sortie(self):
        self.partie_courante.verifier_sortie()

    def reinitialiser_objets(self):
        self.partie_courante.reinitialiser_objets()

    def calculer_points(self):
        self.partie_courante.calculer_points()

    def ajouter_score(self, duree):
        self.liste_scores.append([duree, self.partie_courante.points])

    def sauvegarder_session(self, nom):
        if nom == "":
            nom = "anonyme"
        with open("donnees/scores.csv", "a") as f:
            for i in self.liste_scores:
                f.write(nom + "," + i[0] + "," + str(i[1]) + "\n")
            f.close()
        self.liste_scores = []

    def supprimer_session(self):
        self.liste_scores = []

    def lire_scores(self):
        with open("donnees/scores.csv", "r") as f:
            donnees = f.read().split()
            f.close()
        return donnees

    def trier_scores(self):
        with open("donnees/scores.csv", "r") as f:
            donnees = f.read().split()
            f.close()
        for i in range(len(donnees)):
            for j in range(len(donnees)):
                if int(donnees[j].split(",")[2]) > int(donnees[i].split(",")[2]):
                    temp = donnees[j]
                    donnees[j] = donnees[i]
                    donnees[i] = temp
        return donnees

    def effacer_scores(self):
        with open("donnees/scores.csv", "w") as f:
            f.write("")
            f.close()

    def sauvegarder_options(self, choix_sentinelles, choix_pion, choix_jeu, choix_difficulte):
        self.choix_sentinelles = choix_sentinelles
        self.choix_pion = choix_pion
        self.choix_jeu = choix_jeu
        self.choix_difficulte = choix_difficulte
        if choix_jeu == "1":
            dimension_jeu = 1
        elif choix_jeu == "2":
            dimension_jeu = 1.5
        elif choix_jeu == "3":
            dimension_jeu = 2
        self.largeur_fenetre = 550 * dimension_jeu
        self.hauteur_fenetre = 550 * dimension_jeu
        self.largeur_zone = 450 * dimension_jeu
        self.hauteur_zone = 450 * dimension_jeu
        self.partie_courante = Partie(self)
        self.partie_courante.sauvegarder_options()