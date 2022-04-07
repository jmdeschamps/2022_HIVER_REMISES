import random
import tkinter.messagebox
from tkinter import *
from tkinter import simpledialog
import time
from helper import *
from PIL import ImageTk, Image
import re

id = 0


def creer_id():
    global id
    id += 1
    monid = "id : " + str(id)
    return monid


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.geometry("1200x900")
        self.root.title("TKTD, Vers1.0")
        self.creer_interface()
        self.background = 0
        self.tour_choix = None

    def creer_interface(self):

        # TOP FRAME
        self.frame_stats = Frame(self.root, bg="#000000")

        # SCORE, EXP, $, ET TEMPS
        frame_stats1 = Frame(self.frame_stats, bg="#000000")
        frame_stats2 = Frame(self.frame_stats, bg="#000000")
        frame_stats3 = Frame(self.frame_stats, bg="#000000")
        frame_stats4 = Frame(self.frame_stats, bg="#000000")
        frame_stats5 = Frame(self.frame_stats, bg="#000000")

        frame_stats1.pack(side=LEFT, expand=1)
        frame_stats2.pack(side=LEFT, expand=1)
        frame_stats3.pack(side=LEFT, expand=1)
        frame_stats4.pack(side=LEFT, expand=1)
        frame_stats5.pack(side=LEFT, expand=1)

        self.points_vie = StringVar()
        self.points_vie.set("0")
        self.score = StringVar()
        self.score.set("0")
        self.sagesse = StringVar()
        self.sagesse.set("0")
        self.argent = StringVar()
        self.argent.set("0")
        self.meilleur_score = StringVar()
        self.meilleur_score.set("0")


        label_meilleur_score = Label(frame_stats1, text="High Score:", bg="#000000", borderwidth=3,
                                     relief="sunken", fg="#FFF", font="Courier 16 bold")
        label_meilleur_score_text =Label(frame_stats1, text="Vie:", textvariable=self.meilleur_score, bg="#000000",
                                         borderwidth=3, relief="sunken", font="Courier 24 bold", fg="#FFF")

        label_score = Label(frame_stats2, text="Score:", bg="#000000", borderwidth=3,
                            relief="sunken", fg="#FFF", font="Courier 16 bold")
        label_score_text = Label(frame_stats2, text="Vie:", textvariable=self.score, bg="#000000",
                                 borderwidth=3, relief="sunken", font="Courier 24 bold", fg="#FFF")

        label_vie_text = Label(frame_stats3, text="État du système:", bg="#000000", borderwidth=3,
                               relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_vie = Label(frame_stats3, text="Vie:", textvariable=self.points_vie, bg="#000000",
                          borderwidth=3, relief="sunken", font="Courier 24 bold", fg="#FFF")

        label_sagesse = Label(frame_stats4, text="Sagesse(௹):", bg="#000000", borderwidth=3,
                              relief="sunken", fg="#FFF", font="Courier 16 bold")
        label_sagesse_text = Label(frame_stats4, text="Vie:", textvariable=self.sagesse,
                                   bg="#000000", borderwidth=3, relief="sunken", font="Courier 24 bold", fg="#FFF")
        label_argent = Label(frame_stats5, text="Argent(৳):", bg="#000000", borderwidth=3,
                             relief="sunken", fg="#FFF", font="Courier 16 bold")
        label_argent_text = Label(frame_stats5, text="", textvariable=self.argent, bg="#000000",
                                  borderwidth=3, relief="sunken", font="Courier 24 bold", fg="#FFF")



        label_score.pack(expand=1)
        label_score_text.pack(expand=1)

        label_vie_text.pack(expand=1)
        label_vie.pack(expand=1)

        label_sagesse.pack(expand=1)
        label_sagesse_text.pack(expand=1)

        label_argent.pack(expand=1)
        label_argent_text.pack(expand=1)

        label_meilleur_score.pack(expand=1)
        label_meilleur_score_text.pack(expand=1)

        # BOTTOM FRAME
        self.frame_bas = Frame(self.root, bg="#7FB069")

        # INFOS PARTIE, INFO TOUR, BOUTONS
        frame_infos_partie = Frame(self.frame_bas, borderwidth=3, relief="sunken", bg="#000000")
        frame_infos_partie1 = Frame(frame_infos_partie, borderwidth=3, relief="sunken", bg="#000000")
        frame_infos_partie2 = Frame(frame_infos_partie, borderwidth=3, relief="sunken", bg="#000000")
        frame_infos_partie3 = Frame(frame_infos_partie, borderwidth=3, relief="sunken", bg="#000000")

        # frame_infos_tour = Frame(self.frame_bas, borderwidth=3, relief="sunken", bg="#000000")
        frame_bouttons = Frame(self.frame_bas, borderwidth=3, relief="sunken", bg="#000000")
        frame_bouttons_row1 = Frame(frame_bouttons)
        frame_bouttons_row2 = Frame(frame_bouttons)
        frame_bouttons_row3 = Frame(frame_bouttons)
        frame_bouttons_row4 = Frame(frame_bouttons)

        ##label debuter partie

        self.niveau = StringVar()
        self.niveau.set("0")
        self.bombes = StringVar()
        self.bombes.set("0")
        self.nbcreepstues = StringVar()
        self.nbcreepstues.set("0")
        label_niveau = Label(frame_infos_partie1, text="Niveau:", bg="#000000", borderwidth=3,
                             relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_niveau_texte = Label(frame_infos_partie1, textvariable=self.niveau, bg="#000000", borderwidth=3,
                                   relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_bombes = Label(frame_infos_partie2, text="Scans:", bg="#000000", borderwidth=3,
                             relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_bombes_texte = Label(frame_infos_partie2, textvariable=self.bombes, bg="#000000", borderwidth=3,
                                   relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_creeps_tues = Label(frame_infos_partie3, text="Virus tués:", bg="#000000", borderwidth=3,
                                  relief="sunken", font="Courier 16 bold", fg="#FFF")
        label_creeps_tues_texte = Label(frame_infos_partie3, textvariable=self.nbcreepstues, bg="#000000",
                                        borderwidth=3,
                                        relief="sunken", font="Courier 16 bold", fg="#FFF")

        label_niveau.pack(expand=1)
        label_niveau_texte.pack(expand=1, fill=X)
        frame_infos_partie1.pack(expand=1)
        label_bombes.pack(expand=1)
        label_bombes_texte.pack(expand=1, fill=X)
        frame_infos_partie2.pack(expand=1)
        label_creeps_tues.pack(expand=1)
        label_creeps_tues_texte.pack(expand=1, fill=X)

        frame_infos_partie3.pack()

        frame_infos_partie.pack(expand=1, fill=BOTH, side=LEFT)
        # frame_infos_tour.pack(expand=1, fill=BOTH, side=LEFT)
        frame_bouttons.pack(expand=1, fill=BOTH, side=LEFT)

        btn_tour_bleue = Button(frame_bouttons_row1, text="TOUR VERTE 500৳ ", bg="#000", fg="#fff",
                                font="courier 16 bold")
        btn_tour_mauve = Button(frame_bouttons_row1, text=" TOUR MAUVE 700৳ ", bg="#000", fg="#fff",
                                font="courier 16 bold")
        btn_tour_blanche = Button(frame_bouttons_row1, text="TOUR BLANCHE 1000৳", bg="#000", fg="#fff",
                                  font="courier 16 bold")

        btn_debuter_partie = Button(frame_bouttons_row2, text="DÉBUTER PARTIE", bg="#000", fg="#fff",
                                    font="courier 16 bold")
        btn_nouvelle_vague = Button(frame_bouttons_row2, text="NOUVELLE VAGUE", bg="#000", fg="#fff",
                                    font="courier 16 bold")
        btn_pause = Button(frame_bouttons_row2, text="PAUSE", bg="#000", fg="#fff", font="courier 16 bold", )

        label_acheter_tours = Label(frame_bouttons, text="Acheter tours: ", bg="#000000", font="Courier 24 bold",
                                    fg="#FFF")

        btn_mine = Button(frame_bouttons_row3, text="PLACER MINE 100৳", bg="#000", fg="#fff", font="courier 16 bold")
        btn_bombe = Button(frame_bouttons_row3, text="SCAN 1000৳", bg="#000", fg="#fff", font="courier 16 bold")

        btn_upgrade_range = Button(frame_bouttons_row4, text="AMÉLIORER RANGE 300௹", bg="#000",
                                  fg="#fff", font="courier 16 bold", )
        btn_upgrade_degats = Button(frame_bouttons_row4, text="AMÉLIORER DÉGATS 300௹", bg="#000",
                                  fg="#fff", font="courier 16 bold", )
        btn_upgrade_special = Button(frame_bouttons_row4, text="AMÉLIORER SPÉCIAL 500௹", bg="#000",
                                  fg="#fff", font="courier 16 bold", )

        # label_map.pack(side=LEFT, expand=1)

        label_acheter_tours.pack(fill=X)
        btn_tour_bleue.pack(side=LEFT, fill=X, expand=1)
        btn_tour_mauve.pack(side=LEFT, fill=X, expand=1)
        btn_tour_blanche.pack(side=LEFT, fill=X, expand=1)
        btn_mine.pack(side=LEFT, fill=X, expand=1)
        btn_bombe.pack(side=LEFT, fill=X, expand=1)
        btn_nouvelle_vague.pack(side=LEFT, fill=X, expand=1)
        btn_debuter_partie.pack(side=LEFT, fill=X, expand=1)
        btn_pause.pack(side=LEFT, fill=X, expand=1)
        btn_upgrade_range.pack(side=LEFT, fill=X, expand=1)
        btn_upgrade_degats.pack(side=LEFT, fill=X, expand=1)
        btn_upgrade_special.pack(side=LEFT, fill=X, expand=1)


        frame_bouttons_row1.pack(fill=X, side=TOP)
        frame_bouttons_row4.pack(fill=X, side=TOP)
        frame_bouttons_row3.pack(fill=X, side=TOP)
        frame_bouttons_row2.pack(fill=X, side=LEFT, expand=1)

        # le canevas de jeu
        self.canevas = Canvas(self.root, width=1200, height=600, highlightthickness=0)

        btn_debuter_partie.bind("<Button-1>", self.parent.debuter_partie)
        btn_nouvelle_vague.bind("<Button-1>", self.parent.creer_niveau)
        btn_tour_bleue.bind("<Button-1>", self.parent.choisir_couleur_bleu)
        btn_tour_mauve.bind("<Button-1>", self.parent.choisir_couleur_mauve)
        btn_tour_blanche.bind("<Button-1>", self.parent.choisir_couleur_blanche)
        btn_pause.bind("<Button-1>", self.parent.pause)
        btn_mine.bind("<Button-1>", self.parent.choisir_mine)
        btn_bombe.bind("<Button-1>", self.parent.choisir_bombe)
        btn_upgrade_range.bind("<Button-1>", self.parent.upgrade_range)
        btn_upgrade_degats.bind("<Button-1>", self.parent.upgrade_degats)
        btn_upgrade_special.bind("<Button-1>",self.parent.upgrade_special)

        # visualiser
        self.frame_stats.pack(fill=X)
        self.canevas.pack()

        self.img = ImageTk.PhotoImage(Image.open("./backgroundGrand.png"))
        self.canevas.create_image(0, 0, anchor=NW, image=self.img, tags=("background",))

        # filename = PhotoImage(file = "./backgroundGrand.png")
        # image = self.canevas.create_image(50,50,anchor=NW, image=filename)

        # img_label = Label(image=image)
        # self.canevas.create_image(0, 0, image=image, anchor=NW)
        # img_label.pack()
        self.frame_bas.pack(expand=1, fill=BOTH)

    def afficher_partie(self):
        self.points_vie.set(str(self.modele.partie.total_vie))
        self.argent.set(str(self.modele.partie.total_argent))
        self.sagesse.set(str(self.modele.partie.total_sagesse))
        self.score.set(str(self.modele.partie.total_points))
        self.niveau.set(str(self.modele.partie.niveau_actuel))
        self.bombes.set(str(self.modele.partie.total_bombes))
        self.nbcreepstues.set(str(self.modele.partie.creeps_tues))
        self.meilleur_score.set(str(self.modele.partie.meilleur_score))

        self.canevas.delete("dynamique")
        self.canevas.delete("sentier")
        self.canevas.delete("projectile")
        self.canevas.delete("statique")


        if self.background == 0:
            # self.canevas.create_rectangle(0, 600, 1200, 0, fill="#FFFFFF", tags="background")
            self.background += 1

        self.canevas.tag_bind("background", "<Button-1>", self.creer_tour)
        self.canevas.tag_bind("tour", "<Button-1>", self.choisir_tour)
        self.canevas.tag_bind("sentier", "<Button-1>", self.placer_mine)

        for i in self.modele.sentier[self.parent.modele.sentier_choisi]:
            self.canevas.create_line(i, width=40, fill="#AAAAAA", tags=("sentier"))

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

                self.canevas.create_oval(x_p - i.rayon, y_p - i.rayon, x_p + i.rayon, y_p + i.rayon,
                                         fill=couleur_projectile, tags="projectile")
        for i in self.modele.partie.niveau.liste_de_mines_a_l_ecran:
            if not i.creep_touche:
                self.canevas.create_oval(i.x - i.rayon, i.y - i.rayon, i.x + i.rayon,
                                         i.y + i.rayon, fill="brown",
                                         tags="dynamique")

    def effacer_sentier(self):
        self.canevas.delete("tour")


    def creer_tour(self, evt):
        self.effacer_rayon()
        couleur_tour = self.parent.modele.partie.couleur_choisie
        tour_creee = self.parent.creer_tour(evt, couleur_tour)
        if tour_creee is not None:
            if couleur_tour != 0:
                self.canevas.create_oval(evt.x - tour_creee.rayon, evt.y - tour_creee.rayon,
                                         evt.x + tour_creee.rayon, evt.y + tour_creee.rayon,
                                         fill=None,width=3,outline="white", tags=("rayon_tour"))

        # TOUR BLEUE = VERT
        # TOUR MAUVE = ROUGE
        # TOUR BLANCHE = BLANCHE
        # REFACTOR LORS DU MERGE
        if couleur_tour == 1:
            couleur_tour = "#10B531"  # GREEN
        if couleur_tour == 2:
            couleur_tour = "purple"
        if couleur_tour == 3:
            couleur_tour = "white"
        if tour_creee is not None:
            if couleur_tour != 0:
                self.canevas.create_rectangle(evt.x + tour_creee.demitaillex, evt.y + tour_creee.demitailley,
                                              evt.x - tour_creee.demitaillex, evt.y - tour_creee.demitailley,
                                              fill=couleur_tour, tags=("tour", tour_creee.id))

    def choisir_tour(self, evt):
        pour_upgrade = self.canevas.gettags(CURRENT)
        self.canevas.delete("rayon_tour")
        self.tour_choix = self.modele.partie.dictionnaire[(pour_upgrade[1])]

        print(pour_upgrade[0], pour_upgrade[1], "choisie, de rayon : ",
              self.tour_choix.rayon,
              "pour la n ième tour:",
              self.tour_choix.id)
        self.tour_choix.afficher_rayon()
        self.mise_ajour_rayon(self.tour_choix)

    def mise_ajour_rayon(self, evt):
        if self.tour_choix.rayon_visible is True:
            self.canevas.create_oval(self.tour_choix.position_x_tour - self.tour_choix.rayon, self.tour_choix.position_y_tour - self.tour_choix.rayon,
                                     self.tour_choix.position_x_tour + self.tour_choix.rayon, self.tour_choix.position_y_tour + self.tour_choix.rayon,
                                     fill=None, width=3,outline="white", tags=("rayon_tour"))
            self.tour_choix.rayon_visible = False

    def effacer_rayon(self):
        self.canevas.delete("rayon_tour")


    def placer_mine(self, evt):
        self.effacer_rayon()
        self.parent.modele.partie.niveau.creer_mine(evt)


    def fin_partie(self):
        self.canevas.delete("statique")
        self.canevas.delete("dynamique")
        self.canevas.delete("tour")

        reponse1 = tkinter.simpledialog.askstring("Score", "Quel est votre nom?",
                                                  parent=self.parent.vue.root)


        if reponse1 is not None:
            if(self.modele.partie.total_points<self.modele.partie.meilleur_score):
                nice_try = reponse1 + ", votre performance laisse à désirer " + str(self.modele.partie.total_points) + " points ont étés octroyés. Votre système est inopérable..."

            else:
                nice_try = reponse1 + ", congratulations, votre performance est tout un exploit. " + str(self.modele.partie.total_points) + " points ont étés octroyés. J'espère que vous ayez des amis à qui en parler... "

            if self.modele.partie.meilleur_score < self.modele.partie.total_points:

                with open("Score.txt", "w") as file1:
                    nouveau_record = reponse1 + " a juste fait " + str(self.modele.partie.total_points) + ' points'
                    file1.write(nouveau_record)
            tkinter.messagebox.showinfo( 'Votre survie a échoué ',nice_try,
                                        parent=self.parent.vue.root)





class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partie = None
        self.sentier_choisi = 0
        self.sentier = [
            #premier sentier
            [
                [[0, 275], [240, 275]],
                [[240, 275], [240, 50]],
                [[240, 50], [840, 50]],
                [[840, 50], [840, 515]],
                [[840, 515], [1400, 515]]
            ],
            #deuxieme sentier
            [
                [[1000, 0], [1000, 240]],
                [[1000, 240], [100, 240]],
                [[100, 240], [100, 120]],
                [[100, 120], [800, 120]],
                [[800, 120], [800, 575]],
                [[800, 575], [1100, 575]],
                [[1100, 575], [1100, 475]],
                [[1100, 475], [100, 475]],
                [[100, 475], [100, 350]],
                [[100, 350], [1400, 350]]
            ]
        ]


        self.largeur = 1200
        self.hauteur = 600
        self.debut = None
        self.duree = 0
        self.partie = None

    def nb_creeps(self, evt):
        print("ÉCRAN", len(self.partie.niveau.liste_creep_a_l_ecran))
        print("ATTENTE", len(self.partie.niveau.liste_creep_attente))

    def creer_partie(self):
        self.partie = Partie(self)
        self.lire_highscore()
        print("Partie créée :", self.partie)

    def jouer_tour(self):
        self.partie.jouer_tour()

    def lire_highscore(self):
        with open("Score.txt", "r") as file1:
            meilleur_score = file1.read()
        matches = re.findall("[+-]?\d+", meilleur_score)
        self.partie.meilleur_score = int(matches[0])
        return self.partie.meilleur_score


class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.total_creep_tues = 0
        self.total_points = 0
        self.total_vie = 100
        self.total_argent = 1000
        self.total_sagesse = 200
        self.niveau_actuel = 1
        self.niveau = Niveau(self, self.niveau_actuel)
        self.creeps_tues = 0
        self.couleur_choisie = 0
        self.i = 1  # Utiliser pour l'augmentation de la sagesse de niveau
        self.dictionnaire = {}
        self.total_bombes = 0
        self.cout_upgrade = 300
        self.ratio_upgrade = 1
        self.meilleur_score = 55
        self.sentier_a_change = False




    def changement_niveau(self):
        if (self.niveau_actuel > 4):
            if not self.sentier_a_change:
                self.parent.changer_sentier = True
                self.dictionnaire.clear()
                self.parent.parent.vue.canevas.delete("tour")
                self.parent.parent.vue.effacer_rayon()
                self.sentier_a_change = True
            else:
                pass


    def creer_niveau(self, evt):
        if len(self.niveau.liste_creep_a_l_ecran) == 0:
            self.niveau_actuel += 1
            if (self.niveau_actuel > 4):
                self.parent.sentier_choisi = 1
                self.changement_niveau()
            self.niveau.fin_niveau = False
            self.total_bombes +=1
            self.niveau.creer_creeps()

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

    def creer_tour(self, evt, couleur_tour):
        tour_creee = None
        if self.total_argent > 100:
            if couleur_tour == 1:
                if self.total_argent >= self.niveau.tour_bleue_valeur:
                    id = creer_id()
                    self.total_argent -= self.niveau.tour_bleue_valeur
                    tour_creee = Tour_Bleu(self, evt.x, evt.y, id)

            if couleur_tour == 2:
                if self.total_argent >= self.niveau.tour_mauve_valeur:
                    id = creer_id()
                    self.total_argent -= self.niveau.tour_mauve_valeur
                    tour_creee = Tour_Mauve(self, evt.x, evt.y, id)

            if couleur_tour == 3:
                if self.total_argent >= self.niveau.tour_blanche_valeur:
                    id = creer_id()
                    self.total_argent -= self.niveau.tour_blanche_valeur
                    tour_creee = Tour_Blanche(self, evt.x, evt.y, id)

        if tour_creee is not None:
            self.dictionnaire[id] = tour_creee
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
        self.liste_de_mines_a_l_ecran = []
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
        self.mine_valeur = 100
        self.bombe_valeur = 100
        self.valeur_degat = 0.5
        self.creer_creeps()
        self.pour_shotgun = None
        self.mine_cliquee = False


    def jouer_tour(self):

        for i in self.liste_creep_a_l_ecran:
            i.jouer_tour(self)
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

        for j in self.parent.dictionnaire:
            l = self.parent.dictionnaire[j]
            l.verification_range()
            self.pour_shotgun = self.parent.dictionnaire[j]

        for k in self.liste_de_projectile_a_l_ecran:
            if len(self.liste_de_projectile_a_l_ecran) != 0:
                if isinstance(k, Projectil_a):
                    k.projectile_a_tete_chercheuse()
                    if k.creep_touche:
                        self.liste_de_projectile_a_l_ecran.remove(k)
                if isinstance(k, Projectil_b):
                    k.projectile_shotgun(self.liste_creep_a_l_ecran,self.pour_shotgun)
                    if k.creep_touche or k.out_of_bound:
                        self.liste_de_projectile_a_l_ecran.remove(k)
                if isinstance(k, Projectil_c):
                    k.projectile_rebound(self.liste_creep_a_l_ecran)
                    if not self.liste_creep_a_l_ecran:
                        self.liste_de_projectile_a_l_ecran.remove(k)
                    if k.creep_touche:
                        self.liste_de_projectile_a_l_ecran.remove(k)

    def creer_creeps(self):
        print(self.niveau_actuel)
        if self.ratio_creep_vert > 0:
            for i in range(int(self.ratio_creep * self.ratio_creep_vert)):
                self.liste_creep_attente.append(Creep_vert(self.parent.niveau_actuel))



        for i in range(int(self.ratio_creep * self.ratio_creep_jaune)):
            self.liste_creep_attente.append(Creep_jaune(self.parent.niveau_actuel))

        for i in range(int(self.ratio_creep * self.ratio_creep_rouge)):
            self.liste_creep_attente.append(Creep_rouge(self.parent.niveau_actuel))

        self.liste_creep_attente.append(Boss(self.parent.niveau_actuel))

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


    def cliquer_mine(self, evt):
        self.mine_cliquee = True

    def creer_mine(self, evt):
        if self.mine_cliquee:
            if self.parent.total_argent >= self.mine_valeur:
                if len(self.liste_de_mines_a_l_ecran) < 6:
                    self.parent.total_argent -= self.mine_valeur
                    mine_creee = Mine(evt.x, evt.y, self)
                    self.liste_de_mines_a_l_ecran.append(mine_creee)
                    print(self.liste_de_mines_a_l_ecran)
                    self.parent.couleur_choisie = 0
                    return mine_creee

    def detonation_bombe(self, evt):
        if self.parent.total_argent >= self.bombe_valeur:
            if self.parent.total_bombes>0:

                self.parent.total_argent -= self.bombe_valeur
                self.parent.total_bombes -=1
                for i in self.liste_creep_a_l_ecran:
                    i.vie_creep -= 75
                self.parent.couleur_choisie = 0


class Creep():
    def __init__(self, parent):
        self.parent = parent
        self.vie_creep = 42
        self.x1 = -1500
        self.y1 = -1500
        self.rayon = 15
        self.valeur_monetaire_creep = 0
        self.vitesse_creep_X = 5
        self.vitesse_creep_Y = 5
        self.troncon = 0
        self.debut = 0
        self.i_pyth = 0
        self.cooldown = 0
        self.cooldown_mine = 30
        self.creep_touche = False
        self.est_cible = False
        self.est_vivant = False
        self.est_en_attente = False
        self.faiblesse_a = False
        self.faiblesse_b = False
        self.faiblesse_c = False



    def jouer_tour(self, parent):
        self.deplacement(parent)

    def deplacement(self, parent):


        map = parent.parent.parent.sentier_choisi
        sen = parent.parent.parent.sentier

        if self.debut == 0:
            self.x1 = sen[map][0][0][0] 
            self.y1 = sen[map][0][0][1]
            self.debut = 1



        distance = Helper.calcDistance(sen[map][self.i_pyth][0][0], sen[map][self.i_pyth][0][1], sen[map][self.i_pyth][1][0],sen[map][self.i_pyth][1][1])
        angle = Helper.calcAngle(sen[map][self.i_pyth][0][0], sen[map][self.i_pyth][0][1], sen[map][self.i_pyth][1][0],sen[map][self.i_pyth][1][1])
        prochainpoint = Helper.getAngledPoint(angle, distance, sen[map][self.i_pyth][0][0], sen[map][self.i_pyth][0][1])

        if sen[map][self.i_pyth][0][0] < sen[map][self.i_pyth][1][0]:
            if self.x1 < prochainpoint[0]:
                for j in range(self.vitesse_creep_X):
                    self.x1 += 1
                    if self.x1 >= prochainpoint[0]:
                        self.x1 = round(prochainpoint[0])

        if sen[map][self.i_pyth][0][0] > sen[map][self.i_pyth][1][0]:
            if self.x1 > prochainpoint[0]:
                for j in range(self.vitesse_creep_X):
                    self.x1 -= 1
                    if self.x1 <= prochainpoint[0]:
                        self.x1 = round(prochainpoint[0])

        if sen[map][self.i_pyth][0][1] < sen[map][self.i_pyth][1][1]:
            if self.y1 < prochainpoint[1]:
                for j in range(self.vitesse_creep_Y):
                    self.y1 += 1
                    if self.y1 >= prochainpoint[1]:
                        self.y1 = round(prochainpoint[1])

        if sen[map][self.i_pyth][0][1] > sen[map][self.i_pyth][1][1]:
            if self.y1 > prochainpoint[1]:
                for j in range(self.vitesse_creep_Y):
                    self.y1 -= 1
                    if self.y1 <= prochainpoint[1]:
                        self.y1 = round(prochainpoint[1])

        if self.x1 == round(prochainpoint[0]) and self.y1 == round(prochainpoint[1]):
            if self.i_pyth <= len(sen[map]) - 1:
                self.i_pyth += 1
                self.x1 = prochainpoint[0]
                self.y1 = prochainpoint[1]

        if self.cooldown > 0:
            self.cooldown -= 1
        if self.cooldown == 0:
            for i in parent.liste_de_mines_a_l_ecran:
                for j in parent.liste_creep_a_l_ecran:
                    distance_mine_verif = Helper.calcDistance(i.x, i.y, j.x1, j.y1)

                    if distance_mine_verif < (i.rayon + j.rayon):
                        i.liste_creep_sur_mine.append(j)

                    if isinstance(j, Boss):
                        self.cooldown_mine = 0

                if len(i.liste_creep_sur_mine) != 0:

                    i.detonation_mine(i.liste_creep_sur_mine)
                    i.liste_creep_sur_mine = []

            self.cooldown = self.cooldown_mine


class Creep_vert(Creep):
    def __init__(self, niveau):
        Creep.__init__(self, Creep)
        self.niveau = niveau
        self.valeur_monetaire_creep = 45
        self.vitesse_creep = 4
        self.vitesse_creep_X = random.randrange(4) + 2
        self.vitesse_creep_Y = random.randrange(4) + 2
        self.faiblesse_c = True
        self.valeur_points = 110
        self.couleur = "orange"
        self.ratio_vie = 10
        self.vie_creep = 50 + (self.ratio_vie * self.niveau)


class Creep_jaune(Creep):
    def __init__(self, niveau):
        Creep.__init__(self, Creep)
        self.niveau = niveau
        self.valeur_monetaire_creep = 75
        self.vitesse_creep = 6
        self.vitesse_creep_X = random.randrange(6) + 3
        self.vitesse_creep_Y = random.randrange(6) + 3
        self.faiblesse_a = True
        self.valeur_points = 275
        self.couleur = "yellow"
        self.ratio_vie = 10
        self.vie_creep = 80 + (self.ratio_vie * self.niveau+15)


class Creep_rouge(Creep):
    def __init__(self, niveau):
        Creep.__init__(self, Creep)
        self.niveau = niveau
        self.valeur_monetaire_creep = 100
        self.vitesse_creep = 3
        self.vitesse_creep_X = random.randrange(4) + 4
        self.vitesse_creep_Y = random.randrange(4) + 4
        self.faiblesse_a = True
        self.valeur_points = 325
        self.couleur = "red"
        self.ratio_vie = 10
        self.vie_creep = 140 + (self.ratio_vie * self.niveau)


class Boss(Creep):
    def __init__(self, niveau):
        Creep.__init__(self, Creep)
        self.niveau = niveau
        self.valeur_monetaire_creep = 300
        self.rayon = 15
        self.couleur = "pink"
        self.valeur_points = 500
        self.ratio_vie = 5
        self.vie_creep = 280 + (self.ratio_vie * self.niveau)


class Tour():
    def __init__(self, parent, x, y):
        self.couleur_tour = None
        self.parent = parent
        self.position_x_tour = x
        self.position_y_tour = y
        self.demitaillex = 25
        self.demitailley = 25
        self.valeur_monnetaire_tour = 0
        self.rayon = 0
        self.valeur_vente = 0
        self.cooldown = 0
        self.cooldown_tower = 0
        self.placement_valide = False
        self.rayon_visible = False
        self.degats_tour = 0
        self.rebound_tour = 0
        self.vitesse_projectile_tour = 0

    def verification_range(self):
        liste = self.parent.parent.partie.niveau.liste_creep_a_l_ecran
        for i in liste:
            distance = Helper.calcDistance(i.x1, i.y1, self.position_x_tour, self.position_y_tour)
            somme_rayon = i.rayon + self.rayon
            if distance < somme_rayon:
                if self.cooldown == 0:
                    i.est_cible = True
                    self.tirer_creep(i)
                    self.cooldown = self.cooldown_tower

        if self.cooldown > 0:
            self.cooldown -= 1

    def tirer_creep(self, creep_cible):
        if isinstance(self, Tour_Bleu):
            self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(Projectil_a(self.position_x_tour, self.position_y_tour, creep_cible,self))
        if isinstance(self, Tour_Mauve):
            for j in range(self.nb_projectile):
                self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(Projectil_b(self.position_x_tour + random.randrange(50), self.position_y_tour + random.randrange(50),creep_cible,self))
        if isinstance(self, Tour_Blanche):
            self.parent.parent.partie.niveau.liste_de_projectile_a_l_ecran.append(
                Projectil_c(self.position_x_tour, self.position_y_tour, creep_cible,self))

    def afficher_rayon(self):
        self.rayon_visible = not self.rayon_visible

    def up_degats(self):
        if self.parent.total_sagesse >= 300:
            self.degats_tour += 5
            self.parent.total_sagesse -= 300

    def up_range(self):
        if self.parent.total_sagesse >= 300:
            self.rayon *= 1.1
            self.parent.total_sagesse -= 300

    def up_special(self):
        if self.parent.total_sagesse >= 500:
            if isinstance(self,Tour_Bleu):
                if self.vitesse_projectile_tour < 30:
                    self.vitesse_projectile_tour += 3
                    self.parent.total_sagesse -= 500

            if isinstance(self,Tour_Mauve):
                self.nb_projectile += 1
                self.parent.total_sagesse -= 500

            if isinstance(self,Tour_Blanche):
                self.rebound_tour += 1
                self.parent.total_sagesse -= 500

class Tour_Bleu(Tour):
    def __init__(self, parent, x, y, id):
        Tour.__init__(self, parent, x, y)
        self.valeur_monnetaire_tour = 500
        self.couleur_tour = 1
        self.cooldown_tower = 20
        self.rayon = 150
        self.id = id
        self.degats_tour = 30
        self.vitesse_projectile_tour = 6


class Tour_Mauve(Tour):
    def __init__(self, parent, x, y, id):
        Tour.__init__(self, parent, x, y)
        self.nb_projectile = 6
        self.valeur_monnetaire_tour = 700
        self.couleur_tour = 2
        self.rayon = 200
        self.cooldown_tower = 30
        self.id = id
        self.degats_tour = 10
        self.vitesse_projectile_tour = 5


class Tour_Blanche(Tour):
    def __init__(self, parent, x, y, id):
        Tour.__init__(self, parent, x, y)
        self.valeur_monnetaire_tour = 1000
        self.couleur_tour = 3
        self.rayon = 500
        self.cooldown_tower = 40
        self.id = id
        self.degats_tour = 10
        self.rebound_tour = 3
        self.vitesse_projectile_tour = 20


class Projectile():
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix):
        self.tour = Tour
        self.position_projectile_x = position_projectile_x
        self.position_projectile_y = position_projectile_y
        self.degats = 0
        self.rayon = 10
        self.creep_touche = False
        self.creep_cible = creep_cible
        self.couleur_projectile = ""
        self.unefois = 0
        self.out_of_bound = False
        self.cible = 0
        self.tour = tour_de_choix


class Projectil_a(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix):
        Projectile.__init__(self, position_projectile_x, position_projectile_y,creep_cible,tour_de_choix)
        self.couleur_projectile = 1

    def projectile_a_tete_chercheuse(self):
        distance_projectile = Helper.calcDistance(self.position_projectile_x, self.position_projectile_y,
                                                  self.creep_cible.x1, self.creep_cible.y1)
        angle_projectile = Helper.calcAngle(self.position_projectile_x, self.position_projectile_y, self.creep_cible.x1,
                                            self.creep_cible.y1)
        cible_projectile = Helper.getAngledPoint(angle_projectile, self.tour.vitesse_projectile_tour, self.position_projectile_x,
                                                 self.position_projectile_y)


        self.position_projectile_x = cible_projectile[0]
        self.position_projectile_y = cible_projectile[1]

        if distance_projectile < 15:
            self.creep_touche = True
        if self.creep_touche:
            if self.creep_cible.vie_creep > 0:
                self.creep_cible.vie_creep -= self.tour.degats_tour

    def changement_sentier(self):
        self.vue.effacer_sentier()




class Projectil_b(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix):
        Projectile.__init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix)
        self.couleur_projectile = 2
        self.rayon = 5
        self.position_vise_x = 0
        self.position_vise_y = 0
        self.position_ini_x = 0
        self.position_ini_y = 0

    def projectile_shotgun(self, listedecreep, tour):

        if self.unefois == 0:
            self.position_vise_x = self.creep_cible.x1
            self.position_vise_y = self.creep_cible.y1
            self.unefois += 1
            self.position_ini_x = self.position_projectile_x
            self.position_ini_y = self.position_projectile_y

        if self.position_ini_x < self.position_vise_x:
            if self.position_projectile_x < self.position_vise_x * 100:
                self.position_projectile_x += self.tour.vitesse_projectile_tour
                if self.position_projectile_x > self.position_ini_x + tour.rayon - 50:
                    self.out_of_bound = True

        if self.position_ini_x > self.position_vise_x:
            if self.position_projectile_x > self.position_vise_x / 100:
                self.position_projectile_x -= self.tour.vitesse_projectile_tour
                if self.position_projectile_x < self.position_ini_x - tour.rayon + 50:
                    self.out_of_bound = True

        if self.position_ini_y < self.position_vise_y:
            if self.position_projectile_y < self.position_vise_y * 100:
                self.position_projectile_y += self.tour.vitesse_projectile_tour
                if self.position_projectile_y > self.position_ini_y + tour.rayon - 50:
                    self.out_of_bound = True

        if self.position_ini_y > self.position_vise_y:
            if self.position_projectile_y > self.position_vise_y / 100:
                self.position_projectile_y -= self.tour.vitesse_projectile_tour
                if self.position_projectile_y < self.position_ini_y - tour.rayon + 50:
                    self.out_of_bound = True

        for i in listedecreep:
            distance_projectile_verification = Helper.calcDistance(self.position_projectile_x,
                                                                   self.position_projectile_y, i.x1, i.y1)
            if distance_projectile_verification < i.rayon:
                i.creep_touche = True
                self.creep_touche = True
            if i.creep_touche:
                if i.vie_creep > 0:
                    i.vie_creep -= self.tour.degats_tour
                    i.creep_touche = False

class Projectil_c(Projectile):
    def __init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix):
        Projectile.__init__(self, position_projectile_x, position_projectile_y, creep_cible,tour_de_choix)
        self.couleur_projectile = 3
        self.rayon = 5
        self.cible = 0
        self.rebound = self.tour.rebound_tour

    def projectile_rebound(self, liste_de_creep):
        if self.cible < len(liste_de_creep):
            distance_projectile = Helper.calcDistance(self.position_projectile_x, self.position_projectile_y,liste_de_creep[self.cible].x1, liste_de_creep[self.cible].y1)
            angle_projectile = Helper.calcAngle(self.position_projectile_x, self.position_projectile_y,liste_de_creep[self.cible].x1, liste_de_creep[self.cible].y1)
            cible_projectile = Helper.getAngledPoint(angle_projectile, self.tour.vitesse_projectile_tour,self.position_projectile_x, self.position_projectile_y)

            self.position_projectile_x = cible_projectile[0]
            self.position_projectile_y = cible_projectile[1]

            if distance_projectile < liste_de_creep[self.cible].rayon:
                liste_de_creep[self.cible].creep_touche = True

            if liste_de_creep[self.cible].creep_touche:
                if liste_de_creep[self.cible].vie_creep > 0:
                    liste_de_creep[self.cible].vie_creep -= self.tour.degats_tour
                    liste_de_creep[self.cible].creep_touche = False

                if liste_de_creep[self.cible].vie_creep < 0:
                    self.rebound -= 1

                if liste_de_creep[self.cible].vie_creep > 0:
                    self.cible += 1

                if len(liste_de_creep) < 3:
                    self.cible = 0
                    self.rebound = 0

                if self.cible == self.rebound:
                    self.creep_touche = True

    def ajouter_rebound(self):
        self.rebound += 1

class Mine():
    def __init__(self, position_mine_x, position_mine_y, niveau):
        self.parent = niveau
        self.x = position_mine_x
        self.y = position_mine_y
        self.degats = 60
        self.rayon = 10
        self.creep_touche = False
        self.liste_creep_sur_mine = []
        # self.couleur_mine = "brown"


    def detonation_mine(self, liste_creep):
        print("boom\n\n")
        self.creep_touche = True
        if self.creep_touche:
            self.parent.liste_de_mines_a_l_ecran.remove(self)
        for i in liste_creep:
            i.creep_touche = True
            if i.vie_creep > 0:
                i.vie_creep -= self.degats

class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.pause_en_cours = 0
        self.changer_sentier = False
        self.vue.root.mainloop()


    def pause(self, evt):
        if not self.pause_en_cours:
            self.pause_en_cours = 1
            self.jouer_partie()
        elif self.pause_en_cours:
            self.pause_en_cours = 0
            self.jouer_partie()

    def mettre_creeps_en_jeu(self):
        self.modele.partie.niveau.mettre_creeps_en_jeu()

    def debuter_partie(self, evt):
        if not self.partie_en_cours:
            self.partie_en_cours = 1
            self.modele.creer_partie()

            self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            if not self.pause_en_cours:
                if self.changer_sentier:
                    self.changement_sentier()
                    self.changer_sentier = False
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

    def choisir_mine(self, evt):
        if self.partie_en_cours != 0:
            self.modele.partie.niveau.cliquer_mine(evt)
            print("mine sélectionnée")

    def choisir_bombe(self, evt):
        if self.partie_en_cours != 0:
            print("bombe sélectionnée")
            self.modele.partie.niveau.detonation_bombe(evt)

    def creer_tour(self, evt, couleur_tour):
        return self.modele.partie.creer_tour(evt, couleur_tour)

    def creer_niveau(self, evt):
        if self.partie_en_cours != 0:
            self.modele.partie.creer_niveau(evt)

    def upgrade_range(self, evt):
        if self.partie_en_cours != 0:
            if self.vue.tour_choix is not None:
                monchoix = self.vue.tour_choix
                monchoix.up_range()

    def upgrade_degats(self, evt):
        if self.partie_en_cours != 0:
            if self.vue.tour_choix is not None:
                monchoix = self.vue.tour_choix
                monchoix.up_degats()

    def upgrade_special(self, evt):
        if self.partie_en_cours != 0:
            if self.vue.tour_choix is not None:
                monchoix = self.vue.tour_choix
                monchoix.up_special()

if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
