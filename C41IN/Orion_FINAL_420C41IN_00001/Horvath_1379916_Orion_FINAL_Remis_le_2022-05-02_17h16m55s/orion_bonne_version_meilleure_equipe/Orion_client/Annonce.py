# dans toutes les actions, utiliser fonction Joueur.nouvelle_annonce(self, message, type)

class Annonce:
    def __init__(self, message):

        self.type = type
        self.message = message
        self.x = 850
        self.y = 150
        self.supprimer = False
        self.cooldown = 40

    def tick(self):
        self.cooldown -= 1
        if self.cooldown == 0:
            self.supprimer = True



