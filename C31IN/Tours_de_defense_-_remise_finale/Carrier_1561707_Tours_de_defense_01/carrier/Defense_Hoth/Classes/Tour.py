import math


class Tour:
    def __init__(self, parent, idTour, archetype, apparence, cout, tirParSeconde, dommage, portee,
                 largeur_modele, hauteur_modele, position_x, position_y, type_dommage, upgrades):
        self.parent = parent
        self.idTour = idTour
        self.archetype = archetype
        self.apparence = apparence
        self.valeur = cout
        self.tirParSeconde = tirParSeconde
        self.cooldown_max = (1000 / 50) / self.tirParSeconde
        self.cooldown = 0
        self.dommage = dommage
        self.type_dommage = type_dommage
        self.portee = portee
        self.position_x = position_x
        self.position_y = position_y
        self.largeur = largeur_modele
        self.hauteur = hauteur_modele
        self.pew_pew = []
        self.victime = None
        self.creeps_in_range = []
        self.upgrade_possible = upgrades
        self.upgrades_actuelles = 0

        self.tour_construite = False
        self.index_creation = 0
        self.locked_on = False

    def avancer_projectiles(self):
        for projectile in self.pew_pew:
            rendu = projectile.avancer()
            if rendu:
                del self.pew_pew[self.pew_pew.index(projectile)]

    def surveiller(self):
        self.creeps_in_range = []
        for creep in self.parent.liste_creeps:
            dx = abs(creep.x - self.position_x) ** 2
            dy = abs(creep.y - self.position_y) ** 2
            distance = math.sqrt(dx + dy)
            if distance <= self.portee:
                self.creeps_in_range.append(creep)
        if len(self.creeps_in_range) > 0:
            if self.cooldown == 0:
                self.cooldown = self.cooldown_max
                self.tirer()
            else:
                self.cooldown -= 1

    def tirer(self):
        """Définis dans les sous-classes"""
        pass

    def upgradeTour(self, upgrade):
        if upgrade in self.upgrade_possible:
            cout = 0
            if upgrade == "vitesse":
                self.tirParSeconde *= 1.5
                cout = 10
            if upgrade == "dommage":
                self.dommage *= 1.5
                cout = 10
            if upgrade == "range":
                self.portee *= 1.25
                cout = 10
            return cout


class TourMitraillette(Tour):
    def __init__(self, parent, idTour, prix, x, y):
        Tour.__init__(self, parent,
                      idTour,
                      archetype='Mitraillette',
                      apparence='#6666FF',
                      cout=prix,
                      tirParSeconde=4,
                      dommage=1 * 1.5,
                      portee=100 * 1.8,
                      largeur_modele=8,
                      hauteur_modele=10,
                      position_x=x,
                      position_y=y,
                      type_dommage="kinetic",
                      upgrades=["vitesse", "dommage"])

    def tirer(self):
        self.victime = self.creeps_in_range[0]
        for creep in self.creeps_in_range:
            if creep.distance_parcourue > self.victime.distance_parcourue:
                self.victime = creep
        self.pew_pew.append(Blaster(self))


class TourLanceRoquette(Tour):
    def __init__(self, parent, idTour, prix, x, y):
        Tour.__init__(self, parent,
                      idTour,
                      archetype='Lance-Roquette',
                      apparence='#66FF66',
                      cout=prix,
                      tirParSeconde=1,
                      dommage=3,
                      portee=150*1.8,
                      largeur_modele=10,
                      hauteur_modele=13,
                      position_x=x,
                      position_y=y,
                      type_dommage="energie",
                      upgrades=["dommage", "range"])

    def tirer(self):
        self.victime = self.creeps_in_range[0]
        for creep in self.creeps_in_range:
            if creep.vie > self.victime.vie:
                self.victime = creep
        self.pew_pew.append(Roquette(self))


