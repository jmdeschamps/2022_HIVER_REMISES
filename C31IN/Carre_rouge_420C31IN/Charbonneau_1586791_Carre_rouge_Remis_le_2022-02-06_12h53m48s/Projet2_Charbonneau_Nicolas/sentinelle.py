class Sentinelle:
    def __init__(self, parent, largeur, hauteur, position_x, position_y, vitesse):
        self.parent = parent
        self.largeur = largeur
        self.hauteur = hauteur
        self.position_x = position_x
        self.position_y = position_y
        self.vitesse_x = vitesse
        self.vitesse_y = vitesse

    def deplacer(self):
        min_x = 0 - (self.parent.largeur_fenetre - self.parent.largeur_zone) / 2
        max_x = self.parent.largeur_zone + (self.parent.largeur_fenetre - self.parent.largeur_zone) / 2
        min_y = 0 - (self.parent.hauteur_fenetre - self.parent.hauteur_zone) / 2
        max_y = self.parent.hauteur_zone + (self.parent.hauteur_fenetre - self.parent.hauteur_zone) / 2
        if self.position_x - self.largeur / 2 <= min_x or self.position_x + self.largeur / 2 >= max_x:
            self.vitesse_x = -self.vitesse_x
        if self.position_y - self.hauteur / 2 <= min_y or self.position_y + self.hauteur / 2 >= max_y:
            self.vitesse_y = -self.vitesse_y
        self.position_x += self.vitesse_x
        self.position_y += self.vitesse_y

    def incrementer_vitesse(self):
        if self.vitesse_x > 0:
            self.vitesse_x += 3
        else:
            self.vitesse_x -= 3
        if self.vitesse_y > 0:
            self.vitesse_y += 3
        else:
            self.vitesse_y -= 3
