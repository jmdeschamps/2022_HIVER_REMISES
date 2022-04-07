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
        self.liste_score = []
        self.tour_confiance = Tour_Confiance
        self.tour_relation = Tour_Relation

    def jouer(self):
        if not self.partie.partie_terminee and not self.partie.partie_gagnee:
            creeps_morts = []
            for creep in self.partie.creeps:
                creep.avancer()
                if creep.vie <= 0:
                    self.partie.score += creep.butin
                    if random.randint(1, 22) == 1:
                        self.partie.antidepresseur += 1
                        self.partie.valeur_texte.append(Valeur_Texte(creep, "antidepresseur", "+1 ANTI-DÉPRESSEUR"))
                    else:
                        self.partie.valeur_texte.append(Valeur_Texte(creep, "butin", creep.butin))
                        self.partie.motivation += creep.butin

                    creeps_morts.append(creep)
            for creep in creeps_morts:
                try:
                    self.partie.creeps.remove(creep)
                except Exception:
                    pass

            for tour in self.partie.tours:
                to_delete = []
                tour.tick()
                tour.scanner_creeps()
                if isinstance(tour, Tour_Confiance):
                    for missile in tour.missiles:
                        missile.suivre_creep()
                        if missile.cible_atteinte:
                            to_delete.append(missile)
                    for missile in to_delete:
                        tour.missiles.remove(missile)
                elif isinstance(tour, Tour_Relation):
                    if tour.laser_actif:
                        tour.laser.suivre_creep()
                elif isinstance(tour, Tour_Sommeil):
                    tour.explosion()

            for valeur in self.partie.valeur_texte:
                to_delete = []
                valeur.tick()
                if valeur.supprimer:
                    to_delete.append(valeur)
                for valeur in to_delete:
                    self.partie.valeur_texte.remove(valeur)

            if self.partie.annonce:
                self.partie.annonce.tick()
                if self.partie.annonce.supprimer:
                    self.partie.annonce = None

            self.partie.generer_creep()

            if self.partie.ap_en_cours:
                if self.partie.cooldown_antidepresseur >= 0:
                    self.partie.cooldown_antidepresseur -= 1
                    if self.partie.cooldown_antidepresseur == 0:
                        self.partie.ap_en_cours = False
                elif self.partie.cooldown_antidepresseur < 0:
                    self.partie.cooldown_antidepresseur = self.partie.cooldown_antidepresseur_max

    def game_over(self):
        self.partie.partie_terminee = True
        self.parent.fin_partie()

    def demarrer_partie(self):
        Tour_Confiance.demarrer_partie()
        Tour_Sommeil.demarrer_partie()
        Tour_Relation.demarrer_partie()
        self.partie = Partie(self)



