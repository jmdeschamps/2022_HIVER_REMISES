import random

import Modele
from tkinter import *

class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.centre_interface = self.modele.interface.largeur/2
        self.root = Tk()
        self.root.title("Tower Defense - Smile, Even A Little")
        listeimmagecreep_gauche = self.charger_gifs('./images/sad_creep_gauche.gif')
        listeimmagecreep_doite = self.charger_gifs('./images/sad_creep_droite.gif')
        self.sprites = {"creep_gauche": listeimmagecreep_gauche,
                        "creep_droite": listeimmagecreep_doite}
        self.img_tour_confiance = PhotoImage(file='./images/tour_confiance.png')
        self.img_tour_relation = PhotoImage(file='./images/tour_relation.png')
        self.img_cartes = {"carte1": PhotoImage(file='./images/carte1.png')}
        self.largeur_bouton = 100
        self.menu_game_over = False
        self.root.config(cursor="heart")

    def creer_interface(self):
        self.canevas = Canvas(self.root, width=self.modele.carte.largeur, height=self.modele.hauteur, bg="ivory")
        self.canevas.pack(side=LEFT)
        self.interface = Canvas(self.root, width=self.modele.interface.largeur, height=self.modele.hauteur, bg="ivory")
        self.interface.pack(side=RIGHT)

        self.sante_mentale_texte = Label(self.interface, text="SANTÉ MENTALE", font=("Arial", 16))
        self.sante_mentale_valeur = Label(self.interface, text=self.modele.partie.sante_mentale, font=("Arial", 16))
        self.motivation_texte = Label(self.interface, text="MOTIVATION", font=("Arial", 16))
        self.motivation_valeur = Label(self.interface, text=self.modele.partie.motivation, font=("Arial", 16))
        self.antidepresseur_texte = Label(self.interface, text="ANTI-DÉPRESSEURS", font=("Arial", 16))
        self.antidepresseur_valeur = Label(self.interface, text=self.modele.partie.antidepresseur, font=("Arial", 16))
        self.vague_texte = Label(self.interface, text="VAGUE " + str(self.modele.partie.no_vague + 1), font=("Arial", 16))
        self.vague_max_creeps = self.modele.partie.vagues[self.modele.partie.no_vague].nbr_creeps
        self.vague_creeps_cumules = self.vague_max_creeps - len(self.modele.partie.vagues[self.modele.partie.no_vague].creeps_attente)
        self.vague_creeps = Label(self.interface,
                             text=str(self.vague_creeps_cumules) + " / " + str(self.vague_max_creeps), font=("Arial", 16))
        self.creeps_vivant_texte = Label(self.interface, text="CREEPS EN VIE", font=("Arial", 16))
        self.creeps_vivant = Label(self.interface, text=len(self.modele.partie.creeps), font=("Arial", 16))

        self.bouton_tour_confiance = Button(self.interface, text="Tour Confiance", image=self.img_tour_confiance,
                                            command=lambda: self.parent.placer_tour("confiance"), compound="top", width=self.largeur_bouton)
        self.tour_confiance_prix = Label(self.interface, text=Modele.Tour_Confiance.prix, font=("Arial", 14))

        self.bouton_tour_relation = Button(self.interface, text="Tour Relation", image=self.img_tour_relation,
                                           command=lambda: self.parent.placer_tour("relation"), compound="top", width=self.largeur_bouton)
        self.tour_relation_prix = Label(self.interface, text=Modele.Tour_Relation.prix, font=("Arial", 14))


        self.toggle_bouton_tour = self.interface.create_rectangle(self.centre_interface - 15, 435,
                                                                  self.centre_interface + 15, 445,
                                                                  fill="black")
        #pour gérer un futur compte à rebours
        #self.timer = Label(self.interface, text=str(self.modele.partie.timer), font=("Arial", 16))

        self.interface.create_window(self.centre_interface, 50, window=self.sante_mentale_texte)
        self.interface.create_window(self.centre_interface, 75, window=self.sante_mentale_valeur, tags="rafraichir")
        self.interface.create_window(self.centre_interface, 130, window=self.motivation_texte)
        self.interface.create_window(self.centre_interface, 155, window=self.motivation_valeur, tags="rafraichir")
        self.interface.create_window(self.centre_interface, 210, window=self.antidepresseur_texte)
        self.interface.create_window(self.centre_interface, 235, window=self.antidepresseur_valeur, tags="rafraichir")
        self.interface.create_window(self.centre_interface, 290, window=self.vague_texte, tags="rafraichir")
        self.interface.create_window(self.centre_interface, 315, window=self.vague_creeps, tags="rafraichir")
        self.interface.create_window(self.centre_interface, 370, window=self.creeps_vivant_texte)
        self.interface.create_window(self.centre_interface, 395, window=self.creeps_vivant, tags="rafraichir")
        self.interface.create_window(self.centre_interface - 35, 520, window=self.bouton_tour_confiance)
        self.interface.create_window(self.centre_interface + 55, 520, window=self.tour_confiance_prix)
        self.interface.create_window(self.centre_interface - 35, 645, window=self.bouton_tour_relation)
        self.interface.create_window(self.centre_interface + 55, 645, window=self.tour_relation_prix)

        #pour gérer un futur compte à rebours
        #self.interface.create_window(self.centre_interface, 800, window=self.timer)

        self.afficher_carte_de_jeu()

    # On affiche l'arrière-plan, chemins et autres décorations dès le début
    def afficher_carte_de_jeu(self):

        self.canevas.create_image(0, 0, image=self.img_cartes["carte1"], anchor="nw", tags="libre")

        for chemin in self.modele.carte.chemins:
            self.canevas.create_line(chemin.x1, chemin.y1, chemin.x2, chemin.y2, fill='', width=chemin.bordure, tags="zone_chemin")
            self.canevas.create_line(chemin.x1, chemin.y1, chemin.x2, chemin.y2, fill='', width=chemin.largeur, tags="chemin")

        self.canevas.tag_bind("libre", "<Button-1>", self.creer_tour)
        self.canevas.bind("<Motion>", self.recibler_tour)
        self.curseur_tour = self.canevas.create_image(0, 0, image="", anchor="center", tag=("", "curseur_tour"))


    def afficher_partie(self):
        self.canevas.delete("mobile")

        # On change le contenu textuel du Label plutôt que le reconstruire
        self.sante_mentale_valeur.config(text=self.modele.partie.sante_mentale)
        self.motivation_valeur.config(text=self.modele.partie.motivation)
        self.antidepresseur_valeur.config(text=self.modele.partie.antidepresseur)

        self.vague_texte.config(text="VAGUE " + str(self.modele.partie.no_vague + 1))
        self.vague_max_creeps = self.modele.partie.vagues[self.modele.partie.no_vague].nbr_creeps
        self.vague_creeps_cumules = self.vague_max_creeps - len(self.modele.partie.vagues[self.modele.partie.no_vague].creeps_attente)
        self.vague_creeps.config(text=str(self.vague_creeps_cumules) + " / " + str(self.vague_max_creeps))
        self.creeps_vivant.config(text=len(self.modele.partie.creeps), font=("Arial", 16))

        if self.modele.partie.activer_placer:
            self.interface.itemconfig(self.toggle_bouton_tour, fill="#668cff")
        else:
            self.interface.itemconfig(self.toggle_bouton_tour, fill="black")

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
            self.canevas.create_rectangle(x - r * 1.6, y - hauteur_barre_vie - (r + 15),
                                          (x - r * 1.8) + largeur_barre_vie, y + hauteur_barre_vie - (r + 15),
                                          fill="OliveDrab1", tags=("creep", "mobile"))

        # On efface et réaffiche ici seulement les missiles de la tour et pas les tours elles-mêmes,
        # dont on se charge dans la fonction afficher_tour()
        for tour in self.modele.partie.tours:
            if isinstance(tour, Modele.Tour_Confiance):
                for missile in tour.missiles:
                    if not missile.cible_atteinte:
                        x = missile.x
                        y = missile.y
                        d = missile.demitaille
                        self.canevas.create_oval(x - d, y - d, x + d, y + d, fill="orange", outline="",
                                                 tags=("", "mobile"))
                        self.canevas.create_oval(x-d/2, y-d/2, x+d/2, y+d/2, fill="yellow", outline="", tags=("", "mobile"))
            if isinstance(tour, Modele.Tour_Relation):
                if tour.laser is not None and tour.laser_actif:
                    self.canevas.create_line(tour.x, tour.y, tour.laser.cible_x, tour.laser.cible_y, fill='red',
                                             width=tour.laser.largeur, tags=("", "mobile"))
                    self.canevas.create_line(tour.x, tour.y, tour.laser.cible_x, tour.laser.cible_y, fill='orange',
                                             width=tour.laser.largeur/2, tags=("", "mobile"))



    # On affiche la nouvelle tour, qu'on efface PAS par la suite.
    # Réception de la tour retourné par la fonction creer_tour() dans le Contrôleur
    def afficher_tour(self, tour):
        x = tour.x
        y = tour.y
        d = tour.demi_taille
        r = tour.rayon_detection
        z = tour.zone_occupee
        self.canevas.create_oval(x - r, y - r, x + r, y + r, outline="grey", dash="30", tags=("zone_tour", ""))
        self.canevas.create_rectangle(x - d - z, y - d - z, x + d + z, y + d + z, fill="", outline="",
                                      tags=("zone_tour", ""))
        if isinstance(tour, Modele.Tour_Confiance):
            self.canevas.create_rectangle(x - d, y - d, x + d, y + d, fill="sienna1", tags=("tour", ""))
        elif isinstance(tour, Modele.Tour_Relation):
            self.canevas.create_rectangle(x - d, y - d, x + d, y + d, fill="aquamarine", tags=("tour", ""))

    def recibler_tour(self, evt):
        if self.parent.modele.partie.activer_placer:
            self.root.config(cursor="heart")
        else:
            self.root.config(cursor="arrow")

    def placer_tour(self, evt):
        if evt.widget == self.bouton_tour_confiance:
            self.parent.placer_tour(self, evt, "confiance")

    def creer_tour(self, evt):
        self.x = evt.x
        self.y = evt.y
        self.parent.creer_tour(self.x, self.y)

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
                print(noindex)
            except Exception:
                testverite = 0
                print("erreur")
        return listeimages

    def afficher_fin_partie(self):
        if not self.menu_game_over:
            self.menu_game_over = True
            self.canevas.create_text(450, 312, text="GAME OVER", fill="black", font=('Helvetica 30 bold'),tags="bouton_partie")
            self.bouton_partie_game_over = Button(self.canevas, text="Redémarer",width=25,bg="gold2")
            self.bouton_partie_game_over.bind("<Button-1>", self.parent.redemarrer)
            self.canevas.create_window(450,350,window=self.bouton_partie_game_over,tags="bouton_partie")

    def afficher_partie_gagnee(self):
        self.canevas.create_text(450, 312, text="GAME WON !", fill="black", font=('Helvetica 30 bold'),
                                 tags="bouton_partie")
        self.bouton_partie_game_won = Button(self.canevas, text="Redémarer", width=25, bg="gold2")
        self.bouton_partie_game_won.bind("<Button-1>", self.parent.redemarrer)
        self.canevas.create_window(450, 350, window=self.bouton_partie_game_won, tags="bouton_partie")

    def redemarrer_interface(self):
        self.menu_game_over = False
        self.canevas.delete("bouton_partie")
        self.canevas.delete("tour")
        self.canevas.delete("zone_tour")
        self.canevas.delete("no_vague")


