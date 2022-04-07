from random import randrange

class Creep:
    def __init__(self, id, parent, chemin, archetype, apparence, vie, vitesse, valeur_dommage, valeur_monetaire, immunite):
        self.parent = parent
        self.archetype = archetype
        self.vie = vie
        self.vie_max = vie
        self.immunite = immunite
        self.vitesse = vitesse
        self.valeur_dommage = valeur_dommage
        self.valeur_monetaire = valeur_monetaire
        self.distance_parcourue = 0
        self.apparence = apparence
        self.largeur = 20
        self.hauteur = 20
        self.chemin = chemin
        self.id = id
        self.derniere_position = len(chemin) - 1
        self.x = chemin[0][0]
        self.y = chemin[0][1]
        self.destination = 1
        self.orientation = 0 #0 = droite et le reste clockwise
        self.destination_x = self.chemin[self.destination][0]
        self.destination_y = self.chemin[self.destination][1]
        self.random_position_x_variation = randrange(-1, 1)
        self.random_position_y_variation = randrange(-1, 1)

    def avancer(self):
        vertical = ""
        horizontal = ""
        if self.x < self.destination_x:
            vertical = "droite" #0
            self.x = self.x + self.vitesse
            if self.x > self.destination_x:
                self.x = self.destination_x
        elif self.x > self.destination_x:
            vertical = "gauche" #4
            self.x = self.x - self.vitesse
            if self.x < self.destination_x:
                self.x = self.destination_x

        if self.y < self.destination_y:
            horizontal = "bas" #2
            self.y = self.y + self.vitesse
            if self.y > self.destination_y:
                self.y = self.destination_y
        elif self.y > self.destination_y:
            horizontal = "haut" #7
            self.y = self.y - self.vitesse
            if self.y < self.destination_y:
                self.y = self.destination_y

        if vertical == "droite" and horizontal == "":
            self.orientation = 0
        elif vertical == "droite" and horizontal == "bas":
            self.orientation = 1
        elif vertical == "" and horizontal == "bas":
            self.orientation = 2
        elif vertical == "gauche" and horizontal == "bas":
            self.orientation = 3
        elif vertical == "gauche" and horizontal == "":
            self.orientation = 4
        elif vertical == "gauche" and horizontal == "haut":
            self.orientation = 5
        elif vertical == "" and horizontal == "haut":
            self.orientation = 6
        elif vertical == "droite" and horizontal == "haut":
            self.orientation = 7

        if self.x == self.destination_x and self.y == self.destination_y:
            if self.destination < self.derniere_position:
                self.destination += 1
                self.destination_x = self.chemin[self.destination][0]
                self.destination_y = self.chemin[self.destination][1]
            else:
                return self.valeur_dommage
        return 0

    def baisser_vie(self, dommage, type_dommage):
        if type_dommage != self.immunite:
            self.vie -= dommage
        if self.vie <= 0:
            self.parent.tuer_creep(self)
        return True

class Trooper(Creep):
    def __init__(self, id, parent, chemin):
        super().__init__(id,
                         parent,
                         chemin,
                         archetype="Trooper",
                         apparence='yellow',
                         vie=15,
                         vitesse=2,
                         valeur_dommage=20,
                         valeur_monetaire=8,
                         immunite=None)

class Droid(Creep):
    def __init__(self, id, parent, chemin):
        super().__init__(id,
                         parent,
                         chemin,
                         archetype="Droid",
                         apparence='orange',
                         vie=25,
                         vitesse=4,
                         valeur_dommage=30,
                         valeur_monetaire=12,
                         immunite=None)

class AtAt(Creep):
    def __init__(self, id, parent, chemin):
        super().__init__(id,
                         parent,
                         chemin,
                         archetype="At-At",
                         apparence='#052624',
                         vie=80,
                         vitesse=1,
                         valeur_dommage=30,
                         valeur_monetaire=40,
                         immunite="kinetic")
        self.largeur = 80
        self.hauteur = 80

class Vader(Creep):
    def __init__(self, id, parent, chemin):
        super().__init__(id,
                         parent,
                         chemin,
                         archetype="Vader",
                         apparence='red',
                         vie=50,
                         vitesse=2,
                         valeur_dommage=60,
                         valeur_monetaire=35,
                         immunite=None)