class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.score = 0
        self.sante_mentale = 1000
        self.motivation = 1750
        self.antidepresseur = 1
        self.antidepresseur_effet = 0.5
        self.cooldown_antidepresseur = 0
        self.cooldown_antidepresseur_max = 10
        self.ap_en_cours = False
        self.no_vague = 0
        self.vagues = [
            Vague(self, 3, 0, 0),
            Vague(self, 6, 0, 0),
            Vague(self, 8, 2, 0),
            Vague(self, 12, 5, 0),
            Vague(self, 16, 6, 1),
            Vague(self, 30, 8, 3),
            Vague(self, 50, 12, 7),
            Vague(self, 80, 30, 15),
            Vague(self, 3, 0, 0),
            Vague(self, 6, 0, 0),
            Vague(self, 8, 2, 0),
            Vague(self, 12, 5, 0),
            Vague(self, 16, 6, 1),
            Vague(self, 30, 8, 3),
            Vague(self, 50, 12, 7),
            Vague(self, 80, 30, 15),
            Vague(self, 3, 0, 0),
            Vague(self, 6, 0, 0),
            Vague(self, 8, 2, 0),
            Vague(self, 12, 5, 0),
            Vague(self, 16, 6, 1),
            Vague(self, 30, 8, 3),
            Vague(self, 50, 12, 7),
            Vague(self, 80, 30, 15),
            Vague(self, 3, 0, 0),
            Vague(self, 6, 0, 0),
            Vague(self, 8, 2, 0),
            Vague(self, 12, 5, 0),
            Vague(self, 16, 6, 1),
            Vague(self, 30, 8, 3),
            Vague(self, 50, 12, 7),
            Vague(self, 80, 30, 15),
            Vague(self, 150, 50, 35, True)
        ]
        self.creeps = []
        self.tours = []
        self.cooldown = 0
        self.max_cooldown = 55
        self.creep_acceleration = 0.3
        self.creep_vie_supp = 5
        self.type_tour = ""
        self.partie_terminee = False
        self.partie_gagnee = False
        self.annonce = Annonce(self, "VAGUE 1", "principale")
        self.valeur_texte = []


    def faire_acheter(self, type_tour):
        self.type_tour = type_tour
        if self.type_tour == "confiance":
            if self.motivation >= Tour_Confiance.prix:
                return True
        elif self.type_tour == "relation":
            if self.motivation >= Tour_Relation.prix:
                return True
        elif self.type_tour == "sommeil":
            if self.motivation >= Tour_Sommeil.prix:
                return True
        else:
            return False

    def faire_upgrade_tour(self, type_tour):
        self.type_tour = type_tour
        nbrTours = self.counterTypeTour()
        if self.type_tour == "confiance" and nbrTours["confiance"] > 0:
                if self.motivation >= Tour_Confiance.prix_upgrade:
                    self.motivation -= Tour_Confiance.prix_upgrade
                    Tour_Confiance.niveau += 1
                    Tour_Confiance.puissance += 1
                    Tour_Confiance.max_cooldown -= 1
                    for tour in self.tours:
                        if isinstance(tour, Tour_Confiance):
                            tour.niveau = Tour_Confiance.niveau
                            tour.max_cooldown = Tour_Confiance.max_cooldown
                            tour.puissance = Tour_Confiance.puissance
                            self.valeur_texte.append(Valeur_Texte(tour, "upgrade", "Niveau " + str(tour.niveau)))
                else:
                    self.annoncePasMotivation()
        elif self.type_tour == "relation" and nbrTours["relation"] > 0:
            if self.motivation >= Tour_Relation.prix_upgrade:
                self.motivation -= Tour_Relation.prix_upgrade
                Tour_Relation.niveau += 1
                Laser.duree_max += 2
                for tour in self.tours:
                    if isinstance(tour, Tour_Relation):
                        tour.niveau = Tour_Relation.niveau
                        if tour.laser is not None:
                            tour.laser.duree_max = Laser.duree_max
                        self.valeur_texte.append(Valeur_Texte(tour, "upgrade", "Niveau " + str(tour.niveau)))
            else:
                self.annoncePasMotivation()
        elif self.type_tour == "sommeil" and nbrTours["sommeil"] > 0:
            if self.motivation >= Tour_Sommeil.prix_upgrade:
                self.motivation -= Tour_Sommeil.prix_upgrade
                Tour_Sommeil.niveau += 1
                Tour_Sommeil.rayon += 5
                Tour_Sommeil.max_cooldown -= 1
                for tour in self.tours:
                    if isinstance(tour, Tour_Sommeil):
                        tour.niveau = Tour_Sommeil.niveau
                        tour.rayon_detection_max = Tour_Sommeil.rayon
                        tour.max_cooldown = Tour_Sommeil.max_cooldown
                        self.valeur_texte.append(Valeur_Texte(tour, "upgrade", "Niveau " + str(tour.niveau)))
            else:
                self.annoncePasMotivation()
        else:
            self.nouvelle_annonce("Aucune tour de ce type", "secondaire")

    def annoncePasMotivation(self):
        self.nouvelle_annonce("Pas assez de motivation", "secondaire")

    def typeTour(self, tour):
        if isinstance(tour, Tour_Relation):
            return "relation"
        if isinstance(tour, Tour_Sommeil):
            return "sommeil"
        # par default, c'est confiance
        return "confiance"

    def counterTypeTour(self):
        nbrtours = {
            "confiance": 0,
            "relation": 0,
            "sommeil": 0,
        }

        for tour in self.tours:
            nbrtours[self.typeTour(tour)] +=1

        return nbrtours

    def creer_tour(self, x, y, type_tour):
        self.type_tour = type_tour
        if self.type_tour == "confiance":
            la_tour = Tour_Confiance(self, x, y)
        elif self.type_tour == "relation":
            la_tour = Tour_Relation(self, x, y)
        elif self.type_tour == "sommeil":
            la_tour = Tour_Sommeil(self, x, y)
        if self.motivation >= la_tour.prix:
            self.tours.append(la_tour)
            self.motivation -= la_tour.prix
            vue = self.parent.parent.vue
            self.valeur_texte.append(
                Valeur_Texte_Interface(la_tour, "motivation", "-" + str(la_tour.prix), vue.centre_interface,
                                       vue.motivation_y))
        else:
            la_tour = None
        return la_tour

    def generer_creep(self):
        if self.no_vague < len(self.vagues):
            if len(self.vagues[self.no_vague].creeps_attente) > 0:
                if self.cooldown == 0:
                    creep = self.vagues[self.no_vague].creeps_attente.pop()
                    creep.vitesse += self.no_vague * self.creep_acceleration + self.no_vague / 10
                    creep.vie_initial += (self.no_vague * self.creep_vie_supp) + self.creep_vie_supp
                    creep.vie = creep.vie_initial
                    self.creeps.append(creep)
                    if isinstance(creep, Boss):
                        self.nouvelle_annonce("BOSS !", "principale")
                    self.cooldown = self.max_cooldown
                else:
                    self.cooldown -= 1
            elif len(self.creeps) == 0:
                if self.no_vague + 1 < len(self.vagues):
                    self.no_vague += 1
                    self.nouvelle_annonce("VAGUE " + str(self.no_vague + 1), "principale")
                    self.max_cooldown -= 5
                else:
                    self.partie_gagnee = True
                    self.parent.game_over()

    def utiliser_antidepresseur(self):
        if self.ap_en_cours == False:
            if self.antidepresseur - 1 >= 0:
                self.antidepresseur -= 1
                self.nouvelle_annonce("Anti-Dépresseur", "principale")
                for creep in self.creeps:
                    creep.vitesse -= self.antidepresseur_effet
                    if creep.vitesse < 0:
                        creep.vitesse = 0.1
                self.ap_en_cours = True

    def pause(self):
        self.partie_terminee = not self.partie_terminee

    def nouvelle_annonce(self, message, type):
        self.annonce = Annonce(self, message, type)



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
        self.bordure = 88


