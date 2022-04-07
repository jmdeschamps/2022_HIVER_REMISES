from jeu import Jeu
from vue import Vue


class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def jouer(self):
        if self.modele.partie_courante.peut_ajouter_creep:
            self.modele.creer_creeps()
        # Activation des creeps selon un interval de 1sec
        if self.modele.compteur_activation == 15:
            self.modele.activer_creep()
        self.modele.compteur_activation += 1
        # Déplacement des creeps
        self.modele.deplacer_creeps()
        # Animer les creeps
        self.modele.animer_creeps()

        # Vérifie si un creep franchit le sentier
        self.verifier_attaque_forteresse()

        # Vérifier si un creep est dans la zone d'attaque d'une tour
        # -> depuis cette méthode -> invocation de l'affichage d'attaque
        if self.modele.compteur_attaque_feu == 4:
            self.verifier_creep_en_zone_danger("FEU")
            self.modele.compteur_attaque_feu = 0
        self.modele.compteur_attaque_feu += 1


        # Vérifier si un creep est dans la zone d'attaque d'une tour Glace
        # -> depuis cette méthode -> invocation de l'affichage d'attaque
        if self.modele.compteur_attaque_glace == 20:
            self.verifier_creep_en_zone_danger("GLACE")
            self.modele.compteur_attaque_glace = 0
        self.modele.compteur_attaque_glace += 1

        if self.modele.compteur_attaque_mitraille == 20:
            self.verifier_creep_en_zone_danger("MITRAILLE")
            self.modele.compteur_attaque_mitraille = 0
        self.modele.compteur_attaque_mitraille += 1

        # Déplacement des projectiles + retrait des projectiles
        self.deplacer_projectiles()

        # Affichage des objets ( creeps et ? tours + attaques ? )
        self.vue.afficher_objets()

        # Vérifier si un creep est dans la zone d'attaque d'une tour
        # -> depuis cette méthode -> invocation de l'affichage d'attaque
        if self.modele.compteur_attaque_poison == 20:
            if self.modele.compteur_nbr_attaques_poison == 2:
                self.decrementer_attaques_poison()
                self.modele.compteur_nbr_attaques_poison = 0
            self.verifier_creep_en_zone_danger("POISON")
            self.modele.compteur_attaque_poison = 0
            self.modele.compteur_nbr_attaques_poison += 1
        self.modele.compteur_attaque_poison += 1

        # Boucle avec taux de rafraîchissement de 40ms
        if len(self.modele.partie_courante.creeps) > 0:
            self.vue.root.after(40, self.jouer)
        # Vérifier si le nombre de creeps a été éliminé
        else:
            est_valide = True
            for i in self.modele.partie_courante.creeps:
                if not i.est_actif:
                    est_valide = False
                    break
            if est_valide:
                # On doit afficher une derniere fois car le programme n'a pas le temps de supprimer le dernier creep mort
                # avant d'afficher les objets dans la dernière boucle
                self.vue.effacer_projectiles()
                self.vue.afficher_objets()
                self.modele.fin_vague()

    def en_jeu(self):
        self.modele.en_jeu()

    def traiter_creation_tour(self, clic_x, clic_y, type_tour):
        # if selection_tour_depuis_menu:
        est_valide = self.modele.traiter_creation_tour(clic_x, clic_y, type_tour)
        if est_valide:
            self.vue.unbind_creation_tour()
            self.vue.afficher_tours()

    def demarrer_chrono(self):
        self.modele.demarrer_chrono()

    def verifier_attaque_forteresse(self):
        # Si un des creeps franchit le sentier, attaque la forteresse ( à partir de la vue )
        self.modele.verifier_attaque_forteresse()

    def verifier_creep_en_zone_danger(self, type_tour):
        self.modele.verifier_creep_en_zone_danger(type_tour)

    def deplacer_projectiles(self):
        self.modele.deplacer_projectiles()

    def decrementer_attaques_poison(self):
        self.modele.decrementer_attaques_poison()

    def retirer_poison(self):
        self.modele.retirer_poison()

    def verifier_fin_vague(self):
        self.modele.partie_courante.fin_vague()

    def retirer_projectile(self, tour_source, projectile, cible_a_retirer=None):
        self.modele.retirer_projectile(tour_source, projectile, cible_a_retirer)

    def update_message(self, message):
        self.vue.update_message_tutoriel(message)

    def update_exp(self):
        self.vue.update_exp()

    def update_argent(self):
        self.vue.update_argent()

    def update_score(self):
        self.vue.update_score()

    def game_over(self):
        self.vue.creer_page_fin_partie()
        
    def update_commencer(self, message):
        self.vue.update_commencer(message)

