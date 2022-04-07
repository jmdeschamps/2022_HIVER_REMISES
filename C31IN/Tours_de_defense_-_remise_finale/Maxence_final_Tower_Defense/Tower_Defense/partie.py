import time

from projectileGlace import ProjectileGlace
from sentier1 import Sentier1
from tour import Tour
from tourFeu import TourFeu
from tourPoison import TourPoison
from tourGlace import TourGlace
from tourMitraille import TourMitraille
from projectileMitraille import ProjectileMitraille
from creep import Creep, Creep1, Creep2, Creep3, Creep4, Boss
import random
import math

class Partie:
    def __init__(self, parent):
        self.parent = parent
        self.largeur_fenetre = self.parent.largeur_fenetre
        self.hauteur_fenetre = self.parent.hauteur_fenetre
        self.largeur_zone = self.parent.largeur_canevas
        self.hauteur_zone = self.parent.hauteur_canevas
        self.sentier = Sentier1()
        self.creeps = []
        self.vie = self.parent.vie
        self.score = self.parent.score
        self.argent = parent.argent
        self.message = self.parent.message
        self.ennemi_vague = [8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80]
        self.vague = 0 # survivre 19 vagues
        self.vague_penalite = 0
        # nombre de creeps dans la vague
        self.nbr_creeps_vague = self.ennemi_vague[0]
        # compteur pour le nombre de creeps créés dans la vague depuis le début
        self.nbr_creeps_ajoutes = 0
        # boolean qui vérifie l'interval entre la création des creeps
        self.peut_ajouter_creep = True
        # boolean qui vérifie pour l'activation des creeps
        self.peut_activer_creep = True
        # Nombres de creeps par type
        self.nbr_creeps_un = 8
        self.nbr_creeps_un = 10
        self.nbr_creeps_deux = 0
        self.nbr_creeps_trois = 0
        self.nbr_creeps_quatre = 0
        # Liste d'animations des creeps
        self.animations = []
        # Création des creeps pour le niveau
        self.creer_creeps()
        # Index des creeps utilisé pour démarrer le déplacement d'un creep selon un interval de 1sec
        self.index_creep = 0
        self.tours_feu = []
        self.tours_poison = []
        self.tours_glace = []
        self.tours_mitraille = []
        self.plages_x_y_interdites = []
        self.aires_occupees_par_tours = []
        self.tours_cout = self.parent.tours_cout

    def creer_creeps(self):
        # Création aléatoire des creeps selon le nombre de creeps dans la vague et selon le nombre par type
        while self.nbr_creeps_ajoutes < self.nbr_creeps_vague:
            est_valide = False
            numero = 0
            if self.vague == len(self.ennemi_vague) - 1 and self.nbr_creeps_ajoutes == self.nbr_creeps_vague - 1: # dernière vague ET dernier élément?
                self.creeps.append(Boss(self.sentier.depart_x, self.sentier.depart_y, self.sentier.chemin))
            else:
                while not est_valide:
                    numero = random.randint(0, 4)
                    if numero == 0 or numero == 1:
                        if self.nbr_creeps_un > 0:
                            est_valide = True
                    elif numero == 2:
                        if self.nbr_creeps_deux > 0:
                            est_valide = True
                    elif numero == 3:
                        if self.nbr_creeps_trois > 0:
                            est_valide = True
                    elif numero == 4:
                        if self.nbr_creeps_quatre > 0:
                            est_valide = True
                if numero == 0 or numero == 1:
                    self.creeps.append(Creep1(self.sentier.depart_x, self.sentier.depart_y, self.sentier.chemin))
                    self.nbr_creeps_un -= 1
                elif numero == 2:
                    self.creeps.append(Creep2(self.sentier.depart_x, self.sentier.depart_y, self.sentier.chemin))
                    self.nbr_creeps_deux -= 1
                elif numero == 3:
                    self.nbr_creeps_trois -= 1
                    self.creeps.append(Creep3(self.sentier.depart_x, self.sentier.depart_y, self.sentier.chemin))
                elif numero == 4:
                    self.creeps.append(Creep4(self.sentier.depart_x, self.sentier.depart_y, self.sentier.chemin))
                    self.nbr_creeps_quatre -= 1
            self.nbr_creeps_ajoutes += 1
        self.peut_ajouter_creep = False
        multiple = 1
        if self.vague > 8:
            multiple = 1.75
        elif self.vague > 10:
            multiple = 2.5
        elif self.vague > 12:
            multiple = 3
        elif self.vague > 15:
            multiple = 4
        elif multiple > 18:
            multiple = 5
        for i in self.creeps:
            if not isinstance(i, Boss):
                i.points_vie *= multiple
                i.max_points_vie *= multiple

    def activer_creep(self):
        # Lorsqu'on élimine un creep, la liste redéfini son index donc on a un espace de moins dans le tableau de creep
        if self.index_creep < len(self.creeps):
            self.creeps[self.index_creep].activer()
            self.index_creep += 1

    def deplacer_creeps(self):
        for i in self.creeps:
            i.deplacer()

    def animer_creeps(self):
        for i in self.creeps:
            i.changer_image()

    def verifier_attaque_forteresse(self):
        for i in self.creeps:
            if i.stade_chemin == len(i.chemin) - 1:
                attaque, creep = i.verifier_attaque_forteresse()
                if attaque:
                    self.attaquer_forteresse(creep)

    # Lorsqu'un creep franchit le sentier, diminue les points de vie du joueur et supprime le creep #
    def attaquer_forteresse(self, creep):

        self.vie -= creep.degats
        if self.vie > 0:
            self.message = str(self.vie)
        else:
            self.message = "0"
        self.parent.update_vie(self.message)
        self.creeps.remove(creep)
        self.index_creep -= 1
        self.vague_penalite += 1
        self.nbr_creeps_ajoutes -= 1
        if self.vie <= 0:
            self.parent.game_over()
            

    def fin_vague(self):
        self.parent.en_cours = False
        print(self.parent.en_cours)
        self.nbr_creeps_ajoutes = 0
        self.peut_ajouter_creep = True
        self.index_creep = 0
        bonus = self.ennemi_vague[self.vague] -self.vague_penalite

        self.argent += bonus *5
        self.parent.update_argent()
        self.vague_penalite = 0
        if (self.vague <= 19 ):
            self.vague += 1
            self.message = "Prochaine vague : " + str(self.vague+1) + "\n nombre de creep : " + str(self.ennemi_vague[self.vague]) + " \n Vie : " + str(self.vie) + "\n XP avant le prochain niveau : " + str(self.parent.niveau_joueur[self.parent.calculer_niveau_joueur()] - self.parent.exp)
        else: 
            self.parent.partie_gagnee()
            self.message = "Fin de partie"

        self.parent.update_commencer("Commencer")
        self.parent.update_message(self.message)

        # initialiser le nombre de creeps voulu
        # À peaufiner selon la vague

        self.nbr_creeps_vague = self.ennemi_vague[self.vague]
        if self.ennemi_vague[self.vague] < 10:
            self.nbr_creeps_un = 0
            self.nbr_creeps_deux = 0
            self.nbr_creeps_trois = math.floor(self.nbr_creeps_vague/4)
            self.nbr_creeps_quatre = 0
        elif  10 < self.ennemi_vague[self.vague] <= 20:
            self.nbr_creeps_un = math.floor(self.ennemi_vague[self.vague] *0.75)
            self.nbr_creeps_deux = math.floor(self.ennemi_vague[self.vague] *0.25)
        elif 20 < self.ennemi_vague[self.vague] <= 40 :
            self.nbr_creeps_un = 4
            self.nbr_creeps_deux = math.floor((self.ennemi_vague[self.vague]-4) * 0.75)
            self.nbr_creeps_trois = math.floor((self.ennemi_vague[self.vague]-4) * 0.25)
        elif 40 < self.ennemi_vague[self.vague] <= 64:
            self.nbr_creeps_un = math.floor(self.nbr_creeps_deux * 0.50)
            self.nbr_creeps_deux = math.floor((self.ennemi_vague[self.vague]-4) * 0.50)
            self.nbr_creeps_trois = math.floor(self.nbr_creeps_deux * 0.50)
            self.nbr_creeps_quatre = math.floor(self.nbr_creeps_deux * 0.50)
            self.nbr_creeps_quatre += self.ennemi_vague[self.vague] - \
                                  (self.nbr_creeps_un + self.nbr_creeps_deux + self.nbr_creeps_trois + self.nbr_creeps_quatre)
        elif 64 < self.ennemi_vague[self.vague]:
            self.nbr_creeps_un = math.floor( self.nbr_creeps_trois * 0.25)
            self.nbr_creeps_deux = math.floor( self.nbr_creeps_trois * 0.25)
            self.nbr_creeps_trois = math.floor((self.ennemi_vague[self.vague] - 4) * 0.50)
            self.nbr_creeps_quatre = math.floor((self.ennemi_vague[self.vague] - 4) * 0.25)
            self.nbr_creeps_quatre += self.ennemi_vague[self.vague] - \
                                  (self.nbr_creeps_un + self.nbr_creeps_deux + self.nbr_creeps_trois + self.nbr_creeps_quatre)

        if self.vie <= 0:
            self.game_over()

    def game_over(self):
        self.message = "Vous avez perdu \n :("
        self.parent.update_message(self.message)

    def calculer_experience(self, creep):
        if isinstance(creep, Creep1):
            self.parent.exp += 2
        elif isinstance(creep, Creep2):
            self.parent.exp += 4
        elif isinstance(creep, Creep3):
            self.parent.exp += 8
        elif isinstance(creep, Creep4):
            self.parent.exp += 16
        elif isinstance(creep, Boss):
            self.parent.exp += 256
        self.parent.update_exp()

    def calculer_argent(self, creep):
        # Maxence
        if isinstance(creep, Creep1):
            self.argent += 1
        elif isinstance(creep, Creep2):
            self.argent += 4
        elif isinstance(creep, Creep3):
            self.argent += 8
        elif isinstance(creep, Creep4):
            self.argent += 11
        elif isinstance(creep, Boss):
            self.argent += 150
        self.parent.update_argent()

    def retirer_argent(self, type):
        # Maxence
        if type == "FEU":
            if self.argent >= self.tours_cout[type]:
                self.argent -= self.tours_cout[type] #TourFeu.prix
                self.parent.update_argent()
                return True
            else :
                self.parent.update_message("Pas assez d'argent \n Besoin de 180 pieces d'or")
                return False
        elif type == "GLACE":
            if self.argent >= self.tours_cout[type]:
                self.argent -= self.tours_cout[type]  # TourGlace.prix
                self.parent.update_argent()
                return True
            self.parent.update_message("Pas assez d'argent \n Besoin de 220 pieces d'or")
            return False
        elif type == "POISON":
            if self.argent >= self.tours_cout[type]:
                self.argent -= self.tours_cout[type]  # TourPoison.prix
                self.parent.update_argent()
                return True
            self.parent.update_message("Pas assez d'argent \n Besoin de 275 pieces d'or")
            return False
        elif type == "MITRAILLE":
            if self.argent >= self.tours_cout[type]:
                self.argent -= self.tours_cout[type]  # TourMitraille.prix
                self.parent.update_argent()
                return True
            else :
                self.parent.update_message("Pas assez d'argent \n Besoin de 335 pieces d'or")
                return False
        else:
            return False

    def calculer_score(self, creep):
        # Maxence
        if isinstance(creep, Creep1):
            self.score += 5
        elif isinstance(creep, Creep2):
            self.score += 15
        elif isinstance(creep, Creep3):
            self.score += 25
        elif isinstance(creep, Creep4):
            self.score += 40
        elif isinstance(creep, Boss):
            self.score += 250
        self.parent.update_score()

    def traiter_creation_tour(self, clic_x, clic_y, type_tour):
        # if sentier_courant == sentier 1 (par exemple)
        tour_largeur = 17.5
        tour_longueur = 17.5
        self.plages_x_y_interdites = [
            [810 - tour_largeur, 850 + tour_largeur, 0, 150 + tour_longueur],
            [675 - tour_largeur, 850 + tour_largeur, 150 - tour_largeur, 195 + tour_longueur],
            [675 - tour_largeur, 720 + tour_largeur, 60 - tour_largeur, 150 + tour_longueur],
            [170 - tour_largeur, 720 + tour_largeur, 60 - tour_largeur, 110 + tour_longueur],
            [170 - tour_largeur, 210 + tour_largeur, 60 - tour_largeur, 340 + tour_longueur],
            [160 - tour_largeur, 330 + tour_largeur, 285 - tour_largeur, 340 + tour_longueur],
            [285 - tour_largeur, 330 + tour_largeur, 180 - tour_largeur, 340 + tour_longueur],
            [280 - tour_largeur, 425 + tour_largeur, 180 - tour_largeur, 235 + tour_longueur],
            [380 - tour_largeur, 425 + tour_largeur, 180 - tour_largeur, 340 + tour_longueur],
            [380 - tour_largeur, 425 + tour_largeur, 182 - tour_largeur, 343 + tour_longueur],
            [379 - tour_largeur, 515 + tour_largeur, 284 - tour_largeur, 340 + tour_longueur],
            [468 - tour_largeur, 514 + tour_largeur, 181 - tour_largeur, 340 + tour_longueur],
            [468 - tour_largeur, 514 + tour_largeur, 181 - tour_largeur, 340 + tour_longueur],
            [470 - tour_largeur, 615 + tour_largeur, 180 - tour_largeur, 238 + tour_longueur],
            [571 - tour_largeur, 618 + tour_largeur, 182 - tour_largeur, 452 + tour_longueur],
            [571 - tour_largeur, 732 + tour_largeur, 399 - tour_largeur, 455 + tour_longueur],
            [685 - tour_largeur, 731 + tour_largeur, 255 - tour_largeur, 455 + tour_longueur],
            [684 - tour_largeur, 852 + tour_largeur, 255 - tour_largeur, 315 + tour_longueur],
            [807 - tour_largeur, 853 + tour_largeur, 259 - tour_largeur, 451 + tour_longueur],
            [445 - tour_largeur, 852 + tour_largeur, 483 - tour_largeur, 543 + tour_longueur],
            [447 - tour_largeur, 496 + tour_largeur, 483 - tour_largeur, 543 + tour_longueur],
            [447 - tour_largeur, 496 + tour_largeur, 483 - tour_largeur, 543 + tour_longueur],
            [447 - tour_largeur, 496 + tour_largeur, 398 - tour_largeur, 538 + tour_longueur],
            [0, 492 + tour_largeur, 399 - tour_largeur, 455 + tour_longueur]
        ]

        for plage_interdite in self.plages_x_y_interdites:
            if plage_interdite[0] <= clic_x < plage_interdite[1]:
                if plage_interdite[2] <= clic_y < plage_interdite[3]:
                    print("TOUR NE PEUT PAS ÊTRE POSITIONNÉE SUR SENTIER")
                    return False

        # vérifier si une tour est déjà positionnée à l'endroit cliqué...
        # seulement si la liste d'aire occupées par les tours N'EST PAS vide
        if self.aires_occupees_par_tours:
            for aire in self.aires_occupees_par_tours:
                if aire[0] <= clic_x <= aire[1]:
                    if aire[2] <= clic_y <= aire[3]:
                        print("TOUR NE PEUT PAS ÊTRE POSITIONNÉE SUR UNE AUTRE TOUR")
                        return False

        if self.retirer_argent(type_tour):
            if type_tour == "FEU":
                self.tours_feu.append(TourFeu(self, clic_x, clic_y)),
                self.determiner_aire_occupee(clic_x, clic_y, self.tours_feu[-1])
                # "GLACE": self.tours.append(TourGlace(clic_x, clic_y)),
                # "MITRAILLE": self.tours.append(TourMitraille(clic_x, clic_y)),
            elif type_tour == "POISON":
                self.tours_poison.append(TourPoison(self, clic_x, clic_y))
                self.determiner_aire_occupee(clic_x, clic_y, self.tours_poison[-1])
            elif type_tour == "GLACE":
                self.tours_glace.append(TourGlace(self, clic_x, clic_y))
                self.determiner_aire_occupee(clic_x, clic_y, self.tours_glace[-1])
            elif type_tour == "MITRAILLE":
                self.tours_mitraille.append(TourMitraille(self, clic_x, clic_y))
                self.determiner_aire_occupee(clic_x, clic_y, self.tours_mitraille[-1])

            return True
        else:
            return False

    # déterminer l'aire de position de nouvelle tour comme aire occupée
    def determiner_aire_occupee(self, clic_x, clic_y, nouvelle_tour):
        # ajouter aire au aires_occupees_par_tour
        self.aires_occupees_par_tours.append([
            clic_x - nouvelle_tour.largeur/1.5,
            clic_x + nouvelle_tour.largeur/1.5,
            clic_y - nouvelle_tour.longueur/1.5,
            clic_y + nouvelle_tour.longueur/1.5,
            nouvelle_tour
        ])

    def clicker_tour(self, clicX, clicY):
        if self.aires_occupees_par_tours:
            for aire in self.aires_occupees_par_tours:
                if aire[0] <= clicX <= aire[1]:
                    if aire[2] <= clicY <= aire[3]:
                        print("TOUR NE PEUT PAS ÊTRE POSITIONNÉE SUR UNE AUTRE TOUR")

    def demarrer_chrono(self):
        self.time = time.time()

    # MANIL / source: https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle
    def verifier_creep_en_zone_danger(self, type_tour):
        for creep in self.creeps:
            # vérifie si tour feu
            # conditions selon le type recu en parametre
            if type_tour == "FEU":
                for tour in self.tours_feu:
                    # si dans "l'aire" d'attaque
                    if ((creep.pos_x - tour.x) ** 2) + ((creep.pos_y - tour.y) ** 2) < (tour.portee_attaque ** 2):
                        # la tour attaque alors le creep en question
                        # ON N'AS PLUS BESOIN DE CE IF (VOIR CONTROLEUR methode jouer)
                        #if not tour.attaque_en_cours:  # assumons que cette tour ne peut faire qu'une attaque à la fois
                        if creep.est_actif and not creep.est_tuer:
                            tour.attaque(creep)
                            tour.creeps_attaquer.append(creep)
                            creep.est_attaquer = True
            elif type_tour == "POISON":
                for tour in self.tours_poison:
                    # si dans "l'aire" d'attaque
                    if ((creep.pos_x - tour.x) ** 2) + ((creep.pos_y - tour.y) ** 2) < (tour.portee_attaque ** 2):
                        if creep.est_actif and not creep.est_tuer and not creep.a_poison:
                            tour.attaque(creep)
                            tour.creeps_attaquer.append(creep)
                            creep.est_attaquer = True
            elif type_tour == "GLACE":
                for tour in self.tours_glace:
                    tour.est_en_mode_attaque()  # **
                    # si dans "l'aire" d'attaque
                    if ((creep.pos_x - tour.x) ** 2) + ((creep.pos_y - tour.y) ** 2) < (tour.portee_attaque ** 2):
                        # la tour attaque alors le creep en question
                        # ON N'AS PLUS BESOIN DE CE IF (VOIR CONTROLEUR methode jouer)
                        #if not tour.attaque_en_cours:  # assumons que cette tour ne peut faire qu'une attaque à la fois
                        if creep.est_mobile and creep.est_actif and not creep.est_tuer:
                            tour.attaque(creep)
                            tour.creeps_attaquer.append(creep)
                            tour.est_en_mode_attaque()  # **
                            creep.est_attaquer_par_glace = True
            elif type_tour == "MITRAILLE":
                for tour in self.tours_mitraille:
                    # si dans "l'aire" d'attaque
                    if ((creep.pos_x - tour.x) ** 2) + ((creep.pos_y - tour.y) ** 2) < (tour.portee_attaque ** 2):
                        if creep.est_actif:
                            tour.attaque(creep)

    def deplacer_projectiles(self):
        for tour in self.tours_feu:
            if tour.attaque_en_cours:
                for projectile in tour.projectiles:
                    cible_a_retirer = projectile.parcours_la_zone_de_jeu()
                    if cible_a_retirer is not None:
                        self.retirer_projectile(tour, projectile, cible_a_retirer)
                    elif projectile.est_hors_portee(tour):
                        self.retirer_projectile(tour, projectile)
                    elif projectile.cible.est_tuer:
                        self.retirer_projectile(tour, projectile)
        for tour in self.tours_poison:
            if tour.attaque_en_cours:
                for projectile in tour.projectiles:
                    cible_a_retirer = projectile.parcours_la_zone_de_jeu()
                    if cible_a_retirer is not None:
                        self.retirer_projectile(tour, projectile, cible_a_retirer)
                    elif projectile.est_hors_portee(tour):
                        self.retirer_projectile(tour, projectile)
                    elif projectile.cible.est_tuer:
                        self.retirer_projectile(tour, projectile)
        for tour in self.tours_glace:
            if tour.attaque_en_cours:
                for projectile in tour.projectiles:
                    cible_a_retirer = projectile.parcours_la_zone_de_jeu()
                    if cible_a_retirer is not None:
                        self.retirer_projectile(tour, projectile, cible_a_retirer)
                    elif projectile.est_hors_portee(tour):
                        self.retirer_projectile(tour, projectile)
                    elif projectile.cible.est_tuer:
                        self.retirer_projectile(tour, projectile)
        for tour in self.tours_mitraille:
            for projectile in tour.projectiles:
                cible_a_retirer = projectile.parcours_la_zone_de_jeu()
                if cible_a_retirer is not None:
                    self.retirer_projectile(tour, projectile, cible_a_retirer)
                elif projectile.est_hors_portee(tour):
                    self.retirer_projectile(tour, projectile)
                elif projectile.cible.est_tuer:
                    self.retirer_projectile(tour, projectile)

    def decrementer_attaques_poison(self):
        for tour in self.tours_poison:
            if tour.nbr_attaques_en_cours > 0:
                tour.nbr_attaques_en_cours -= 1

    def retirer_projectile(self, tour_source, projectile, creep_a_retirer=None):
        tour_source.projectiles.remove(projectile)

        if creep_a_retirer is not None:
            if isinstance(projectile, ProjectileMitraille):
                creep_a_retirer.est_mitraille = False
            if not creep_a_retirer.est_tuer:
                # if projectile.degat is None:
                #     creep_a_retirer.est_mobile = False  # immobiliser le Creep
                # else:
                if not isinstance(projectile, ProjectileGlace):
                    print(projectile.degat)
                    creep_a_retirer.points_vie -= projectile.degat

            if isinstance(projectile, ProjectileGlace):
                tour_source.cibles.remove(projectile.cible)
                projectile.cible.est_mobile = False
                projectile.cible.temps_immobilisation_atteint *= tour_source.niveau  # doubler temps immobilisation
                projectile.cible.est_attaquer_par_glace = False

            if creep_a_retirer.points_vie <= 0 and not creep_a_retirer.est_tuer:
                self.retirer_creep(creep_a_retirer)
                creep_a_retirer.est_tuer = True

        if not isinstance(projectile, ProjectileGlace):
            tour_source.attaque_en_cours = False
        tour_source.creeps_attaquer = []

    def retirer_creep(self, creep_a_retirer):
        # utiliser "creep_a_retirer" : représente le creep à retirer
        self.calculer_argent(creep_a_retirer)
        self.calculer_score(creep_a_retirer)
        self.calculer_experience(creep_a_retirer)
        self.creeps.remove(creep_a_retirer)
        self.index_creep -= 1

    def verifier_direction_creep(self, creep):
        if creep.rotate == 1:
            creep.direction = "bas"
        elif creep.rotate == -1:
            creep.direction = "haut"
        elif creep.rotate == 0:
            if creep.sens_image:
                creep.direction = "gauche"
            else:
                creep.direction = "droite"

    def ameliorer_tour(self, tour):
        if self.argent >= tour.cout_amelioration:
            niv = self.parent.calculer_niveau_joueur()
            confirmer = tour.ameliorer(niv)
            if confirmer:
                self.argent -= tour.cout_amelioration
                return "Tour améliorée"
            else:
                return "Pas assez haut niveau, vous devez être niveau : " + str(tour.augmentation)
        else:
            return "Pas assez d'argent"

    def vendre_tour(self, tour):
        self.argent += (int)(self.parent.tours_cout[tour.type]*0.80)
        self.parent.update_argent()
        for tour_placee in self.aires_occupees_par_tours:
            if tour_placee[-1] == tour:
                self.aires_occupees_par_tours.remove(tour_placee)
                break;
        if tour.type == 'FEU':
            self.tours_feu.remove(tour)
        elif tour.type == 'GLACE':
            self.tours_glace.remove(tour)
        elif tour.type == 'POISON':
            self.tours_poison.remove(tour)
        elif tour.type == 'MITRAILLE':
            self.tours_mitraille.remove(tour)