class Marche:
    def __init__(self, parent):
        self.liste_echange = []
        self.parent = parent

    def ajouter_echange(self, nom_joueur, param):
        ressource_offerte, quantite_offerte, ressource_demande, quantite_demande = param
        obj = Echange(nom_joueur, ressource_offerte, quantite_offerte, ressource_demande, quantite_demande)
        self.liste_echange.append(obj)
        ressource = self.trouver_ressource(ressource_offerte, nom_joueur)
        self.retirer_ressource(ressource, quantite_offerte)

    def retirer_echange(self, nom_joueur, param):
        ressource_offerte, quantite_offerte, id = param
        del self.liste_echange[id - 1]
        ressource = self.trouver_ressource(ressource_offerte, nom_joueur)
        self.ajouter_ressource(ressource, quantite_offerte)

    def accepter_offre(self, nom_joueur, param):
        ressource_offerte, quantite_offerte, ressource_demande, quantite_demande, id, nom_vendeur = param
        del self.liste_echange[id - 1]
        ressource_acheteur_ajouter = self.trouver_ressource(ressource_offerte, nom_joueur)
        ressource_acheteur_retirer = self.trouver_ressource(ressource_demande, nom_joueur)
        ressource_vendeur_ajouter = self.trouver_ressource(ressource_demande, nom_vendeur)
        self.ajouter_ressource(ressource_acheteur_ajouter, quantite_offerte)
        self.retirer_ressource(ressource_acheteur_retirer, quantite_demande)
        self.ajouter_ressource(ressource_vendeur_ajouter, quantite_demande)

    def ajouter_ressource(self, ressource, quantite):
        ressource.quantite += quantite

    def retirer_ressource(self, ressource, quantite):
        ressource.quantite -= quantite

    def trouver_ressource(self, ressource, nom_joueur):
        quantite = 0
        if ressource == "nourriture":
            quantite = self.parent.joueurs[nom_joueur].nourriture
        elif ressource == "cuivre":
            quantite = self.parent.joueurs[nom_joueur].cuivre
        elif ressource == "titanium":
            quantite = self.parent.joueurs[nom_joueur].titanium
        elif ressource == "eau":
            quantite = self.parent.joueurs[nom_joueur].eau
        elif ressource == "fer":
            quantite = self.parent.joueurs[nom_joueur].fer
        elif ressource == "energie":
            quantite = self.parent.joueurs[nom_joueur].energie
        return quantite


class Echange:
    def __init__(self, nom, ressource_offerte, quantite_offerte, ressource_demande, quantite_demande):
        self.nom = nom
        self.ressource_offerte = ressource_offerte
        self.ressource_demande = ressource_demande
        self.quantite_offerte = quantite_offerte
        self.quantite_demande = quantite_demande
