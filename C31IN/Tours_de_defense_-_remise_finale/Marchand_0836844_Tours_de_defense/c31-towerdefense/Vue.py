import os
import random
from tkinter import simpledialog, messagebox

import Modele
from tkinter import *

class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.centre_interface = self.modele.interface.largeur/2
        self.root = Tk()
        self.root.title("Tower Defense - Smile, Even A Little")
        listeimmagecreep_depression_gauche = self.charger_gifs('./images/creep_depression_gauche.gif')
        listeimmagecreep_depression_doite = self.charger_gifs('./images/creep_depression_droite.gif')
        listeimmagecreep_anxiete_droite = self.charger_gifs('./images/creep_anxiete_droite.gif')
        listeimmagecreep_anxiete_gauche = self.charger_gifs('./images/creep_anxiete_gauche.gif')
        listeimmagecreep_insomnie_droite = self.charger_gifs('./images/creep_insomnie_droite.gif')
        listeimmagecreep_insomnie_gauche = self.charger_gifs('./images/creep_insomnie_gauche.gif')
        listeimmagecreep_boss_droite = self.charger_gifs('./images/boss_droite.gif')
        listeimmagecreep_boss_gauche = self.charger_gifs('./images/boss_gauche.gif')

        self.sprites = {"creep_depression_gauche": listeimmagecreep_depression_gauche,
                        "creep_depression_droite": listeimmagecreep_depression_doite,
                        "creep_anxiete_droite": listeimmagecreep_anxiete_droite,
                        "creep_anxiete_gauche": listeimmagecreep_anxiete_gauche,
                        "creep_insomnie_droite": listeimmagecreep_insomnie_droite,
                        "creep_insomnie_gauche": listeimmagecreep_insomnie_gauche,
                        "boss_droite": listeimmagecreep_boss_droite,
                        "boss_gauche": listeimmagecreep_boss_gauche}

        self.sprites = {"creep_depression_gauche": listeimmagecreep_depression_gauche,
                        "creep_depression_droite": listeimmagecreep_depression_doite,
                        "creep_anxiete_droite": listeimmagecreep_anxiete_droite,
                        "creep_anxiete_gauche": listeimmagecreep_anxiete_gauche,
                        "creep_insomnie_droite": listeimmagecreep_insomnie_droite,
                        "creep_insomnie_gauche": listeimmagecreep_insomnie_gauche,
                        "boss_droite": listeimmagecreep_boss_droite,
                        "boss_gauche": listeimmagecreep_boss_gauche}

        self.img_tour = {}
        self.img_tour["tour_confiance"] = PhotoImage(file='./images/tour_confiance.png')
        self.img_tour["tour_confiance_trans"] = PhotoImage(file='./images/tour_confiance_trans.png')
        self.img_tour["tour_relation"] = PhotoImage(file='./images/tour_relation.png')
        self.img_tour["tour_relation_trans"] = PhotoImage(file='./images/tour_relation_trans.png')
        self.img_tour["tour_sommeil"] = PhotoImage(file='./images/tour_sommeil.png')
        self.img_tour["tour_sommeil_trans"] = PhotoImage(file='./images/tour_sommeil_trans.png')
        self.img_tour_relation = PhotoImage(file='./images/tour_relation.png')
        self.img_cartes = {"carte1": PhotoImage(file='./images/carte1.png')}
        self.img_interface = PhotoImage(file='./images/interface_background.png')
        self.type_tour = ""
        self.largeur_bouton = 100
        self.menu_game_over = False
        self.partie_en_pause = False
        self.splash_img = PhotoImage(file='./images/splash.png')
        self.cadres = {}
        self.cadre_actif = None
        self.coul_primaire = "#1f0532"
        self.coul_sec = "#c2d8ff"
        self.creer_cadres()

    def creer_cadres(self):
        self.cadres["splash"] = self.creer_cadre_splash()
        self.cadres["jeu"] = None
        self.cadre_actif = self.cadres["splash"]
        self.cadre_actif.pack()

    def changer_cadre(self, nom_cadre):
        if nom_cadre == "jeu":
                self.cadres["jeu"] = self.creer_cadre_jeu()

        if self.cadre_actif:
            self.cadre_actif.pack_forget()
            self.cadre_actif = self.cadres[nom_cadre]
        else:
            self.cadre_actif = self.cadres[nom_cadre]

        self.cadre_actif.pack()

    def creer_cadre_splash(self):
        self.frame_splash = Frame(self.root)
        self.canevas_splash = Canvas(self.frame_splash, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        self.canevas_splash.create_image(0, 0, image=self.splash_img, anchor="nw", tag="")
        self.canevas_splash.pack()

        self.btn_nouvelle_partie = Button(self.canevas_splash, text="Nouvelle partie", font=('Helvetica 14 bold'), width=24, height=2, fg='#1f0532', bg="#c2d8ff")
        self.btn_nouvelle_partie.pack()
        self.btn_nouvelle_partie.bind("<Button-1>", self.parent.nouvelle_partie)

        self.btn_afficher_scores = Button(self.canevas_splash, text="Scores", font=('Helvetica 14 bold'), width=24, height=2, fg='#1f0532', bg="#c2d8ff")
        self.btn_afficher_scores.pack()
        self.btn_afficher_scores.bind("<Button-1>", self.afficher_score)

        self.canevas_splash.create_window(280, 500, window=self.btn_nouvelle_partie)
        self.canevas_splash.create_window(280, 580, window=self.btn_afficher_scores)
        return self.frame_splash

    def creer_cadre_jeu(self):
        self.frame_jeu = Frame(self.root)
        self.canevas = Canvas(self.frame_jeu, width=self.modele.carte.largeur, height=self.modele.hauteur, bg="ivory")
        self.canevas.pack(side=LEFT)
        self.interface = Canvas(self.frame_jeu, width=self.modele.interface.largeur, height=self.modele.hauteur, bg="#180426")
        self.interface.create_image(0, 0, image=self.img_interface, anchor="nw")
        self.interface.pack(side=RIGHT)

        self.interface.create_text(self.centre_interface, 40, text="SANTÉ MENTALE", font=('Helvetica 14 bold'), tags="", fill=self.coul_sec, anchor="center")
        self.interface.create_text(self.centre_interface, 110, text="MOTIVATION", font=('Helvetica 14 bold'), fill=self.coul_sec, tags="",
                                   anchor="center")
        self.interface.create_text(self.centre_interface, 180, text="ANTI-DÉPRESSEURS", font=('Helvetica 14 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")

        self.bouton_tour_confiance = Radiobutton(self.interface, text="Tour Confiance", image=self.img_tour["tour_confiance"],
                                            command=lambda: self.creer_tour("confiance"),
                                                 indicator=0, value=1, compound="top", width=self.largeur_bouton, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec)
        self.interface.create_text(self.centre_interface - 95, 385, text=Modele.Tour_Confiance.prix, font=('Helvetica 18 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.interface.create_text(self.centre_interface + 85, 400, text=Modele.Tour_Confiance.prix_upgrade,
                                   font=('Helvetica 16 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.bouton_update_tour_confiance = Button(self.interface, text="NIV. +", width=7, height=1, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec,
                                                   command=lambda: self.upgrade_tour("confiance"))



        self.bouton_tour_relation = Radiobutton(self.interface, text="Tour Relation", image=self.img_tour["tour_relation"],
                                           command=lambda: self.creer_tour("relation"),
                                                indicator=0, value=2, compound="top", width=self.largeur_bouton, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec)

        self.interface.create_text(self.centre_interface - 95, 535, text=Modele.Tour_Relation.prix, font=('Helvetica 18 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.interface.create_text(self.centre_interface + 85, 550, text=Modele.Tour_Relation.prix_upgrade,
                                   font=('Helvetica 16 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.bouton_update_tour_relation = Button(self.interface, text="NIV. +", width=7, height=1, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec,
                                                   command=lambda: self.upgrade_tour("relation"))



        self.bouton_tour_sommeil = Radiobutton(self.interface, text="Tour Sommeil", image=self.img_tour["tour_sommeil"],
                                          command=lambda: self.creer_tour("sommeil"),
                                               indicator=0, value=3, compound="top",  width=self.largeur_bouton, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec)
        self.interface.create_text(self.centre_interface - 95, 680, text=Modele.Tour_Sommeil.prix,
                                   font=('Helvetica 18 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.interface.create_text(self.centre_interface + 85, 700, text=Modele.Tour_Sommeil.prix_upgrade,
                                   font=('Helvetica 16 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")
        self.bouton_update_tour_sommeil = Button(self.interface, text="NIV. +", width=7, height=1, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec,
                                                  command=lambda: self.upgrade_tour("sommeil"))


        self.interface.create_text(self.centre_interface, 780, text="SCORE",
                                   font=('Helvetica 14 bold'),
                                   fill=self.coul_sec, tags="",
                                   anchor="center")

        self.score_texte = Label(self.interface, text="SCORE", font=("Arial", 14))

        self.bouton_redemarrer = Button(self.interface, text="Redémarrer", width=24, height=2, font=('Helvetica 10 bold'), fg=self.coul_primaire, bg=self.coul_sec)
        self.bouton_redemarrer.bind("<Button-1>", self.parent.redemarrer)

        self.root.bind("<Escape>", self.parent.pause)
        self.root.bind("<space>", self.parent.utiliser_antidepresseur)

        # Variables de positionnement récupérées ailleurs:
        self.sante_mentale_y = 65
        self.motivation_y = 135
        self.antidepresseur_y = 205
        self.vague_y = 280

        self.interface.create_window(self.centre_interface - 10, 385, window=self.bouton_tour_confiance)
        self.interface.create_window(self.centre_interface + 85, 430, window=self.bouton_update_tour_confiance)

        self.interface.create_window(self.centre_interface - 10, 535, window=self.bouton_tour_relation)
        self.interface.create_window(self.centre_interface + 85, 580, window=self.bouton_update_tour_relation)

        self.interface.create_window(self.centre_interface - 10, 685, window=self.bouton_tour_sommeil)
        self.interface.create_window(self.centre_interface + 85, 730, window=self.bouton_update_tour_sommeil)

        self.interface.create_window(self.centre_interface, 850, window=self.bouton_redemarrer)

        self.afficher_carte_de_jeu()

        return self.frame_jeu

    # On affiche l'arrière-plan, chemins et autres décorations dès le début
    def afficher_carte_de_jeu(self):

        self.canevas.create_image(0, 0, image=self.img_cartes["carte1"], anchor="nw", tags="libre")

        for chemin in self.modele.carte.chemins:
            self.canevas.create_line(chemin.x1, chemin.y1, chemin.x2, chemin.y2, fill='', width=chemin.bordure, tags="zone_chemin")
            self.canevas.create_line(chemin.x1, chemin.y1, chemin.x2, chemin.y2, fill='', width=chemin.largeur, tags="chemin")

        self.curseur_tour = self.canevas.create_image(0, 0, image="", anchor="center", tag=("", "curseur_tour"))


    def afficher_partie(self):
        self.canevas.delete("mobile")
        self.interface.delete("mobile")

        self.interface.create_text(self.centre_interface, self.sante_mentale_y, text=self.modele.partie.sante_mentale, fill="#eb8a98",
                                   font=('Helvetica 16 bold'), tags=("", "mobile"), anchor="center")
        self.interface.create_text(self.centre_interface, self.motivation_y, text=self.modele.partie.motivation, fill="#608400",
                                   font=('Helvetica 16 bold'), tags=("", "mobile"), anchor="center"),
        self.interface.create_text(self.centre_interface, self.antidepresseur_y, text=self.modele.partie.antidepresseur, fill="white",
                                   font=('Helvetica 16 bold'), tags=("", "mobile"), anchor="center")


        self.interface.create_text(self.centre_interface, 250, text="VAGUE " + str(self.modele.partie.no_vague + 1),
                                   fill=self.coul_sec,
                                   font=('Helvetica 14 bold'), tags=("", "mobile"), anchor="center")


        self.vague_max_creeps = self.modele.partie.vagues[self.modele.partie.no_vague].nbr_creeps
        self.vague_creeps_cumules = self.vague_max_creeps - len(self.modele.partie.vagues[self.modele.partie.no_vague].creeps_attente)
        self.interface.create_text(self.centre_interface, self.vague_y, text=str(self.vague_creeps_cumules) + " / " + str(self.vague_max_creeps),
                                   fill=self.coul_sec,
                                   font=('Helvetica 24 bold'), tags=("", "mobile"), anchor="center")


        self.interface.create_text(self.centre_interface + 85, 345, text="NIV. " + str(Modele.Tour_Confiance.niveau),
                                   fill=self.coul_sec,
                                   font=('Helvetica 12 bold'), tags=("", "mobile"), anchor="center")

        self.interface.create_text(self.centre_interface + 85, 495, text="NIV. " + str(Modele.Tour_Relation.niveau),
                                   fill=self.coul_sec,
                                   font=('Helvetica 12 bold'), tags=("", "mobile"), anchor="center")

        self.interface.create_text(self.centre_interface + 85, 650, text="NIV. " + str(Modele.Tour_Sommeil.niveau),
                                   fill=self.coul_sec,
                                   font=('Helvetica 12 bold'), tags=("", "mobile"), anchor="center")

        self.interface.create_text(self.centre_interface, 805, text=self.modele.partie.score,
                                   fill="#d7ca3f",
                                   font=('Helvetica 14 bold'), tags=("", "mobile"), anchor="center")

        # pour gérer un futur compte à rebours
        #self.timer.config(text=str(self.modele.partie.timer))

        # On dessine les creeps en ajoutant le tag mobile puisqu'on efface et réaffiche les choses mobiles
        for creep in self.modele.partie.creeps:
            x = creep.x
            y = creep.y
            r = creep.rayon
            largeur_barre_vie = creep.barre_vie.largeur
            hauteur_barre_vie = creep.barre_vie.hauteur
            type_image = creep.typeimage
            self.canevas.create_image(x, y, image=self.sprites[type_image][creep.noimage], tags=("creep", "mobile"))
            if (isinstance(creep, Modele.Boss)):
                self.canevas.create_rectangle(x - r * 1.6, y - hauteur_barre_vie - (r + 25),
                                              (x - r * 1.8) + largeur_barre_vie, y + hauteur_barre_vie - (r + 25),
                                              fill="OliveDrab1", tags=("creep", "mobile"))
            else:
                self.canevas.create_rectangle(x - r * 1.6, y - hauteur_barre_vie - (r + 15),
                                              (x - r * 1.8) + largeur_barre_vie, y + hauteur_barre_vie - (r + 15),
                                              fill="OliveDrab1", tags=("creep", "mobile"))
            if(isinstance(creep, Modele.Creep_Insomnie)):
                d = creep.rayon_detection
                self.canevas.create_oval(x - d, y - d, x + d, y + d, outline="#ffcc00", dash=6, width=2,
                                         tags=("creep", "mobile"))

        # On efface et réaffiche ici seulement les missiles de la tour et pas les tours elles-mêmes,
        # dont on se charge dans la fonction afficher_tour()
        for tour in self.modele.partie.tours:
            if isinstance(tour, Modele.Tour_Confiance):
                self.canevas.create_image(tour.x, tour.y, image=self.img_tour["tour_confiance"], tags=("tour", "mobile"))
                for missile in tour.missiles:
                    if not missile.cible_atteinte:
                        x = missile.x
                        y = missile.y
                        d = missile.demitaille
                        self.canevas.create_oval(x - d, y - d, x + d, y + d, fill="orange", outline="",
                                                 tags=("", "mobile"))
                        self.canevas.create_oval(x-d/2, y-d/2, x+d/2, y+d/2, fill="yellow", outline="", tags=("", "mobile"))

                        for flammeche in range(3):
                            x_flammeche = x + random.randrange(-12, 12)
                            y_flammeche = y + random.randrange(-12, 12)
                            taille_flammeche = 1
                            self.canevas.create_oval(x_flammeche + taille_flammeche, y_flammeche + taille_flammeche, x_flammeche - taille_flammeche, y_flammeche - taille_flammeche,
                                                     fill="orange", outline="", tags=("", "mobile"))

            elif isinstance(tour, Modele.Tour_Relation):
                self.canevas.create_image(tour.x, tour.y, image=self.img_tour["tour_relation"], tags=("tour", "mobile"))
                if tour.laser is not None and tour.laser_actif:
                    self.canevas.create_line(tour.x, tour.y - tour.buffer_y, tour.laser.cible_x, tour.laser.cible_y, fill='red',
                                             width=tour.laser.largeur, tags=("", "mobile"))
                    self.canevas.create_line(tour.x, tour.y - tour.buffer_y, tour.laser.cible_x, tour.laser.cible_y, fill='orange',
                                             width=tour.laser.largeur/2, tags=("", "mobile"))
            elif isinstance(tour, Modele.Tour_Sommeil):
                self.canevas.create_image(tour.x, tour.y, image=self.img_tour["tour_sommeil"], tags=("tour", "mobile"))
                x = tour.x + tour.buffer_x
                y = tour.y - tour.buffer_y
                r = tour.rayon_detection
                self.canevas.create_oval(x - r, y - r, x + r, y + r, width=tour.bordure, outline="white", dash=(1, 6, 2, 1),
                                                tags=("zone_tour", "", "mobile"))

        for valeur in self.modele.partie.valeur_texte:
            if valeur.type == "butin":
                self.canevas.create_text(valeur.x, valeur.y,
                                     text=valeur.val,
                                     fill="black", font=('Helvetica 14 bold'), tags=("", "mobile"), anchor="center")
                self.canevas.create_text(valeur.x, valeur.y - 2,
                                         text=valeur.val,
                                         fill="white", font=('Helvetica 14 bold'), tags=("", "mobile"), anchor="center")
            elif valeur.type == "ralentie":
                self.canevas.create_text(valeur.x, valeur.y,
                                     text=valeur.val,
                                     fill="black", font=('Helvetica 11 bold'), tags=("", "mobile"), anchor="center")
                self.canevas.create_text(valeur.x, valeur.y - 2,
                                         text=valeur.val,
                                         fill="#ffcc00", font=('Helvetica 11 bold'), tags=("", "mobile"), anchor="center")
            elif valeur.type == "antidepresseur":
                self.canevas.create_text(valeur.x, valeur.y,
                                         text=valeur.val,
                                         fill="black", font=('Helvetica 11 bold'), tags=("", "mobile"), anchor="center")
                self.canevas.create_text(valeur.x, valeur.y - 2,
                                         text=valeur.val,
                                         fill="#37c418", font=('Helvetica 11 bold'), tags=("", "mobile"),
                                         anchor="center")
            elif valeur.type == "degat":
                self.interface.create_text(valeur.x, valeur.y - 2,
                                           text=valeur.val,
                                           fill=self.coul_sec, font=('Helvetica 14 bold'), tags=("", "mobile"),
                                           anchor="center")
                self.interface.create_text(valeur.x, valeur.y,
                                           text=valeur.val,
                                           fill="#eb8a98", font=('Helvetica 14 bold'), tags=("", "mobile"),
                                           anchor="center")
            elif valeur.type == "motivation":
                self.interface.create_text(valeur.x, valeur.y - 2,
                                           text=valeur.val,
                                           fill=self.coul_sec, font=('Helvetica 14 bold'), tags=("", "mobile"),
                                           anchor="center")
                self.interface.create_text(valeur.x, valeur.y,
                                           text=valeur.val,
                                           fill="#608400", font=('Helvetica 14 bold'), tags=("", "mobile"),
                                           anchor="center")
            elif valeur.type == "upgrade":
                self.canevas.create_text(valeur.x, valeur.y,
                                         text=valeur.val,
                                         fill="black", font=('Helvetica 11 bold'), tags=("", "mobile"), anchor="center")
                self.canevas.create_text(valeur.x, valeur.y - 2,
                                         text=valeur.val,
                                         fill="#37c418", font=('Helvetica 11 bold'), tags=("", "mobile"),
                                         anchor="center")

        if self.modele.partie.annonce:
            type = self.parent.modele.partie.annonce.type
            if type == "principale":
                font = str(42)
            else:
                font = str(22)
            self.canevas.create_text(self.modele.partie.annonce.x, self.modele.partie.annonce.y,
                                     text=self.modele.partie.annonce.message,
                                     fill="red", font=('Helvetica ' + font + ' bold'), tags=("", "mobile",  "annonce"), anchor="center")
            self.canevas.create_text(self.modele.partie.annonce.x, self.modele.partie.annonce.y - 3,
                                     text=self.modele.partie.annonce.message,
                                     fill="orange", font=('Helvetica ' + font + ' bold'), tags=("", "mobile",  "annonce"), anchor="center")

    # On affiche la nouvelle tour, qu'on efface PAS par la suite.
    # Réception de la tour retourné par la fonction creer_tour() dans le Contrôleur
    def afficher_tour(self, tour):
        self.canevas.delete("tour_temp")
        x = tour.x
        y = tour.y
        d = tour.demi_taille
        r = tour.rayon_detection
        z = tour.zone_occupee
        self.canevas.create_oval(x - r, y - r, x + r, y + r, outline="grey", dash="30", tags=("rayon_tour"))
        self.canevas.create_rectangle(x - d - z, y - d - z, x + d + z, y + d + z, fill="", outline="",
                                      tags=("zone_tour", ""))

    def suivre_tour(self, evt):
        x = evt.x
        y = evt.y
        self.canevas.delete("tour_temp")
        if self.type_tour == "confiance":
            self.canevas.create_image(x, y, image=self.img_tour["tour_confiance_trans"], tags=("tour_temp"))
        elif self.type_tour == "relation":
            self.canevas.create_image(x, y, image=self.img_tour["tour_relation_trans"], tags=("tour_temp"))
        elif self.type_tour == "sommeil":
            self.canevas.create_image(x, y, image=self.img_tour["tour_sommeil_trans"], tags=("tour_temp"))

    def creer_tour(self, type_tour):
        if not self.partie_en_pause:
            if self.parent.faire_acheter(type_tour):
                self.type_tour = type_tour
                # Motion pour promener le fantome
                self.canevas.bind("<Motion>", self.suivre_tour)
                # Button pour l'installer
                self.canevas.bind("<Button>", self.installer_tour)
            else:
                if type_tour == "confiance":
                    self.bouton_tour_confiance.deselect()
                elif type_tour == "relation":
                    self.bouton_tour_relation.deselect()
                elif type_tour == "sommeil":
                    self.bouton_tour_sommeil.deselect()
                self.parent.creer_annonce("Pas assez de motivation", "secondaire")

    def installer_tour(self, evt):
        x = evt.x
        y = evt.y
        listeitems = self.canevas.find_overlapping(evt.x - 16, evt.y - 16, evt.x + 16, evt.y + 16)
        for item in listeitems:
            if "chemin" in self.canevas.gettags(item) \
                    or "zone_chemin" in self.canevas.gettags(item) \
                    or "tour" in self.canevas.gettags(item) \
                    or "zone_tour" in self.canevas.gettags(item):
                        self.parent.creer_annonce("Impossible!", "secondaire")
                        return False
        if self.type_tour == "confiance":
            self.parent.creer_tour(x, y, "confiance")
            self.bouton_tour_confiance.deselect()  # ceci relache le bouton radio
        elif self.type_tour == "relation":
            self.parent.creer_tour(x, y, "relation")
            self.bouton_tour_relation.deselect()
        elif self.type_tour == "sommeil":
            self.parent.creer_tour(x, y, "sommeil")
            self.bouton_tour_sommeil.deselect()
        self.canevas.unbind("<Motion>")
        self.canevas.unbind("<Button>")

    def upgrade_tour(self, type_tour):
        self.parent.faire_upgrade_tour(type_tour)

    def charger_gifs(self, fichier):
        nom_gif = fichier
        listeimages = []
        testverite = 1
        noindex = 0
        while testverite:
            try:
                img = PhotoImage(file=nom_gif, format="gif -index " + str(noindex))
                listeimages.append(img)
                noindex += 1
            except Exception:
                testverite = 0
        return listeimages

    def afficher_fin_partie(self):
        if not self.menu_game_over:
            self.menu_game_over = True
            self.canevas.create_text(self.modele.carte.largeur/2, 312, text="PARTIE TERMINÉE", fill="red", font=('Helvetica 42 bold'), tags="bouton_partie")
            self.canevas.create_text(self.modele.carte.largeur/2, 309, text="PARTIE TERMINÉE", fill="orange", font=('Helvetica 42 bold'), tags="bouton_partie")
            self.afficher_btn_partie_terminee()

    def afficher_partie_gagnee(self):
        self.canevas.create_text(self.modele.carte.largeur/2, 312, text="VICTOIRE !", fill="red", font=('Helvetica 42 bold'),
                                 tags="bouton_partie", anchor="center")
        self.canevas.create_text(self.modele.carte.largeur/2, 309, text="VICTOIRE !", fill="orange", font=('Helvetica 42 bold'),
                                 tags="bouton_partie", anchor="center")
        self.afficher_btn_partie_terminee()

    def afficher_btn_partie_terminee(self):
        self.bouton_partie_game_over = Button(self.canevas, text="Réessayer", width=25, font=('Helvetica 12 bold'),
                                              fg=self.coul_primaire, bg=self.coul_sec, anchor="center")
        self.bouton_partie_game_over.bind("<Button-1>", self.parent.game_over)
        self.canevas.create_window(self.modele.carte.largeur / 2, 375, window=self.bouton_partie_game_over,
                                   tags="bouton_partie")

        self.bouton_retour_menu = Button(self.canevas, text="Retourner au menu", width=25, font=('Helvetica 12 bold'),
                                         fg=self.coul_primaire, bg=self.coul_sec, anchor="center")
        self.bouton_retour_menu.bind("<Button-1>", self.afficher_menu)
        self.canevas.create_window(self.modele.carte.largeur / 2, 420, window=self.bouton_retour_menu,
                                   tags="bouton_partie")

    def afficher_menu(self, evt):
        self.menu_game_over = False
        self.changer_cadre("splash")

    def redemarrer_interface(self):
        self.menu_game_over = False
        self.canevas.delete("bouton_partie")
        self.canevas.delete("tour")
        self.canevas.delete("zone_tour")
        self.canevas.delete("rayon_tour")
        self.canevas.delete("tour_temp")
        self.canevas.delete("no_vague")

    def pause(self, source):
        if source != "redemarrer":
            self.partie_en_pause = not self.partie_en_pause
        else:
            self.partie_en_pause = False
        if self.partie_en_pause and source != "redemarrer":
            self.canevas.delete("annonce")
            self.canevas.create_text(480, self.modele.hauteur / 2 - 100,
                                     text="PAUSE",
                                     fill="red", font=('Helvetica 42 bold'), tags=("", "mobile", "annonce"),
                                     anchor="center")
            self.canevas.create_text(480, self.modele.hauteur/2-103,
                                     text="PAUSE",
                                     fill="orange", font=('Helvetica 42 bold'), tags=("", "mobile", "annonce"),
                                     anchor="center")

    def nouveau_score(self):
        score = (self.modele.partie.score)
        nom = simpledialog.askstring(f"Nouveau score de {score}!", "Quel est votre nom?",
                                     parent=self.root)
        if nom:
            nom = nom.replace(" ", "")
            with open('score.txt', 'a') as f:
                f.write(f"{score} {nom}" + "\n")


    def afficher_score(self, evt):
        scores_affiches = ""
        if not os.path.exists('score.txt'):
            with open('score.txt', 'w'):
                pass

        with open('score.txt', 'r') as f:
            for line in f:
                score_entree = line.split()
                score_valeur, score_nom = score_entree
                self.modele.liste_score.append([int(score_valeur), score_nom.strip()])

            self.modele.liste_score = sorted(self.modele.liste_score, key=lambda x: x[0], reverse=True)
            for score in self.modele.liste_score:
                scores_affiches += f"{score[0]:<16} {score[1]}\n"

        messagebox.showinfo("Scores", scores_affiches)
        self.modele.liste_score.clear()