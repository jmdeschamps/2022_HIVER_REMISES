from Id import get_prochain_id


class Satellite:
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.type = None
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.hp = 0


class Telecommunication(Satellite):
    def __init__(self, parent, nom, x, y):
        Satellite.__init__(self, parent, nom, x, y)
        self.energie = 500
        self.taille = 6
        self.vitesse = .5
        self.cible = 0
        self.hp = 200


class Galileo(Satellite):
    def __init__(self, parent, nom, x, y):
        Satellite.__init__(self, parent, nom, x, y)
        self.energie = 500
        self.taille = 6
        self.vitesse = .5
        self.cible = 0
        self.hp = 200
