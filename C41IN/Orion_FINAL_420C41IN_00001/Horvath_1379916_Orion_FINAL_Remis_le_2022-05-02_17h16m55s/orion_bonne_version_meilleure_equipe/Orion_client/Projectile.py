from random import randint

from helper import *


class Projectile:
    def __init__(self, source, cible, acte_defensif=False):
        self.__source = source
        self.__cible = cible
        self.__x = source.x
        self.__y = source.y
        self.__target_x = cible.x
        self.__target_y = cible.y
        self.__largeur = 10
        self.__longueur = 10
        self.__vitesse = 15
        self.__couleur = "green" if acte_defensif is False else "red"
        self.__degat = 3  # self.__source.degat
        self.__lifetime = 60
        self.__est_detruit = False
        self.__aire_de_degat = 15
        self.attaque_cible()

    def attaque_cible(self):
        if self.__lifetime > 0:
            self.__lifetime -= 1

            distance_projectile_cible = Helper.calcDistance(self.__x, self.__y, self.__cible.x, self.__cible.y)
            angle_projectile = Helper.calcAngle(self.__x, self.__y, self.__cible.x, self.__cible.y)
            cible_projectile = Helper.getAngledPoint(angle_projectile, self.__vitesse, self.__x, self.__y)

            self.__x = cible_projectile[0]
            self.__y = cible_projectile[1]

            if distance_projectile_cible < self.__aire_de_degat:
                if self.__cible.hp > 0:
                    self.__cible.hp -= self.__degat
                    self.__cible.est_cible_pour_attaque = True if self.__cible.est_cible_pour_attaque is False else None
                    self.__cible.est_cible_pour_attaque = True
                    self.__cible.cible = self.__source
                    try:
                        self.__source.projectiles.remove(self)
                    except:
                        print("projectile (self) déjà retiré de liste (fast patch")
                else:
                    try:
                        self.__cible.tuer_satellite(self.__cible)
                    except:
                        pass
                    self.__cible.parent.parent.joueurs[self.__cible.proprietaire] \
                        .flotte[self.__cible.type_vaisseau].pop(self.__cible.id, None)
                    self.__source.cible = self.__source.etoile_mere
        else:
            self.__source.projectiles.remove(self)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def longueur(self):
        return self.__longueur

    @property
    def largeur(self):
        return self.__largeur

    @property
    def couleur(self):
        return self.__couleur
