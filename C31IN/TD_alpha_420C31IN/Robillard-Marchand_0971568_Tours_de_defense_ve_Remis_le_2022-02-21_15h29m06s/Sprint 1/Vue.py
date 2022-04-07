from datetime import date
from tkinter import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Tower Defense Alpha_0.1")
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.cadres_menu = self.creer_menu()
        self.cadres = self.creer_interface()
        self.afficher_sentier(self.parent.modele.partie.map.sentier)

        self.index_animation = 0

    def creer_menu(self):
        self.file_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Se connecter", command=self.ouvrir_fenetre_login)
        self.menu_bar.add_cascade(label="Scores", command=self.ouvrir_fenetre_scores)
        self.menu_bar.add_cascade(label="Options", command=None)

    def ouvrir_fenetre_login(self):
        self.fenetre_login = Toplevel(self.root)
        self.fenetre_login.title("Se connecter")
        self.fenetre_login.geometry("400x400")

        Label(self.fenetre_login, text="Nom d'usager : ").pack()
        self.nom = StringVar()
        Entry(self.fenetre_login, textvariable=self.nom).pack()

        Label(self.fenetre_login, text="Mot de passe : ").pack()
        self.mdp = StringVar()
        Entry(self.fenetre_login, textvariable=self.mdp).pack()

        Button(self.fenetre_login, text="OK", command=self.validation_vue_login).pack()

    def validation_vue_login(self):
        self.modele.sauvegarde_info_dict["Nom_utilisateur"] = self.nom.get()
        self.modele.sauvegarde_info_dict["Mot_de_passe"] = self.mdp.get()

        self.modele.validation_login()

        self.joueur = self.nom.get()
        Label(self.fenetre_login,
              text="Bonjour " + self.joueur + "!").pack()

    def enregistrement_vue_score(self):
        today = date.today()

        self.modele.score_dict["Nom_utilisateur"] = self.joueur
        self.modele.score_dict["temps"] = self.modele.duree.get()
        self.modele.score_dict["date"] = today

        self.modele.validation_score()

    def ouvrir_fenetre_scores(self):

        fenetre_scores = Toplevel(self.root)
        fenetre_scores.title("Scores")
        fenetre_scores.geometry("200x200")
        Label(fenetre_scores, text="Voici tous les scores !").pack()
        Label(fenetre_scores, textvariable=self.modele.duree ).pack()

    def creer_interface(self):
        self.cadre_principal = Frame(self.root, width=self.parent.modele.largeur, height=self.parent.modele.hauteur,
                                     bg="white")
        self.cadre_principal.pack()

        self.cadre_haut = Frame(self.cadre_principal, width=self.parent.modele.largeur, height=50, bg="blue")
        self.cadre_haut.pack()

        self.canevas_map = Canvas(self.cadre_principal, width=self.parent.modele.largeur, height=self.modele.hauteur,
                                  bg="white")
        self.img = PhotoImage(file = r"./Carte/GC_Wilderness.png")
        self.canevas_map.create_image(10, 10, anchor=NW, image=self.img)
        self.canevas_map.pack()

        self.cadre_bas = Frame(self.cadre_principal, width=self.parent.modele.largeur, height=40, bg="blue")
        self.cadre_bas.pack(fill=X)

        self.cadre_action = Frame(self.cadre_bas, width=200, height=40, bg='blue')
        self.btn_lancer_vague = Button(self.cadre_action, text="Lancer une vague", command=self.btn_lancer_vague)
        self.btn_pause = Button(self.cadre_action, text="Pause", command=self.btn_pause)

        self.cadre_messages = Text(self.cadre_bas, width=40, height=4, bg="white", border=2)

        self.cadre_magasin = Frame(self.cadre_bas, width=200, height=40, bg='blue')

        self.cadre_action.pack(fill=X, side=LEFT)
        self.btn_pause.grid(column=2, row=1, padx=5)
        self.btn_lancer_vague.grid(column=1, row=1, padx=5)

        self.cadre_messages.pack(side=LEFT)

        self.cadre_magasin.pack(fill=X, side=RIGHT)

        tourData = self.modele.partie.types_tour
        self.choixTour = StringVar()

        for n in range(len(self.modele.partie.types_tour)):
            btn_tour = Radiobutton(self.cadre_magasin,
                                   text=tourData[n + 1][0],
                                   variable=self.choixTour,
                                   value=n + 1,
                                   bg=tourData[n + 1][1])
            btn_tour.grid(column=n, row=2, padx=5)
            btn_tour.deselect()

        self.canevas_map.bind('<ButtonPress-1>', self.dessiner_tour)


    def afficher_sentier(self, positions):
        for i in range(len(positions)):
            if (i + 1) < len(positions):
                self.canevas_map.create_line(positions[i], positions[i + 1], fill="lightblue", width=15)

    def afficher_creeps(self):
        self.var_duree.set(str(round(self.modele.duree, 2)))
        liste_creeps = self.modele.partie.liste_creeps
        for creep in liste_creeps:
            self.x = creep.x + creep.random_position_x_variation
            self.y = creep.y + creep.random_position_y_variation
            largeur = creep.largeur / 2
            hauteur = creep.hauteur / 2
            zone_barre = creep.vie_max / 2
            self.canevas_map.create_oval(self.x - largeur, self.y - hauteur, self.x + largeur, self.y + hauteur,
                                         fill=creep.apparence, tag="dynamique")
            self.canevas_map.create_rectangle(self.x - zone_barre, self.y + 2, self.x + zone_barre, self.y + 4,
                                              fill="red", tag="dynamique")

            self.canevas_map.create_rectangle(self.x - zone_barre, self.y + 2,
                                              self.x - zone_barre + creep.vie, self.y + 4,
                                              fill="green", tag="dynamique")

    def afficher_projectiles(self):
        liste_projectiles = []
        for tour in self.modele.partie.liste_tours:
            for projectile in tour.pew_pew:
                liste_projectiles.append(projectile)

            if tour.archetype == "Shocker" and tour.creeps_in_range:
                portee = tour.portee * self.index_animation / 40
                self.canevas_map.create_oval(tour.position_x - portee, tour.position_y - portee, tour.position_x + portee,
                                             tour.position_y + portee, outline=tour.apparence, tags="dynamique")

            for projectile in liste_projectiles:
                x = projectile.x
                y = projectile.y
                if 0 <= self.index_animation < 10:
                    self.canevas_map.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", tags="dynamique")
                if 10 <= self.index_animation < 20:
                    self.canevas_map.create_oval(x - 1, y - 1, x + 1, y + 1, fill="yellow", tags="dynamique")
                if 20 <= self.index_animation < 30:
                    self.canevas_map.create_oval(x, y, x, y, fill="white", tags="dynamique")
                if 30 <= self.index_animation < 40:
                    self.canevas_map.create_oval(x - 1, y - 1, x + 1, y + 1, fill="green", tags="dynamique")


    def btn_lancer_vague(self):
        self.parent.lancer_vague()

    def btn_pause(self):
        self.parent.pause()
        if self.parent.paused:
            self.btn_pause.config(text="Play")
        elif not self.parent.paused:
            self.btn_pause.config(text="Pause")

    def dessiner_tour(self, event):
        self.cadre_messages.delete("1.0", END)
        type_tour = self.choixTour.get().split()[0]
        x = event.x
        y = event.y
        tour = self.parent.acheter_tour(type_tour, x, y)
        if tour:
            couleur = tour.apparence
            prix = tour.valeur
            largeur = tour.largeur
            hauteur = tour.hauteur
            self.montant = self.modele.partie.argent
            self.canevas_map.create_rectangle(x - largeur, y - hauteur, x + largeur, y + hauteur, fill=couleur)
            self.cadre_messages.insert(INSERT, "Vous avez acheté une tour pour " + str(prix) + "\n")
            self.canevas_map.create_oval(x - tour.portee, y - tour.portee, x + tour.portee, y + tour.portee)
        else:
            self.cadre_messages.insert(INSERT, "Il ne vous reste plus assez d'argent!")

    def afficher_ressources(self):
        cash = IntVar()
        hit_points = IntVar()
        self.var_duree = IntVar()

        vagues_restantes = IntVar()
        vagues_restantes.set(self.modele.partie.numero_vague)
        vagues_totales = IntVar()
        vagues_totales.set(self.modele.partie.nbr_vagues)

        self.label_vagues_restantes = Label(self.cadre_haut, text="Vague: ")
        self.quantite_vagues_restantes = Label(self.cadre_haut, textvariable=vagues_restantes)
        self.label_trait = Label(self.cadre_haut, text="/")
        self.quantite_vague = Label(self.cadre_haut, textvariable=vagues_totales)

        self.label_vagues_restantes.place(anchor=E, rely=0.5, relx=0.8)
        self.quantite_vagues_restantes.place(anchor=E, rely=0.5, relx=0.9)
        self.label_trait.place(anchor=E, rely=0.5, relx=0.92)
        self.quantite_vague.place(anchor=E, rely=0.5, relx=0.96)

        cash.set(self.parent.modele.partie.argent)
        hit_points.set(self.parent.modele.partie.vie)

        self.label_duree = Label(self.cadre_haut, text="0", textvariable=self.var_duree)
        self.label_credits = Label(self.cadre_haut, text="Credits: ")
        self.quantite_credits = Label(self.cadre_haut, textvariable=cash)
        self.label_vie = Label(self.cadre_haut, text="Points de vie: ")
        self.quantite_vie = Label(self.cadre_haut, textvariable=hit_points)

        self.label_vie.place(anchor=E, rely=0.72, relx=0.108)
        self.quantite_vie.place(anchor=E, rely=0.72, relx=0.143)
        self.label_credits.place(anchor=E, rely=0.26, relx=0.07)
        self.quantite_credits.place(anchor=E, rely=0.26, relx=0.105)
        self.label_duree.place(anchor=CENTER, relx=0.5, rely=0.5)

    def update_dynamique(self):
        self.canevas_map.delete("dynamique")
        self.afficher_creeps()
        self.afficher_projectiles()

        self.index_animation += 5
        if self.index_animation == 40:
            self.index_animation = 0