class Monstre(object):
    vie_max = 70
    prix = 20
    point = 50
    vitesse = 1

    def __init__(self, x, y, vitesse, vie, listeimages):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.index = 0
        self.vie = vie
        self.empoisonne = False
        self.stack_poison = 0
        self.frozen = False

        self.images = listeimages
        self.indice = 0
        self.max_image = len(self.images)
        self.delai_indice = 0
        self.delai_max = 2

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

            if cibleX - 5 <= self.x <= cibleX + 5 and cibleY - 5 <= self.y <= cibleY + 5:
                self.x = cibleX
                self.y = cibleY
                self.index += 1


            self.delai_indice += 1
            if self.delai_indice == self.delai_max:
                self.delai_indice = 0
                self.indice += 1
            if self.indice == self.max_image:
                self.indice = 0


class Boss(Monstre):
    vie_max = 200


    def __init__(self, x, y, vitesse, vie,liste_images):
        super().__init__(x, y, vitesse, vie,liste_images)
        self.indice = 0
        self.max_image = len(self.images)

    def avancer_monstre(self, path):
        super().avancer_monstre(path)


class Portail():
    def __init__(self,listeimages):
        self.x = 1143
        self.y = 350
        self.images = listeimages
        self.indice = 0
        self.max_image = len(self.images)
        self.delai_indice = 0
        self.delai_max = 2

    def animer(self):
        self.delai_indice += 1
        if self.delai_indice == self.delai_max:
            self.delai_indice = 0
            self.indice += 1

        if self.indice == self.max_image:
            self.indice = 0