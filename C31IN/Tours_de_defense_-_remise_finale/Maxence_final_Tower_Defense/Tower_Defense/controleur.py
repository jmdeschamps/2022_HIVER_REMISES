from jeu import Jeu
from vue import Vue
import os

class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)
        self.vitesse_jeu = 100
        self.vit_jeu = False
        self.pause = False
        self.en_cours = True
        self.vue.root.mainloop()

    def jouer(self):
        if not self.pause:
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
            if self.modele.compteur_attaque_glace == 30:
                self.verifier_creep_en_zone_danger("GLACE")
                self.modele.compteur_attaque_glace = 0
            self.modele.compteur_attaque_glace += 1

            if self.modele.compteur_attaque_poison == 20:
                if self.modele.compteur_nbr_attaques_poison == 2:
                    self.decrementer_attaques_poison()
                    self.modele.compteur_nbr_attaques_poison = 0
                self.verifier_creep_en_zone_danger("POISON")
                self.modele.compteur_attaque_poison = 0
                self.modele.compteur_nbr_attaques_poison += 1
            self.modele.compteur_attaque_poison += 1

            if self.modele.compteur_attaque_mitraille == 20:
                self.verifier_creep_en_zone_danger("MITRAILLE")
                self.modele.compteur_attaque_mitraille = 0
            self.modele.compteur_attaque_mitraille += 1

            # Déplacement des projectiles + retrait des projectiles
            self.deplacer_projectiles()

            # Affichage des objets ( creeps et ? tours + attaques ? )
            self.vue.afficher_objets()

        if len(self.modele.partie_courante.creeps) > 0:
            self.vue.root.after(self.vitesse_jeu, self.jouer)
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

    def update_vie(self, message):
        self.vue.update_vie(message)

    def update_score(self):
        self.vue.update_score()

    def update_commencer(self, message):
        self.vue.update_commencer(message)

    def game_over(self):
        self.pause = True
        self.en_cours = False
        self.vue.creer_page_fin_partie()

    def partie_gagnee(self):
        self.pause = True
        self.en_cours = False
        self.vue.creer_page_fin_partie_sucess()
        
    def update_commencer(self, message):
        self.vue.update_commencer(message)

    def changement_vitesse(self):
        if not self.vit_jeu:
            self.vitesse_jeu = 20
            self.vit_jeu = True
        else:
            self.vitesse_jeu = 40
            self.vit_jeu = False

    def changement_pause(self):
        if self.en_cours:
            self.pause = True
            self.en_cours = False
        else:
            self.pause = False
            self.en_cours = True

    def charger_images(self):
        self.modele.charger_images()
        print(self.modele.dic_img)


    def reinitialiser_jeu(self):
        self.vue.root.destroy()
        os.system("python main.py")

    def verifier_direction_creep(self, creep):
        self.modele.verifier_direction_creep(creep)

    def bind_tour(self, type_tour):
        self.vue.bind_tour(type_tour)

    def ameliorer_tour(self, tour):
        confirmation = self.modele.ameliorer_tour(tour)
        return confirmation

    def vendre_tour(self,tour):
        self.modele.vendre_tour(tour)

    def determiner_type(self, x, y, tour):
        tour = self.modele.determiner_type(x,y, tour)
        return tour