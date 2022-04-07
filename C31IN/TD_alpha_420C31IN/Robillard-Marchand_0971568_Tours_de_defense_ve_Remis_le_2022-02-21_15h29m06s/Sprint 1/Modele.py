import json
import math
import time
from random import randrange


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.partie = None

        self.maps = {
            1: ["Hoth", "./Carte/GC_Wilderness.png",
                [[0, 55], [104, 59], [119, 109], [125, 281], [146, 298], [279, 356], [392, 390], [584, 376],
                 [636, 264], [705, 265], [711, 156], [784, 144], [800, 136]]],
            2: ["Endor", "#274e13",
                [[0, 300], [200, 300], [200, 200], [300, 200], [300, 400], [400, 400], [400, 200], [500, 200],
                 [500, 400], [600, 400], [600, 300], [800, 300]]],
            3: ["Tatooine", "#e7a477",
                [[0, 300], [200, 300], [200, 200], [300, 200], [300, 400], [400, 400], [400, 200], [500, 200],
                 [500, 400], [600, 400], [600, 300], [800, 300]]]
        }
        self.largeur = 800
        self.hauteur = 600
        self.pause = True
        self.duree = 0
        self.debut = None

        self.score_dict = {"Nom_utilisateur": [], "Temps": [], "Date": []}
        self.sauvegarde_info_dict = {"Nom_utilisateur": [], "Mot_de_passe": []}

    def nouvelle_partie(self, map_choisie):
        map = Map(self.maps[map_choisie])
        self.partie = Partie(self, map)

    def nouvelle_vague(self):
        self.partie.nouvelle_vague()

    def acheter_tour(self, tour_achetee, pos_x, pos_y):
        return self.partie.acheter_tour(tour_achetee, pos_x, pos_y)

    def jouer_tour(self):
        if self.debut == None:
            self.debut = time.time()
        self.duree = time.time() - self.debut
        self.partie.activer_tour()
        self.partie.avancer_creeps()

    def validation_login(self):
        with open('information_utlisateurs.json', 'w') as f:
            json.dump(self.sauvegarde_info_dict,f)

    def validation_score(self):
        if self.partie.vie > 0 and self.partie.liste_creeps == 0:
            with open('scores.json', 'w') as f:
                json.dump(self.score_dict,f)


class Partie:
    def __init__(self, parent, map):
        self.parent = parent
        self.map = map
        self.argent = 100
        self.vie = 100

        self.liste_tours = []
        # Type, apparence, coût, vitesse, dommage, portée (en pixel), rayon_explosion (en pixel), largeur_modele, hauteur_modele
        self.types_tour = {
            1: ['Mitraillette', '#6666FF', 15, 4, 1, 100, 0, 8, 10],
            2: ['Lance-Roquette', '#66FF66', 30, 1, 6, 150, 25, 10, 13],
            3: ['Shocker', '#FF6666', 50, 1, 1, 80, 0, 12, 16]
        }

        self.liste_creeps = []
        # Type, apparence, vie, vitesse, dommage au joueur
        self.type_creeps = {
            1: ['Normal', 'yellow', 10, 3, 20],
            2: ['Rapide', 'orange', 20, 6, 30],
            3: ['Boss', 'red', 50, 3, 60]
        }

        self.composition_vagues = [[1, 1, 1, 1, 1],
                                   [1, 1, 1, 2, 2],
                                   [1, 1, 2, 2, 3]]
        self.nbr_vagues = len(self.composition_vagues)
        self.numero_vague = 0
        self.partie_finie = False


    def nouvelle_vague(self):
        if self.numero_vague < self.nbr_vagues:
            numero = 0
            composition_vague = self.composition_vagues[self.numero_vague]
            for type_creep in composition_vague:
                numero += 1
                parametres = self.type_creeps[type_creep]
                chemin = self.map.sentier
                creep = Creep(self, parametres, chemin, numero)
                self.liste_creeps.append(creep)
            self.numero_vague += 1
        else:
            self.numero_vague = 0

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
        if self.vie <= 0:
            self.arreter_partie()

    def arreter_partie(self):
        if not self.partie_finie:
            print("Fin de la partie!")
            self.partie_finie = True

    def acheter_tour(self, tour_achetee, pos_x, pos_y):
        tour_choisie = self.types_tour[int(tour_achetee)]
        if self.argent >= tour_choisie[2]:
            tour = Tour(self, tour_choisie, pos_x, pos_y)
            self.liste_tours.append(tour)
            self.argent -= tour.valeur
            return tour

    def tuer_creep(self, creep):
        index = self.liste_creeps.index(creep)
        self.argent += creep.valeur_monetaire
        del self.liste_creeps[index]
        for tour in self.liste_tours:
            tour.victime = None
            tour.surveiller()

    def activer_tour(self):
        for tour in self.liste_tours:
            tour.avancer_projectiles()
            tour.surveiller()


class Map:
    def __init__(self, tableau_parametres):
        name, background, sentier = tableau_parametres
        self.name = name
        self.path_fichier = background
        self.sentier = sentier


