import helper
import projectile


class Tour:
    prix = 400

    def __init__(self, x, y, rayon, demie_taille):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.demie_taille = demie_taille
        self.delai_tire = 0
        self.liste_projectiles = []
        self.vitesse_attaque = 20
        self.degat = 50
        # mitraillette vitesse = 2

    def analyse_rayon(self, monstre):
        if helper.Helper().calcDistance(self.x, self.y, monstre.x, monstre.y) <= self.rayon:
            return True

    def attaque(self, liste_monstre):
        self.delai_tire += 1
        for monstre in liste_monstre:
            if self.analyse_rayon(monstre) and self.delai_tire >= self.vitesse_attaque:
                self.liste_projectiles.append(projectile.Projectile(self, monstre))
                self.delai_tire = 0
        self.lancer_projectiles(liste_monstre)

    def lancer_projectiles(self, liste_monstre):
        if len(self.liste_projectiles) != 0:
            for projectile in self.liste_projectiles:
                projectile.lancer_projectile()
                if projectile.atteindre_cible():
                    self.liste_projectiles.remove(projectile)