class Tour:
    prix = 50

    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.flotte_vitesse = 0.65
        self.flotte_amplitude = 3
        self.min_y = self.y - self.flotte_amplitude
        self.max_y = self.y + self.flotte_amplitude
        self.largeur = 40
        self.demi_taille = self.largeur / 2
        self.rayon_detection = 128
        self.zone_occupee = 32
        self.puissance = 6
        self.cooldown = 0
        self.max_cooldown = 50
        self.prix = Tour.prix

    def scanner_creeps(self):
        tx = self.x
        ty = self.y
        tr = self.rayon_detection

        for creep in self.parent.creeps:
            rc = creep.rayon
            distance = sqrt((creep.x - tx) * (creep.x - tx) + (creep.y - ty) * (creep.y - ty))
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

    def tick(self):
        if self.y >= self.max_y or self.y <= self.min_y:
            self.flotte_vitesse = -self.flotte_vitesse
        self.y += self.flotte_vitesse


class Tour_Confiance(Tour):

    def demarrer_partie():
        Tour_Confiance.niveau = 1
        Tour_Confiance.prix = 5
        Tour_Confiance.prix_upgrade = 25
        Tour_Confiance.puissance = 10
        Tour_Confiance.max_cooldown = 10

    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.niveau = Tour_Confiance.niveau
        self.prix = Tour_Confiance.prix
        self.puissance = Tour_Confiance.puissance
        self.max_cooldown = Tour_Confiance.max_cooldown
        self.missiles = []

    def tirer(self, creep):
        self.missiles.append(Missile(self, creep))


