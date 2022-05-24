
from Pillow import *
from Orion_vue import *


class Vaisseau_vue():
    def __init__(self, parent):
        self.parent = parent

        self.id_vaisseau1 = []
        self.id_vaisseau2 = []
        self.id_vaisseau3 = []
        self.id_vaisseau4 = []
        self.id_vaisseau5 = []
        self.id_vaisseau6 = []
        self.id_vaisseau7 = []
        self.id_vaisseau8 = []
        self.vaisseau1 = {}
        self.vaisseau2 = {}
        self.vaisseau3 = {}
        self.vaisseau4 = {}
        self.vaisseau5 = {}
        self.vaisseau6 = {}
        self.vaisseau7 = {}
        self.vaisseau8 = {}
        self.scout1 = {}
        self.scout2 = {}
        self.scout3 = {}
        self.scout4 = {}
        self.scout5 = {}
        self.scout6 = {}
        self.scout7 = {}
        self.scout8 = {}
        self.vaisseau_actif = {"type": None, "vie": None, "degats": None, "energie": None, "nb_capsules": None,
                               "ressource": None}
        self.angle = [270, 225, 180, 135, 90, 45, 0, 315, 270]

    def creercouleurVaisseau(self):
        mod = self.parent.modele
        for i in mod.joueurs.keys():
            compteur = 0
            self.parent.vue.nombre_joueur += 1
            i = mod.joueurs[i]

            if self.parent.vue.nombre_joueur == 1:
                for h in self.angle:
                    self.vaisseau1[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout1[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau1.append(i.id)
                compteur = 0

            if self.parent.vue.nombre_joueur == 2:
                for h in self.angle:
                    self.vaisseau2[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout2[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau2.append(i.id)

            if self.parent.vue.nombre_joueur == 3:
                for h in self.angle:
                    self.vaisseau3[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout3[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau3.append(i.id)

            if self.parent.vue.nombre_joueur == 4:
                for h in self.angle:
                    self.vaisseau4[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout4[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau4.append(i.id)
            if self.parent.vue.nombre_joueur == 5:
                for h in self.angle:
                    self.vaisseau5[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout5[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau5.append(i.id)

            if self.parent.vue.nombre_joueur == 6:
                for h in self.angle:
                    self.vaisseau6[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout6[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau6.append(i.id)

            if self.parent.vue.nombre_joueur == 7:
                for h in self.angle:
                    self.vaisseau7[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout7[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau7.append(i.id)

            if self.parent.vue.nombre_joueur == 8:
                for h in self.angle:
                    self.vaisseau8[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout8[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau8.append(i.id)
        pass