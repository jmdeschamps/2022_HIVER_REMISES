from random import randrange

class Vague:
    def __init__(self):
        self.composition = []
        self.index = -1
        self.delai_spawn_max = 25
        self.delai_spawn = self.delai_spawn_max

    def spawn(self):
        if self.index < len(self.composition)-1:
            if self.delai_spawn == 0:
                self.delai_spawn = self.delai_spawn_max + randrange(0,20)
                self.index+=1
                return self.composition[self.index]
            else:
                self.delai_spawn -= 1

    def ajouter(self, creep):
        self.composition.append(creep)
