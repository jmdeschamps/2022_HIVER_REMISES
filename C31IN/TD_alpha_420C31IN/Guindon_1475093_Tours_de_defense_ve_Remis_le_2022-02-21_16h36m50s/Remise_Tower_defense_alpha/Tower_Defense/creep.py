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
        # Étape du chemin à parcourir
        self.stade_chemin = 1
        # Liste des coordonnées du chemin à franchir
        self.chemin = chemin
        # Pour animer le creep
        self.max_image = len(self.images)
        self.index = 0
        # POUR ATTAQUE TOUR
        self.est_attaquer = False
        self.est_tuer = False
        # POUR ATTAQUE POISON
        self.a_poison = False
        self.compteur_poison = 0
        self.vitesse = 5
        self.vitesse_initial = 5
        self.est_mobile = True
        self.temps_immobilise = 0
        # POUR ATTAQUE MITRAILLE
        self.est_mitraille = False


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
        if self.compteur_poison == 200:
            self.a_poison = False
            self.compteur_poison = 0
            self.vitesse = self.vitesse_initial

    def verifier_glace(self):
        if self.temps_immobilise == 60:
            self.est_mobile = True
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


class Creep1(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # Dégâts du creep
        self.degats = 1
        # Points de vie du creep
        self.points_vie = 10
        self.max_points_vie = 10
        # Image du creep
        self.images = ["images/Creeps/1/walk1.png", "images/Creeps/1/walk3.png",
                      "images/Creeps/1/walk10.png", "images/Creeps/1/walk12.png",
                      "images/Creeps/1/walk14.png", "images/Creeps/1/walk16.png"]
        super().__init__(pos_x, pos_y, chemin)


class Creep2(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # Dégâts du creep
        self.degats = 2
        # Points de vie du creep
        self.points_vie = 20
        self.max_points_vie = 20
        # Image du creep
        self.images = ["images/Creeps/2/walk0.png", "images/Creeps/2/walk5.png",
                      "images/Creeps/2/walk9.png", "images/Creeps/2/walk15.png",
                      "images/Creeps/2/walk17.png", "images/Creeps/2/walk18.png"]
        super().__init__(pos_x, pos_y, chemin)


class Creep3(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # Dégâts du creep
        self.degats = 3
        # Points de vie du creep
        self.points_vie = 30
        self.max_points_vie = 30
        # Image du creep
        self.images = ["images/Creeps/3/walk0.png", "images/Creeps/3/walk2.png",
                      "images/Creeps/3/walk6.png", "images/Creeps/3/walk11.png",
                      "images/Creeps/3/walk16.png", "images/Creeps/3/walk18.png"]
        super().__init__(pos_x, pos_y, chemin)


class Creep4(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # Dégâts du creep
        self.degats = 4
        # Points de vie du creep
        self.points_vie = 40
        self.max_points_vie = 40
        # Image du creep
        self.images = ["images/Creeps/5/walk0.png", "images/Creeps/5/walk2.png",
                      "images/Creeps/5/walk11.png", "images/Creeps/5/walk14.png",
                      "images/Creeps/5/walk16.png", "images/Creeps/5/walk17.png"]
        super().__init__(pos_x, pos_y, chemin)


class Boss(Creep):
    def __init__(self, pos_x, pos_y, chemin):
        # Vitesse du creep
        self.vitesse = 5
        # Dégâts du creep
        self.degats = 50
        # Points de vie du creep
        self.points_vie = 100
        self.max_points_vie = 100
        # Image du creep
        self.images = ["images/Creeps/10/walk0.png", "images/Creeps/10/walk2.png",
                      "images/Creeps/10/walk4.png", "images/Creeps/10/walk8.png",
                      "images/Creeps/10/walk17.png", "images/Creeps/10/walk18.png"]
        super().__init__(pos_x, pos_y, chemin)
        self.largeur *= 1.5
        self.hauteur *= 1.5