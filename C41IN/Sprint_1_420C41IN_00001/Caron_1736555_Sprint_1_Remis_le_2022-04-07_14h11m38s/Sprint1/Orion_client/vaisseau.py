import random
from Id import *
from helper import Helper as hlp
from skillcheck import *

class Vaisseau():
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.espace_cargo = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {"SystemeSolaire": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte}
        self.ang = 0

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.systemes)
            self.acquerir_cible(cible, "SystemeSolaire")

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
        # c'Est ici qu'on va commencer l'acquésion militaire ou diplomatique

    def avancer(self):
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                type_obj = type(self.cible).__name__
                cible = self.arriver[type_obj]()
                return cible

    def arriver_etoile(self):
        # parent = joueur
        # parent.parent = modele
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "SystemeSolaire", self.id, self.cible.id,
                                self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
            # c'Est ici qu'on va completer l'acquésion militaire ou diplomatique en changeant le propriétaire
        cible = self.cible
        self.cible = 0
        return ["SystemeSolaire", cible]

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]


class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
        self.cible = 0
        self.ang = 0


class Combat(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
        self.cible = 0
        self.ang = 0

    def conquete(self):
        pass
