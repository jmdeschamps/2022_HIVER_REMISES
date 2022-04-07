import tkinter.messagebox
from tkinter import *
from tkinter import simpledialog
import time
from helper import *


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.geometry("1200x900")
        self.root.title("TKTD, Vers1.0")
        self.creer_interface()
        self.background = 0

    def creer_interface(self):

        # TOP FRAME
        self.frame_stats = Frame(self.root, bg="#7FB069")

        # SCORE, EXP, $, ET TEMPS
        frame_stats1 = Frame(self.frame_stats, bg="#f5f5f5")
        frame_stats2 = Frame(self.frame_stats, bg="#f5f5f5")
        frame_stats3 = Frame(self.frame_stats, bg="#f5f5f5")
        frame_stats4 = Frame(self.frame_stats, bg="#f5f5f5")

        frame_stats1.pack(side=LEFT, expand=1)
        frame_stats2.pack(side=LEFT, expand=1)
        frame_stats3.pack(side=LEFT, expand=1)
        frame_stats4.pack(side=LEFT, expand=1)

        self.points_vie = StringVar()
        self.points_vie.set("0")
        self.score = StringVar()
        self.score.set("0")
        self.sagesse = StringVar()
        self.sagesse.set("0")
        self.argent = StringVar()
        self.argent.set("0")

        label_vie_text = Label(frame_stats1, text="          Vie:          ", bg="#FFFBBD", borderwidth=3,
                               relief="sunken")
        label_vie = Label(frame_stats1, text="          Vie:          ", textvariable=self.points_vie, bg="#FFFBBD",
                          borderwidth=3, relief="sunken")

        label_score = Label(frame_stats2, text="          Score:          ", bg="#FFFBBD", borderwidth=3,
                            relief="sunken")
        label_score_text = Label(frame_stats2, text="          Vie:          ", textvariable=self.score, bg="#FFFBBD",
                                 borderwidth=3, relief="sunken")
        label_sagesse = Label(frame_stats3, text="          Sagesse:          ", bg="#FFFBBD", borderwidth=3,
                              relief="sunken")
        label_sagesse_text = Label(frame_stats3, text="          Vie:          ", textvariable=self.sagesse,
                                   bg="#FFFBBD",
                                   borderwidth=3, relief="sunken")
        label_argent = Label(frame_stats4, text="          Argent:          ", bg="#FFFBBD", borderwidth=3,
                             relief="sunken")
        label_argent_text = Label(frame_stats4, text="          Vie:          ", textvariable=self.argent, bg="#FFFBBD",
                                  borderwidth=3, relief="sunken")

        label_vie_text.pack(expand=1)
        label_vie.pack(expand=1)

        label_score.pack(expand=1)
        label_score_text.pack(expand=1)

        label_sagesse.pack(expand=1)
        label_sagesse_text.pack(expand=1)

        label_argent.pack(expand=1)
        label_argent_text.pack(expand=1)

        # BOTTOM FRAME
        self.frame_bas = Frame(self.root, bg="#7FB069")

        # INFOS PARTIE, INFO TOUR, BOUTONS
        frame_infos_partie = Frame(self.frame_bas, borderwidth=3, relief="sunken")
        frame_infos_tour = Frame(self.frame_bas, borderwidth=3, relief="sunken")
        frame_bouttons = Frame(self.frame_bas, borderwidth=3, relief="sunken")
        frame_bouttons_row1 = Frame(frame_bouttons)
        frame_bouttons_row2 = Frame(frame_bouttons)

        frame_infos_partie.pack(expand=1, fill=BOTH, side=LEFT)
        frame_infos_tour.pack(expand=1, fill=BOTH, side=LEFT)
        frame_bouttons.pack(expand=1, fill=BOTH, side=LEFT)

        btn_tour_bleue = Button(frame_bouttons_row1, text="TOUR BLEUE (500$)", width=20)
        btn_tour_mauve = Button(frame_bouttons_row1, text="TOUR MAUVE (700$)", width=20)
        btn_tour_blanche = Button(frame_bouttons_row1, text="TOUR BLANCHE (1000$)", width=20)

        btn_debuter_partie = Button(frame_bouttons_row1, text="DÉBUTER PARTIE", width=20)
        btn_nouvelle_vague = Button(frame_bouttons_row2, text="NOUVELLE VAGUE", width=20)
        btn_creeps_ecran = Button(frame_bouttons_row2, text="NB CREEPS À L'ÉCRAN", width=20)

        label_map = Label(frame_infos_partie, text="INFO PARTIE: \n"
                                                   "Niveau: \n"
                                                   "# Vague: \n"
                                                   "# Bombes: \n"
                                                   "Kill Count: \n",
                          bg="#FFFBBD")
        label_tours = Label(frame_infos_tour, text="INFO TOUR \n À venir ", bg="#FFFBBD")
        label_acheter_tours = Label(frame_bouttons, text="Acheter tours: ", bg="#FFFBBD")

        label_map.pack(side=LEFT, expand=1)
        label_tours.pack(side=LEFT, expand=1)
        label_acheter_tours.pack(fill=X)
        btn_tour_bleue.pack(side=LEFT, fill=X)
        btn_tour_mauve.pack(side=LEFT, fill=X)
        btn_tour_blanche.pack(side=LEFT, fill=X)
        btn_debuter_partie.pack(side=LEFT, fill=X, expand=1)
        btn_nouvelle_vague.pack(side=TOP, fill=X, expand=1)
        btn_creeps_ecran.pack(side=TOP, fill=X, expand=1)
        frame_bouttons_row1.pack(fill=X, side=TOP)
        frame_bouttons_row2.pack(fill=X, side=LEFT)

        # le canevas de jeu
        self.canevas = Canvas(self.root, width=1200, height=600, bg="#D9F7FA", highlightthickness=0)

        btn_debuter_partie.bind("<Button-1>", self.parent.debuter_partie)
        btn_nouvelle_vague.bind("<Button-1>", self.parent.creer_niveau)
        btn_tour_bleue.bind("<Button-1>", self.parent.choisir_couleur_bleu)
        btn_tour_mauve.bind("<Button-1>", self.parent.choisir_couleur_mauve)
        btn_tour_blanche.bind("<Button-1>", self.parent.choisir_couleur_blanche)
        btn_creeps_ecran.bind("<Button-1>", self.modele.nb_creeps)

        # visualiser
        self.frame_stats.pack(fill=X)
        self.canevas.pack()
        self.frame_bas.pack(expand=1, fill=BOTH)

    def afficher_partie(self):
        self.points_vie.set(str(self.modele.partie.total_vie))
        self.argent.set(str(self.modele.partie.total_argent))
        self.sagesse.set(str(self.modele.partie.total_sagesse))
        self.score.set(str(self.modele.partie.total_points))

        self.canevas.delete("dynamique")
        self.canevas.delete("sentier")
        self.canevas.delete("projectile")

        if self.background == 0:
            self.canevas.create_rectangle(0, 600, 1200, 0, fill="#D9F7FA", tags="background")
            self.background += 1

        self.canevas.tag_bind("background", "<Button-1>", self.creer_tour)

        for i in self.modele.sentier[0]:
            self.canevas.create_line(i, width=40, fill="brown", tags=("sentier"))

        for i in self.modele.partie.niveau.liste_creep_a_l_ecran:
            x = i.x1
            y = i.y1
            self.canevas.create_oval(x - i.rayon, y - i.rayon, x + i.rayon, y + i.rayon, fill=i.couleur,
                                     tags=("dynamique"))

        for i in self.modele.partie.niveau.liste_de_projectile_a_l_ecran:
            if not i.creep_touche:
                x_p = i.position_projectile_x
                y_p = i.position_projectile_y
                couleur_projectile = None

                if i.couleur_projectile == 1:
                    couleur_projectile = "green"
                if i.couleur_projectile == 2:
                    couleur_projectile = "yellow"
                if i.couleur_projectile == 3:
                    couleur_projectile = "red"

                self.canevas.create_oval(x_p - i.rayon, y_p - i.rayon, x_p + i.rayon, y_p + i.rayon, fill=couleur_projectile,
                                         tags="projectile")

    def creer_tour(self, evt):
        couleur_tour = self.parent.modele.partie.couleur_choisie
        tour_creee = self.parent.creer_tour(evt, couleur_tour)
        if couleur_tour != 0:
            self.canevas.create_oval(evt.x - tour_creee.rayon, evt.y - tour_creee.rayon,
                                     evt.x + tour_creee.rayon, evt.y + tour_creee.rayon,
                                     fill=None, tags=("statique"))
        if couleur_tour == 1:
            couleur_tour = "blue"
        if couleur_tour == 2:
            couleur_tour = "purple"
        if couleur_tour == 3:
            couleur_tour = "white"
        if couleur_tour != 0:
            self.canevas.create_rectangle(evt.x + tour_creee.demitaillex, evt.y + tour_creee.demitailley,
                                          evt.x - tour_creee.demitaillex, evt.y - tour_creee.demitailley,
                                          fill=couleur_tour, tags=("statique"))

    def fin_partie(self):
        self.canevas.delete("statique")
        self.canevas.delete("dynamique")
        tkinter.messagebox.showinfo('Votre survie a échoué ',
                                    "Désirez-vous récupérer votre honneur?\n Appuyez débuter Partie",
                                    parent=self.parent.vue.root)

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partie = None
        self.sentier = [[
            [[0, 275], [240, 275]],
            [[240, 275], [240, 50]],
            [[240, 50], [840, 50]],
            [[840, 50], [840, 515]],
            [[840, 515], [1200, 515]]
        ]]

        self.chemins = [[0, 275, 315, 275, 315, 50, 840, 50, 840, 440, 1200, 440, 1200, 515,
                         840, 515, 765, 515, 765, 440, 765, 125, 390, 125, 390, 350, 240, 350, 0, 350, ]]

        self.largeur = 1200
        self.hauteur = 600
        self.debut = None
        self.duree = 0
        self.partie = None

    def nb_creeps(self, evt):
        print("ÉCRAN" ,len(self.partie.niveau.liste_creep_a_l_ecran))
        print("ATTENTE", len(self.partie.niveau.liste_creep_attente))

    def creer_partie(self):
        self.partie = Partie(self)
        print("Partie créée :", self.partie)

    def jouer_tour(self):
        self.partie.jouer_tour()


