import math
import helper
from math import sqrt
import random


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 1152
        self.hauteur = 896
        self.partie = None
        self.interface = Interface(self)
        self.carte = Carte(self)
        # pour lire les données de classes et les afficher dans l'interface (prix des tours) :
        self.tour_confiance = Tour_Confiance
        self.tour_relation = Tour_Relation

    def jouer(self):
        if not self.partie.partie_terminee and not self.partie.partie_gagnee:
            creeps_morts = []
            for creep in self.partie.creeps:
                creep.avancer()
                if creep.vie <= 0:
                    self.partie.motivation += creep.butin
                    creeps_morts.append(creep)
            for creep in creeps_morts:
                try:
                    self.partie.creeps.remove(creep)
                except Exception:
                    pass



            for tour in self.partie.tours:
                to_delete = []
                tour.scanner_creeps()
                if isinstance(tour, Tour_Confiance):
                    for missile in tour.missiles:
                        missile.suivre_creep()
                        if missile.cible_atteinte:
                            to_delete.append(missile)
                    for missile in to_delete:
                        tour.missiles.remove(missile)
                if isinstance(tour, Tour_Relation):
                    if tour.laser_actif:
                        tour.laser.suivre_creep()

            self.partie.generer_creep()

    def game_over(self):
        self.partie.partie_terminee = True
        self.parent.fin_partie()

    def demarrer_partie(self):
        self.partie = Partie(self)


class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.sante_mentale = 1000
        self.motivation = 175
        self.antidepresseur = 1
        self.no_vague = 0
        self.vagues = [

            Vague(self, 3),
            Vague(self, 5),
            Vague(self, 10),
            Vague(self, 15),
            Vague(self, 20),
            Vague(self, 30),
            Vague(self, 50),
            Vague(self, 100),
                Vague(self, 3),
                Vague(self, 5),
                Vague(self, 10),
                Vague(self, 15),
                Vague(self, 20),
                Vague(self, 30),
                Vague(self, 50),
                Vague(self, 100),
                Vague(self, 3),
                Vague(self, 5),
                Vague(self, 10),
                Vague(self, 15),
                Vague(self, 20),
                Vague(self, 30),
                Vague(self, 50),
                Vague(self, 100),
                Vague(self, 3),
                Vague(self, 5),
                Vague(self, 10),
                Vague(self, 15),
                Vague(self, 20),
                Vague(self, 30),
                Vague(self, 50),
                Vague(self, 100),
                Vague(self, 150)
                ]
        self.creeps = []
        self.tours = []
        self.cooldown = 0
        self.max_cooldown = 55
        self.creep_acceleration = 0.3
        self.type_tour = ""
        self.activer_placer = False
        self.partie_terminee = False
        self.partie_gagnee = False
        #self.timer = 10
        #self.compteur = 35
        #self.commencer_timer = False
        #self.partie_terminee = False

    def placer_tour(self, type_tour):
        self.type_tour = type_tour
        self.activer_placer = True
        self.commencer_timer = True
        self.timer = 5

    def countdown(self):
        if self.commencer_timer:
            self.compteur -= 1
            if self.compteur == 0:
                self.timer -= 1
                print(self.timer)
                self.compteur = 35
        if self.timer == 0:
            self.commencer_timer = False
            self.compteur = 30
            self.timer = 0

    def creer_tour(self, x, y):
        if self.type_tour == "confiance":
            la_tour = Tour_Confiance(self, x, y)
        elif self.type_tour == "relation":
            la_tour = Tour_Relation(self, x, y)
        if self.motivation >= la_tour.prix:
            self.tours.append(la_tour)
            self.motivation -= la_tour.prix
        else:
            la_tour = None
        return la_tour

    def generer_creep(self):
        if self.no_vague < len(self.vagues):
            if len(self.vagues[self.no_vague].creeps_attente) > 0:
                if self.cooldown == 0:
                    creep = self.vagues[self.no_vague].creeps_attente.pop()
                    creep.vitesse += self.no_vague * self.creep_acceleration + self.no_vague / 10
                    self.creeps.append(creep)
                    self.cooldown = self.max_cooldown
                else:
                    self.cooldown -= 1
            elif len(self.creeps) == 0:
                if self.no_vague + 1 < len(self.vagues):
                    self.no_vague += 1
                    self.max_cooldown -= 5
                else:
                    self.partie_gagnee = True
                    self.parent.game_over()


class Interface:
    def __init__(self, parent):
        self.largeur = 256


class Carte:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur - self.parent.interface.largeur
        self.hauteur = self.parent.hauteur
        self.chemins = [
            Chemin(192, 0, 192, 128),
            Chemin(192, 128, 768, 128),
            Chemin(768, 128, 768, 320),
            Chemin(768, 320, 128, 320),
            Chemin(128, 320, 128, 704),
            Chemin(128, 704, 384, 704),
            Chemin(384, 704, 384, 512),
            Chemin(384, 512, 644, 512),
            Chemin(644, 512, 644, 768),
            Chemin(644, 768, self.largeur, 768)
        ]

class Chemin:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.largeur = 64
        self.bordure = 100


class Tour:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.largeur = 64
        self.demi_taille = self.largeur/2
        self.rayon_detection = 128
        self.zone_occupee = 32
        self.puissance = 6
        self.cooldown = 0
        self.max_cooldown = 50
        prix = 50
        self.prix = prix

    def scanner_creeps(self):
        tx = self.x
        ty = self.y
        tr = self.rayon_detection

        for creep in self.parent.creeps:
            rc = creep.rayon
            distance = sqrt((creep.x-tx) * (creep.x-tx) + (creep.y-ty) * (creep.y-ty))
            somme = tr + rc
            if distance < somme:
                if self.cooldown == 0:
                    self.tirer(creep)
                    self.cooldown = self.max_cooldown
            creep.etat_barre_vie()

        if self.cooldown > 0:
            self.cooldown -= 1

    def tirer(self, creep):
        pass


