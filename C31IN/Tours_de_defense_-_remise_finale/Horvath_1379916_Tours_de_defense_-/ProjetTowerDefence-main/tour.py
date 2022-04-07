import helper

from monstre import Monstre


class Tour(object):
    prix = 400

    def __init__(self, x, y, rayon, demie_taille, vitesse_attaque=20, degat=50):
        self.voir_rayon = False
        self.x = x
        self.y = y
        self.rayon = rayon
        self.demie_taille = demie_taille
        self.vitesse_attaque = vitesse_attaque
        self.degat = degat
        self.niveau = 1
        self.delai_tire = 0
        self.liste_projectiles = []

    def analyse_rayon(self, monstre):
        if helper.Helper().calcDistance(self.x, self.y, monstre.x, monstre.y) <= self.rayon:
            return True

    def action(self, liste_monstre):
        self.delai_tire += 1
        for monstre in liste_monstre:
            if self.analyse_rayon(monstre) and self.delai_tire >= self.vitesse_attaque:
                if isinstance(self, Tour_Bombe):
                    self.liste_projectiles.append(Projectile_Bombe(self.x, self.y, self.degat, monstre))
                elif isinstance(self, Tour_Sniper):
                    self.liste_projectiles.append(Projectile(self.x, self.y, self.degat, monstre))
                else:
                    self.liste_projectiles.append(Projectile(self.x, self.y, self.degat, monstre))
                self.delai_tire = 0
        self.lancer_projectiles(liste_monstre)

    def lancer_projectiles(self, liste_monstre):
        if len(self.liste_projectiles) != 0:
            for projectile in self.liste_projectiles:
                projectile.lancer_projectile()
                if projectile.atteindre_cible(liste_monstre):
                    self.liste_projectiles.remove(projectile)

    def upgrade(self):
        self.niveau += 1

    def rayon_visible(self):
        self.voir_rayon = not self.voir_rayon


class Tour_Glace(Tour):
    prix = 300

    def __init__(self, x, y, rayon, demie_taille, id):
        Tour.__init__(self, x, y, rayon, demie_taille)
        self.vitesse_ralentissement = 0.2
        self.id = id
        self.prix_niveau = Tour_Glace.prix + 100

    def action(self, liste_monstre):

        for monstre in liste_monstre:

            if self.analyse_rayon(monstre):
                print(monstre.vitesse)
                monstre.vitesse = 1-self.vitesse_ralentissement
                monstre.frozen = True
                print(monstre.vitesse)
            else:
                monstre.vitesse = Monstre.vitesse
                monstre.frozen = False

    def upgrade(self):

        if self.niveau < 3:
            self.niveau += 1
            if self.niveau == 1:
                self.vitesse_ralentissement -= 0.2
            elif self.niveau == 2:
                self.prix_niveau += 200
                self.rayon += 25
            elif self.niveau == 3:
                self.prix_niveau = "max"
                self.vitesse_ralentissement -= 0.6


class Tour_Sniper(Tour):
    prix = 400

    def __init__(self, x, y, rayon, demie_taille, id):
        Tour.__init__(self, x, y, rayon, demie_taille, 60, 100)
        self.delai_tire = 0
        self.liste_projectiles = []
        self.id = id
        self.prix_niveau = Tour_Sniper.prix+100

    def upgrade(self):
        if self.niveau < 3:
            self.niveau += 1
            if self.niveau == 1:
                self.vitesse_attaque -= 20
            elif self.niveau == 2:
                self.prix_niveau += 200
                self.degat += 50
            elif self.niveau == 3:
                self.prix_niveau = "max"
                self.rayon += 50
                self.degat += 50
                self.vitesse_attaque -= 20


