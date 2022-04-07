from Id import get_prochain_id

class Batiment:
    def __init__(self, parent, nom):
        self.parent = parent
        self.type = None
        self.id = get_prochain_id()
        self.proprietaire = nom



class Tour(Batiment):
    def __init__(self, parent, nom):
        Batiment.__init__(self, parent, nom)

class Senat(Batiment):
    def __init__(self, parent, nom):
        Batiment.__init__(self, parent, nom)