class Tour_Relation(Tour):

    def demarrer_partie():
        Tour_Relation.niveau = 1
        Tour_Relation.prix = 12
        Tour_Relation.prix_upgrade = 32
        Tour_Relation.puissance = 1
        Tour_Relation.max_cooldown = 10


    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.buffer_y = 30
        self.prix = Tour_Relation.prix
        self.puissance = Tour_Relation.puissance
        self.rayon_detection = 150
        self.max_cooldown = Tour_Relation.max_cooldown
        self.laser = None
        self.laser_actif = False
        self.niveau = Tour_Relation.niveau

    def scanner_creeps(self):
        tx = self.x
        ty = self.y
        tr = self.rayon_detection

        for creep in self.parent.creeps:
            rc = creep.rayon
            distance = sqrt((creep.x - tx) * (creep.x - tx) + (creep.y - ty) * (creep.y - ty))
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


class Tour_Sommeil(Tour):

    def demarrer_partie():
        Tour_Sommeil.niveau = 1
        Tour_Sommeil.prix = 12
        Tour_Sommeil.prix_upgrade = 25
        Tour_Sommeil.puissance = 1
        Tour_Sommeil.max_cooldown = 12
        Tour_Sommeil.rayon = 125

    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.buffer_x = 5
        self.buffer_y = 33
        self.prix = Tour_Sommeil.prix
        self.puissance = Tour_Sommeil.puissance
        self.max_cooldown = Tour_Sommeil.max_cooldown
        self.cooldown = self.max_cooldown
        self.max_duree = 60
        self.duree = 0
        self.rayon_detection = 0
        self.rayon_detection_max = Tour_Sommeil.rayon
        self.incrementation = 10
        self.zones = []
        self.bordure = 0
        self.niveau = Tour_Sommeil.niveau

    def explosion(self):
        tx = self.x + self.buffer_x
        ty = self.y - self.buffer_y
        tr = self.rayon_detection

        for creep in self.parent.creeps:
            rc = creep.rayon
            distance = sqrt((creep.x - tx) * (creep.x - tx) + (creep.y - ty) * (creep.y - ty))
            somme = tr + rc
            if distance < somme:
                creep.vie -= self.puissance
            creep.etat_barre_vie()

        if self.duree > 0:
            if self.rayon_detection >= self.rayon_detection_max:
                self.rayon_detection = self.rayon_detection_max
                self.rayon_detection -= self.incrementation
                self.cooldown = self.max_cooldown
            self.rayon_detection += self.incrementation
            self.duree -= 1
        else:
            self.rayon_detection -= self.incrementation
            if self.rayon_detection <= 0:
                self.rayon_detection = 0

        if self.cooldown > 0:
            self.cooldown -= 1

        elif self.cooldown <= 0:
            self.duree = self.max_duree

        self.bordure += 0.1
        if self.bordure >= 5:
            self.bordure -= 1

    def scanner_creeps(self):
        pass


class Projectile:
    def __init__(self, parent, creep):
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.largeur = 16
        self.demitaille = self.largeur / 2
        self.creep = creep
        self.puissance = self.parent.puissance


