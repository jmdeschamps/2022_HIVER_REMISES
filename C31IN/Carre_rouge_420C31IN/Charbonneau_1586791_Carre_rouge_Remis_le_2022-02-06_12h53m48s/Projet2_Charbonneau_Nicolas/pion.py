class Pion:
    def __init__(self, parent, largeur_fenetre, hauteur_fenetre, dimension_pion=1):
        self.parent = parent
        self.largeur = 40 * dimension_pion
        self.hauteur = 40 * dimension_pion
        self.position_x = largeur_fenetre / 2
        self.position_y = hauteur_fenetre / 2
        self.vitesse = 2

    def deplacer(self, x, y):
        self.position_x = x
        self.position_y = y