class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.total_creep_tues = 0
        self.total_points = 0
        self.total_vie = 100
        self.total_argent = 1000
        self.total_sagesse = 0
        self.niveau_actuel = 0
        self.niveau = Niveau(self, self.niveau_actuel)
        self.creeps_tues = 0
        self.couleur_choisie = 0
        self.i = 1  # Utiliser pour l'augmentation de la sagesse de niveau
        self.liste_tours = []

    def creer_niveau(self, evt):
        self.niveau.liste_creep_a_l_ecran.clear()
        self.niveau_actuel += 1
        self.niveau.fin_niveau = False
        self.niveau.creer_creeps()
        print("A L'ÉCRAN:", len(self.niveau.liste_creep_a_l_ecran))
        print("EN ATTENTE:", len(self.niveau.liste_creep_attente))

    def augmenter_sagesse(self):
        augsag = 50 * self.i
        self.i += 1
        return augsag

    def jouer_tour(self):
        self.niveau.jouer_tour()

    def choisir_couleur_bleu(self):
        print("couleur Bleue(1) choisie")
        self.couleur_choisie = 1

    def choisir_couleur_mauve(self):
        print("couleur Mauve(2) choisie")
        self.couleur_choisie = 2

    def choisir_couleur_blanche(self):
        print("couleur Blanche(3) choisie")
        self.couleur_choisie = 3

    def creer_tour(self,evt, couleur_tour):
        if couleur_tour == 1:
            if self.total_argent >= self.niveau.tour_bleue_valeur:
                self.total_argent -= self.niveau.tour_bleue_valeur
                tour_creee = Tour_Bleu(self, evt.x, evt.y)
                self.liste_tours.append(tour_creee)
                return tour_creee

        if couleur_tour == 2:
            if self.total_argent >= self.niveau.tour_mauve_valeur:
                self.total_argent -= self.niveau.tour_mauve_valeur
                tour_creee = Tour_Mauve(self, evt.x, evt.y)
                self.liste_tours.append(tour_creee)
                return tour_creee

        if couleur_tour == 3:
            if self.total_argent >= self.niveau.tour_blanche_valeur:
                self.total_argent -= self.niveau.tour_blanche_valeur
                tour_creee = Tour_Blanche(self, evt.x, evt.y)
                self.liste_tours.append(tour_creee)
                return tour_creee


