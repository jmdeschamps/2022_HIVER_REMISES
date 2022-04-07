from Id import get_prochain_id

class Merveille:
    def __init__(self, parent, nom):
        self.parent = parent
        self.type = None
        self.id = get_prochain_id()
        self.proprietaire = nom

class Muraille_Chine(Merveille):
    def __init__(self, parent, nom):
        Merveille.__init__(self, parent, nom)
