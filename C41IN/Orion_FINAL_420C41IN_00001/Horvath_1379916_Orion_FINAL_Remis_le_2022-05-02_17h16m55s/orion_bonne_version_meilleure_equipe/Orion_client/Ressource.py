class Ressource:
    def __init__(self, quantite):
        self.quantite = quantite

    def retrait_quantite(self, quantite_retrait):
        self.quantite -= quantite_retrait
        return quantite_retrait

    def ajout_quantite(self, quantite_ajout):
        self.quantite += quantite_ajout
        return quantite_ajout

    def set_quantite(self, new_quantite):
        self.quantite = new_quantite


class Nourriture(Ressource):
    taux_rarete = 0.4
    nom = "NOURRITURE"

    def __init__(self, quantite):
        super().__init__(quantite)


class Energie(Ressource):
    taux_rarete = .03
    nom = "ENERGIE"

    def __init__(self, quantite):
        super().__init__(quantite)


class Eau(Ressource):
    taux_rarete = .02
    nom = "EAU"

    def __init__(self, quantite):
        super().__init__(quantite)


class Fer(Ressource):
    taux_rarete = .05
    nom = "FER"

    def __init__(self, quantite):
        super().__init__(quantite)


class Titanium(Ressource):
    taux_rarete = .05
    nom = "TITANIUM"

    def __init__(self, quantite):
        super().__init__(quantite)


class Cuivre(Ressource):
    taux_rarete = .02
    nom = "CUIVRE"

    def __init__(self, quantite):
        super().__init__(quantite)