class Niveau():
    def __init__(self, parent, niveau_actuel):
        self.parent = parent
        self.niveau_actuel = niveau_actuel
        self.ratio_creep = 50.0
        self.nombre_creep_total = self.ratio_creep * self.niveau_actuel
        self.liste_creep_attente = []
        self.liste_creep_a_l_ecran = []
        self.liste_de_projectile_a_l_ecran = []
        self.niveau_est_parfait = True
        self.bonus_niveau_parfait = 30
        self.ratio_bonus_niveau = 1.5
        self.sagesse_du_niveau = 50 * self.niveau_actuel
        self.ratio_creep_vert = 0.9
        self.ratio_creep_jaune = 0.1
        self.ratio_creep_rouge = 0.0
        self.delai = 0
        self.delai_nouveau_creep = 20
        self.tour_bleue_valeur = 500
        self.tour_mauve_valeur = 700
        self.tour_blanche_valeur = 1000
        self.fin_niveau = False
        self.creer_creeps()

    def jouer_tour(self):

        for i in self.liste_creep_a_l_ecran:
            i.jouer_tour()
            if i.x1 > self.parent.parent.largeur:
                self.parent.total_vie -= 5
                self.liste_creep_a_l_ecran.remove(i)
                self.niveau_est_parfait = False
                if self.parent.total_vie < 1:
                    self.parent.parent.parent.partie_en_cours = 0

            if i.vie_creep <= 0:
                self.parent.niveau.liste_creep_a_l_ecran.remove(i)
                self.parent.total_points += i.valeur_points
                self.parent.total_argent += i.valeur_monetaire_creep
                self.parent.creeps_tues += 1

        if len(self.liste_creep_a_l_ecran) <= 0:
            if self.fin_niveau == False and self.parent.creeps_tues > 0:
                if self.niveau_est_parfait:
                    self.parent.total_points += int(self.bonus_niveau_parfait * self.ratio_bonus_niveau)
                    self.parent.total_sagesse += int(self.parent.augmenter_sagesse() * self.ratio_bonus_niveau)
                    self.ratio_bonus_niveau += 0.05
                    self.liste_creep_a_l_ecran.clear()
                    self.fin_niveau = True
                else:
                    self.parent.total_sagesse += self.parent.augmenter_sagesse()
                    self.liste_creep_a_l_ecran.clear()
                    self.fin_niveau = True

        if self.delai < 1:
            if self.liste_creep_attente:
                rep = self.liste_creep_attente.pop(0)
                self.liste_creep_a_l_ecran.append(rep)
                self.delai = self.delai_nouveau_creep
        else:
            self.delai -= 1

            for j in self.parent.liste_tours:
                j.verification_range()
                for k in self.liste_de_projectile_a_l_ecran:
                    k.projectile_a_tete_chercheuse()
                    if k.creep_touche:
                        self.liste_de_projectile_a_l_ecran.remove(k)

    def creer_creeps(self):
        if self.ratio_creep_vert > 0:
            for i in range(int(self.ratio_creep * self.ratio_creep_vert)):
                self.liste_creep_attente.append(Creep_vert())

        for i in range(int(self.ratio_creep * self.ratio_creep_jaune)):
            self.liste_creep_attente.append(Creep_jaune())

        for i in range(int(self.ratio_creep * self.ratio_creep_rouge)):
            self.liste_creep_attente.append(Creep_rouge())

        self.liste_creep_attente.append(Boss())

        self.ratio_creep_vert -= 0.05
        self.ratio_creep_jaune += 0.1
        self.ratio_creep_rouge += 0.05

    def incrementer_niveau(self, evt):
        if len(self.liste_creep_attente) <= 0 and len(self.liste_creep_a_l_ecran) <= 0:
            self.niveau_actuel += 1

    def mettre_creeps_en_jeu(self):
        if len(self.liste_creep_attente) >= 0:
            tmp = self.liste_creep_attente.pop(0)
            self.liste_creep_a_l_ecran.append(tmp)