class Tour_Confiance(Tour):
    prix = 20
    puissance = 10
    max_cooldown = 10
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.prix = Tour_Confiance.prix
        self.puissance = Tour_Confiance.puissance
        self.max_cooldown = Tour_Confiance.max_cooldown
        self.missiles = []

    def tirer(self, creep):
        self.missiles.append(Missile(self, creep))


class Tour_Relation(Tour):
    prix = 50
    puissance = 2
    max_cooldown = 90
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.prix = Tour_Relation.prix
        self.puissance = Tour_Relation.puissance
        self.rayon_detection = 150
        self.max_cooldown = Tour_Relation.max_cooldown
        self.laser = None
        self.laser_actif = False

    def scanner_creeps(self):
        tx = self.x
        ty = self.y
        tr = self.rayon_detection

        for creep in self.parent.creeps:
            rc = creep.rayon
            distance = sqrt((creep.x-tx) * (creep.x-tx) + (creep.y-ty) * (creep.y-ty))
            somme = tr + rc
            if distance < somme:
                if self.cooldown == 0:
                    self.tirer(creep)
            creep.etat_barre_vie()

        if self.cooldown > 0:
            self.cooldown -= 1

    def tirer(self, creep):
        if not self.laser_actif and self.cooldown == 0:
            self.laser_actif = True
            self.laser = Laser(self, creep)
        if self.laser_actif:
            if self.laser.duree <= 0:
                self.laser = None
                self.laser_actif = False
                self.cooldown = self.max_cooldown


class Projectile:
    def __init__(self, parent, creep):
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.largeur = 16
        self.demitaille = self.largeur/2
        self.creep = creep
        self.puissance = self.parent.puissance


class Missile(Projectile):
    def __init__(self, parent, creep):
        super().__init__(parent, creep)
        self.largeur = 10
        self.cible_atteinte = False
        self.vitesse = 10
        self.suivre_creep()

    def suivre_creep(self):
        distance = helper.Helper.calcDistance(self.x, self.y, self.creep.x, self.creep.y)
        angle = helper.Helper.calcAngle(self.x, self.y, self.creep.x, self.creep.y)
        point_cible = helper.Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        self.x, self.y = point_cible
        if distance < 5:
            self.cible_atteinte = True

        if self.cible_atteinte:
            if self.creep.vie > 0:
                self.creep.vie -= self.puissance
            else:
                self.creep.vie = 0


class Laser(Projectile):
    def __init__(self, parent, creep):
        super().__init__(parent, creep)
        self.largeur = 8
        self.creep = creep
        self.parent = parent
        self.puissance = self.parent.puissance
        self.cible_x = self.creep.x
        self.cible_y = self.creep.y
        self.duree_max = 30
        self.duree = self.duree_max
        self.suivre_creep()

    def suivre_creep(self):
        self.duree -= 1
        self.cible_x = self.creep.x
        self.cible_y = self.creep.y
        if self.creep.vie > 0:
            self.creep.vie -= self.puissance
        else:
            self.creep.vie = 0

        if self.duree == 0 or self.creep.vie == 0 or self.creep.echappe:
            self.parent.laser_actif = False
            self.parent.cooldown = self.parent.max_cooldown


class Vague:
    def __init__(self, parent, nbr_creeps):
        self.parent = parent
        self.nbr_creeps = nbr_creeps
        self.creeps_attente = []
        self.creer_creeps()

    def creer_creeps(self):
        i = 0
        while i < self.nbr_creeps:
            self.creeps_attente.append(Creep(self, self.parent.parent.carte.chemins[0].x1, self.parent.parent.carte.chemins[0].y1))
            i += 1
        random.shuffle(self.creeps_attente)


class Creep:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.buffer_pos = 20 # Pour éviter que le sprite marche sur le bord du chemin
        self.cible_x = self.parent.parent.parent.carte.chemins[0].x2
        self.cible_y = self.parent.parent.parent.carte.chemins[1].y2 - self.buffer_pos
        self.angle = helper.Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
        self.rayon = 18
        self.vitesse = 2.4
        self.no_troncon = 0
        self.vie = 100
        self.degat = 10
        self.butin = 25
        self.barre_vie = Barre_Vie(self)
        self.echappe = False
        self.typeimage = "creep_droite"
        self.noimage = 0

    def avancer(self):

        if not self.echappe:
            self.x, self.y = helper.Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
            self.noimage += 1

            distance = helper.Helper.calcDistance(self.x, self.y, self.cible_x, self.cible_y)
            if distance < self.vitesse:
                self.no_troncon += 1
                if self.no_troncon < len(self.parent.parent.parent.carte.chemins):
                    self.cible_x = self.parent.parent.parent.carte.chemins[self.no_troncon].x2
                    self.cible_y = self.parent.parent.parent.carte.chemins[self.no_troncon].y2 - self.buffer_pos
                    self.angle = helper.Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
                else:
                    self.echappe = True
                    self.parent.parent.sante_mentale -= self.degat
                    self.parent.parent.creeps.remove(self)
                    if self.parent.parent.sante_mentale <= 0:
                        self.parent.parent.parent.game_over()

            if self.x >= self.cible_x:
                self.typeimage = "creep_gauche"
            elif self.x <= self.cible_x:
                self.typeimage = "creep_droite"

            if self.noimage == len(self.parent.parent.parent.parent.vue.sprites[self.typeimage]):
                self.noimage = 0


    def etat_barre_vie(self):
        self.barre_vie.largeur = self.vie * 60 / 100


class Barre_Vie:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 60
        self.hauteur = 3


