from partie import Partie


class Jeu:

    def __init__(self):
        self.largeur = 8
        self.hauteur = 6
        self.teleportation = 1
        self.partie_courante = None

    def demarrer_partie(self):
        self.partie_courante = Partie(largeur=self.largeur, hauteur=self.hauteur, teleportation=self.teleportation)

    def changer_options(self, options_jeu):
        self.largeur = options_jeu['largeur']
        self.hauteur = options_jeu['hauteur']
        self.teleportation = options_jeu['difficulte']

    def lire_scores(self):
        with open('donnees/scores.csv', 'r') as f:
            donnees = f.read()
            f.close()
        return donnees.split()

    def trier_scores(self, liste_scores):
        for i in range(len(liste_scores)):
            for j in range(len(liste_scores)):
                if int(liste_scores[j].split(",")[1]) > int(liste_scores[i].split(",")[1]):
                    temp = liste_scores[j]
                    liste_scores[j] = liste_scores[i]
                    liste_scores[i] = temp
        return liste_scores

    def ecrire_score(self, nom):
        with open('donnees/scores.csv', 'a') as f:
            f.write(nom + "," + str(self.partie_courante.score) + "\n")
            f.close()

    def jouer_tour_dalek(self, dalek):
        self.partie_courante.trouver_positions_occupees()
        self.partie_courante.deplacer_dalek(dalek)
        self.partie_courante.verifier_collision(dalek)
        self.partie_courante.verifier_mort_par_ferraille(dalek)
        return self.partie_courante.verifier_attaque(dalek)

    def changer_niveau(self):
        self.partie_courante.changer_niveau()