class Creep():
    def __init__(self, parent):
        self.parent = parent
        self.vie_creep = 42
        self.x1 = 0
        self.y1 = 275
        self.rayon = 15
        self.valeur_monetaire_creep = 0
        self.vitesse_creep_X = 5
        self.vitesse_creep_Y = 5
        self.troncon = 0

        self.max1 = 237
        self.max2 = 55
        self.max3 = 835
        self.max4 = 505
        self.max5 = 1210

        self.est_cible = False
        self.est_vivant = False
        self.est_en_attente = False
        self.faiblesse_a = False
        self.faiblesse_b = False
        self.faiblesse_c = False

    def jouer_tour(self):
        self.deplacement()

    def deplacement(self):

        if self.x1 < self.max1:
            self.x1 += self.vitesse_creep_X
        elif self.x1 >= self.max1 and self.y1 >= self.max2 and self.x1 < 400:
            self.y1 -= self.vitesse_creep_Y
        elif self.y1 <= self.max2 and self.x1 <= self.max3:
            self.x1 += self.vitesse_creep_X
        elif self.x1 >= self.max3 and self.y1 <= self.max4 and self.x1 > 400:
            self.y1 += self.vitesse_creep_Y
        elif self.y1 <= self.max3 and self.x1 <= self.max5 and self.x1 > 400:
            self.x1 += self.vitesse_creep_X


