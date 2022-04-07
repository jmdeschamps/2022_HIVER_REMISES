from tkinter import *

import monstre
import tour


mon_id = 0


def creer_id():
    global mon_id
    mon_id += 1
    id = "id_" + str(mon_id)
    return id



class Vue:
    def __init__(self, parent):
        self.tour_selectionne = None
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("TowerDefence, alpha_0.1")
        self.root.geometry('+%d+%d' % (0, 0))
        self.dictionnaire_images = {}
        self.cadre_actif = None
        self.cadres = {}
        self.creer_cadres()
        self.initialiser_images()
        self.changer_cadre("cadre_splash")
        self.ouvrir_gif()

    def changer_cadre(self, nom_cadre):
        if nom_cadre in self.cadres.keys():
            if self.cadre_actif:
                self.cadre_actif.pack_forget()
            cadre = self.cadres[nom_cadre]
            self.cadre_actif = cadre
            cadre.pack()

    def creer_cadres(self):
        self.cadres["cadre_splash"] = self.creer_cadre_splash()
        self.cadres["cadre_jeu"] = self.creer_interface()
        self.cadres["menu_mort"] = self.creer_cadre_mort()
        self.cadres["scores"] = self.creer_menu_score()


    def initialiser_images(self):
        self.dictionnaire_images["monstre"] = "Images/gifs/monstres.gif"
        self.dictionnaire_images["portail"] = "Images/gifs/portal.gif"
        self.dictionnaire_images["boss"] = "Images/gifs/Boss.gif"


    def ouvrir_gif(self):
        animations = self.charger_gifs()
        if animations:
            self.parent.inserer_animation(animations)


    def charger_gifs(self):
        dictionnaire_temp = {}
        for nom_gif, chemin in self.dictionnaire_images.items():
            if chemin:
                listeimages = []
                testverite = 1
                noindex = 0
                while testverite:
                    try:
                        img = PhotoImage(file=chemin, format="gif -index " + str(noindex))
                        listeimages.append(img)
                        noindex += 1
                    except Exception:
                        testverite = 0
                dictionnaire_temp[nom_gif] = listeimages

        return dictionnaire_temp

    def creer_tour(self, event):
        self.parent.creer_tour(event)

    def creer_tour_glace(self):
        self.parent.creer_tour_glace()

    def creer_tour_poison(self):
        self.parent.creer_tour_poison()

    def creer_tour_sniper(self):
        self.parent.creer_tour_sniper()

    def creer_tour_mitraillette(self):
        self.parent.creer_tour_mitraillette()

    def creer_tour_bombe(self):
        self.parent.creer_tour_bombe()


    def creer_cadre_splash(self):
        menu_bg_width = 1000
        menu_bg_heigth = 667
        self.cadre_splash = Frame(self.root)
        self.ouverture_canvas = Canvas(self.cadre_splash, width=menu_bg_width, height=menu_bg_heigth)
        self.menu_bg = PhotoImage(file="Images/backgrounds/splash_bg.png")
        self.menu_bg.width()
        self.menu_bg.height()

        bouton_depart = Button(self.ouverture_canvas, text='Jouer', font=('', 12, 'bold'), width=10)
        bouton_depart.bind("<Button>", self.redirection_jeu)
        self.ouverture_canvas.create_window(menu_bg_width / 2, menu_bg_heigth / 2 + 75, window=bouton_depart)

        bouton_score = Button(self.ouverture_canvas, text='Scores', font=('', 12))
        bouton_score.bind("<Button>", self.redirection_score)
        self.ouverture_canvas.create_window(menu_bg_width / 2, menu_bg_heigth / 2 + 125, window=bouton_score)

        self.ouverture_canvas.pack()
        self.ouverture_canvas.create_image(menu_bg_width / 2, menu_bg_heigth / 2, image=self.menu_bg,
                                           tags=("statique", "bg_menu"))

        return self.cadre_splash



    def creer_menu_score(self):
        self.cadre_scores = Frame(self.root, bg="blue")
        text = Text(self.cadre_scores)
        text.insert(INSERT, self.modele.get_scores())
        text.pack()
        bouton = Button(self.cadre_scores, text='Menu', width=15, height=2)
        bouton.bind("<Button>", self.redirection_menu)
        bouton.pack(expand=True)

        return self.cadre_scores

    def creer_cadre_mort(self):
        mort_bg_width = 640
        mort_bg_heigth = 469
        self.cadre_mort = Frame(self.root)
        self.canvas_mort = Canvas(self.cadre_mort, width=mort_bg_width, height=mort_bg_heigth)
        self.mort_bg = PhotoImage(file="Images/backgrounds/mort_bg.png")
        self.mort_bg.width()
        self.menu_bg.height()

        bouton_jeu = Button(self.canvas_mort, text='Rejouer')
        bouton_jeu.bind("<Button>", self.redirection_jeu)
        self.canvas_mort.create_window(mort_bg_width / 2 + 200, mort_bg_heigth / 2 + 100, window=bouton_jeu)

        bouton_menu = Button(self.canvas_mort, text='Menu')
        bouton_menu.bind("<Button>", self.redirection_menu)
        self.canvas_mort.create_window(mort_bg_width / 2 + 200, mort_bg_heigth / 2 + 150, window=bouton_menu)

        self.canvas_mort.pack()
        self.canvas_mort.create_image(mort_bg_width / 2, mort_bg_heigth / 2, image=self.mort_bg,
                                      tags=("statique", "bg_mort"))
        return self.cadre_mort

    def redirection_jeu(self, evt):
        self.changer_cadre("cadre_jeu")

    def redirection_menu(self, evt):
        self.changer_cadre("cadre_splash")

    def redirection_score(self, evt):
        self.changer_cadre("scores")

    def creer_interface(self):

        self.cadre_jeu = Frame(self.root)
        # cadre HUD affichant la duree
        self.canevas = Canvas(self.cadre_jeu, width=self.modele.largeur_carte, height=self.modele.hauteur_carte)
        self.bg = PhotoImage(file="Images/backgrounds/carte.png")
        self.bg.width()

        self.message = ""
        self.var_vie = StringVar()
        self.var_score = StringVar()
        self.var_vague = StringVar()
        self.var_argent = StringVar()
        self.var_upgrade = StringVar()

        self.image_argent = PhotoImage(file="Images/money.png")
        self.image_tour_glace1 = PhotoImage(file="Images/towers/ice_tower1.png")
        self.image_tour_glace2 = PhotoImage(file="Images/towers/ice_tower2.png")
        self.image_tour_glace3 = PhotoImage(file="Images/towers/ice_tower3.png")

        self.image_tour_sniper1 = PhotoImage(file="Images/towers/tour_sniper1.png")
        self.image_tour_sniper2 = PhotoImage(file="Images/towers/tour_sniper2.png")
        self.image_tour_sniper3 = PhotoImage(file="Images/towers/tour_sniper3.png")

        self.image_tour_feu1 = PhotoImage(file="Images/towers/tour_feu1.png")
        self.image_tour_feu2 = PhotoImage(file="Images/towers/tour_feu2.png")
        self.image_tour_feu3 = PhotoImage(file="Images/towers/tour_feu3.png")

        self.image_tour_mitraillette1 = PhotoImage(file="Images/towers/tour_mitraillette1.png")
        self.image_tour_mitraillette2 = PhotoImage(file="Images/towers/tour_mitraillette2.png")
        self.image_tour_mitraillette3 = PhotoImage(file="Images/towers/tour_mitraillette3.png")

        self.image_tour_bombe1 = PhotoImage(file="Images/towers/tower_bombe.png")
        self.image_tour_bombe2 = PhotoImage(file="Images/towers/tower_bombe2.png")
        self.image_tour_bombe3 = PhotoImage(file="Images/towers/tower_bombe3.png")

        self.cadre_depart = Frame(self.cadre_jeu, bg='darkgreen')
        self.cadre_fin = Frame(self.cadre_jeu, bg="darkgreen")
        self.icon_tour_glace = PhotoImage(file="Images/ice_tower1_icon.png")
        self.icon_tour_bombe = PhotoImage(file="Images/tower_bombe_icon.png")
        self.icon_tour_poison = PhotoImage(file="Images/tour_feu1_icon.png")
        self.icon_tour_sniper = PhotoImage(file="Images/tour_sniper1_icon.png")
        self.icon_tour_mitrailette = PhotoImage(file="Images/tour_mitraillette1_icon.png")

        bouton_depart = Button(self.cadre_depart, text='Commencer la partie', command=self.parent.debuter_partie)
        bouton_pause = Button(self.cadre_depart, text='Pause', command=self.parent.partie_pause)
        bouton_tour_glace = Button(self.cadre_fin, text='TOUR GLACE - ' + str(tour.Tour_Glace.prix) + '$', width=20,
                                   height=1, font=('Arial', 8),
                                   command=self.creer_tour_glace)
        bouton_tour_poison = Button(self.cadre_fin, text='TOUR POISON - ' + str(tour.Tour_Poison.prix) + '$',
                                    font=('Arial', 8), width=20, height=1,
                                    command=self.creer_tour_poison)
        bouton_tour_mitraillette = Button(self.cadre_fin,
                                          text='TOUR MITRAILETTE - ' + str(tour.Tour_Mitraillette.prix) + '$',
                                          font=('Arial', 8), width=22, height=1,
                                          command=self.creer_tour_mitraillette)
        bouton_tour_bombe = Button(self.cadre_fin, text='TOUR BOMBE - ' + str(tour.Tour_Bombe.prix) + '$',
                                   font=('Arial', 8), width=20, height=1,
                                   command=self.creer_tour_bombe)
        bouton_tour_sniper = Button(self.cadre_fin, text='TOUR SNIPER - ' + str(tour.Tour_Sniper.prix) + '$',
                                    font=('Arial', 8), width=20, height=1,
                                    command=self.creer_tour_sniper)

        bouton_upgrade = Button(self.cadre_depart, text="Amélioration de la tour", command=self.upgrade)
        label_information_amelioration = Label(self.cadre_fin, height=1, textvariable=self.var_upgrade)

        self.canevas.tag_bind("bg", "<Button-1>", self.creer_tour)
        self.canevas.tag_bind("tour", "<Button-1>", self.update_information)

        label_image_score = Label(self.cadre_depart, text='SCORE', height=1, font='Arial 11 bold')
        label_vague_texte = Label(self.cadre_depart, text='VAGUE', height=1, font='Arial 11 bold')
        label_vie_texte = Label(self.cadre_depart, text='VIE', height=1, font='Arial 11 bold')
        label_tour_glace = Label(self.cadre_fin,image=self.icon_tour_glace,height=50,bg="darkgreen")
        label_tour_poison = Label(self.cadre_fin, image=self.icon_tour_poison, height=50,bg="darkgreen")
        label_tour_bombe = Label(self.cadre_fin, image=self.icon_tour_bombe, height=50,bg="darkgreen")
        label_tour_sniper = Label(self.cadre_fin, image=self.icon_tour_sniper, height=50,bg="darkgreen")
        label_tour_mitraillette = Label(self.cadre_fin, image=self.icon_tour_mitrailette, height=50,bg="darkgreen")

        label_image_argent = Label(self.cadre_depart, image=self.image_argent, height=36)
        label_argent = Label(self.cadre_depart, width=10, height=2, font=('Arial', 11),
                             textvariable=self.var_argent)
        label_vague = Label(self.cadre_depart, width=5, height=1, font=('Arial', 11),
                            textvariable=self.var_vague)

        label_score = Label(self.cadre_depart, width=5, height=1, font=('Arial', 11),
                            textvariable=self.var_vie)
        label_vie = Label(self.cadre_depart, width=5, height=1, font=('Arial', 11),
                          textvariable=self.var_score)

        self.cadre_depart.pack(expand=True, fill=BOTH)
        bouton_depart.pack(side=LEFT, padx=20)
        bouton_pause.pack(side=LEFT, padx=5)
        bouton_upgrade.pack(side=LEFT, padx=30)

        label_tour_glace.pack(side=LEFT)
        bouton_tour_glace.pack(side=LEFT)
        label_tour_poison.pack(side=LEFT,padx=5)
        bouton_tour_poison.pack(side=LEFT)
        label_tour_sniper.pack(side=LEFT)
        bouton_tour_sniper.pack(side=LEFT, padx=5)
        label_tour_mitraillette.pack(side=LEFT)
        bouton_tour_mitraillette.pack(side=LEFT, padx=5)
        label_tour_bombe.pack(side=LEFT)
        bouton_tour_bombe.pack(side=LEFT, padx=5)

        label_information_amelioration.pack(side=LEFT, padx=5)


        label_argent.pack(side=RIGHT)
        label_image_argent.pack(side=RIGHT)
        label_score.pack(side=RIGHT, padx=20)
        label_vie_texte.pack(side=RIGHT)
        label_vie.pack(side=RIGHT, padx=20)
        label_image_score.pack(side=RIGHT)
        label_vague.pack(side=RIGHT, padx=20)
        label_vague_texte.pack(side=RIGHT)

        self.canevas.pack()
        self.cadre_fin.pack(expand=True, fill=BOTH)
        return self.cadre_jeu

    def afficher_debut_partie(self):
        self.canevas.delete("dynamique")
        self.canevas.create_image(self.modele.largeur_carte / 2, self.modele.hauteur_carte / 2, image=self.bg,
                                  tags=("statique", "bg"))
        self.afficher_path()


        self.ouvrir_gif()

    def afficher_partie(self):
        self.canevas.delete("dynamique")
        self.var_argent.set(str(self.modele.argent) + "$")
        self.var_score.set(self.modele.pointage)
        self.var_vie.set(self.modele.vie)
        self.var_vague.set(self.modele.vague)
        self.update_message()

        self.var_upgrade.set(self.message)
        if len(self.modele.dictionnaire_tours) > 0:
            if self.tour_selectionne is not None:
                if self.tour_selectionne.voir_rayon:
                    i = self.tour_selectionne
                    rayon = self.tour_selectionne.rayon
                    self.canevas.create_oval(i.x - rayon, i.y - rayon, i.x + rayon, i.y + rayon, outline="black",
                                             tags=("rayon", "bg"))

        for i in self.modele.dictionnaire_tours:
            i = self.modele.dictionnaire_tours[i]
            if len(i.liste_projectiles) != 0:
                for j in i.liste_projectiles:
                    if isinstance(i, tour.Tour_Bombe):
                        self.canevas.create_oval(j.x - 10, j.y - 10, j.x + 10, j.y + 10,
                                                 fill="darkred", tags="dynamique")
                    elif isinstance(i, tour.Tour_Mitraillette):
                        self.canevas.create_oval(j.x - 5, j.y - 5, j.x + 5, j.y + 5,
                                                 fill="yellow", tags="dynamique")
                    elif isinstance(i, tour.Tour_Sniper):
                        self.canevas.create_rectangle(j.x - 5, j.y - 5, j.x + 5, j.y + 5,
                                                      fill="#6b83a6", tags="dynamique")
        self.afficher_portail()
        self.afficher_monstres()


    def afficher_portail(self):
        portail = self.modele.portail
        self.canevas.create_image(portail.x, portail.y, image=portail.images[portail.indice], tags=("dynamique"))

    def afficher_tour(self, tour_a_afficher):
        self.canevas.delete(tour_a_afficher.id)

        tag = None

        if isinstance(tour_a_afficher, tour.Tour_Sniper):
            if tour_a_afficher.niveau == 1:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_sniper1,
                                          tags=("statique", tour_a_afficher.id, "tour", "sn1"))
            if tour_a_afficher.niveau == 2:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_sniper2,
                                          tags=("statique", tour_a_afficher.id, "tour", "sn2"))
            if tour_a_afficher.niveau == 3:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_sniper3,
                                          tags=("statique", tour_a_afficher.id, "tour", "sn3"))
        elif isinstance(tour_a_afficher, tour.Tour_Poison):
            if tour_a_afficher.niveau == 1:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_feu1,
                                          tags=("statique", tour_a_afficher.id, "tour", "pn1"))
            if tour_a_afficher.niveau == 2:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_feu2,
                                          tags=("statique", tour_a_afficher.id, "tour", "pn2"))
            if tour_a_afficher.niveau == 3:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_feu3,
                                          tags=("statique", tour_a_afficher.id, "tour", "pn3"))
        elif isinstance(tour_a_afficher, tour.Tour_Glace):
            if tour_a_afficher.niveau == 1:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_glace1,
                                          tags=("statique", tour_a_afficher.id, "tour", "gn1"))
            if tour_a_afficher.niveau == 2:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_glace2,
                                          tags=("statique", tour_a_afficher.id, "tour", "gn2"))
            if tour_a_afficher.niveau == 3:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_glace3,
                                          tags=("statique", tour_a_afficher.id, "tour", "gn3"))
        elif isinstance(tour_a_afficher, tour.Tour_Bombe):
            if tour_a_afficher.niveau == 1:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_bombe1,
                                          tags=("statique", tour_a_afficher.id, "tour", "bn1"))
            if tour_a_afficher.niveau == 2:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_bombe2,
                                          tags=("statique", tour_a_afficher.id, "tour", "bn2"))
            if tour_a_afficher.niveau == 3:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_bombe3,
                                          tags=("statique", tour_a_afficher.id, "tour", "bn3"))
        elif isinstance(tour_a_afficher, tour.Tour_Mitraillette):
            if tour_a_afficher.niveau == 1:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_mitraillette1,
                                          tags=("statique", tour_a_afficher.id, "tour", "mn1"))
            if tour_a_afficher.niveau == 2:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_mitraillette2,
                                          tags=("statique", tour_a_afficher.id, "tour", "mn2"))
            if tour_a_afficher.niveau == 3:
                self.canevas.create_image(tour_a_afficher.x, tour_a_afficher.y, image=self.image_tour_mitraillette3,
                                          tags=("statique", tour_a_afficher.id, "tour", "mn3"))


    def afficher_path(self):
        self.canevas.create_rectangle(0, 355, 240, 475, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(160, 140, 240, 400, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(160, 140, 485, 250, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(400, 140, 485, 560, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(400, 460, 800, 560, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(720, 320, 800, 560, fill="", outline="", tags="statique")
        self.canevas.create_rectangle(720, 300, 1200, 400, fill="", outline="", tags="statique")

    def afficher_monstres(self):
        for i in self.modele.liste_monstres_terrain:

            if isinstance(i, monstre.Monstre):

                if i.images != None:
                    self.canevas.create_image(i.x, i.y, image=i.images[i.indice], tags=("dynamique"))
                else:
                    self.canevas.create_oval(i.x - 5, i.y - 5, i.x + 5, i.y + 5, fill="black", tags=("dynamique"))
                x1 = i.x - 10
                x2 = x1 + 20
                longueur = 30
                x3 = x1 + (i.vie / monstre.Monstre.vie_max * 20)

                self.canevas.create_rectangle(x1, i.y - 15, x2, i.y - 10, fill="#7a0004", tags=("dynamique"))
                self.canevas.create_rectangle(x1, i.y - 15, x3, i.y - 10, fill="#33673b", tags=("dynamique"))

                if i.empoisonne:
                    self.canevas.create_rectangle(x1, i.y - 15, x2, i.y - 10, fill="#e09f3e", tags=("dynamique"))
                    self.canevas.create_rectangle(x1, i.y - 15, x3, i.y - 10, fill="darkgreen", tags=("dynamique"))
                if i.frozen:
                    self.canevas.create_rectangle(x1, i.y - 15, x2, i.y - 10, fill="lightblue", tags=("dynamique"))
                    self.canevas.create_rectangle(x1, i.y - 15, x3, i.y - 10, fill="darkblue", tags=("dynamique"))

            if isinstance(i, monstre.Boss):
                self.canevas.create_image(i.x, i.y, image=i.images[i.indice], tags=("dynamique"))
                # self.canevas.create_oval(i.x - 15, i.y - 15, i.x + 15, i.y + 15, fill="red", tags=("dynamique", "boss"))
                x1 = i.x - 10
                x2 = x1 + 20
                x3 = x1 + (i.vie / monstre.Boss.vie_max *20)
                self.canevas.create_rectangle(x1, i.y - 15, x2, i.y - 10, fill="red", tags="dynamique")
                self.canevas.create_rectangle(x1, i.y - 15, x3, i.y - 10, fill="green", tags="dynamique")



    def afficher_fin_partie(self):
        self.canevas.delete("dynamique")
        self.var_argent.set(str(self.modele.argent) + "$")
        self.var_score.set(self.modele.pointage)
        self.var_vie.set(self.modele.vie)
        self.var_vague.set(self.modele.vague)
        self.parent.score_dans_fichier("Utilisateur1", self.modele.pointage)
        self.changer_cadre("menu_mort")


    def reinitialiser_vue(self):
        self.canevas.delete(ALL)
        self.afficher_debut_partie()

    def update_information(self, event):
        val = self.canevas.gettags(CURRENT)
        self.canevas.delete("rayon")
        self.tour_selectionne = self.modele.dictionnaire_tours[(val[1])]
        self.tour_selectionne.rayon_visible()

    def upgrade(self):
        self.parent.upgrade(self.tour_selectionne)

        self.canevas.delete("rayon")
        self.afficher_tour(self.tour_selectionne)

    def update_message(self):
        if self.tour_selectionne:
            self.message = "niveau : " + str(self.tour_selectionne.niveau) + " - prix de l'amélioration : " + str(
                self.tour_selectionne.prix_niveau) + " $"


class Modele:
    def __init__(self, parent):
        self.tour_en_cours = None
        self.parent = parent
        self.largeur_carte = 1200
        self.hauteur_carte = 800
        self.path = [[200, 450], [200, 200], [440, 200], [440, 520], [760, 520], [760, 370], [1250, 370]]
        self.fin_de_partie = 1
        self.delai_creation_creep = 0
        self.nb_creep_vague = 10
        self.delai_creation_creep_max = 50
        self.pointage = 0
        self.argent = 1000
        self.score = 0
        self.vie = 3
        self.vague = 0
        self.liste_monstres_terrain = []
        self.liste_monstres_entrepot = []
        self.liste_projectiles = []
        self.dictionnaire_tours = {}
        self.animations = {}
        self.portail = None

    def get_scores(self):
        texte = ""
        file = open('scores.txt', 'r')
        while True:
            line = file.readline()
            texte += line
            if line == '': break
        return texte

    def score_dans_fichier(self, nom, score):
        fichier = open('scores.txt', 'a')
        fichier.write(nom + ' : ' + str(score) + "\n")
        fichier.close()

    def jouer_partie(self):
        if not self.parent.pause:
            self.bouger_monstres()
            if len(self.dictionnaire_tours) > 0:
                self.attaque_monstres()
            self.verifier_etat_monstre()
            self.verifier_etat_joueur()
        return self.fin_de_partie

    def jouer_tour(self):
        self.bouger_monstres()

    def creer_monstre(self):
        self.portail = monstre.Portail(self.animations["portail"])
        self.vague += 1
        self.argent += 50 * self.vague
        vitesse = 1 + self.vague / 3
        monstre.Monstre.vie_max = 100 + self.vague * 20
        self.nb_creep_vague = self.vague * 7
        self.delai_creation_creep -= 3

        if self.vague % 5 == 0:
            self.liste_monstres_terrain.append(monstre.Boss(-10, 450, vitesse, 1000, self.animations["boss"]))
        for i in range(self.nb_creep_vague):
            self.liste_monstres_entrepot.append(
                monstre.Monstre(-10, 450, vitesse, monstre.Monstre.vie_max, self.animations["monstre"]))
        self.delai_creation_creep = 0


    def bouger_monstres(self):
        if not self.liste_monstres_entrepot and not self.liste_monstres_terrain:
            self.creer_monstre()
        self.portail.animer()
        self.spawn_monstre()
        for i in self.liste_monstres_terrain:
            i.avancer_monstre(self.path)


    def spawn_monstre(self):
        self.delai_creation_creep += 1
        if self.delai_creation_creep == self.delai_creation_creep_max and len(self.liste_monstres_entrepot) != 0:
            temp = self.liste_monstres_entrepot.pop(0)
            self.liste_monstres_terrain.append(temp)
            self.delai_creation_creep = 0

    def attaque_monstres(self):
        for i in self.dictionnaire_tours:
            i = self.dictionnaire_tours[i]
            i.action(self.liste_monstres_terrain)

    def creer_tour(self, event):

        x = event.x
        y = event.y
        id = creer_id()
        t = None
        if self.tour_en_cours == 'S':
            self.argent -= tour.Tour_Sniper.prix
            t = tour.Tour_Sniper(x, y, 250, 10, id)
        if self.tour_en_cours == 'P':
            self.argent -= tour.Tour_Poison.prix
            t = tour.Tour_Poison(x, y, 120, 10, id)
        if self.tour_en_cours == 'G':
            self.argent -= tour.Tour_Glace.prix
            t = tour.Tour_Glace(x, y, 120, 10, id)
        if self.tour_en_cours == 'B':
            self.argent -= tour.Tour_Bombe.prix
            t = tour.Tour_Bombe(x, y, 100, 10, id)
        if self.tour_en_cours == 'M':
            self.argent -= tour.Tour_Mitraillette.prix
            t = tour.Tour_Mitraillette(x, y, 200, 8, id)
        if t is not None:
            self.dictionnaire_tours[id] = t
            self.parent.afficher_tour(t)
        self.tour_en_cours = None

    def verifier_etat_monstre(self):
        for i in self.liste_monstres_terrain:
            if i.vie <= 0:
                self.pointage += 5
                self.score += 50
                self.argent += 25
                self.liste_monstres_terrain.remove(i)
            if i.x > 1143:
                self.liste_monstres_terrain.remove(i)
                if self.vie > 0:
                    self.vie -= 1
            if i.empoisonne:
                i.vie -= tour.Tour_Poison.degat + i.stack_poison / 1000

    def verifier_etat_joueur(self):
        if self.vie == 0:
            self.parent.partie_en_cours = 0
            self.fin_de_partie = 0




    def reinitialiser(self):
        self.liste_monstres_terrain = []
        self.liste_monstres_entrepot = []
        self.liste_projectiles = []
        self.dictionnaire_tours = {}
        self.vie = 3
        self.vague = 0
        self.pointage = 0
        self.fin_de_partie = 1
        self.argent = 1000
        self.parent.reinitialiser_vue()
        self.tour_en_cours = None

    def creer_sniper(self):
        if (self.argent - tour.Tour_Sniper.prix) >= 0:
            self.tour_en_cours = 'S'

    def creer_poison(self):
        if (self.argent - tour.Tour_Poison.prix) >= 0:
            self.tour_en_cours = 'P'

    def creer_bombe(self):
        if (self.argent - tour.Tour_Bombe.prix) >= 0:
            self.tour_en_cours = 'B'

    def creer_glace(self):
        if (self.argent - tour.Tour_Glace.prix) >= 0:
            self.tour_en_cours = 'G'

    def creer_mitraillette(self):
        if (self.argent - tour.Tour_Mitraillette.prix) >= 0:
            self.tour_en_cours = 'M'

    def trouver_tour(self, id):
        objet = self.dictionnaire_tours[id]
        return objet

    def upgrade(self, tour):
        if tour.prix_niveau <= self.argent:
            self.argent -= tour.prix_niveau
            tour.upgrade()



class Controleur:
    def __init__(self):
        self.partie_en_cours = 0
        self.pause = False
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.afficher_debut_partie()
        self.vue.root.mainloop()


    def debuter_partie(self):
        if not self.partie_en_cours:
            self.partie_en_cours = 1
            self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            partie_roule = self.modele.jouer_partie()
            if partie_roule:
                if not self.pause:
                    self.modele.jouer_tour()
                self.vue.afficher_partie()
                self.vue.root.after(40, self.jouer_partie)
            else:
                self.vue.afficher_fin_partie()
                self.partie_en_cours = 0
                self.modele.reinitialiser()

    def creer_tour(self, event):
        if self.partie_en_cours:
            self.modele.creer_tour(event)

    def creer_tour_glace(self):
        if self.partie_en_cours:
            self.modele.creer_glace()

    def creer_tour_sniper(self):
        if self.partie_en_cours:
            self.modele.creer_sniper()

    def creer_tour_poison(self):
        if self.partie_en_cours:
            self.modele.creer_poison()

    def creer_tour_mitraillette(self):
        if self.partie_en_cours:
            self.modele.creer_mitraillette()

    def creer_tour_bombe(self):
        if self.partie_en_cours:
            self.modele.creer_bombe()

    def inserer_animation(self, info_gif):
        self.modele.animations = info_gif

    def trouver_tour(self, id):
        self.modele.trouver_tour(id)

    def score_dans_fichier(self, nom, score):
        self.modele.score_dans_fichier(nom, score)

    def afficher_tour(self, tour):
        self.vue.afficher_tour(tour)

    def reinitialiser_vue(self):
        self.vue.reinitialiser_vue()

    def partie_pause(self):
        if self.partie_en_cours:
            if self.pause:
                self.pause = False
                return self.pause
            self.pause = True
        return self.pause

    def upgrade(self, tour):
        self.modele.upgrade(tour)


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
