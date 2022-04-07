import os
from tkinter import *
from PIL import Image, ImageTk
import math
import random


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Defense de Hoth")
        self.root.configure()
        self.index_animation = 0
        self.index_animation_sprite = 0

        self.nom_joueur = ""
        self.score_affiche = 0

        self.sprites = {}
        self.charger_sprites()

    def charger_sprites(self):
        for i in os.listdir("./Sprite"):
            if os.path.isdir("./Sprite/" + i):
                temp_dico_sprites = {}
                for j in os.listdir("./Sprite/" + i):
                    rep = self.charger_gifs("./Sprite/" + i + "/" + j)
                    temp_dico_sprites[j] = rep
                self.sprites[i] = temp_dico_sprites

    def charger_gifs(self, nom_gif):
        if nom_gif:
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

    def accueil(self):
        self.cadre_accueil = Canvas(self.root, width=self.parent.modele.largeur, height=self.parent.modele.hauteur,
                                   bg="black")

        self.Titre = ImageTk.PhotoImage(Image.open("./Sprite/Titre/Titre.jpg"))
        self.cadre_accueil.create_image(425, 250, anchor=N, image=self.Titre, tag="impraticable", tags="dynamique")
        self.btn_highscore = ImageTk.PhotoImage(Image.open("./Menu/btn_highscore.png"))
        self.btn_highscore1 = ImageTk.PhotoImage(Image.open("./Menu/btn_highscore1.png"))
        self.btn_highscore2 = ImageTk.PhotoImage(Image.open("./Menu/btn_highscore2.png"))
        self.btn_highscore3 = ImageTk.PhotoImage(Image.open("./Menu/btn_highscore3.png"))

        self.btn_close = ImageTk.PhotoImage(Image.open("./Menu/btn_close.png"))
        self.btn_accueil = ImageTk.PhotoImage(Image.open("./Menu/btn_accueil.png"))


        self.btn_easy = ImageTk.PhotoImage(Image.open("./Menu/btn_easy.png"))
        self.btn_moyen = ImageTk.PhotoImage(Image.open("./Menu/btn_medium.png"))
        self.btn_hard = ImageTk.PhotoImage(Image.open("./Menu/btn_hard.png"))



        self.niveau = IntVar()
        self.btn_facile = Radiobutton(self.cadre_accueil, image=self.btn_easy, variable=self.niveau, value=3, indicatoron=0,bg="black", activebackground='black',selectcolor="gold",border=0)
        self.btn_medium = Radiobutton(self.cadre_accueil, image=self.btn_moyen, variable=self.niveau, value=2, indicatoron=0,bg="black", activebackground='black',selectcolor="gold",border=0)
        self.btn_difficile = Radiobutton(self.cadre_accueil, image=self.btn_hard, variable=self.niveau, value=1,
                                         indicatoron=0,bg="black", activebackground='black',selectcolor="gold",border=0)
        self.map1 = ImageTk.PhotoImage(Image.open("./Carte/debarquement_thumb.png"))
        self.map2 = ImageTk.PhotoImage(Image.open("./Carte/grotte_thumb.png"))
        self.map3 = ImageTk.PhotoImage(Image.open("./Carte/plaines_thumb.png"))
        self.btnMap1 = Button(self.cadre_accueil, text="1", image=self.map1, bg="black",
                              activebackground='black')
        self.btnMap1.bind('<ButtonPress-1>', self.goMap)
        self.btnMap2 = Button(self.cadre_accueil, text="2", image=self.map2, bg="black",
                              activebackground='black')
        self.btnMap2.bind('<ButtonPress-1>', self.goMap)
        self.btnMap3 = Button(self.cadre_accueil, text="3", image=self.map3, bg="black",
                              activebackground='black')
        self.btnMap3.bind('<ButtonPress-1>', self.goMap)
        self.btnScore = Button(self.cadre_accueil, image=self.btn_highscore, command=self.montrer_scores, border=0,
                                bg="gold", activebackground='black')

        self.cadre_accueil.pack( fill=BOTH)
        self.cadre_accueil.pack_propagate(0)
        self.btn_facile.grid(row=1, column=1, padx=100, pady=30)
        self.btn_medium.grid(row=1, column=2, padx=100, pady=30)
        self.btn_difficile.grid(row=1, column=3, padx=100, pady=30)
        self.btn_medium.select()
        self.btnMap1.grid(row=1, column=4, padx=100, pady=15)
        self.btnMap2.grid(row=2, column=4, padx=100, pady=15)
        self.btnMap3.grid(row=3, column=4, padx=100, pady=15)
        self.btnScore.grid(row=4, column=4, padx=100, pady=15)

    def montrer_scores(self):
        for grid in self.cadre_accueil.winfo_children():
            grid.grid_forget()


        self.btnScore.grid_forget()
        self.cadre_accueil.delete("all")
        self.fenetre_scores = Frame(self.cadre_accueil, bg="white")
        self.scores_map1 = Text(self.cadre_accueil, width=40, height=20, background="black", fg="lightblue", border=1,
                                bg="black", highlightthickness=0,highlightcolor="black", pady=25)
        self.scores_map2 = Text(self.cadre_accueil, width=40, height=20, background="black", fg="lightblue", border=1,
                                bg="black",pady=25)
        self.scores_map3 = Text(self.cadre_accueil, width=40, height=20, background="black", fg="lightblue", border=1,
                                bg="black",pady=25)
        self.titre1 = Label(self.cadre_accueil, image=self.btn_highscore1)
        self.titre2 = Label(self.cadre_accueil, image=self.btn_highscore2)
        self.titre3 = Label(self.cadre_accueil, image=self.btn_highscore3)
        self.btn_fermer = Button(self.cadre_accueil, image=self.btn_close, command=self.fermer_scores,border=0,
                                bg="black", activebackground='black')
        self.titre1.grid(row=1, column=1, padx=40, pady=30)
        self.titre2.grid(row=1, column=2, padx=40)
        self.titre3.grid(row=1, column=3, padx=40)
        self.scores_map1.grid(row=2, column=1, padx=40, pady=79)
        self.scores_map2.grid(row=2, column=2, padx=40)
        self.scores_map3.grid(row=2, column=3, padx=45)
        self.btn_fermer.grid(row=3, column=2, pady=10)
        self.afficher_scores(self.modele.high_scores)

    def fermer_scores(self):
        self.titre1.grid_forget()
        self.titre2.grid_forget()
        self.titre3.grid_forget()
        self.scores_map1.grid_forget()
        self.scores_map2.grid_forget()
        self.scores_map3.grid_forget()
        self.btn_fermer.grid_forget()
        for grid in self.cadre_accueil.winfo_children():
            grid.grid_forget()
        self.cadre_accueil.destroy()
        self.accueil()



    def afficher_scores(self, scores):
        niveau = {1: "Difficile", 2: "Moyen", 3: "Facile"}
        for line in scores:
            map = int(line[0])
            difficulte = niveau[int(line[1])]
            difficulte = difficulte.ljust(18, ".")
            nom = str(line[2]).ljust(10, ".")
            score = str(line[3]).rjust(12, ".")
            if map == 1:
                self.scores_map1.insert(END, difficulte + nom + str(score) + "\n\n")
            if map == 2:
                self.scores_map2.insert(END, difficulte + nom + str(score) + "\n\n")
            if map == 3:
                self.scores_map3.insert(END, difficulte + nom + str(score) + "\n\n")

    def goMap(self, evt):
        obj = evt.widget
        carte = int(obj.cget('text'))
        self.cadre_accueil.pack_forget()
        self.parent.nouvelle_partie(carte)
        self.generer_images()
        self.creer_interface()
        self.generer_magasin()
        self.afficher_sentier(self.modele.partie.map.sentier)

    def fin_partie(self, succes, score, inscrire):
        self.succes = succes
        self.inscrire = inscrire

        self.score = score
        self.nom_joueur = StringVar()
        self.score_affiche = DoubleVar()
        self.cadre_fin = Frame(self.root, width=800, height=800,
                               bg="black")
        self.message_fin = Label(self.cadre_fin, text="Partie terminée")

        self.btnAccueil = Button(self.cadre_fin,image=self.btn_accueil, text="Accueil", command=self.retour_accueil)

        self.message_score = Label(self.cadre_fin, text="Votre score")
        self.score_final = Label(self.cadre_fin, textvariable=self.score_affiche)

        self.cadre_fin.place(anchor=CENTER, y=self.parent.modele.hauteur/ 2,
                             x=self.parent.modele.largeur / 2)
        self.message_fin.pack(padx=100,pady=50)
        self.message_score.pack(padx=100,pady=50)
        self.score_final.pack(padx=100,pady=50)
        self.score_affiche.set(round(score, 2))

        if succes and inscrire:
            self.bravo = Label(self.cadre_fin, text="Bravo, vous marquez au tableau")
            self.entry_nom = Entry(self.cadre_fin)
            self.bravo.pack(pady=10)
            self.entry_nom.pack(pady=10)

        self.btnAccueil.pack(pady=50)

    def retour_accueil(self):
        if self.inscrire:
            self.nom_joueur = self.entry_nom.get()
            self.parent.inscrire_nouv_score(self.nom_joueur)
        self.cadre_principal.pack_forget()
        self.cadre_fin.place_forget()
        self.cadre_accueil.pack()

    def creer_interface(self):
        self.cadre_principal = Canvas(self.root, width=self.parent.modele.largeur, height=self.parent.modele.hauteur,
                                      bg="black")
        self.canevas_map = Canvas(self.cadre_principal, width=self.parent.modele.largeur, height=self.modele.hauteur,
                                  bg="black")
        self.btn_pause = Button(self.canevas_map, text="Pause", image=self.btn_p1, command=self.btn_pause, border=0,
                                bg="black", activebackground='black')
        self.btn_lancer_vague = Button(self.canevas_map, text="Next ", image=self.btn_vague,
                                       command=self.lancer_vague, border=0, bg="black", activebackground='black')

        self.cadre_messages = Text(self.canevas_map, width=37, height=8, bg="black", fg="lightblue", border=2)
        self.cadre_magasin = Frame(self.canevas_map, width=200, height=40, bg='')

        self.btn_lancer_vague.place(anchor=S, y=self.parent.modele.hauteur - 135,
                                    x=self.parent.modele.largeur / 2 - 368)
        self.btn_pause.place(anchor=S, y=self.parent.modele.hauteur - 105, x=self.parent.modele.largeur / 2 - 368)

        self.cadre_messages.place(anchor=CENTER, y=self.parent.modele.hauteur - 85,
                                  x=self.parent.modele.largeur / 2 + 185)
        self.cadre_magasin.place(anchor=CENTER, y=self.parent.modele.hauteur - 128,
                                 x=self.parent.modele.largeur / 2 + 377)
        self.canevas_map.create_image(0, 0, anchor=NW, image=self.map)
        self.canevas_map.create_image(((self.parent.modele.largeur - self.menu_ressouces.width()) / 2), 0, anchor=NW,
                                      image=self.menu_ressouces, tag="impraticable", tags="dynamique")
        self.canevas_map.create_image(((self.parent.modele.largeur - self.menu_magasin.width()) / 2),
                                      (self.parent.modele.hauteur - self.menu_magasin.height()),
                                      anchor=NW, image=self.menu_magasin, tag="impraticable", tags="dynamique")

        self.canevas_map.bind('<ButtonPress-1>', self.dessiner_tour)

        self.cadre_principal.pack()
        self.canevas_map.pack()
        self.generer_ressources()

    def replacer_menu_dynamique(self):
        self.canevas_map.create_image(((self.parent.modele.largeur - self.menu_ressouces.width()) / 2), 0, anchor=NW,
                                      image=self.menu_ressouces, tag="impraticable", tags="dynamique")
        self.canevas_map.create_image(((self.parent.modele.largeur - self.menu_magasin.width()) / 2),
                                      (self.parent.modele.hauteur - self.menu_magasin.height()),
                                      anchor=NW, image=self.menu_magasin, tag="impraticable", tags="dynamique")

    def neige(self):
        self.xs = []
        self.ys = []
        self.sizes = []

        for i in range(100):
            self.xs.append(random.randint(0, self.parent.modele.largeur))
            self.ys.append(random.randint(0, self.parent.modele.hauteur))
            self.sizes.append(random.randint(1, 5))
        for i in range(100):
            x = self.xs[i]
            y = self.ys[i]
            s = self.sizes[i]

            self.canevas_map.create_oval(x, y, x + s, y + s, fill="white", outline="white", tag="dynamique")

            self.ys[i] = self.ys[i] + (s / 100) * ((100 / self.parent.modele.hauteur) + 1)
            self.xs[i] = self.xs[i] + ((100 / self.parent.modele.largeur) * 2) - 1
            if y > self.parent.modele.hauteur:
                self.ys[i] = 0
            if x < 0:
                self.xs[i] = self.parent.modele.largeur
            elif x > self.parent.modele.largeur:
                self.xs[i] = 0

    def afficher_creation_tours(self):
        for tour in self.modele.partie.liste_tours:

            if not tour.tour_construite:
                self.canevas_map.create_image(tour.position_x, tour.position_y,
                                              image=self.sprites["Tour"][tour.archetype + "Construction" + ".gif"][
                                                  math.floor(tour.index_creation / 2)],
                                              tags="dynamique")
                tour.index_creation += 1
                if math.floor(tour.index_creation / 2) == 5:
                    tour.tour_construite = True
            else:
                if not tour.locked_on:
                    self.canevas_map.create_image(tour.position_x, tour.position_y,
                                                  image=self.sprites["Tour"][tour.archetype + "Orientation" + ".gif"][
                                                      math.floor(self.index_animation_sprite / 2)],
                                                  tags="dynamique")

                elif tour.locked_on:
                    self.canevas_map.create_image(tour.position_x, tour.position_y,
                                                  image=self.sprites["Tour"][tour.archetype + "Orientation" + ".gif"][
                                                      tour.orientation],
                                                  tags="dynamique")

            self.canevas_map.create_oval(tour.position_x - tour.portee, tour.position_y - tour.portee,
                                         tour.position_x + tour.portee, tour.position_y + tour.portee,
                                         outline=tour.apparence, width=self.index_animation / 15, dash=(5, 2),
                                         tags=("impraticable", "dynamique"))

    def afficher_creeps(self):
        liste_creeps = self.modele.partie.liste_creeps
        for creep in reversed(liste_creeps):
            x = creep.x
            y = creep.y
            zone_barre = creep.vie_max / 2

            if creep.archetype == "At-At":
                self.canevas_map.create_image(x, y-100, image=self.sprites[creep.archetype][creep.archetype+ str(creep.orientation) + ".gif"][self.index_animation_sprite],
                                             tag="dynamique")
                self.canevas_map.create_oval(x, y, x, y, fill="red", tags="dynamique")
            elif creep.archetype == "Droid":
                self.canevas_map.create_image(x, y, image=self.sprites[creep.archetype][creep.archetype+ str(1) + ".gif"][math.floor(self.index_animation_sprite/2)],
                                             tag="dynamique")
            else:
                self.canevas_map.create_image(x, y, image=self.sprites[creep.archetype][creep.archetype + str(creep.orientation) + ".gif"][math.floor(self.index_animation_sprite/2)],
                                               tag="dynamique")

            self.canevas_map.create_rectangle(x - zone_barre, y + 2, x + zone_barre, y + 4,
                                              fill="red", tag="dynamique")
            self.canevas_map.create_rectangle(x - zone_barre, y + 2,
                                              x - zone_barre + creep.vie, y + 4,
                                              fill="green", tag="dynamique")

    def afficher_projectiles(self):
        liste_projectiles = []
        for tour in self.modele.partie.liste_tours:
            for projectile in tour.pew_pew:
                liste_projectiles.append(projectile)

            if tour.archetype == "Shocker" and tour.creeps_in_range:
                portee = tour.portee * self.index_animation / 40
                self.canevas_map.create_oval(tour.position_x - portee, tour.position_y - portee,
                                             tour.position_x + portee,
                                             tour.position_y + portee, outline=tour.apparence, tags="dynamique")

            for projectile in liste_projectiles:
                x = projectile.x
                y = projectile.y

                x2 = projectile.x2
                y2 = projectile.y2
                if projectile.__class__.__name__ == "Blaster":
                    self.canevas_map.create_line([x, y], [x2, y2], fill="red", width=3, tags="dynamique",
                                                 capstyle="round")

                if projectile.__class__.__name__ == "Roquette":
                    self.canevas_map.create_line([x, y], [x2, y2], fill="orange", width=10, tags="dynamique",
                                                 capstyle="round", arrow=BOTH)

    def afficher_ressources(self):
        self.credits.set(self.parent.modele.partie.argent)
        self.vagues_restantes.set(self.modele.partie.numero_vague)
        self.vagues_totales.set(self.modele.partie.nbr_vagues)
        self.hit_points.set(self.parent.modele.partie.vie)
        self.var_duree.set(str(round(self.modele.duree, 2)))

    def afficher_sentier(self, positions):
        for i in range(len(positions)):
            if (i + 1) < len(positions):
                self.canevas_map.create_line(positions[i], positions[i + 1], fill="", width=100,
                                             tag="impraticable")

    def lancer_vague(self):
        self.parent.lancer_vague()

    def btn_pause(self):
        self.parent.pause()
        if self.parent.paused:
            self.btn_pause.config(text="Play")
            self.btn_pause.config(image=self.btn_p2)

        elif not self.parent.paused:
            self.btn_pause.config(text="Pause")
            self.btn_pause.config(image=self.btn_p1)


    def dessiner_tour(self, event):
        if self.choixTour.get() != "":
            self.cadre_messages.delete("1.0", END)
            type_tour = self.choixTour.get().split()[0]
            x = event.x
            y = event.y
            if self.canevas_map.gettags(CURRENT)[0] != "impraticable":
                tour = self.parent.acheter_tour(type_tour, x, y)
                if tour:
                    
                    self.canevas_map.create_image(x, y, image=self.sprites["Tour"][tour.archetype+"Construction"+".gif"][0],
                                                  tags=("impraticable", "dynamique"))
                    self.canevas_map.create_oval(x - tour.portee, y - tour.portee, x + tour.portee, y + tour.portee, outline=tour.apparence, width=5, dash = (5, 2),tags=("impraticable", "dynamique"))
                else:
                    self.cadre_messages.insert(INSERT, "Vous n'avez pas assez de crédits!")
            self.afficher_ressources()



    def generer_images(self):
        self.map = ImageTk.PhotoImage(Image.open(self.modele.partie.map.path_fichier).resize(
            (self.parent.modele.largeur, self.parent.modele.hauteur)))
        self.menu_magasin = ImageTk.PhotoImage(Image.open("./Menu/magasin.png"))
        self.menu_ressouces = ImageTk.PhotoImage(Image.open("./Menu/ressources.png"))
        self.btn_test = ImageTk.PhotoImage(Image.open("./Menu/btn_test.png"))
        self.btn_p1 = ImageTk.PhotoImage(Image.open("./Menu/btn_pause.png"))
        self.btn_p2 = ImageTk.PhotoImage(Image.open("./Menu/btn_play.png"))
        self.btn_vague = ImageTk.PhotoImage(Image.open("./Menu/btn_vague.png"))



    def generer_ressources(self):
        self.credits = IntVar()
        self.hit_points = IntVar()
        self.var_duree = IntVar()
        self.vagues_restantes = IntVar()
        self.vagues_totales = IntVar()

        self.quantite_credits = Label(self.canevas_map, textvariable=self.credits, bg="black", fg="lightblue")
        self.quantite_vagues_restantes = Label(self.canevas_map, textvariable=self.vagues_restantes, bg="black",
                                               fg="lightblue")
        self.label_trait = Label(self.canevas_map, text="/", bg="black", fg="lightblue")
        self.quantite_vague = Label(self.canevas_map, textvariable=self.vagues_totales, bg="black", fg="lightblue")
        self.quantite_vie = Label(self.canevas_map, textvariable=self.hit_points, bg="black", fg="lightblue")
        self.label_duree = Label(self.canevas_map, text="0", textvariable=self.var_duree, bg="black", fg="lightblue")

        self.quantite_credits.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) - 325)
        self.quantite_vague.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) - 175)
        self.label_trait.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) - 185)
        self.quantite_vagues_restantes.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) - 195)
        self.quantite_vie.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) - 50)
        self.label_duree.place(anchor=CENTER, y=20, x=(self.parent.modele.largeur / 2) + 140)

        self.afficher_ressources()

    def generer_magasin(self):
        self.tourData = self.modele.partie.types_tour
        self.tourArchetype = ['Mitraillette','Lance-Roquette','Shocker','Sniper']

        self.choixTour = StringVar()
        for n in range(len(self.tourArchetype)):
            btn_tour = Radiobutton(self.cadre_magasin,
                                   variable=self.choixTour,
                                   value=n + 1,image=self.sprites["Tour"][self.tourArchetype[n]+"Orientation" + ".gif"][4],bg="black", indicatoron=0,
                                   highlightcolor="black", selectcolor="grey20", activebackground="black"
                                   )
            btn_tour.grid(column=1, row=n)

            btn_tour.deselect()


    def update_tour(self, event):
        x = event.x
        y = event.y
        if self.canevas_map.gettags(CURRENT)[0] != "updatable":
            self.canevas_map.create_rectangle(x, y, 100, 50, fill='red')

    def update_dynamique(self):
        self.canevas_map.delete("dynamique")
        self.afficher_creation_tours()
        self.afficher_creeps()
        self.afficher_projectiles()


        self.index_animation += 5
        if self.index_animation == 40:
            self.index_animation = 0

        self.neige()
        self.index_animation_sprite += 1
        if self.index_animation_sprite == 16:
            self.index_animation_sprite = 0
        self.replacer_menu_dynamique()


