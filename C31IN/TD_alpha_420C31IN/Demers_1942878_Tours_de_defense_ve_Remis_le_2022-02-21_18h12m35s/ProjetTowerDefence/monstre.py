import random


class Monstre(object):
    vie_max = 100
    prix = 20
    point = 50

    def __init__(self, x, y, vitesse, vie):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.index = 0
        self.vie = vie

    def avancer_monstre(self, path):
        if self.index != len(path):
            cibleX = path[self.index][0]
            cibleY = path[self.index][1]
            if self.x < cibleX:
                self.x = self.x + self.vitesse

            if self.y < cibleY:
                self.y += self.vitesse
            elif self.y > cibleY:
                self.y -= self.vitesse

            if self.y == cibleY and self.x == cibleX:
                self.x = cibleX
                self.y = cibleY
                self.index += 1
