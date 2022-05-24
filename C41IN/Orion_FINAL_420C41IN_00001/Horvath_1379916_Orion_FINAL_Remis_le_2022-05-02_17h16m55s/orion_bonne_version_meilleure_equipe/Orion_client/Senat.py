class Senat:
    def __init__(self):
        self.liste_loi = []
        self.prochain_juge = []

    def ajouter_echange(self, Loi):
        if self.voter_loi(Loi):
            self.liste_loi.append(Loi)

    def retirer_loi(self, Loi):
        self.liste_loi.remove(Loi)

    def voter_loi(self, Loi):
       pass

    def élir_juge(self):
        pass #fonction pour passer au prochain joueur décidant de la nouvelle loi.



class Loi:
    def __init__(self, nom, norme , devoirs):
        self.nom = nom
        self.norme = norme
        self.devoirs = devoirs