class Missile(Projectile):
    def __init__(self, parent, creep):
        super().__init__(parent, creep)
        self.x = self.parent.x
        self.buffer_y = 24
        self.y = self.parent.y - self.buffer_y
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
    duree_max = 35

    def __init__(self, parent, creep):
        super().__init__(parent, creep)
        self.largeur = 8
        self.creep = creep
        self.parent = parent
        self.puissance = self.parent.puissance
        self.cible_x = self.creep.x
        self.cible_y = self.creep.y
        self.duree_max = Laser.duree_max
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
    def __init__(self, parent, nbr_creeps_depression, nbr_creeps_anxiete, nbr_creeps_insomnie, boss=None):
        self.parent = parent
        self.boss = boss
        self.nbr_creeps_depression = nbr_creeps_depression
        self.nbr_creeps_anxiete = nbr_creeps_anxiete
        self.nbr_creeps_insomnie = nbr_creeps_insomnie
        self.nbr_creeps = (self.nbr_creeps_insomnie + self.nbr_creeps_anxiete + self.nbr_creeps_depression)
        if self.boss:
            self.nbr_creeps += 1
        self.creeps_attente = []
        self.creer_creeps()

    def creer_creeps(self):
        i = 0
        j = 0
        k = 0
        while i < self.nbr_creeps_depression:
            self.creeps_attente.append(
                Creep_Drepression(self, self.parent.parent.carte.chemins[0].x1, self.parent.parent.carte.chemins[0].y1))
            i += 1
        while j < self.nbr_creeps_anxiete:
            self.creeps_attente.append(
                Creep_Anxiete(self, self.parent.parent.carte.chemins[0].x1, self.parent.parent.carte.chemins[0].y1))
            j += 1

        while k < self.nbr_creeps_insomnie:
            self.creeps_attente.append(
                Creep_Insomnie(self, self.parent.parent.carte.chemins[0].x1, self.parent.parent.carte.chemins[0].y1))
            k += 1
        if self.boss:
            self.creeps_attente.append(
                Boss(self, self.parent.parent.carte.chemins[0].x1, self.parent.parent.carte.chemins[0].y1))

        random.shuffle(self.creeps_attente)


class Creep:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.demitaille = 32
        self.buffer_pos = 20  # Pour éviter que le sprite marche sur le bord du chemin
        self.cible_x = self.parent.parent.parent.carte.chemins[0].x2
        self.cible_y = self.parent.parent.parent.carte.chemins[1].y2 - self.buffer_pos
        self.angle = helper.Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
        self.rayon = 18
        self.vitesse = None
        self.no_troncon = 0
        self.vie_initial = None
        self.vie = None
        self.degat = 10
        self.barre_vie = Barre_Vie(self)
        self.echappe = False
        self.typeimage = None
        self.type_image_droite = None
        self.type_image_gauche = None
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
                    vue = self.parent.parent.parent.parent.vue
                    self.parent.parent.valeur_texte.append(
                        Valeur_Texte_Interface(self, "degat", "-" + str(self.degat), vue.centre_interface,
                                               vue.sante_mentale_y))
                    self.parent.parent.sante_mentale -= self.degat
                    self.parent.parent.creeps.remove(self)
                    if self.parent.parent.sante_mentale <= 0:
                        self.parent.parent.parent.game_over()

            if self.x >= self.cible_x:
                self.typeimage = self.type_image_gauche
            elif self.x <= self.cible_x:
                self.typeimage = self.type_image_droite

            if self.noimage == len(self.parent.parent.parent.parent.vue.sprites[self.typeimage]):
                self.noimage = 0

    def etat_barre_vie(self):
        self.barre_vie.largeur = self.vie * 60 / self.vie_initial
        if self.barre_vie.largeur <0:
            self.barre_vie.largeur =0

class Creep_Drepression(Creep):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.vitesse = 2.0
        self.vie_initial = 95
        self.type_image_droite = "creep_depression_droite"
        self.type_image_gauche = "creep_depression_gauche"
        self.typeimage = self.type_image_gauche
        self.vie = self.vie_initial
        self.butin = 25