class Creep_vert(Creep):
    def __init__(self):
        Creep.__init__(self, Creep)
        self.vie_creep = 60
        self.valeur_monetaire_creep = 50
        self.vitesse_creep = 4
        self.faiblesse_c = True
        self.valeur_points = 100
        self.couleur = "green"


class Creep_jaune(Creep):
    def __init__(self):
        Creep.__init__(self, Creep)
        self.vie_creep = 90
        self.valeur_monetaire_creep = 100
        self.vitesse_creep = 6
        self.faiblesse_a = True
        self.valeur_points = 200
        self.couleur = "yellow"


class Creep_rouge(Creep):
    def __init__(self):
        Creep.__init__(self, Creep)
        self.vie_creep = 150
        self.valeur_monetaire_creep = 150
        self.vitesse_creep = 3
        self.faiblesse_a = True
        self.valeur_points = 300
        self.couleur = "red"


class Boss(Creep):
    def __init__(self):
        Creep.__init__(self, Creep)
        self.vie_creep = 450
        self.valeur_monetaire_creep = 300
        self.rayon = 15
        self.couleur = "pink"
        self.valeur_points = 500


class Tour():
    def __init__(self, parent, x, y):
        self.couleur_tour = None
        self.parent = parent
        self.position_x_tour = x
        self.position_y_tour = y
        self.demitaillex = 25
        self.demitailley = 50
        self.valeur_monnetaire_tour = 0
        self.rayon = 150
        self.valeur_vente = 0
        self.cooldown = 0
        self.placement_valide = False

    def verification_range(self):
        liste = self.parent.parent.partie.niveau.liste_creep_a_l_ecran
        for i in liste:
            distance = Helper.calcDistance(i.x1, i.y1, self.position_x_tour, self.position_y_tour)
            somme_rayon = i.rayon + self.rayon
            if distance < somme_rayon:
                if self.cooldown == 0:
                    i.est_cible = True
                    self.tirer_creep(i)
                    self.cooldown = 20

        if self.cooldown > 0:
            self.cooldown -= 1

    def tirer_creep(self, creep_cible):
        if self.couleur_tour == 1:
            self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(Projectil_a(self.position_x_tour,self.position_y_tour,creep_cible))
        if self.couleur_tour == 2:
            self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(Projectil_b(self.position_x_tour,self.position_y_tour,creep_cible))
        if self.couleur_tour == 3:
            self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(Projectil_c(self.position_x_tour,self.position_y_tour,creep_cible))


