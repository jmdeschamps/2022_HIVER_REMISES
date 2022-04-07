class Creep:
    def __init__(self, pos_x, pos_y, chemin):
#       Inutilisées
        self.largeur = 40
        self.hauteur = 40
        # Position sur la carte
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Boolean utilisé pour lancer le déplacement du creep
        self.est_actif = False
        # Boolean utilisé pour renverser l'image
        self.sens_image = False
        # Pour faire une rotation de l'image vers le haut ou vers le bas
        self.rotate = 0
        # direction du creep
        self.direction = ["droite", "gauche", "bas", "haut"]
        # Étape du chemin à parcourir
        self.stade_chemin = 1
        # Liste des coordonnées du chemin à franchir
        self.chemin = chemin
        # Pour animer le creep
        self.max_image = 5 # nos tableaux d'animation ne sont jamais plus haut!
        self.direction = ["droite", "gauche", "bas", "haut"]
        self.index = 0
        # POUR ATTAQUE TOUR
        self.est_attaquer = False
        self.est_tuer = False
        # POUR ATTAQUE POISON
        self.a_poison = False
        self.compteur_poison = 0
        self.degat_poison = 0
        self.vitesse = 10
        self.vitesse_initial = 10
        self.est_mobile = True
        self.temps_immobilise = 0
        # POUR ATTAQUE MITRAILLE
        self.est_mitraille = False
        self.est_attaquer_par_glace = False
        self.temps_immobilisation_atteint = 60

    def activer(self):
        self.est_actif = True

    def deplacer(self):
        if self.est_actif and self.est_mobile:
            # Incrémente l'étape du parcours si franchit les coordonnées de l'étape actuelle
            if self.stade_chemin < len(self.chemin) - 1:
                if self.chemin[self.stade_chemin][0] - 5 <= self.pos_x <= self.chemin[self.stade_chemin][0] + 5:
                    if self.chemin[self.stade_chemin][1] - 5 <= self.pos_y <= self.chemin[self.stade_chemin][1] + 5:
                        self.stade_chemin += 1
            # Vérifie dans quelle direction déplacer le creep

            # réussir à merger self.rotate et self.sens_image => self.direction

            # self.direction = [0,1,2,3]
            # réussir à dire la clé de direction au creep pour aller dans la bonne direction
            if self.chemin[self.stade_chemin-1][0] < self.chemin[self.stade_chemin][0]:
                self.pos_x += self.vitesse
                self.sens_image = False
            elif self.chemin[self.stade_chemin-1][0] > self.chemin[self.stade_chemin][0]:
                self.pos_x -= self.vitesse
                self.sens_image = True
            if self.chemin[self.stade_chemin-1][1] < self.chemin[self.stade_chemin][1]:
                self.pos_y += self.vitesse
                self.rotate = 1
            elif self.chemin[self.stade_chemin-1][1] > self.chemin[self.stade_chemin][1]:
                self.pos_y -= self.vitesse
                self.rotate = -1
            else:
                self.rotate = 0

        self.verifier_poison()

        if not self.est_mobile:
            self.verifier_glace()

    def verifier_poison(self):
        if self.a_poison:
            self.compteur_poison += 1
        if self.compteur_poison%50 == 0:
            self.points_vie -= self.degat_poison
        if self.compteur_poison == 200:
            self.a_poison = False
            self.compteur_poison = 0
            self.vitesse = self.vitesse_initial
            self.degat_poison = 0

    def verifier_glace(self):
        if self.temps_immobilise == self.temps_immobilisation_atteint:
            self.est_mobile = True
            self.temps_immobilisation_atteint = 60
            self.temps_immobilise = 0
        self.temps_immobilise += 1

    def verifier_attaque_forteresse(self):
        if self.chemin[self.stade_chemin][0] - 5 <= self.pos_x <= self.chemin[self.stade_chemin][0] + 5:
            if self.chemin[self.stade_chemin][1] - 5 <= self.pos_y <= self.chemin[self.stade_chemin][1] + 5:
                return True, self
        return False, None

    def changer_image(self):
        self.index += 1
        if self.index == self.max_image:
            self.index = 0

    def set_temps_immobilisation_atteint(self, nouveau_temps_immobilisation):
        self.temps_immobilisation_atteint = nouveau_temps_immobilisation

class Creep1(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # clé pour accéder au dictionnaire
        self.cle = "creep1"
        # Dégâts du creep
        self.degats = 1
        # Points de vie du creep
        self.points_vie = 6
        self.max_points_vie = 6
        super().__init__(pos_x, pos_y, chemin)


class Creep2(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 6
        # clé pour accéder au dictionnaire
        self.cle = "creep2"
        # Dégâts du creep
        self.degats = 2
        # Points de vie du creep
        self.points_vie = 12
        self.max_points_vie = 12

        super().__init__(pos_x, pos_y, chemin)


class Creep3(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 7
        # clé pour accéder au dictionnaire
        self.cle = "creep3"
        # Dégâts du creep
        self.degats = 3
        # Points de vie du creep
        self.points_vie = 18
        self.max_points_vie = 18

        super().__init__(pos_x, pos_y, chemin)


class Creep4(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 8
        # clé pour accéder au dictionnaire
        self.cle = "creep4"
        # Dégâts du creep
        self.degats = 4
        # Points de vie du creep
        self.points_vie = 24
        self.max_points_vie = 24

        super().__init__(pos_x, pos_y, chemin)


class Boss(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 8
        # clé pour accéder au dictionnaire
        self.cle = "creep5"
        # Dégâts du creep
        self.degats = 50
        # Points de vie du creep
        self.points_vie = 1000
        self.max_points_vie = 1000

        super().__init__(pos_x, pos_y, chemin)
        self.largeur *= 2
        self.hauteur *= 2