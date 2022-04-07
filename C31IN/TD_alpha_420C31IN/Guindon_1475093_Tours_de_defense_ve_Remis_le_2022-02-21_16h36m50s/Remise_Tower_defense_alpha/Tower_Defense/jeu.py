from partie import Partie


class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.largeur_fenetre = 1400
        self.hauteur_fenetre = 800
        self.largeur_canevas = 1200
        self.hauteur_canevas = 600

        self.argent = 500 # montant initiale
        self.vie = 5 # vie initiale
        self.score = 0 # score initiale
        self.exp = 0 # à voir si l'expérience va avec le joueur où la partie
        self.message = "Appuyer sur COMMENCER pour lancer la partie"
        self.demarrage = 0
        self.en_cours = False
        self.partie_courante = Partie(self)
        self.demarrage = 0
        self.compteur_activation = 0
        self.compteur_attaque_feu = 0
        self.compteur_attaque_poison = 0
        self.compteur_attaque_glace = 0
        self.compteur_attaque_mitraille = 0

        self.compteur_nbr_attaques_poison = 0
        self.compteur_retirer_poison = 0

    # Maxence
    def en_jeu(self):
        self.en_cours = True
        self.partie_courante.peut_ajouter_creep = True

    # À la fin des explications de début de niveau, un booléan nous permettra de lancer cette fonction.
    def initialiser_partie(self):
        if (self.demarrage):
            pass
            # Déverrouiller les tours
            # Déverrouiller les boutons pour lancer la vague
        pass

    def fin_vague(self):
        self.partie_courante.fin_vague()

    def creer_creeps(self):
        self.partie_courante.creer_creeps()

    def activer_creep(self):
        self.partie_courante.activer_creep()
        self.compteur_activation = 0

    def deplacer_creeps(self):
        self.partie_courante.deplacer_creeps()

    def animer_creeps(self):
        self.partie_courante.animer_creeps()

    def verifier_attaque_forteresse(self):
        self.partie_courante.verifier_attaque_forteresse()

    def traiter_creation_tour(self, clic_x, clic_y, type_tour):
        creation_confirme = self.partie_courante.traiter_creation_tour(clic_x, clic_y, type_tour)
        if creation_confirme:
            return True
        else:
            return False

    def demarrer_chrono(self):
        self.partie_courante.demarrer_chrono()

    def verifier_creep_en_zone_danger(self, type_tour):
        self.partie_courante.verifier_creep_en_zone_danger(type_tour)

    def deplacer_projectiles(self):
        self.partie_courante.deplacer_projectiles()

    def decrementer_attaques_poison(self):
        self.partie_courante.decrementer_attaques_poison()

    def retirer_projectile(self, tour_source, projectile, cible_a_retirer=None):
        self.partie_courante.retirer_projectile(tour_source, projectile, cible_a_retirer)

    def update_message(self, message):
        self.parent.update_message(message)

    def update_exp(self):
        self.parent.update_exp()

    def update_argent(self):
        self.parent.update_argent()

    def update_score(self):
        self.parent.update_score()

    def game_over(self):
        self.parent.game_over()
        
    def update_commencer(self, message):
        self.parent.update_commencer(message)
