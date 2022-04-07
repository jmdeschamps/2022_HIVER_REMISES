from email.mime import image
from tkinter import *
from turtle import color
from webbrowser import get
from PIL import Image, ImageTk, ImageDraw
import os


class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.creepsImg = []
        self.toursImg = []
        self.argent = str(self.modele.partie_courante.argent)
        self.score = str(self.modele.partie_courante.score)
        self.exp = str(self.modele.exp)
        self.message = ""
        self.tours_feu_img = []
        self.tours_poison_img = []
        self.tours_glace_img = []
        self.tours_mitraille_img = []
        self.root = Tk()
        self.root.title("Tower Defence EXTREME ACTION")
        self.parent.charger_images()
        self.creer_cadres_jeu()
        self.afficher_background()
        self.image_tour_selectionnee = None
        self.username = ""
        self.btn_ameliorer = None
        self.btn_vendre = None
        self.dic_ameliorations = {"FEU":"Amélioration possible: \ndouble dégâts",
                                  "GLACE":"Amélioration possible: \nimmobilisation longue durée",
                                  "POISON":"Amélioration possible: \noccasionne du dégât sur le temps",
                                  "MITRAILLE":"Amélioration possible: \nvitesse et rayon d'attaque accrue"}

    def creer_cadres_jeu(self):
        self.creer_cadre_fenetre()
        self.creer_cadre_zone_jeu()

    def creer_cadre_fenetre(self):
        self.cadre_fenetre = Frame(self.root, width=self.modele.largeur_fenetre, height=self.modele.hauteur_fenetre,
                                   bg="black")
        self.cadre_fenetre.pack()
        self.cadre_fenetre.pack_propagate(0)

    def creer_cadre_zone_jeu(self):
        self.cadre_zone_jeu = Frame(self.cadre_fenetre, width=self.modele.largeur_canevas,
                                    height=self.modele.hauteur_canevas,
                                    bg="white")
        self.canevas = Canvas(self.cadre_zone_jeu, width=self.modele.largeur_canevas - 200,
                              height=self.modele.hauteur_canevas,
                              bg=self.modele.partie_courante.sentier.couleurBG)

        self.canevas.pack(side=LEFT)
        self.cadre_zone_jeu.place(relx=.5, rely=.5, anchor=CENTER)
        # self.canevas.bind("<Button-1>", self.demarrer_vague)
        self.canevas.bind("<Button-1>", self.afficher_coordonees)
        self.canevas.create_line(55, 85, 155, 85, 105, 180, 55, 85)


        
        self.creer_page_intro()

    def creer_cadre_commande(self):         # Le cadre des commandes / scores / tutoriel            

        self.cadre_commande = LabelFrame(self.cadre_zone_jeu, text="Centre de Commandement", font=("tahoma", 11, "normal"),
                                         width=250,
                                         bg="green", fg="yellow", bd=5)
        self.cadre_commande.pack(side=RIGHT, fill="both")

        self.creer_cadre_statistique_panneau_commande()
        self.creer_cadre_tours_panneau_commande()
        self.creer_cadre_tutoriel()
        self.creer_boutons_panneau_commande()

    def creer_cadre_statistique_panneau_commande(self):         # Le cadre des scores
        
        # Cadre Principale
        self.cadre_statistique = Frame(self.cadre_commande, width=200, height=175, bg="green")
        self.cadre_statistique.pack(side=TOP)
        self.cadre_statistique.pack_propagate(0)

        # Vie
        self.cadre_vie = LabelFrame(self.cadre_statistique, width=150, height=32, text="Vie", bg="green",
                                      fg="yellow",
                                      labelanchor=NE, relief=RAISED)
        self.cadre_vie.pack(side=TOP, padx=5, pady=5)
        self.cadre_vie.pack_propagate(0)
        self.vie = StringVar()
        self.vie.set(str(self.modele.partie_courante.vie))
        self.vie_affichage = Label(self.cadre_vie, text="0", textvariable=self.vie, bg="green", fg="yellow").pack(
            side=LEFT)

        # Score
        self.cadre_score = LabelFrame(self.cadre_statistique, width=150, height=32, text="Score", bg="green",
                                      fg="yellow",
                                      labelanchor=NE, relief=RAISED)
        self.cadre_score.pack(side=TOP, padx=5, pady=5)
        self.cadre_score.pack_propagate(0)
        self.pointage = StringVar()
        self.pointage.set(str(self.modele.partie_courante.score))
        self.score = Label(self.cadre_score, text="0", textvariable=self.pointage, bg="green", fg="yellow").pack(
            side=LEFT)

        # Piece Or
        self.argent = StringVar()
        self.argent.set(str(self.modele.partie_courante.argent))

        self.cadre_piece_or = LabelFrame(self.cadre_statistique, width=150, height=32, text="Piece d'or", bg="green", fg="yellow",
                                         labelanchor=NE, relief=RAISED)
        self.cadre_piece_or.pack(side=TOP, padx=5, pady=5)
        self.cadre_piece_or.pack_propagate(0)
        self.piece_or = Label(self.cadre_piece_or, text="0", textvariable=self.argent, bg="green", fg="yellow").pack(side=LEFT)

        # Experience affichage du niveau
        self.cadre_experience = LabelFrame(self.cadre_statistique, width=150, height=32, text="Experience", bg="green", fg="yellow",
                                           labelanchor=NE, relief=RAISED)
        self.cadre_experience.pack(side=TOP, padx=5, pady=5)
        self.cadre_experience.pack_propagate(0)
        self.exp = StringVar()
        self.exp.set("Niveau " + str(self.modele.calculer_niveau_joueur()))
        self.experience = Label(self.cadre_experience, text="0", textvariable=self.exp, bg="green", fg="yellow").pack(side=LEFT)

        self.update_argent()

    def creer_cadre_tours_panneau_commande(self):
        # Le cadre et l'image des tours
        self.cadre_tours = LabelFrame(self.cadre_commande, width=200, height=165, text="Tours militaires", bg="yellow", font=("tahoma", 11, "normal"))
        self.cadre_tours.pack(side=TOP)
        self.cadre_tours.pack_propagate(0)
        # le cadre de la tour 1-2
        self.cadre_interieur_1_2 = Frame(self.cadre_tours, width=200, height=70, bg="yellow")
        self.cadre_interieur_1_2.pack(side=TOP)
        self.cadre_interieur_1_2.pack_propagate(0)
        # le cadre de la tour 3-4
        self.cadre_interieur_3_4 = Frame(self.cadre_tours, width=200, height=70, bg="yellow")
        self.cadre_interieur_3_4.pack(side=TOP)
        self.cadre_interieur_3_4.pack_propagate(0)
        # Image de la tour 1 (feu)
        self.image_tour_1 = Image.open("images\Towers\Tour_feu.png")

        self.image_tour_1_resize = self.image_tour_1.resize((60, 60), Image.ANTIALIAS)

        self.image_tour_1_tk = ImageTk.PhotoImage(self.image_tour_1_resize)
        self.image_tour_1_label = Label(self.cadre_interieur_1_2, width=70, height=55, image=self.image_tour_1_tk,
                                        bg="yellow", cursor="draped_box", borderwidth=4, relief="raised")
        self.image_tour_1_label.bind("<ButtonPress-1>", self.selectionner_tour_feu)
        self.image_tour_1_label.pack(side=LEFT)


        # Image de la tour 2 (glace)
        self.image_tour_2 = Image.open("images\Towers\Tour_bois.png")

        self.image_tour_2_resize = self.image_tour_2.resize((60, 60), Image.ANTIALIAS)
        self.image_tour_2_tk = ImageTk.PhotoImage(self.image_tour_2_resize)
        self.image_tour_2_label = Label(self.cadre_interieur_1_2, width=70, height=55, image=self.image_tour_2_tk,
                                        bg="yellow", cursor="draped_box", borderwidth=4, relief="raised")
        self.image_tour_2_label.bind("<ButtonPress-1>", self.selectionner_tour_glace)
        self.image_tour_2_label.pack(side=RIGHT)

        # Image de la tour 3 (poison)
        self.image_tour_3 = Image.open("images\Towers\Tour_poison.png")

        self.image_tour_3_resize = self.image_tour_3.resize((60, 60), Image.ANTIALIAS)
        self.image_tour_3_tk = ImageTk.PhotoImage(self.image_tour_3_resize)
        self.image_tour_3_label = Label(self.cadre_interieur_3_4, width=70, height=55, image=self.image_tour_3_tk,
                                        bg="yellow", cursor="draped_box", borderwidth=4, relief="raised")
        self.image_tour_3_label.bind("<ButtonPress-1>",  self.selectionner_tour_poison)
        self.image_tour_3_label.pack(side=LEFT)

        # Image de la tour 4
        self.image_tour_4 = Image.open("images\Towers\Tour_roche.png")

        self.image_tour_4_resize = self.image_tour_4.resize((60, 60), Image.ANTIALIAS)
        self.image_tour_4_tk = ImageTk.PhotoImage(self.image_tour_4_resize)
        self.image_tour_4_label = Label(self.cadre_interieur_3_4, width=70, height=55, image=self.image_tour_4_tk,
                                        bg="yellow", cursor="draped_box", borderwidth=4, relief="raised")
        self.image_tour_4_label.bind("<ButtonPress-1>",  self.selectionner_tour_mitraille)
        self.image_tour_4_label.pack(side=RIGHT)

    def creer_boutons_panneau_commande(self):        # Les boutons

        # Le cadre des niveaux


        # Bouton Reinitialiser
        self.btn_start = StringVar()
        self.btn_start.set("Reinitialiser")
        self.bouton_commencer = Button(self.cadre_zone_jeu, text="", textvariable=self.btn_start, borderwidth=5, width=10, padx=5, pady=5, command=self.parent.reinitialiser_jeu)

        self.bouton_commencer.pack(side=RIGHT)
        self.bouton_commencer.place(x=1010, y=553)
        # Bouton Commencer / Pause
        self.btn_pause_nom = StringVar()
        self.btn_pause_nom.set("Commencer")
        self.bouton_pause = Button(self.cadre_zone_jeu, text="", textvariable=self.btn_pause_nom, borderwidth=5, width=10, padx=5, pady=5, command=self.changement_pause)
        self.bouton_pause.pack(side=RIGHT)
        self.bouton_pause.place(x=1110, y=510)
        # Bouton Vitesse
        self.btn_vitesse_nom = StringVar()
        self.btn_vitesse_nom.set("Vitesse")
        self.bouton_vitesse = Button(self.cadre_zone_jeu, text="", textvariable=self.btn_vitesse_nom, borderwidth=5, width=10, padx=5, pady=5, command=self.changement_vitesse)
        self.bouton_vitesse.pack(side=RIGHT)
        self.bouton_vitesse.place(x=1010, y=510)
        # Bouton quitter
        self.bouton_quitter = Button(self.cadre_zone_jeu, text="Quitter", borderwidth=5, width=10, padx=5, pady=5,
                                     fg="red", command=self.exit_program)
        self.bouton_quitter.pack(side=RIGHT)
        self.bouton_quitter.place(x=1110, y=553)

    def changement_vitesse(self):
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()
        if self.btn_vendre is not None:
            self.btn_vendre.destroy()

        self.parent.changement_vitesse()
        if self.parent.vit_jeu:
            self.btn_vitesse_nom.set("Vitesse (X2)")
        else :
            self.btn_vitesse_nom.set("Vitesse")

    def changement_pause(self):
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()
        if self.btn_vendre is not None:
            self.btn_vendre.destroy()
        if not self.modele.en_cours:
            self.parent.en_jeu()
            self.parent.update_message("Vague " + str(self.modele.partie_courante.vague + 1) + " démarrée")
            self.vie.set(str(self.modele.partie_courante.vie))
            self.parent.demarrer_chrono()
            self.parent.jouer()
            self.btn_pause_nom.set("Pause")
        else:
            self.parent.changement_pause()
            if not self.parent.en_cours:
                self.btn_pause_nom.set("Play")
            else :
                self.btn_pause_nom.set("Pause")

    def creer_cadre_tutoriel(self):         # Le cadre du tutoriel

        self.cadre_tutoriel = LabelFrame(self.cadre_commande, width=200, height=150, text="Centre de renseignement", fg="yellow", font=("tahoma", 11, "normal"),
                                        bg="green", relief=RIDGE)
        self.cadre_tutoriel.pack(side=TOP)
        self.message = StringVar()
        self.message.set(str(self.modele.partie_courante.message))

        self.cadre_tutoriel.pack_propagate(0)

        self.cadre_fenetre_tutoriel = Label(self.cadre_tutoriel, text="", textvariable=self.message,
                                            wraplength=180, width=180, height=100, bg="green", fg="yellow")
        self.cadre_fenetre_tutoriel.pack(side=TOP, anchor=CENTER, padx=5, pady=5)

    def creer_page_intro(self):         # Page d'introduction

        # Image de la page d'intro
        self.page_intro_Img = Image.open("images\PageIntro\page_intro.png")
        self.background_intro = ImageTk.PhotoImage(self.page_intro_Img)

        # Frame de la page d'intro
        self.cadre_intro = Frame(self.canevas, width=self.modele.largeur_canevas - 200,
                                 height=self.modele.hauteur_canevas, bg=self.modele.partie_courante.sentier.couleurBG)
        self.cadre_intro.pack()
        self.cadre_intro.pack_propagate(0)
        self.cadre_intro_image = Label(self.cadre_intro, image=self.background_intro, anchor=NE)
        self.cadre_intro_image.pack()
        self.cadre_intro_image.pack_propagate(0)
        
        self.creer_cadre_registre()

    def creer_page_fin_partie(self):         # Page de fin de partie

        # Image de la page de fin de partie
        self.page_fin_partie_Img = Image.open("images\PageIntro\page_final.png")
        self.page_fin_partie_Img_resized = self.page_fin_partie_Img.resize((1100, 800), Image.ANTIALIAS)

        self.background_final = ImageTk.PhotoImage(self.page_fin_partie_Img_resized)

        # Frame de la page de fin de partie
        self.cadre_final = Frame(self.canevas, width=self.modele.largeur_canevas - 200,
                                 height=self.modele.hauteur_canevas, bg=self.modele.partie_courante.sentier.couleurBG)
        self.cadre_final.pack()
        self.cadre_final.pack_propagate(0)
        self.cadre_final_image = Label(self.cadre_final, image=self.background_final, anchor=N)
        self.cadre_final_image.pack()

    def afficher_coordonees(self, event):
        print(event.x, event.y)

    def update_commencer(self, message):
        self.btn_start.set(message)

    def afficher_objets(self):
        self.canevas.delete(ALL)
        self.afficher_background()
        self.afficher_creeps()
        self.afficher_tours()
        self.afficher_attaque_tour()

    def update_vie(self, message):
        self.vie.set(message)

    def update_argent(self):
       self.argent.set(str(self.modele.partie_courante.argent))

    def update_score(self):
        self.pointage.set(str(self.modele.partie_courante.score))

    def update_exp(self):
        self.exp.set("Niveau " + str(self.modele.calculer_niveau_joueur()))

    def update_message_tutoriel(self, message):
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()
        if self.btn_vendre is not None:
            self.btn_vendre.destroy()
        self.message.set(message)

    def update_commencer(self, message):
        self.btn_pause_nom.set(message)


    def afficher_background(self):
        self.canevas.create_image(0, 0, anchor=NW, image=self.modele.dic_img["autre"]["background"][0])

    def afficher_creeps(self):
        #self.creepsImg = []
        for i in self.modele.partie_courante.creeps:
            if i.est_actif:
                self.parent.verifier_direction_creep(i)
                #self.creepsImg.append(img)
                delta_x = i.largeur / 2
                delta_y = i.hauteur / 2
                self.canevas.create_rectangle(i.pos_x - delta_x, i.pos_y - delta_y, i.pos_x + delta_x,
                                              i.pos_y - delta_y + 2, fill="red")
                if i.points_vie == i.max_points_vie:
                    self.canevas.create_rectangle(i.pos_x - delta_x, i.pos_y - delta_y, i.pos_x + delta_x,
                                                  i.pos_y - delta_y + 2, fill="green")
                else:
                    self.canevas.create_rectangle(i.pos_x - delta_x, i.pos_y - delta_y,
                                                  i.pos_x - delta_x + (i.largeur / i.max_points_vie * i.points_vie),
                                                  i.pos_y - delta_y + 2, fill="green")
                self.canevas.create_image(i.pos_x, i.pos_y, anchor=CENTER, image=self.modele.dic_img[i.cle][i.direction][i.index])

    def traiter_creation_tour(self, evt, type_tour):
        if 20 <= evt.x <= 980:  # éviter créer tours sur menu d'affichage | largeur map == 1000px - demitaille tour
            if 20 <= evt.y <= 580:  # même chose pour hauteur | hauteur map == 600px
                self.parent.traiter_creation_tour(evt.x, evt.y, type_tour)

    def unbind_creation_tour(self):
        self.canevas.unbind("<ButtonRelease-1>")

    def afficher_tours(self):
        tours_feu = self.modele.partie_courante.tours_feu
        tours_poison = self.modele.partie_courante.tours_poison
        tours_glace = self.modele.partie_courante.tours_glace
        tours_mitraille = self.modele.partie_courante.tours_mitraille

        for tour_feu in tours_feu:
            img = self.canevas.create_image(tour_feu.x, tour_feu.y, anchor=CENTER, image=self.modele.dic_img["tour"]["feu"][0])
            self.canevas.tag_bind(img, '<1>', lambda event: self.click_tour(event, tour_feu))
        for tour_poison in tours_poison:
            img = self.canevas.create_image(tour_poison.x, tour_poison.y, anchor=CENTER, image=self.modele.dic_img["tour"]["poison"][0])
            self.canevas.tag_bind(img, '<1>', lambda event: self.click_tour(event, tour_poison))
        for tour_glace in tours_glace:
            img = self.canevas.create_image(tour_glace.x,tour_glace.y, anchor=CENTER, image=self.modele.dic_img["tour"]["glace"][0])
            self.canevas.tag_bind(img, '<1>', lambda event: self.click_tour(event, tour_glace))
        for tour_mitraille in tours_mitraille:
            img = self.canevas.create_image(tour_mitraille.x, tour_mitraille.y, anchor=CENTER, image=self.modele.dic_img["tour"]["mitraille"][0])
            self.canevas.tag_bind(img, '<1>', lambda event: self.click_tour(event, tour_mitraille))


    def click_tour(self, event, tour):
        # Bouton Vitesse
        print("afficher")
        if self.btn_vendre is not None:
            self.btn_vendre.destroy()
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()

        tour_selectionnee = self.parent.determiner_type(event.x, event.y, tour)

        if tour_selectionnee.niveau < tour_selectionnee.max_niveau:
            self.parent.update_message(self.dic_ameliorations[tour_selectionnee.type])
            # bouton améliorer
            self.text_ameliorer = StringVar()
            self.text_ameliorer.set("Améliorer (" + str(tour_selectionnee.cout_amelioration) + "$)")
            self.btn_ameliorer = Button(self.cadre_zone_jeu, text="", textvariable=self.text_ameliorer, borderwidth=5)
            self.btn_ameliorer.bind("<Button-1>", lambda event: self.ameliorer(tour_selectionnee))
            self.btn_ameliorer.place(x=1106, y=400, anchor=CENTER)
        else:
            self.parent.update_message("Potentiel maximum de la tour atteint")

        self.btn_vendre = Button(self.cadre_zone_jeu, text="Vendre (" + str(
            (int)(self.parent.modele.tours_cout[tour_selectionnee.type] * 0.8)) + "$)", borderwidth=5)
        self.btn_vendre.bind("<Button-1>", lambda event: self.tour_vendre(tour_selectionnee))
        self.btn_vendre.place(x=1106, y=475, anchor=CENTER)

    def ameliorer(self, tour):
        confirmation = self.parent.ameliorer_tour(tour)
        self.update_argent()
        self.btn_ameliorer.destroy()
        self.btn_vendre.destroy()
        self.parent.update_message(confirmation)

    def tour_vendre(self, tour):
        # supprimer la tour dans la partie et la vue
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()
        self.btn_vendre.destroy()
        self.parent.vendre_tour(tour)
        self.afficher_objets()
        self.parent.update_message("Tour vendue")

    def afficher_attaque_tour(self):
        tours_feu = self.modele.partie_courante.tours_feu
        tours_glace = self.modele.partie_courante.tours_glace
        tours_poison = self.modele.partie_courante.tours_poison
        tours_mitraille = self.modele.partie_courante.tours_mitraille
        for tour in tours_feu:
            for projectile in tour.projectiles:
                self.canevas.create_rectangle(
                    projectile.x - projectile.largeur/2,
                    projectile.y - projectile.longueur/2,
                    projectile.x + projectile.largeur/2,
                    projectile.y + projectile.longueur/2,
                    fill="red",
                    tags="projectile_feu"
                )
        for tour in tours_glace:
            for projectile in tour.projectiles:
                self.canevas.create_rectangle(
                    projectile.x - projectile.largeur/2,
                    projectile.y - projectile.longueur/2,
                    projectile.x + projectile.largeur/2,
                    projectile.y + projectile.longueur/2,
                    fill="blue",
                    tags="projectile_glace"
                )
        for tour in tours_poison:
            for projectile in tour.projectiles:
                self.canevas.create_rectangle(
                    projectile.x - projectile.largeur/2,
                    projectile.y - projectile.longueur/2,
                    projectile.x + projectile.largeur/2,
                    projectile.y + projectile.longueur/2,
                    fill="purple",
                    tags="projectile_poison"
                )
        for tour in tours_mitraille:
            for projectile in tour.projectiles:
                self.canevas.create_rectangle(
                    projectile.x - projectile.largeur/2,
                    projectile.y - projectile.longueur/2,
                    projectile.x + projectile.largeur/2,
                    projectile.y + projectile.longueur/2,
                    fill="grey",
                    tags="projectile_mitraille"
                )

    def effacer_projectiles(self):
        tours_feu = self.modele.partie_courante.tours_feu
        tours_glace = self.modele.partie_courante.tours_glace
        tours_poison = self.modele.partie_courante.tours_poison
        tours_mitraille = self.modele.partie_courante.tours_mitraille
        for tour in tours_feu:
            tour.projectiles = []
            tour.attaque_en_cours = False
        for tour in tours_glace:
            tour.projectiles = []
            tour.attaque_en_cours = False
        for tour in tours_poison:
            tour.projectiles = []
            tour.attaque_en_cours = False
        for tour in tours_mitraille:
            tour.projectiles = []
            tour.attaque_en_cours = False

    def selectionner_tour_feu(self, evt):
        self.image_tour_selectionnee = "FEU"
        self.positionner_tour("FEU")
        self.parent.update_message("Type : Feu \n Prix : 180 pièces d'or \n Niveau : 1") # ajouter la variable niveau pour les tours

    def selectionner_tour_poison(self, evt):
        self.image_tour_selectionnee = "POISON"
        self.positionner_tour("POISON")
        self.parent.update_message("Type : poison \n Prix : 275 pièces d'or \n Niveau : 1 \n \nCapacité spéciale : Ralentis les creeps")

    def selectionner_tour_glace(self, evt):
        if self.modele.calculer_niveau_joueur() >= 2:
            self.image_tour_selectionnee = "GLACE"
            self.positionner_tour("GLACE")
            self.parent.update_message("Type : glace \n Prix : 220 pièces d'or \n Niveau : 1 \n \n Capacité spéciale : Gèle un creep pour 1 secondes")
            self.parent.update_message("Type : glace \n "
                                       "Prix : 220 pièces d'or \n "
                                       "Niveau : 1 \n "
                                       "Lance des balles de neige \n\n"
                                       "Capacité: Gèle un creep durant 1 seconde \n!")
        else:
            self.parent.update_message("La tour Glace est disponible à partir du niveau 2 d'expérience.")

    def consulter_tour_glace(self, evt, tour_source, img_tour, img_id):
        self.parent.update_message("Type: " + str(tour_source.type) + "\n"
                                   "Niveau actuel: " + str(tour_source.niveau) + "\n"
                                   "Dégât actuel: " + str(tour_source.degat) + "\n\n"
                                   "Pour améliorer cette tour, faîtes CLIC-DROIT")
        self.canevas.tag_bind(
            img_id,
            '<Button-3>',
            # lambda event: self.afficher_suggestions_tour_glace(tour_source, img_tour)
            lambda event:self.parent.update_message("Hello World")
        )

    def afficher_suggestions_tour_glace(self, tour_source, img_tour):
        self.parent.update_message("Hello World")

    def traiter_amelioration_tour_glace(self, evt):
        self.parent.update_message("HELLO WORLD")

    def selectionner_tour_mitraille(self, evt):
        if self.modele.calculer_niveau_joueur() > 5:
            self.image_tour_selectionnee = "MITRAILLE"
            self.positionner_tour("MITRAILLE")
            self.parent.update_message("Type : Mitraille \n Prix : 335 pièces d'or \n Niveau : 1 \n \n Capacité spéciale : Attaque tous les creeps dans sa zone d'attaque")
        else:
            self.parent.update_message("La tour Mitraille est disponible à partir du niveau 6 d'expérience.")

    def positionner_tour(self, type_tour):
        if self.btn_ameliorer is not None:
            self.btn_ameliorer.destroy()
        if self.btn_vendre is not None:
            self.btn_vendre.destroy()
        types_tours = {
            "FEU": self.canevas.bind("<ButtonRelease-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "GLACE": self.canevas.bind("<ButtonRelease-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "POISON": self.canevas.bind("<ButtonRelease-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "MITRAILLE": self.canevas.bind("<ButtonRelease-1>", lambda event: self.traiter_creation_tour(event, type_tour))
        }
        types_tours[type_tour]

    def creer_page_fin_partie(self):         # Page de fin de partie
        # ajouter le joueur dans le DAO
        self.ficher_DAO_inscription_score()
        # affichage du joueur sur le cadre final
        self.inscription_score_background_final()

        # Image de la page de fin de partie
        self.page_fin_partie_Img = Image.open("images\PageIntro\page_final_score.png")
        self.background_final = ImageTk.PhotoImage(self.page_fin_partie_Img)

        # Frame de la page de fin de partie
        self.cadre_final = Frame(self.canevas, width=self.modele.largeur_canevas - 200,
                                 height=self.modele.hauteur_canevas, bg=self.modele.partie_courante.sentier.couleurBG)
        self.cadre_final.pack()
        self.cadre_final.pack_propagate(0)
        self.cadre_final_image = Label(self.cadre_final, anchor=NE, image=self.background_final, compound=CENTER, text= "== Game Over ==")
        self.cadre_final_image.pack()

    # Modification du background final en cas d'echec (avec les scores)
    def inscription_score_background_final(self):
        if self.username == "":
            self.username = "Joueur inconnu" 
        # ouverture de l<image pour ajouter score final
        self.original = Image.open("images\PageIntro\page_final.png")

        self.draw = ImageDraw.Draw(self.original)
        self.draw.text((1100,50), "== VOTRE SCORE FINAL == \n" + self.username + " : " + str(self.modele.partie_courante.score) + " points") 
        self.draw.text((300,50), "== Palmares TOP 10 == \n" + self.fichier_DAO_score_final_lecture()) 

        self.original.save("images\PageIntro\page_final_score.png")

    def creer_page_fin_partie_sucess(self):         # Page de fin de partie WIN
        # ajouter le joueur dans le DAO
        self.ficher_DAO_inscription_score()
        # affichage du joueur sur le cadre final
        self.inscription_score_background_final_sucess()

        # Image de la page de fin de partie
        self.page_fin_partie_Img = Image.open("images\PageIntro\page_win_score.png")
        self.background_final = ImageTk.PhotoImage(self.page_fin_partie_Img)

        # Frame de la page de fin de partie
        self.cadre_final = Frame(self.canevas, width=self.modele.largeur_canevas - 200,
                                 height=600, bg=self.modele.partie_courante.sentier.couleurBG)
        self.cadre_final.pack(side=BOTTOM)
        self.cadre_final.pack_propagate(0)
        self.cadre_final_image = Label(self.cadre_final, anchor=CENTER, image=self.background_final)
        self.cadre_final_image.pack()


    # Modification du background final en cas d'echec (avec les scores)
    def inscription_score_background_final_sucess(self):
        if self.username == "":
            self.username = "Joueur inconnu" 
        # ouverture de l<image pour ajouter score final
        self.original = Image.open("images\PageIntro\page_win.png")
        self.original_resize = self.original.resize((1200, 600), Image.ANTIALIAS)

        self.draw = ImageDraw.Draw(self.original_resize)
        self.draw.text((800,50), "== VOTRE SCORE FINAL == \n" + self.username + " : " + str(self.modele.partie_courante.score) + " points") 
        self.draw.text((800,100), "== Palmares TOP 10 == \n" + self.fichier_DAO_score_final_lecture()) 

        self.original_resize.save("images\PageIntro\page_win_score.png")

    def exit_program(self):
        self.root.destroy()

        # Creation du cadre de registre
    def creer_cadre_registre(self):
        # Cadre de Registre
        self.cadre_registre = Frame(self.cadre_intro_image, width = 250, height=150, bg=None)
        self.cadre_registre.pack(side=BOTTOM)
        self.cadre_registre.pack_propagate(0)
                
        # Nom du joueur
        self.registre = Label(self.cadre_registre, text="Entrer le nom du joueur", anchor=CENTER, width=50, padx=10, pady=15, bd=None)
        self.registre.pack()
        self.registre.pack_propagate(0)
        # Registre
        self.registre_nom_joueur = Entry(self.cadre_registre, width=50)
        self.registre_nom_joueur.pack()
        # Bouton start
        self.button_start_game = Button(self.cadre_registre, anchor=CENTER, text="Brint it ON !!!",
                                        borderwidth=15, padx=5, pady=5, bg="white", cursor='hand2', command=self.start_page_intro)
        self.button_start_game.pack(side=BOTTOM) 
    
    def start_page_intro(self):
        self.username = self.registre_nom_joueur.get()
        if self.username != "":
            self.lire_exp()
        self.cadre_intro.destroy()
        self.button_start_game.destroy()
        self.creer_cadre_commande()

    def ficher_DAO_inscription_score(self):
        mots = []
        file_path = 'DAO/userDAO.txt'
        file_path_exp = "DAO/data.txt"
        file_exists = os.path.isfile(file_path)
        f = open(file_path,"a")
        if self.username == "":
            self.username = "Joueur inconnu" 

        f.write(self.username + ":" + str(self.modele.partie_courante.score) + "\n")
        f.close()
        fichier = open(file_path_exp, "a")
        #content = fichier.readlines()
        if self.username != "Joueur inconnu":
            fichier.write(self.username + ":" + str(self.modele.exp) + "\n")
            fichier.close()

    def fichier_DAO_score_final_lecture(self):
        best10lines = ""
        count = 0
        file_path = 'DAO/userDAO.txt'
        file_exists = os.path.isfile(file_path)
        f = open(file_path,"r+")
        lines = sorted(f.readlines(), key=lambda line: int(line.strip().split(':')[1]), reverse=True)
        for line in lines:
            count+=1
            if(count <= 10):
                resultat = str(count) + "- " + str(line)
                best10lines += resultat
        f.close()
        return best10lines

    def  lire_exp(self):
        exp = ""
        fichier = open("DAO/data.txt", "r")
        content = fichier.readlines()
        print(content)
        for lignes in content:
            mots = lignes.split(":")
            if self.username == mots[0]:
                if mots[1] > exp:
                    exp = mots[1]

        self.parent.modele.exp = int(exp)

        fichier.close()