class Tour_Poison(Tour):
    degat = 0.15
    prix = 350
    stack_poison = 0

    def __init__(self, x, y, rayon, demie_taille, id):
        Tour.__init__(self, x, y, rayon, demie_taille)
        self.stack_poison = 0
        self.id = id
        self.prix_niveau = Tour_Poison.prix + 100

    def action(self, liste_monstre):
        for monstre in liste_monstre:
            if self.analyse_rayon(monstre):
                monstre.stack_poison += 1
                monstre.empoisonne = True

    def upgrade(self):
        if self.niveau < 3:
            self.niveau += 1
            if self.niveau == 1:
                self.rayon += 10
            elif self.niveau == 2:
                self.prix_niveau += 200
                pass
            elif self.niveau == 3:
                self.prix_niveau = "max"
                pass


class Tour_Bombe(Tour):
    prix = 500

    def __init__(self, x, y, rayon, demie_taille, id):
        Tour.__init__(self, x, y, rayon, demie_taille, 60, 50)
        self.delai_tire = 0
        self.liste_projectiles = []
        self.id = id
        self.niveau = 1
        self.prix_niveau = Tour_Bombe.prix + 100

    def upgrade(self):
        if self.niveau < 3:
            self.niveau += 1
            if self.niveau == 1:
                self.degat += 10
            elif self.niveau == 2:
                self.prix_niveau += 200
                self.vitesse_attaque -= 20
            elif self.niveau == 3:
                self.prix_niveau = "max"
                self.rayon += 10
                self.degat += 15
                self.vitesse_attaque -= 10


class Tour_Mitraillette(Tour):
    prix = 300

    def __init__(self, x, y, rayon, demie_taille, id):
        Tour.__init__(self, x, y, rayon, demie_taille, 10, 10)
        self.delai_tire = 0
        self.liste_projectiles = []
        self.id = id
        self.prix_niveau = Tour_Mitraillette.prix + 100

    def upgrade(self):
        if self.niveau < 3:
            self.niveau += 1
            if self.niveau == 1:
                self.vitesse_attaque -= 2
                self.degat += 3
            elif self.niveau == 2:
                self.prix_niveau += 200
                self.vitesse_attaque -= 3
                self.degat += 4
            elif self.niveau == 3:
                self.prix_niveau = "max"
                self.vitesse_attaque -= 4
                self.degat += 5


class Projectile(object):
    def __init__(self, x, y, degat, monstre):
        self.x = x
        self.y = y
        self.degat = degat
        self.vitesse = 20
        self.monstre = monstre
        self.delai = 0

    def lancer_projectile(self):
        self.delai += 1
        distance = helper.Helper.calcDistance(self.x, self.y, self.monstre.x, self.monstre.y)
        if distance > 0:
            angle = helper.Helper.calcAngle(self.x, self.y, self.monstre.x, self.monstre.y)
            cible = helper.Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
            self.x = cible[0]
            self.y = cible[1]

    def atteindre_cible(self, liste_monstre=None):
        if liste_monstre is None:
            liste_monstre = []
        isDead = False
        if self.monstre is None:
            isDead = True

        cibleX = self.monstre.x
        cibleY = self.monstre.y
        if (cibleX + 12 >= self.x >= cibleX - 12) and (cibleY + 12 >= self.y >= cibleY - 12):
            isDead = True
            self.monstre.vie -= self.degat

        return isDead


class Projectile_Bombe(Projectile):
    def __init__(self, x, y, degat, monstre):
        Projectile.__init__(self, x, y, degat, monstre)
        self.rayon = 100

    def atteindre_cible(self, liste_monstre):
        isDead = False

        if self.monstre is None:
            isDead = True

        cibleX = self.monstre.x
        cibleY = self.monstre.y
        if (cibleX + 12 >= self.x >= cibleX - 12) and (cibleY + 12 >= self.y >= cibleY - 12):
            isDead = True
            explosion_list = self.explosion(liste_monstre)
            for monstre_bombe in explosion_list:
                monstre_bombe.vie -= self.degat

        return isDead

    def explosion(self, monstre_list):
        explosion_list = []
        for monstre in monstre_list:
            if helper.Helper().calcDistance(self.x, self.y, monstre.x, monstre.y) <= self.rayon:
                explosion_list.append(monstre)
        return explosion_list
