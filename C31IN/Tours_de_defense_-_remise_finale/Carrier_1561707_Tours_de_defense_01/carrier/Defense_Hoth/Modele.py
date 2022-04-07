import os
import time
from Classes.Tour import *
from Classes.Map import *


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.partie = None
        self.largeur = 1200
        self.hauteur = 900
        self.pause = True
        self.duree = 0
        self.debut = None
        self.difficulte = 2
        self.argent = 100
        self.vie = 100
        self.high_scores = []
        self.charger_scores()

    def charger_scores(self):
        chemin_fichier = ".\high_scores.txt"
        if os.path.isfile(chemin_fichier):
            with open(chemin_fichier) as f:
                lines = f.readlines()
                for line in lines:
                    if line:
                        cols = line.split(",")
                        cols.pop()
                        self.high_scores.append(cols)

    def sauver_scores(self):
        chemin_fichier = '.\high_scores.txt'
        with open(chemin_fichier, 'w') as f:
            for i in self.high_scores:
                f.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + "\n")

    def acheter_tour(self, tour_achetee, pos_x, pos_y):
        return self.partie.acheter_tour(tour_achetee, pos_x, pos_y)

    def changer_difficultes(self, difficulte):
        self.vie = 150 * (difficulte / 3)
        self.argent = 150 * (difficulte / 3)

    def jouer_tour(self):
        if self.debut == None:
            self.debut = time.time()
        self.duree = time.time() - self.debut
        self.partie.activer_tour()
        self.partie.avancer_creeps()
        self.partie.spawn_creep()
        self.verifier_fin()

    def nouvelle_partie(self, map_choisie):
        self.duree = 0
        self.debut = None
        self.partie = Partie(self, map_choisie, self.difficulte)

    def nouvelle_vague(self):
        self.partie.nouvelle_vague()

    def upgrade_tour(self, id_tour, upgrade):
        self.partie.upgrade_tour(id_tour, upgrade)

    def vendre_tour(self, id_tour):
        self.partie.vendre_tour(id_tour)

    def verifier_fin(self):
        fin = False
        success = False
        inscrire = False
        if self.partie.vie > 0 and self.partie.nbr_creeps_restants == 0:
            fin = True
            success = True
            if self.duree < float(self.partie.scores_a_battre[2][3]):
                inscrire = True
        elif self.partie.vie < 0:
            fin = True
        if fin:
            self.parent.partie_en_cours = False
            self.partie.score_final = round(self.duree, 2)
            self.parent.terminer_partie(success, self.duree, inscrire)


class Partie:
    def __init__(self, parent, map_choisie, difficulte):
        self.parent = parent
        self.id = 0
        self.maps = {1: Debarquement, 2: Grotte, 3: Plaines}
        self.map = self.maps[map_choisie](self)
        self.scores_a_battre = []
        self.difficulte = difficulte
        self.argent = self.parent.argent
        self.vie = self.parent.vie

        self.liste_tours = []
        self.types_tour = {1: [TourMitraillette, '#6666FF', 15], 2: [TourLanceRoquette, '#66FF66', 30],
                           3: [TourShocker, '#FF6666', 65], 4: [TourSniper, '#FFFFFF', 75]}

        self.liste_creeps = []
        self.nbr_vagues = len(self.map.composition_vagues)
        self.numero_vague = 0
        self.nbr_creeps_restants = self.map.total_creeps

        self.score_final = 0
        self.map_choisie = map_choisie
        self.scores_a_battre = []
        self.charger_scores_a_battre()

    def charger_scores_a_battre(self):
        for i in self.parent.high_scores:
            if int(i[0]) == self.map_choisie:
                if int(i[1]) == self.difficulte:
                    self.scores_a_battre.append(i)
        self.scores_a_battre.sort(key=lambda x: x[3])

    def inscire_nouv_score(self, nom, score):
        data = []
        data.append(str(self.map_choisie))
        data.append(str(self.difficulte))
        data.append(str(nom))
        data.append(str(score))
        self.scores_a_battre.append(data)
        self.scores_a_battre.sort(key=lambda x: float(x[3]))
        self.scores_a_battre.pop()
        temp = []
        for i in self.parent.high_scores:
            if int(i[0]) != self.map_choisie:
                temp.append(i)
            if int(i[0]) == self.map_choisie and int(i[1]) != self.difficulte:
                temp.append(i)
        for i in self.scores_a_battre:
            temp.append(i)
        temp.sort(key=lambda x: (int(x[0]), int(x[1]), float(x[3])))
        self.parent.high_scores = temp
        self.parent.sauver_scores()

    def acheter_tour(self, tour_choisie, pos_x, pos_y):
        tour_achetee = self.types_tour[int(tour_choisie)]
        type = tour_achetee[0]
        prix = tour_achetee[2]
        if self.argent >= prix and not self.parent.parent.paused:
            tour = type(self, self.getID(), prix, pos_x, pos_y)
            self.liste_tours.append(tour)
            self.argent -= tour.valeur
            return tour

    def activer_tour(self):
        for tour in self.liste_tours:
            tour.avancer_projectiles()
            tour.surveiller()

    def avancer_creeps(self):
        creeps_sortis = []
        for creep in self.liste_creeps:
            dommage = creep.avancer()
            if dommage > 0:
                self.vie -= dommage
                creeps_sortis.append(creep)
        for creep in creeps_sortis:
            index = self.liste_creeps.index(creep)
            del self.liste_creeps[index]

    def getID(self):
        self.id += 1
        return self.id

    def nouvelle_vague(self):
        if self.numero_vague < self.nbr_vagues:
            self.numero_vague += 1

    def spawn_creep(self):
        if self.numero_vague > 0:
            for i in range(self.numero_vague):
                creep = self.map.composition_vagues[i].spawn()
                if creep:
                    self.liste_creeps.append(creep)

    def tuer_creep(self, creep):
        index = self.liste_creeps.index(creep)
        self.argent += creep.valeur_monetaire
        del self.liste_creeps[index]
        self.nbr_creeps_restants -= 1
        for tour in self.liste_tours:
            tour.victime = None
            tour.surveiller()

    def upgrade_tour(self, id_tour, upgrade):
        for tour in self.liste_tours:
            if tour.idTour == id_tour:
                cout = tour.upgradeTour(upgrade)
                self.argent -= cout

    def vendre_tour(self, id_tour):
        for tour in self.liste_tours:
            if tour.idTour == id_tour:
                index = self.liste_tours.index(tour)
                self.argent += tour.valeur * 0.5
                del self.liste_tours[index]
