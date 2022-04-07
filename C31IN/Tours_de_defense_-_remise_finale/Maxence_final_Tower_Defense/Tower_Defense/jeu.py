from partie import Partie
from PIL import Image, ImageTk


class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.largeur_fenetre = 1400
        self.hauteur_fenetre = 800
        self.largeur_canevas = 1200
        self.hauteur_canevas = 600
        self.argent = 500 # montant initiale
        self.vie = 50 # vie initiale
        self.score = 0 # score initiale
        self.exp = 0  # à voir si l'expérience va avec le joueur où la partie
        self.niveau_joueur = [0, 100, 350, 725, 1290, 2134, 3400, 5300, 8150, 12425] #10 niveau au total
        self.message = "Appuyer sur COMMENCER pour lancer la partie"
        self.demarrage = 0
        self.en_cours = False
        self.tours_cout = {
            'FEU': 180,
            'GLACE': 220,
            'POISON': 275,
            'MITRAILLE': 335
        }
        self.partie_courante = Partie(self)
        self.demarrage = 0
        self.compteur_activation = 0
        self.compteur_attaque_feu = 0
        self.compteur_attaque_poison = 0
        self.compteur_attaque_glace = 0
        self.compteur_attaque_mitraille = 0

        self.compteur_nbr_attaques_poison = 0
        self.compteur_retirer_poison = 0

        self.dic_img_creep_1 = {
            "droite" : [],
            "gauche" : [],
            "bas" : [],
            "haut" : [],
        }

        self.dic_img_creep_2 = {
            "droite" : [],
            "gauche" : [],
            "bas" : [],
            "haut" : [],
        }

        self.dic_img_creep_3 = {
            "droite" : [],
            "gauche" : [],
            "bas" : [],
            "haut" : [],
        }

        self.dic_img_creep_4 = {
            "droite" : [],
            "gauche" : [],
            "bas" : [],
            "haut" : [],
        }

        # dictionnaire pour les images du boss
        self.dic_img_creep_5 = {
            "droite" : [],
            "gauche" : [],
            "bas" : [],
            "haut" : [],
        }

        self.dic_img_tour = {
            "glace" : [],
            "feu" : [],
            "poison" : [],
            "mitraille" : [],
        }

        self.dic_autre = {
            "background": []
        }

        self.dic_img = {
            "creep1" : self.dic_img_creep_1,
            "creep2" : self.dic_img_creep_2,
            "creep3" : self.dic_img_creep_3,
            "creep4" : self.dic_img_creep_4,
            "creep5" : self.dic_img_creep_5,
            "tour" : self.dic_img_tour,
            "autre" : self.dic_autre, #boutton et background, autres
        }

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
    
    def partie_gagnee(self):
        self.parent.partie_gagnee()

    def update_vie(self, message):
        self.parent.update_vie(message)

    def update_commencer(self, message):
        self.parent.update_commencer(message)

    def charger_images(self):
        # Creeps #
        index_cle1 = 0  # va jusqu'à 4 ( 5 creeps )
        cle1 = ["creep1", "creep2", "creep3", "creep4", "creep5"]
        index_cle2 = 0  # va jusqu'à 3 ( 4 directions )
        cle2 = ["droite", "gauche", "bas", "haut"]
        index_cle3 = 0  # va jusqu'à 5 ( 6 images )
        cle3 = ["walk1.png", "walk2.png", "walk3.png", "walk4.png", "walk5.png", "walk6.png"]
        for i in cle1:
            index_cle2 = 0
            for j in cle2:
                index_cle3 = 0
                for k in cle3:
                    img_creep = Image.open("images/" + cle1[index_cle1] + "/" + cle2[index_cle2] + "/" + cle3[index_cle3])
                    img = ImageTk.PhotoImage(img_creep)
                    self.dic_img[cle1[index_cle1]][cle2[index_cle2]].append(img)
                    img_creep.close()
                    # cle1 correspond à 1ère clé, cle2 correspond à la 2e clé
                    index_cle3 += 1
                index_cle2 += 1
            index_cle1 += 1
        # Background #
        img_bg = Image.open(self.partie_courante.sentier.image)
        img = ImageTk.PhotoImage(img_bg)
        self.dic_img['autre']['background'].append(img)
        img_bg.close()
        # Tours #
        img_tour_feu = Image.open("images/Towers/Tour_feu.png").resize((35, 35), Image.ANTIALIAS)
        image_tour_feu = ImageTk.PhotoImage(img_tour_feu)
        self.dic_img["tour"]["feu"].append(image_tour_feu)
        img_tour_feu.close()
        img_tour_glace = Image.open("images/Towers/Tour_bois.png").resize((35, 35), Image.ANTIALIAS)
        image_tour_glace = ImageTk.PhotoImage(img_tour_glace)
        self.dic_img["tour"]["glace"].append(image_tour_glace)
        img_tour_glace.close()
        img_tour_poison = Image.open("images/Towers/Tour_poison.png").resize((35, 35), Image.ANTIALIAS)
        image_tour_poison = ImageTk.PhotoImage(img_tour_poison)
        self.dic_img["tour"]["poison"].append(image_tour_poison)
        img_tour_poison.close()
        img_tour_mitraille = Image.open("images/Towers/Tour_roche.png").resize((35, 35), Image.ANTIALIAS)
        image_tour_mitraille = ImageTk.PhotoImage(img_tour_mitraille)
        self.dic_img["tour"]["mitraille"].append(image_tour_mitraille)
        img_tour_mitraille.close()

    def verifier_direction_creep(self, creep):
        self.partie_courante.verifier_direction_creep(creep)

    def ameliorer_tour(self, tour):
        confirmation = self.partie_courante.ameliorer_tour(tour)
        return confirmation

    def vendre_tour(self,tour):
        self.partie_courante.vendre_tour(tour)

    def calculer_niveau_joueur(self):
        for i in self.niveau_joueur:
            if self.exp < i:
                return self.niveau_joueur.index(i)

    def determiner_type(self, x,y, tour):
        x = x
        y = y
        if tour.type == "FEU":
            for tour_feu in self.partie_courante.tours_feu:
                if tour_feu.x - tour_feu.largeur / 2 <= x <= tour_feu.x + tour_feu.largeur / 2:
                    if tour_feu.y - tour_feu.longueur / 2 <= y <= tour_feu.y + tour_feu.longueur / 2:
                        tour_selectionnee = tour_feu
                        break
        if tour.type == "GLACE":
            for tour_glace in self.partie_courante.tours_glace:
                if tour_glace.x - tour_glace.largeur / 2 <= x <= tour_glace.x + tour_glace.largeur / 2:
                    if tour_glace.y - tour_glace.longueur / 2 <= y <= tour_glace.y + tour_glace.longueur / 2:
                        tour_selectionnee = tour_glace
                        break
        if tour.type == "POISON":
            for tour_poison in self.partie_courante.tours_poison:
                if tour_poison.x - tour_poison.largeur / 2 <= x <= tour_poison.x + tour_poison.largeur / 2:
                    if tour_poison.y - tour_poison.longueur / 2 <= y <= tour_poison.y + tour_poison.longueur / 2:
                        tour_selectionnee = tour_poison
                        break
        if tour.type == "MITRAILLE":
            for tour_mitraille in self.partie_courante.tours_mitraille:
                if tour_mitraille.x - tour_mitraille.largeur / 2 <= x <= tour_mitraille.x + tour_mitraille.largeur / 2:
                    if tour_mitraille.y - tour_mitraille.longueur / 2 <= y <= tour_mitraille.y + tour_mitraille.longueur / 2:
                        tour_selectionnee = tour_mitraille
                        break
        return tour_selectionnee