class Tour_Bleu(Tour):
    def __init__(self, parent, x, y):
        Tour.__init__(self, parent, x, y)
        self.valeur_monnetaire_tour = 500
        self.couleur_tour = 1


class Tour_Mauve(Tour):
    def __init__(self, parent, x, y):
        Tour.__init__(self, parent, x, y)
        self.valeur_monnetaire_tour = 700
        self.couleur_tour = 2


class Tour_Blanche(Tour):
    def __init__(self, parent, x, y):
        Tour.__init__(self, parent, x, y)
        self.valeur_monnetaire_tour = 1000
        self.couleur_tour = 3


class Projectile():
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible):
        self.position_projectile_x = position_projectile_x
        self.position_projectile_y = position_projectile_y
        self.degats = 0
        self.vitesse_projectile = 0
        self.rayon = 10
        self.creep_touche = False
        self.creep_cible = creep_cible
        self.projectile_a_tete_chercheuse()
        self.couleur_projectile = ""

    def projectile_a_tete_chercheuse(self):
        distance_projectile = Helper.calcDistance(self.position_projectile_x, self.position_projectile_y,
                                                  self.creep_cible.x1, self.creep_cible.y1)
        angle_projectile = Helper.calcAngle(self.position_projectile_x, self.position_projectile_y, self.creep_cible.x1,
                                            self.creep_cible.y1)
        cible_projectile = Helper.getAngledPoint(angle_projectile, self.vitesse_projectile, self.position_projectile_x,
                                                 self.position_projectile_y)

        self.position_projectile_x = cible_projectile[0]
        self.position_projectile_y = cible_projectile[1]
        if distance_projectile < 15:
            self.creep_touche = True
        if self.creep_touche:
            if self.creep_cible.vie_creep > 0:
                self.creep_cible.vie_creep -= self.degats


class Projectil_a(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible):
        Projectile.__init__(self, position_projectile_x, position_projectile_y, creep_cible)
        self.couleur_projectile = 1
        self.degats = 30
        self.vitesse_projectile = 6


class Projectil_b(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible):
        Projectile.__init__(self, position_projectile_x, position_projectile_y, creep_cible)
        self.couleur_projectile = 2
        self.degats = 45
        self.vitesse_projectile = 4


class Projectil_c(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible):
        Projectile.__init__(self, position_projectile_x, position_projectile_y, creep_cible)
        self.couleur_projectile = 3
        self.degats = 60
        self.vitesse_projectile = 2


class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop() 

    def mettre_creeps_en_jeu(self):
        self.modele.partie.niveau.mettre_creeps_en_jeu()

    def debuter_partie(self, evt):
        self.partie_en_cours = 1
        self.modele.creer_partie()
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.vue.afficher_partie()
            self.vue.root.after(40, self.jouer_partie)
        else:
            self.vue.fin_partie()

    def choisir_couleur_bleu(self, evt):
        if self.partie_en_cours != 0:
            self.modele.partie.choisir_couleur_bleu()

    def choisir_couleur_mauve(self, evt):
        if self.partie_en_cours != 0:
            self.modele.partie.choisir_couleur_mauve()

    def choisir_couleur_blanche(self, evt):
        if self.partie_en_cours != 0:
            self.modele.partie.choisir_couleur_blanche()

    def creer_tour(self, evt, couleur_tour):
        return self.modele.partie.creer_tour(evt, couleur_tour)

    def creer_niveau(self, evt):
        self.modele.partie.creer_niveau(evt)


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