class Creep_Anxiete(Creep):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.vitesse = 2.6
        self.vie_initial = 55
        self.vie = self.vie_initial
        self.type_image_droite = "creep_anxiete_droite"
        self.type_image_gauche = "creep_anxiete_gauche"
        self.typeimage = self.type_image_gauche
        self.butin = 20


class Creep_Insomnie(Creep):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.vitesse = 1.0
        self.vie_initial = 150
        self.vie = self.vie_initial
        self.type_image_droite = "creep_insomnie_droite"
        self.type_image_gauche = "creep_insomnie_gauche"
        self.typeimage = self.type_image_gauche
        # variables qui seront pertinentes
        self.cooldown = 0
        self.max_cooldown = 80
        self.penalite_cooldown = 1
        self.rayon_detection = 90
        self.butin = 30

    def avancer(self):
        super().avancer()
        self.scanner_tour()

    def scanner_tour(self):
        cx = self.x
        cy = self.y
        cr = self.rayon_detection

        for tour in self.parent.parent.tours:
            tr = tour.largeur / 2  # rayon
            distance = sqrt((cx - tour.x) * (cx - tour.x) + (cy - tour.y) * (cy - tour.y))
            somme = tr + cr
            if distance < somme:
                if self.cooldown == 0:
                    self.parent.parent.valeur_texte.append(Valeur_Texte(tour, "ralentie", "RALENTIE"))
                    tour.cooldown += 5
                    self.cooldown = self.max_cooldown

            if self.cooldown > 0:
                self.cooldown -= 1


class Boss(Creep):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.vitesse = -1
        self.vie_initial = 2000
        self.type_image_droite = "boss_droite"
        self.type_image_gauche = "boss_gauche"
        self.typeimage = self.type_image_gauche
        self.vie = self.vie_initial
        self.cooldown = 0
        self.max_cooldown = 15

    def avancer(self):
        super().avancer()
        if self.cooldown == 0:
            self.parent.parent.sante_mentale -= 1
            vue = self.parent.parent.parent.parent.vue
            self.parent.parent.valeur_texte.append(
                Valeur_Texte_Interface(self, "degat", "-1", vue.centre_interface, vue.sante_mentale_y))
            self.cooldown = self.max_cooldown
        else:
            self.cooldown -= 1
        if self.parent.parent.sante_mentale == 0:
            self.parent.parent.parent.game_over()


class Barre_Vie:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 60
        self.hauteur = 3


class Annonce:
    def __init__(self, parent, message, type):

        self.type = type
        self.parent = parent
        self.vitesse = 32
        self.message = message
        self.pause = False
        self.supprimer = False

        if self.type == "principale":
            self.x = -32
            self.y = self.parent.parent.hauteur / 2 - 100
            self.cooldown = 20

        else:
            self.x = 512
            self.y = self.parent.parent.hauteur / 2 - 275
            self.cooldown = 40

    def tick(self):
        if self.type == "principale":
            if not self.pause:
                self.x += self.vitesse
                if self.x - self.vitesse == 480:
                    self.pause = True
            else:
                self.cooldown -= 1
                if self.cooldown == 0:
                    self.pause = False
            if self.x > 1000:
                self.supprimer = True
        elif self.type == "secondaire":
            self.cooldown -= 1
            if self.cooldown == 0:
                self.supprimer = True


class Valeur_Texte:
    def __init__(self, parent, type, val):
        self.parent = parent
        self.x = parent.x
        self.y = parent.y
        self.vitesse = 2.5
        self.duree = 18
        self.val = val
        self.type = type  # types possibles : butin, antidepresseur, ralenti
        self.supprimer = False

    def tick(self):
        self.duree -= 1
        if self.duree > 0:
            self.y -= self.vitesse
        else:
            self.supprimer = True


class Valeur_Texte_Interface(Valeur_Texte):
    def __init__(self, parent, type, val, x, y):
        super().__init__(parent, type, val)
        self.x = x
        self.y = y
        self.type = type  # types possibles : degat, motivation