class Creep:
    def __init__(self, parent, tableau_parametres, chemin, numero):
        archetype, apparence, vie, vitesse, valeur_dommage = tableau_parametres
        self.parent = parent
        self.archetype = archetype
        self.vie = vie
        self.vie_max = vie
        self.vitesse = vitesse
        self.valeur_dommage = valeur_dommage
        self.valeur_monetaire = self.vie_max
        self.distance_parcourue = 0
        self.apparence = apparence
        self.largeur = 10
        self.hauteur = 10
        self.chemin = chemin
        self.numero = numero
        self.derniere_position = len(chemin) - 1
        self.x = chemin[0][0]
        self.y = chemin[0][1]
        self.destination = 1
        self.destination_x = chemin[self.destination][0]
        self.destination_y = chemin[self.destination][1]
        self.random_position_x_variation = randrange(-25, 25)
        self.random_position_y_variation = randrange(-15, 15)

    def avancer(self):
        if self.x < self.destination_x:
            self.x = self.x + self.vitesse
            if self.x > self.destination_x:
                self.x = self.destination_x
        elif self.x > self.destination_x:
            self.x = self.x - self.vitesse
            if self.x < self.destination_x:
                self.x = self.destination_x

        if self.y < self.destination_y:
            self.y = self.y + self.vitesse
            if self.y > self.destination_y:
                self.y = self.destination_y
        elif self.y > self.destination_y:
            self.y = self.y - self.vitesse
            if self.y < self.destination_y:
                self.y = self.destination_y

        if self.x == self.destination_x and self.y == self.destination_y:
            if self.destination < self.derniere_position:
                self.destination += 1
                self.destination_x = self.chemin[self.destination][0]
                self.destination_y = self.chemin[self.destination][1]
            else:
                return self.valeur_dommage
        return 0

    def baisser_vie(self, dommage):
        self.vie -= dommage
        if self.vie <= 0:
            self.parent.tuer_creep(self)
        return True

class Tour:
    def __init__(self, parent, tableau_parametres, position_x, position_y):
        archetype, apparence, cout, vitesse, dommage, portee, rayon_explosion, largeur_modele, hauteur_modele = tableau_parametres
        self.parent = parent
        self.archetype = archetype
        self.apparence = apparence
        self.valeur = cout
        self.vitesse = vitesse
        self.cooldown_max = (1000/50)/vitesse
        self.cooldown = 0
        self.dommage = dommage
        self.portee = portee
        self.rayon_explosion = rayon_explosion
        self.position_x = position_x
        self.position_y = position_y
        self.largeur = largeur_modele
        self.hauteur = hauteur_modele
        self.pew_pew = []
        self.victime = None
        self.creeps_in_range = []

    def surveiller(self):
        self.creeps_in_range = []
        for creep in self.parent.liste_creeps:
            dx = abs(creep.x - self.position_x) ** 2
            dy = abs(creep.y - self.position_y) ** 2
            distance = math.sqrt(dx + dy)
            if distance <= self.portee:
                self.creeps_in_range.append(creep)
        if len(self.creeps_in_range) > 0:
            self.tirer()

    def tirer(self):
        if self.cooldown == 0:
            if self.archetype == "Mitraillette":
               self.victime = self.creeps_in_range[0]
               for creep in self.creeps_in_range:
                   if creep.distance_parcourue > self.victime.distance_parcourue:
                       self.victime = creep
               self.pew_pew.append(Pew_pew(self, "Balle"))
            elif self.archetype == "Lance-Roquette":
                self.victime = self.creeps_in_range[0]
                for creep in self.creeps_in_range:
                    if creep.vie > self.victime.vie:
                        self.victime = creep
                self.pew_pew.append(Pew_pew(self, "Bombe"))
            elif self.archetype == "Shocker":
                for creep in self.creeps_in_range:
                    if creep.baisser_vie(self.dommage):
                        break
            self.cooldown = self.cooldown_max
        else:
            self.cooldown -= 1

    def avancer_projectiles(self):
        for projectile in self.pew_pew:
            rendu = projectile.avancer()
            if rendu:
                del self.pew_pew[self.pew_pew.index(projectile)]

class Pew_pew:
    def __init__(self, parent, archetype):
        self.parent = parent
        self.archetype = archetype
        self.range = 300
        self.vitesse = 15
        self.x = self.parent.position_x
        self.y = self.parent.position_y
        self.destination_x = None
        self.destination_y = None

    def avancer(self):
        cible = self.parent.victime
        rendu = False
        self.range -= self.vitesse
        if cible != None:
            self.destination_x = cible.x
            self.destination_y = cible.y

            if self.x < self.destination_x and abs(self.x-self.destination_x)>self.vitesse:
                self.x = self.x + self.vitesse
            elif self.x > self.destination_x and abs(self.x-self.destination_x)>self.vitesse:
                self.x = self.x - self.vitesse
            elif abs(self.x-self.destination_x)<self.vitesse:
                self.x = self.destination_x

            if self.y < self.destination_y and abs(self.y-self.destination_y)>self.vitesse:
                self.y = self.y + self.vitesse
            elif self.y > self.destination_y and abs(self.y-self.destination_y)>self.vitesse:
                self.y = self.y - self.vitesse
            elif abs(self.y - self.destination_y) < self.vitesse:
                self.y = self.destination_y


            if (self.x == self.destination_x and self.y == self.destination_y):
                cible.baisser_vie(self.parent.dommage)
                rendu = True
            elif self.range ==0:
                rendu = True
            return rendu
        else:
            return True