from tkinter import *
from PIL import Image, ImageTk

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

        self.root.title("Tower Defence EXTREME ACTION")  # Pierre
        self.creer_cadres_jeu()
        self.afficher_background()


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


        
        self.creer_page_intro()

    def creer_cadre_commande(self):         # Le cadre des commandes / scores / tutoriel            

        self.cadre_commande = LabelFrame(self.cadre_zone_jeu, text="Centre de Commandement", font=("Arial", 10),
                                         width=250,
                                         bg="green", fg="yellow", bd=5)
        self.cadre_commande.pack(side=RIGHT, fill="both")

        self.creer_cadre_statistique_panneau_commande()
        self.creer_cadre_tours_panneau_commande()
        self.creer_cadre_tutoriel()
        self.creer_boutons_panneau_commande()

    def creer_cadre_statistique_panneau_commande(self):         # Le cadre des scores
        
        # Cadre Principale
        self.cadre_statistique = Frame(self.cadre_commande, width=200, height=120, bg="green")
        self.cadre_statistique.pack(side=TOP)
        self.cadre_statistique.pack_propagate(0)


        # Score
        self.cadre_score = LabelFrame(self.cadre_statistique, width=150, height=28, text="Score", bg="green", fg="yellow",
                                      labelanchor=NE, relief=RAISED)
        self.cadre_score.pack(side=TOP, padx=5, pady=5)
        self.cadre_score.pack_propagate(0)
        self.pointage = StringVar()
        self.pointage.set(str(self.modele.partie_courante.score))
        self.score = Label(self.cadre_score, text="0", textvariable=self.pointage, bg="green", fg="yellow").pack(side=LEFT)
        
        
        # Piece Or
        self.argent = StringVar()
        self.argent.set(str(self.modele.partie_courante.argent))

        self.cadre_piece_or = LabelFrame(self.cadre_statistique, width=150, height=28, text="Piece d'or", bg="green", fg="yellow",
                                         labelanchor=NE, relief=RAISED)
        self.cadre_piece_or.pack(side=TOP, padx=5, pady=5)
        self.cadre_piece_or.pack_propagate(0)
        self.piece_or = Label(self.cadre_piece_or, text="0", textvariable=self.argent, bg="green", fg="yellow").pack(side=LEFT)

        # Experience
        self.cadre_experience = LabelFrame(self.cadre_statistique, width=150, height=28, text="Experience", bg="green", fg="yellow",
                                           labelanchor=NE, relief=RAISED)
        self.cadre_experience.pack(side=TOP, padx=5, pady=5)
        self.cadre_experience.pack_propagate(0)
        self.exp = StringVar()
        self.exp.set(str(self.modele.exp))
        self.experience = Label(self.cadre_experience, text="0", textvariable=str(self.exp), bg="green", fg="yellow").pack(side=LEFT)

        self.update_argent()

    def creer_cadre_tours_panneau_commande(self):
        # Le cadre et l'image des tours
        self.cadre_tours = LabelFrame(self.cadre_commande, width=200, height=220, text="Tours militaires", bg="yellow")
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
        # le cadre de la tour 5-6
        self.cadre_interieur_5_6 = Frame(self.cadre_tours, width=200, height=70, bg="yellow")
        self.cadre_interieur_5_6.pack(side=TOP)
        self.cadre_interieur_5_6.pack_propagate(0)
        self.cadre_tour_5 = LabelFrame(self.cadre_interieur_5_6, width=70, height=55, text="En developpement",
                                       bg="yellow", cursor="X_cursor").pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
        self.cadre_tour_6 = LabelFrame(self.cadre_interieur_5_6, width=70, height=55, text="En developpement",
                                       bg="yellow", cursor="X_cursor").pack(side=RIGHT, anchor=CENTER, padx=5, pady=5)

        # Image de la tour 1 (feu)
        self.image_tour_1 = Image.open("images\Towers\Tour_feu.png")
        self.image_tour_1_hautdevant = Image.open("images\Towers\Tour_feu_haut_1.png")
        self.image_tour_1_hautderriere = Image.open("images\Towers\Tour_feu_haut_2.png")
        self.image_tour_1.paste(self.image_tour_1_hautderriere, (10,0), self.image_tour_1_hautderriere)

        self.image_tour_1.paste(self.image_tour_1_hautdevant, (0,15), self.image_tour_1_hautdevant)
        self.image_tour_1_resize = self.image_tour_1.resize((50, 50), Image.ANTIALIAS)

        self.image_tour_1_tk = ImageTk.PhotoImage(self.image_tour_1_resize)
        self.image_tour_1_label = Label(self.cadre_interieur_1_2, width=70, height=55, image=self.image_tour_1_tk,
                                        bg="yellow", cursor="draped_box")
        self.image_tour_1_label.bind("<Button-1>", self.selectionner_tour_feu)
        self.image_tour_1_label.pack(side=LEFT)


        # Image de la tour 2 (glace)
        self.image_tour_2 = Image.open("images\Towers\Tour_bois.png")
        self.image_tour_2_hautdevant = Image.open("images\Towers\Tour_bois_haut.png")
        self.image_tour_2_hautderriere = Image.open("images\Towers\Tour_bois_haut.png")
        self.image_tour_2.paste(self.image_tour_2_hautdevant, (7,-5), self.image_tour_2_hautdevant)
        self.image_tour_2.paste(self.image_tour_2_hautderriere, (80,-5), self.image_tour_2_hautderriere)

        self.image_tour_2_resize = self.image_tour_2.resize((50, 50), Image.ANTIALIAS)
        self.image_tour_2_tk = ImageTk.PhotoImage(self.image_tour_2_resize)
        self.image_tour_2_label = Label(self.cadre_interieur_1_2, width=70, height=55, image=self.image_tour_2_tk,
                                        bg="yellow", cursor="draped_box")
        self.image_tour_2_label.bind("<Button-1>", self.selectionner_tour_glace)
        self.image_tour_2_label.pack(side=RIGHT)

        # Image de la tour 3 (poison)
        self.image_tour_3 = Image.open("images\Towers\Tour_poison.png")
        self.image_tour_3_hautdevant = Image.open("images\Towers\Tour_poison_haut_2.png")
        self.image_tour_3_hautderriere = Image.open("images\Towers\Tour_poison_haut_1.png")
        self.image_tour_3.paste(self.image_tour_3_hautderriere, (0,5), self.image_tour_3_hautderriere)
        self.image_tour_3.paste(self.image_tour_3_hautdevant, (0,30), self.image_tour_3_hautdevant)

        self.image_tour_3_resize = self.image_tour_3.resize((50, 50), Image.ANTIALIAS)
        self.image_tour_3_tk = ImageTk.PhotoImage(self.image_tour_3_resize)
        self.image_tour_3_label = Label(self.cadre_interieur_3_4, width=70, height=55, image=self.image_tour_3_tk,
                                        bg="yellow", cursor="draped_box")
        self.image_tour_3_label.bind("<Button-1>",  self.selectionner_tour_poison)

        self.image_tour_3_label.pack(side=LEFT)

        # Image de la tour 4
        self.image_tour_4 = Image.open("images\Towers\Tour_roche.png")
        self.image_tour_4_hautdevant = Image.open("images\Towers\Tour_roche_haut_1.png")
        self.image_tour_4_hautderriere = Image.open("images\Towers\Tour_roche_haut_2.png")
        self.image_tour_4.paste(self.image_tour_4_hautderriere, (0,5), self.image_tour_4_hautderriere)

        self.image_tour_4.paste(self.image_tour_4_hautdevant, (0,30), self.image_tour_4_hautdevant)
        self.image_tour_4_resize = self.image_tour_4.resize((50, 50), Image.ANTIALIAS)
        self.image_tour_4_tk = ImageTk.PhotoImage(self.image_tour_4_resize)
        self.image_tour_4_label = Label(self.cadre_interieur_3_4, width=70, height=55, image=self.image_tour_4_tk,
                                        bg="yellow", cursor="draped_box")
        self.image_tour_4_label.bind("<Button-1>",  self.selectionner_tour_mitraille)
        self.image_tour_4_label.pack(side=RIGHT)

    def creer_boutons_panneau_commande(self):        # Les boutons

        # Bouton Commencer
        self.btn_start = StringVar()
        self.btn_start.set("Commencer")
        self.bouton_commencer = Button(self.cadre_zone_jeu, text="", textvariable=self.btn_start, borderwidth=5, width=10, padx=5, pady=5,
                                       command=self.demarrer_vague)
        self.bouton_commencer.pack(side=RIGHT)
        self.bouton_commencer.place(x=1010, y=553)
        # Bouton Pause
        self.bouton_pause = Button(self.cadre_zone_jeu, text="Pause", borderwidth=5, width=10, padx=5, pady=5)
        self.bouton_pause.pack(side=RIGHT)
        self.bouton_pause.place(x=1110, y=510)
        # Bouton Vitesse
        self.bouton_vitesse = Button(self.cadre_zone_jeu, text="Vitesse", borderwidth=5, width=10, padx=5, pady=5, command="")
        self.bouton_vitesse.pack(side=RIGHT)
        self.bouton_vitesse.place(x=1010, y=510)
        # Bouton quitter
        self.bouton_quitter = Button(self.cadre_zone_jeu, text="Quitter", borderwidth=5, width=10, padx=5, pady=5,
                                     fg="red", command=self.exit_program)
        self.bouton_quitter.pack(side=RIGHT)
        self.bouton_quitter.place(x=1110, y=553)

    def creer_cadre_tutoriel(self):         # Le cadre du tutoriel

        self.cadre_tutoriel = LabelFrame(self.cadre_commande, width=200, height=150, text="Centre de renseignement", fg="yellow",
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
        self.cadre_intro_image = Label(self.cadre_intro, image=self.background_intro, anchor=N)
        self.cadre_intro_image.pack()

        # Bouton start
        self.button_start_game = Button(self.cadre_intro_image, anchor=CENTER, text="Brint it ON !!!",
                                        borderwidth=15, padx=5, pady=5, bg="white", command=self.start_page_intro)
        self.button_start_game.pack(side=BOTTOM)
        self.button_start_game.place(x=450, y=500)

    def afficher_coordonees(self, event):
        print(event.x, event.y)

    # Quand la vague commence,
    # un chronomètre est lancé (vue -> controleur -> jeu -> partie)
    # la fonction jouer est lancée
    def demarrer_vague(self):
        print("test")

        if not self.modele.en_cours:
            self.parent.en_jeu()
            self.parent.update_message("Vague " + str(self.modele.partie_courante.vague + 1) + " démarrée")
            self.btn_start.set("Vie : " + str(self.modele.partie_courante.vie))
            self.parent.demarrer_chrono()
            self.parent.jouer()

    def update_commencer(self, message):
        self.btn_start.set(message)

    def afficher_objets(self):
        self.canevas.delete(ALL)
        self.afficher_background()
        self.afficher_creeps()
        self.afficher_tours()
        self.afficher_attaque_tour()

    def update_argent(self):
       self.argent.set(str(self.modele.partie_courante.argent))

    def update_score(self):
        self.pointage.set(str(self.modele.partie_courante.score))

    def update_exp(self):
        self.exp.set(str(self.modele.exp))

    def update_message_tutoriel(self, message):
        self.message.set(message)

    def afficher_background(self):
        self.bgImg = Image.open(self.modele.partie_courante.sentier.image)
        self.background = ImageTk.PhotoImage(self.bgImg)
        self.canevas.create_image(0, 0, anchor=NW, image=self.background)

    def afficher_creeps(self):
        self.creepsImg = []
        for i in self.modele.partie_courante.creeps:
            if i.est_actif:
                creep_img = Image.open(i.images[i.index])
                if i.sens_image:
                    creep_img = creep_img.transpose(Image.FLIP_LEFT_RIGHT)
                if i.rotate == 1:
                    if i.sens_image:
                        creep_img = creep_img.rotate(90)
                    else:
                        creep_img = creep_img.rotate(270)
                elif i.rotate == -1:
                    if i.sens_image:
                        creep_img = creep_img.rotate(270)
                    else:
                        creep_img = creep_img.rotate(90)
                creep = ImageTk.PhotoImage(creep_img)
                self.creepsImg.append(creep)
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
                self.canevas.create_image(i.pos_x, i.pos_y, anchor=CENTER, image=creep)

    def traiter_creation_tour(self, evt, type_tour):
        if 20 <= evt.x <= 980:  # éviter créer tours sur menu d'affichage | largeur map == 1000px - demitaille tour
            if 20 <= evt.y <= 580:  # même chose pour hauteur | hauteur map == 600px
                self.parent.traiter_creation_tour(evt.x, evt.y, type_tour)

    def unbind_creation_tour(self):
        self.canevas.unbind("<Button-1>")

    def afficher_tours(self):
        tours_feu = self.modele.partie_courante.tours_feu
        tours_poison = self.modele.partie_courante.tours_poison
        tours_glace = self.modele.partie_courante.tours_glace
        tours_mitraille = self.modele.partie_courante.tours_mitraille
        for tour in tours_feu:
            image_tour_feu_lien = Image.open(tour.image)
            image_tour_feu_resize = image_tour_feu_lien.resize((tour.largeur, tour.longueur), Image.ANTIALIAS)
            image_tour_feu = ImageTk.PhotoImage(image_tour_feu_resize)
            self.tours_feu_img.append(image_tour_feu)
            self.canevas.create_image(tour.x, tour.y, anchor=CENTER, image=image_tour_feu)
        for tour in tours_poison:
            image_tour_poison_lien = Image.open(tour.image)
            image_tour_poison_resize = image_tour_poison_lien.resize((tour.largeur, tour.longueur), Image.ANTIALIAS)
            image_tour_poison = ImageTk.PhotoImage(image_tour_poison_resize)
            self.tours_feu_img.append(image_tour_poison)
            self.canevas.create_image(tour.x, tour.y, anchor=CENTER, image=image_tour_poison)
        for tour in tours_glace:
            image_tour_glace_lien = Image.open(tour.image)
            image_tour_glace_resize = image_tour_glace_lien.resize((tour.largeur, tour.longueur), Image.ANTIALIAS)
            image_tour_glace = ImageTk.PhotoImage(image_tour_glace_resize)
            self.tours_glace_img.append(image_tour_glace)
            self.canevas.create_image(tour.x, tour.y, anchor=CENTER, image=image_tour_glace)
        for tour in tours_mitraille:
            image_tour_mitraille_lien = Image.open(tour.image)
            image_tour_mitraille_resize = image_tour_mitraille_lien.resize((tour.largeur, tour.longueur), Image.ANTIALIAS)
            image_tour_mitraille = ImageTk.PhotoImage(image_tour_mitraille_resize)
            self.tours_mitraille_img.append(image_tour_mitraille)
            self.canevas.create_image(tour.x, tour.y, anchor=CENTER, image=image_tour_mitraille)


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
        self.positionner_tour("FEU")
        self.parent.update_message("Type : Feu \n Prix : 180 pièces d'or \n Niveau : 1") # ajouter la variable niveau pour les tours

    def selectionner_tour_poison(self, evt):
        self.positionner_tour("POISON")
        self.parent.update_message("Type : poison \n Prix : 275 pièces d'or \n Niveau : 1 \n \nCapacité spéciale : Ralentis les creeps")

    def selectionner_tour_glace(self, evt):
        self.positionner_tour("GLACE")
        self.parent.update_message("Type : glace \n Prix : 220 pièces d'or \n Niveau : 1 \n \n Capacité spéciale : Gèle un creep pour 1 secondes")

    def selectionner_tour_mitraille(self, evt):
        self.positionner_tour("MITRAILLE")
        self.parent.update_message("Type : Mitraille \n Prix : 335 pièces d'or \n Niveau : 1 \n \n Capacité spéciale : Attaque tous les creeps dans sa zone d'attaque")

    def positionner_tour(self, type_tour):
        types_tours = {
            "FEU": self.canevas.bind("<Button-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "GLACE": self.canevas.bind("<Button-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "POISON": self.canevas.bind("<Button-1>", lambda event: self.traiter_creation_tour(event, type_tour)),
            "MITRAILLE": self.canevas.bind("<Button-1>", lambda event: self.traiter_creation_tour(event, type_tour))
        }
        types_tours[type_tour]



    # fonction a replacer  // Pierre
    def creer_page_fin_partie(self):         # Page de fin de partie

        # Image de la page d'intro
        self.page_fin_partie_Img = Image.open("images\PageIntro\page_final.png")
        self.background_final = ImageTk.PhotoImage(self.page_fin_partie_Img)

        # Frame de la page d'intro
        self.cadre_final = Frame(self.canevas, width=self.modele.largeur_canevas - 200,
                                 height=self.modele.hauteur_canevas, bg=self.modele.partie_courante.sentier.couleurBG)
        self.cadre_final.pack()
        self.cadre_final.pack_propagate(0)
        self.cadre_final_image = Label(self.cadre_final, image=self.background_final, anchor=N)
        self.cadre_final_image.pack()

    def exit_program(self):
        self.root.destroy()

    def start_page_intro(self):
        self.cadre_intro.destroy()
        self.button_start_game.destroy()
        self.creer_cadre_commande()