class TourShocker(Tour):
    def __init__(self, parent, idTour, prix, x, y):
        Tour.__init__(self, parent,
                      idTour,
                      archetype='Shocker',
                      apparence='#FF6666',
                      cout=prix,
                      tirParSeconde=5,
                      dommage=2*0.60,
                      portee=80*1.7,
                      largeur_modele=12,
                      hauteur_modele=16,
                      position_x=x,
                      position_y=y,
                      type_dommage="energie",
                      upgrades=["range", "dommage"])

    def tirer(self):
        temp = self.creeps_in_range
        for creep in temp:
            if not creep.baisser_vie(self.dommage, self.type_dommage):
                break


class TourSniper(Tour):
    def __init__(self, parent, idTour, prix, x, y):
        Tour.__init__(self, parent,
                      idTour,
                      archetype='Sniper',
                      apparence='#FFFFFF',
                      cout=prix,
                      tirParSeconde=0.5,
                      dommage=5,
                      portee=10000,
                      largeur_modele=10,
                      hauteur_modele=12,
                      position_x=x,
                      position_y=y,
                      type_dommage="kinetic",
                      upgrades=["vitesse", "dommage"])

    def tirer(self):
        self.victime = self.creeps_in_range[0]
        for creep in self.creeps_in_range:
            if creep.distance_parcourue > self.victime.distance_parcourue:
                self.victime = creep
        self.victime.baisser_vie(self.dommage, self.type_dommage)


class Pew_pew:
    def __init__(self, parent):
        self.parent = parent
        self.range = self.parent.portee * 3
        self.vitesse = 15
        self.x = self.parent.position_x
        self.y = self.parent.position_y
        self.x2 = self.x
        self.y2 = self.y
        self.longueur = 10
        self.cible = None
        self.destination_x = None
        self.destination_y = None

    def bouger(self):
        self.range -= self.vitesse
        if self.x < self.destination_x and abs(self.x - self.destination_x) > self.vitesse:
            self.x = self.x + self.vitesse
            self.x2 = self.x-self.longueur
        elif self.x > self.destination_x and abs(self.x - self.destination_x) > self.vitesse:
            self.x = self.x - self.vitesse
            self.x2 = self.x+self.longueur
        elif abs(self.x - self.destination_x) < self.vitesse:
            self.x = self.destination_x
            self.x2 = self.destination_x

        if self.y < self.destination_y and abs(self.y - self.destination_y) > self.vitesse:
            self.y = self.y + self.vitesse
            self.y2 = self.y-self.longueur
        elif self.y > self.destination_y and abs(self.y - self.destination_y) > self.vitesse:
            self.y = self.y - self.vitesse
            self.y2 = self.y+self.longueur
        elif abs(self.y - self.destination_y) < self.vitesse:
            self.y = self.destination_y
            self.y2 = self.destination_y


class Blaster(Pew_pew):
    def __init__(self, parent):
        Pew_pew.__init__(self, parent)
        self.cible = self.parent.victime
        self.destination_x = self.cible.x
        self.destination_y = self.cible.y

    def avancer(self):
        if self.cible:
            rendu = False
            self.bouger()
            for creep in self.parent.parent.liste_creeps:
                if (creep.x - creep.largeur < self.x < creep.x + creep.largeur) and (
                        creep.y - creep.hauteur < self.y < creep.y + creep.hauteur):
                    creep.baisser_vie(self.parent.dommage, self.parent.type_dommage)
                    rendu = True
            if self.range == 0:
                rendu = True
            elif self.x == self.destination_x and self.y == self.destination_y:
                rendu = True
            return rendu
        else:
            return True


class Roquette(Pew_pew):
    def __init__(self, parent):
        Pew_pew.__init__(self, parent)

    def avancer(self):
        self.cible = self.parent.victime
        if self.cible:
            rendu = False
            self.destination_x = self.cible.x
            self.destination_y = self.cible.y
            self.bouger()
            if self.x == self.destination_x and self.y == self.destination_y:
                self.cible.baisser_vie(self.parent.dommage, self.parent.type_dommage)
                rendu = True
            elif self.range == 0:
                rendu = True
            return rendu
        else:
            return True
