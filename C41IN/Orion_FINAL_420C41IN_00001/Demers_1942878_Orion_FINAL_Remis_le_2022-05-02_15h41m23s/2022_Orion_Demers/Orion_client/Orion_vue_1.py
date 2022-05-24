# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.simpledialog import *
import tkinter
from tkinter.messagebox import *
from tkinter import *
from helper import Helper as hlp
from functools import partial
import math

import random
import Orion_modele

from PIL import Image, ImageTk
from PIL import Image, ImageDraw


class Vue:
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):

        self.btn_trou_noir_actif = False

        self.artefacts = [1, 2, 3]
        self.artefacts_possedes = None

        self.label_etoile_or = None
        self.or_extrait = None
        self.stats_bronze = None
        self.stats_argent = None
        self.stats_or = None
        self.stats_hydrogene = None
        self.stats_nourriture = None
        self.stats_population = None
        self.clock = 0

        self.images_joueur = {}
        self.images_univers = {}
        self.images_interface = {}
        self.ressources_hydrogene = None
        self.ressources_bronze = None
        self.ressources_argent = None
        self.ressources_or = None
        self.ressources_nourriture = None
        self.ressources_population = None
        self.liste_options_selection_etoile = []
        self.wigets_creation_batiment = []
        self.widgets_batiment = []
        self.options_batiment = []
        self.parent = parent
        self.root = Tk()
        self.root.title("ORION: LE JEU")
        self.etoile_selectionne = None
        self.etoile_population = StringVar()
        self.etoile_nourriture = StringVar()
        self.etoile_or = StringVar()
        self.etoile_argent = StringVar()
        self.etoile_bronze = StringVar()
        self.etoile_hydrogene = StringVar()
        self.mon_nom = mon_nom
        # attributs
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None
        self.ma_selection_vaisseau = None
        self.cadre_actif = None
        # cadre principal de l'application
        self.cadre_app = Frame(self.root, width=500, height=400, bg="red")
        self.cadre_app.pack(expand=1, fill=BOTH)
        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres = {}
        self.creer_cadres(urlserveur, mon_nom, msg_initial)
        self.changer_cadre("splash")
        # PROTOCOLE POUR INTERCEPTER LA FERMETURE DU ROOT - qui termine l'application
        # self.root.protocol("WM_DELETE_WINDOW", self.demander_abandon)

        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None
        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteur_actif = None
        self.memoire_selection = None
        self.root.attributes("-transparentcolor", "gray13")
        self.mod = Orion_modele.Modele

    def demander_abandon(self):
        rep = askokcancel("Vous voulez vraiment quitter?")
        if rep:
            self.root.after(500, self.root.destroy)

    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadre_actif:
            self.cadre_actif.pack_forget()
        self.cadre_actif = cadre
        self.cadre_actif.pack(expand=1, fill=BOTH)

    ###### LES CADRES ############################################################################################
    def creer_cadres(self, urlserveur, mon_nom, msg_initial):
        self.cadres["splash"] = self.creer_cadre_splash(urlserveur, mon_nom, msg_initial)
        self.cadres["lobby"] = self.creer_cadre_lobby()
        self.cadres["partie"] = self.creer_cadre_partie()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def creer_cadre_splash(self, urlserveur, mon_nom, msg_initial):
        self.cadre_splash = Frame(self.cadre_app)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas

        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="darkgray")

        self.labelTitre = Label(self.canevas_splash, text="ORION: LE JEU", font="Helvetica 28 underline", bg="darkgray",
                                fg='white')
        self.labelTitre.place(x=180, y=20)
        # LOGO
        self.canevas_splash.create_oval(50, 425, 270, 460, outline="#000",
                                        fill="#FFF", width=2)
        self.canevas_splash.create_polygon(160, 280, 240, 450, 160, 380, 80, 450, 160, 280, outline="#ffffff", width=2)
        self.canevas_splash.create_polygon(160, 280, 240, 450, 160, 380, 160, 280, outline="#ffffff", width=2)

        self.canevas_splash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14), width=42)
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevas_splash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevas_splash.create_window(210, 250, window=self.urlsplash, width=360, height=30)
        self.canevas_splash.create_window(480, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)

        # on place les autres boutons
        self.canevas_splash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash

    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadre_app)
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="darkgray")
        # self.afficher_decor(self.mod)
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE, justify=CENTER, font=("monospace", 14))

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie, anchor=CENTER)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    def creer_cadre_partie(self):
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="yellow")
        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="teal")

        self.scrollX = Scrollbar(self.cadrejeu, orient=HORIZONTAL)
        self.scrollY = Scrollbar(self.cadrejeu, orient=VERTICAL)
        self.canevas = Canvas(self.cadrejeu, width=800, height=600,
                              xscrollcommand=self.scrollX.set,
                              yscrollcommand=self.scrollY.set, bg="grey11")

        self.scrollX.config(command=self.canevas.xview)
        self.scrollY.config(command=self.canevas.yview)

        self.canevas.grid(column=0, row=0, sticky=W + E + N + S)
        self.scrollX.grid(column=0, row=1, sticky=W + E)
        self.scrollY.grid(column=1, row=0, sticky=N + S)

        self.cadrejeu.columnconfigure(0, weight=1)
        self.cadrejeu.rowconfigure(0, weight=1)
        self.canevas.bind("<Button>", self.cliquer_cosmos)
        self.canevas.tag_bind(ALL, "<Button>", self.cliquer_cosmos)

        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)

        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)

        self.creer_cadre_outils()

        self.cadrejeu.pack(side=LEFT, expand=1, fill=BOTH)
        self.creer_cadre_ressources()
        self.cadre_messages()
        return self.cadrepartie

    def creer_cadre_outils(self):
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="black")
        self.cadreoutils.pack(side=LEFT, fill=Y)

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="black")
        self.cadreinfo.pack(fill=BOTH)

        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="black")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btn_trou_noir = Button(self.cadreinfogen, text="Trou noir")
        self.btn_trou_noir.bind("<Button>", self.bouton_trou_noir)

        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btn_manipuler = Button(self.cadreoutils, text="Manipuler")
        # self.btn_manipuler.bind("<Button>", self.manipuler)
        self.btnmini.pack()
        # self.btn_trou_noir.pack()

        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30")
        self.btncreerexplorateur = Button(self.cadreinfochoix, text="Explorateur")
        self.btncreerexplorateur.bind("<Button>", self.creer_vaisseau)
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)
        self.btncreercombattant = Button(self.cadreinfochoix, text="Combattant")
        self.btncreercombattant.bind("<Button>", self.creer_vaisseau)

        self.bouton_explorer = Button(self.cadreoutils, text="Explorer")
        self.bouton_ameliorer = Button(self.cadreoutils, text="Améliorer")
        self.bouton_explorer.bind("<Button>", self.exploration)
        self.bouton_ameliorer.bind("<Button>", self.ameliorer_vaisseau)

        self.btncreerexplorateur.pack()
        self.btncreercargo.pack()
        self.btncreercombattant.pack()

        # Action Vaisseau Exploreur
        self.liste_action_explorer = []

        self.bouton_explorer = Button(self.cadreoutils, text="Explorer")
        self.bouton_explorer.bind("<Button>", self.exploration)

        self.liste_action_explorer.append(self.bouton_explorer)

        self.cadreinfoliste = Frame(self.cadreinfo)

        self.scroll_liste_Y = Scrollbar(self.cadreinfoliste, orient=VERTICAL)
        self.info_liste = Listbox(self.cadreinfoliste, width=20, height=6, yscrollcommand=self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-3>", self.centrer_liste_objet)
        self.info_liste.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_Y.grid(column=1, row=0, sticky=N + S)

        self.cadreinfoliste.columnconfigure(0, weight=1)
        self.cadreinfoliste.rowconfigure(0, weight=1)

        self.cadreinfoliste.pack(side=BOTTOM, expand=1, fill=BOTH)

        self.cadreminimap = Frame(self.cadreoutils, height=200, width=200, bg="black")
        self.canevas_minimap = Canvas(self.cadreminimap, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="darkblue")
        self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=BOTTOM)

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def creer_cadre_ressources(self):

        self.stats_population = StringVar()
        self.stats_nourriture = StringVar()
        self.stats_hydrogene = StringVar()
        self.stats_or = StringVar()
        self.stats_argent = StringVar()
        self.stats_bronze = StringVar()
        self.artefacts_possedes = StringVar(value=self.artefacts)

        self.artefacts_possedes.set(self.artefacts)
        self.stats_population.set(self.ressources_population)
        self.stats_nourriture.set(self.ressources_nourriture)
        self.stats_hydrogene.set(self.ressources_hydrogene)
        self.stats_or.set(self.ressources_or)
        self.stats_argent.set(self.ressources_argent)
        self.stats_bronze.set(self.ressources_bronze)

        self.cadre_ressources = Frame(self.canevas, bg="pink")
        self.cadre_ressources_types = Frame(self.canevas, bg="pink")
        self.cadre_artefacts_titre = Frame(self.canevas, bg="pink")
        self.cadre_artefacts = Frame(self.canevas, bg="pink")

        # self.frame_ress_pop = Frame(self.cadre_ressources, height=50, width=100, bg="gray")
        # self.frame_ress_pop.pack(side=LEFT)
        self.label_pop_text = Label(self.cadre_ressources_types, text="Population:", height=2, width=10,
                                    relief=SUNKEN, bg="black", fg="lightblue")
        self.label_pop_text.pack(fill=Y, side=LEFT)
        self.label_pop = Label(self.cadre_ressources, textvariable=self.stats_population, height=2, width=10,
                               relief=SUNKEN, bg="black", fg="lightblue")
        self.label_pop.pack(fill=Y, side=LEFT)

        self.label_nourriture_text = Label(self.cadre_ressources_types, text="Nourriture:", height=2, width=10,
                                           relief=SUNKEN, bg="black", fg="lightblue")
        self.label_nourriture_text.pack(fill=Y, side=LEFT)
        self.label_nourriture = Label(self.cadre_ressources, textvariable=self.stats_nourriture, height=2, width=10,
                                      relief=SUNKEN, bg="black", fg="lightblue")
        self.label_nourriture.pack(fill=Y, side=LEFT)

        self.label_hydrogene_text = Label(self.cadre_ressources_types, text="Hydrogène:", height=2, width=10,
                                          relief=SUNKEN, bg="black", fg="lightblue")
        self.label_hydrogene_text.pack(fill=Y, side=LEFT)
        self.label_hydrogene = Label(self.cadre_ressources, textvariable=self.stats_hydrogene, height=2, width=10,
                                     relief=SUNKEN, bg="black", fg="lightblue")
        self.label_hydrogene.pack(fill=Y, side=LEFT)

        self.label_or_text = Label(self.cadre_ressources_types, text="Or:", height=2, width=10,
                                   relief=SUNKEN, bg="black", fg="lightblue")
        self.label_or_text.pack(fill=Y, side=LEFT)
        self.label_or = Label(self.cadre_ressources, textvariable=self.stats_or, height=2, width=10, relief=SUNKEN,
                              bg="black", fg="lightblue")
        self.label_or.pack(fill=Y, side=LEFT)

        self.label_argent_text = Label(self.cadre_ressources_types, text="Argent:", height=2, width=10,
                                       relief=SUNKEN, bg="black", fg="lightblue")
        self.label_argent_text.pack(fill=Y, side=LEFT)
        self.label_argent = Label(self.cadre_ressources, textvariable=self.stats_argent, height=2, width=10,
                                  relief=SUNKEN, bg="black", fg="lightblue")
        self.label_argent.pack(fill=Y, side=LEFT)

        self.label_bronze_text = Label(self.cadre_ressources_types, text="Bronze:", height=2, width=10,
                                       relief=SUNKEN, bg="black", fg="lightblue")
        self.label_bronze_text.pack(fill=Y, side=LEFT)
        self.label_bronze = Label(self.cadre_ressources, textvariable=self.stats_bronze, height=2, width=10,
                                  relief=SUNKEN, bg="black", fg="lightblue")
        self.label_bronze.pack(fill=Y, side=LEFT)

        self.label_artefacts_text = Label(self.cadre_artefacts_titre, text="Artefacts:", height=1, width=32,
                                          relief=SUNKEN, bg="black", fg="lightblue")
        self.scroll_liste_artefacts_Y = Scrollbar(self.cadre_artefacts, orient=VERTICAL)

        self.label_artefacts = Listbox(self.cadre_artefacts, width=35, height=5, relief=SUNKEN, justify=CENTER,
                                       yscrollcommand=self.scroll_liste_artefacts_Y.set)
        # self.scroll_liste_artefacts_Y.config(command=self.label_artefacts.yview)

        self.label_artefacts.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_artefacts_Y.grid(column=1, row=0, sticky=N + S)
        self.cadre_artefacts.columnconfigure(0, weight=1)
        self.cadre_artefacts.rowconfigure(0, weight=1)

        self.label_artefacts_text.pack()
        # self.label_artefacts.pack()

        self.cadre_ressources_types.pack(side=TOP, anchor=NW)
        self.cadre_ressources.pack(side=TOP, anchor=NW)
        self.cadre_artefacts_titre.pack(side=TOP, anchor=NW)
        self.cadre_artefacts.pack(side=TOP, anchor=NW)

    def cadre_messages(self):
        self.cadre_messages_modele = Frame(self.canevas, height=100, width=800)

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    def centrer_liste_objet(self, evt):
        info = self.info_liste.get(self.info_liste.curselection())
        # print(info)
        liste_separee = info.split(";")
        type_vaisseau = liste_separee[0]
        id = liste_separee[1][1:]
        obj = self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        self.centrer_objet(obj)

    def calc_objets(self, evt):
        print("Univers = ", len(self.canevas.find_all()))

    def defiler_vertical(self, evt):
        rep = self.scrollY.get()[0]
        if evt.delta < 0:
            rep = rep + 0.01
        else:
            rep = rep - 0.01
        self.canevas.yview_moveto(rep)

    def defiler_horizon(self, evt):
        rep = self.scrollX.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

    ##### FONCTIONS DU SPLASH #########################################################################

    ###  FONCTIONS POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="ERREUR - un probleme est survenu")

    def reset_partie(self):
        rep = self.parent.reset_partie()

    def creer_partie(self):
        nom = self.nomsplash.get()
        self.parent.creer_partie(nom)

    ##### FONCTION DU LOBBY #############
    def update_lobby(self, dico):
        self.listelobby.delete(0, END)
        for i in dico:
            self.listelobby.insert(END, i[0])
        if self.parent.joueur_createur:
            self.btnlancerpartie.config(state=NORMAL)

    def inscrire_joueur(self):
        nom = self.nomsplash.get()
        urljeu = self.urlsplash.get()
        self.parent.inscrire_joueur(nom, urljeu)

    def lancer_partie(self):
        self.parent.lancer_partie()

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)
        self.generer_images_joueur()
        self.generer_images_univers()
        self.generer_images_interface()
        self.afficher_decor(modele)

    ####################################################################################################

    def positionner_minicanevas(self, evt):
        x = evt.x
        y = evt.y

        pctx = x / self.taille_minimap
        pcty = y / self.taille_minimap

        xl = (self.canevas.winfo_width() / 2) / self.modele.largeur
        yl = (self.canevas.winfo_height() / 2) / self.modele.hauteur

        self.canevas.xview_moveto(pctx - xl)
        self.canevas.yview_moveto(pcty - yl)
        xl = self.canevas.winfo_width()
        yl = self.canevas.winfo_height()

    def afficher_decor(self, mod):
        # on cree un arriere fond de petites etoieles NPC pour le look
        for i in range(len(mod.etoiles) * 50):
            x = random.randrange(int(mod.largeur))
            y = random.randrange(int(mod.hauteur))
            n = random.randrange(3) + 1
            col = random.choice(["LightYellow", "azure1", "pink"])
            self.canevas.create_oval(x, y, x + n, y + n, fill=col, tags=("fond",))
        # affichage des etoiles
        for i in mod.etoiles:
            t = i.taille * self.zoom
            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80", outline=col,
                                     tags=(i.proprietaire, str(i.id), "Etoile",))
        # affichage des etoiles possedees par les joueurs

        moi = mod.joueurs[self.mon_nom]
        for j in mod.joueurs.keys():
            j = mod.joueurs[j]
            for i in j.etoilescontrolees:
                t = i.taille * self.zoom
                self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                         fill="grey80",
                                         tags=(i.proprietaire, str(i.id), "Etoile"))

                # on affiche dans minimap
                # minix = i.x / self.modele.largeur * self.taille_minimap
                # miniy = i.y / self.modele.hauteur * self.taille_minimap
                # self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                #                                       fill=moi.couleur,
                #                                       tags=(i.proprietaire, str(i.id), "Etoile"))

                # self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                #                          fill=moi.couleur,
                #                          tags=(i.proprietaire, str(i.id), "Etoile"))

        for i in moi.etoilescontrolees:
            t = i.taille * self.zoom
            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80",
                                     tags=(i.proprietaire, str(i.id), "Etoile"))

            # on affiche dans minimap
            minix = i.x / self.modele.largeur * self.taille_minimap
            miniy = i.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                                                  fill=moi.couleur,
                                                  tags=(i.proprietaire, str(i.id), "Etoile"))

            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill=moi.couleur,
                                     tags=(i.proprietaire, str(i.id), "Etoile"))

    def afficher_mini(self, evt):  # univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.taille_minimap
            miniy = j.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 0, miniy + 0,
                                                  fill="black",
                                                  tags=("mini", "Etoile"))
        # # affichage des etoiles possedees par les joueurs
        # for i in mod.joueurs.keys():
        #     for j in mod.joueurs[i].etoilescontrolees:
        #         t = j.taille * self.zoom
        #         self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
        #                                  fill=mod.joueurs[i].couleur,
        #                                  tags=(j.proprietaire, str(j.id),  "Etoile"))

    def centrer_planemetemere(self, evt):
        self.centrer_objet(self.modele.joueurs[self.mon_nom].etoilemere)

    def centrer_objet(self, objet):
        # permet de defiler l'écran jusqu'à cet objet
        x = objet.x
        y = objet.y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.largeur
        pcty = (y - y1) / self.modele.hauteur

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    # change l'appartenance d'une etoile et donc les propriétés des dessins les représentants
    def afficher_etoile(self, joueur, cible):
        joueur1 = self.modele.joueurs[joueur]
        id = cible.id
        couleur = joueur1.couleur
        self.canevas.itemconfig(id, fill=couleur)
        self.canevas.itemconfig(id, tags=(joueur, id, "Etoile",))

    # ajuster la liste des vaisseaux
    def lister_objet(self, obj, id):
        self.info_liste.insert(END, obj + "; " + id)

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau)
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()

    def creer_batiment(self, evt):
        type_batiment = evt.widget.cget("text")[6:]
        if self.ma_selection:
            if self.parent.ressources_necessaires(type_batiment):
                id_etoile = self.ma_selection[1]
                self.ma_selection = None
                print(type_batiment)
                self.parent.creer_batiment(type_batiment, id_etoile)
                self.canevas.delete("marqueur")
                self.retirer_infos_etoile()
            else:
                print("Pas assez de ressources")

    def options_ferme(self, evt, ferme):
        print("Voici les options de votre" + str(ferme.type) + "construite")
        # ON CODE LES OPTIONS DE LEVEL UP ICI

    def options_usine(self, evt, usine):
        print("Voici les options de votre" + str(usine.type) + "construite")
        # ON CODE LES OPTIONS DE LEVEL UP ICI

    def options_mine(self, evt, mine):
        print("Voici les options de votre" + str(mine.type) + "construite")
        # ON CODE LES OPTIONS DE LEVEL UP ICI

    def ameliorer_batiment(self, etoile, batiment):
        if self.parent.ressources_necessaires(batiment.type, batiment):
            self.parent.augmenter_niveau_batiment(batiment.id, etoile.id)
            self.canevas.delete("marqueur")
        else:
            print("Pas assez de ressources")
        self.ma_selection = None
        self.retirer_infos_etoile()

    def ameliorer_vaisseau(self, evt):

        vaisseau_id = self.ma_selection[1]
        self.parent.ameliorer_vaisseau(vaisseau_id)

    def manipuler(self, vaisseau_id):
        self.parent.manipuler(vaisseau_id)
        self.retirer_infos_vaisseau()

    def detruire_batiment(self, etoile, batiment):
        self.parent.detruire_batiment(batiment.id, etoile.id)
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.retirer_infos_etoile()

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("dynamique")
        self.canevas.delete("marqueur")
        self.label_artefacts.delete(0, END)

        self.stats_population.set(str(self.ressources_population))
        self.stats_nourriture.set(str(self.ressources_nourriture))
        self.stats_hydrogene.set(str(self.ressources_hydrogene))
        self.stats_or.set(str(self.ressources_or))
        self.stats_argent.set(str(self.ressources_argent))
        self.stats_bronze.set(str(self.ressources_bronze))
        if self.ma_selection is not None:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoilescontrolees:
                    if i.id == self.ma_selection[1]:
                        x = i.x
                        y = i.y
                        t = 10 * self.zoom
                        # i.espace_vide ON EST LA!!!!!!!!!!!!!!!!!!!!!
                        # afficher_infos_etoile(i)
                        self.canevas.create_oval(x - t, y - t, x + t, y + t,
                                                 dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                 tags=("multiselection", "marqueur"))
            elif self.ma_selection[2] == "Flotte":
                for j in joueur.flotte:
                    for i in joueur.flotte[j]:
                        i = joueur.flotte[j][i]
                        if i.id == self.ma_selection[1]:
                            x = i.x
                            y = i.y
                            t = 10 * self.zoom
                            self.canevas.create_rectangle(x - t, y - t, x + t, y + t,
                                                          dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                          tags=("multiselection", "marqueur"))
        # afficher asset des joueurs
        i = mod.joueurs[self.mon_nom]
        couleur = i.couleur
        self.afficher_projectiles()
        vaisseau_local = []
        for k in i.flotte:
            for j in i.flotte[k]:
                j = i.flotte[k][j]
                tailleF = j.taille * self.zoom
                size = 400 * 0.08
                if k == "Explorateur":
                    angle_dir = int((math.degrees(j.angle_cible) / 9))
                    self.image_actuelle = self.images_joueur[self.mon_nom]["Vaisseaux"]["Explorateur"][j.niveau-1][angle_dir]
                    self.canevas.create_image(j.x - size / 2, j.y - size / 2, anchor=NW, image=self.image_actuelle,
                                              tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                elif k == "Cargo":
                    angle_dir = int((math.degrees(j.angle_cible) / 9))
                    self.image_actuelle = self.images_joueur[self.mon_nom]["Vaisseaux"]["Cargo"][3][angle_dir]
                    self.canevas.create_image(j.x - size / 2, j.y - size / 2, anchor=NW, image=self.image_actuelle,
                                              tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                elif k == "Combattant":
                    angle_dir = int((math.degrees(j.angle_cible) / 9))
                    self.image_actuelle = self.images_joueur[self.mon_nom]["Vaisseaux"]["Combattant"][j.niveau-1][angle_dir]
                    self.canevas.create_image(j.x - size / 2, j.y - size / 2, anchor=NW, image=self.image_actuelle,
                                              tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

        for k in i.visible:

            if isinstance(k, Orion_modele.Vaisseau):
                couleur = k.parent.couleur
                if k.couleur_initiale == i.couleur:
                    couleur = i.couleur

            tailleF = k.taille * self.zoom
            size = 400 * 0.08

            if isinstance(k, Orion_modele.Explorateur):
                angle_dir = int((math.degrees(k.angle_cible) / 9))
                self.image_actuelle = self.images_joueur[k.proprietaire]["Vaisseaux"]["Explorateur"][k.niveau-1][angle_dir]
                self.canevas.create_image(k.x - size / 2, k.y - size / 2, anchor=NW, image=self.image_actuelle,
                                          tags=(k.proprietaire, str(k.id), "Flotte", k, "artefact"))
            elif isinstance(k, Orion_modele.Cargo):
                angle_dir = int((math.degrees(j.angle_cible) / 9))
                self.image_actuelle = self.images_joueur[k.proprietaire]["Vaisseaux"]["Cargo"][k.niveau-1][angle_dir]
                self.canevas.create_image(j.x - size / 2, j.y - size / 2, anchor=NW, image=self.image_actuelle,
                                          tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

            elif isinstance(k, Orion_modele.Combattant):
                    angle_dir = int((math.degrees(k.angle_cible) / 9))
                    self.image_actuelle = self.images_joueur[k.proprietaire]["Vaisseaux"]["Combattant"][k.niveau-1][angle_dir]
                    self.canevas.create_image(k.x - size / 2, k.y - size / 2, anchor=NW, image=self.image_actuelle,
                                              tags=(k.proprietaire, str(k.id), "Flotte", k, "artefact"))

        # for k in i.flotte:
        #     for j in i.flotte[k]:
        #         j = i.flotte[k][j]
        #         tailleF = j.taille * self.zoom
        #         if k == "Explorateur":
        #
        #         elif k == "Cargo":
        #             # self.dessiner_cargo(j,tailleF,i,k)
        #             self.dessiner_cargo(j, tailleF, i, k)
        #
        #             # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
        #             #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
        #             #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
        #         elif k == "Combattant":
        for i in self.modele.liste_trou_noir:
            self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                     i.x + i.pulse, i.y + i.pulse, outline="blue", width=2, fill="grey15",
                                     tags=("", i.id, "Porte_de_ver", "objet_spatial"))
        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

        self.afficher_barrevie()
        self.calculer_ressources()
        self.afficher_carburant()
        self.afficher_artefacts()

        self.clock += 5
        if self.clock >= 60:
            self.clock = 0

    def dessiner_cargo(self, obj, tailleF, joueur, type_obj, couleur):
        t = obj.taille * self.zoom
        a = obj.ang
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="yellow",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    # def dessiner_cargo1(self, j, tailleF, i, k,couleur):
    #     self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
    #                              (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
    #                              tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

    def cliquer_cosmos(self, evt):

        if self.btn_trou_noir_actif:
            x = self.canevas.canvasx(evt.x)
            y = self.canevas.canvasy(evt.y)
            self.parent.creer_trou_noir(x, y)
            self.btn_trou_noir_actif = False

        t = self.canevas.gettags(CURRENT)
        self.retirer_infos_etoile()
        if not t or t[0] != self.mon_nom or t[2] != "Flotte":
            self.retirer_infos_vaisseau()
        if t:  # il y a des tags

            if t[0] == self.mon_nom:  # et
                if t[2] == "Etoile":
                    if self.ma_selection_vaisseau is not None:
                        if self.ma_selection_vaisseau[3] == "Cargo":
                            self.parent.reinitialiser_cargo([self.mon_nom, self.ma_selection_vaisseau[1]])
                        self.parent.cibler_flotte(self.ma_selection_vaisseau[1], t[1], t[2])
                        self.retirer_infos_vaisseau()
                        self.canevas.delete("marqueur")
                        self.ma_selection_vaisseau = None
                        self.ma_selection = None
                    else:
                        self.ma_selection = [self.mon_nom, t[1], t[2]]
                        for i in self.modele.joueurs[self.mon_nom].etoilescontrolees:
                            if i.id == self.ma_selection[1]:
                                self.montrer_etoile_selection(i)
                elif t[2] == "Flotte":
                    self.ma_selection = [self.mon_nom, t[1], t[2]]
                    self.ma_selection_vaisseau = [self.mon_nom, t[1], t[2], t[3]]
                    self.montrer_flotte_selection()

            elif ("Etoile" in t or "Porte_de_ver" in t or "Flotte" in t) and t[0] != self.mon_nom:
                if self.ma_selection:
                    est_valide = True
                    for id_joueur in self.modele.joueurs:
                        if id_joueur != self.mon_nom:
                            if self.modele.joueurs[id_joueur].etoilemere.id == t[1]:
                                est_valide = False
                                break
                    if est_valide:
                        self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                    self.ma_selection = None
                else:
                    if "Flotte" in t or self.modele.joueurs[self.mon_nom].xenomorphe:
                        self.montrer_ennemi_selection(t)

                self.canevas.delete("marqueur")



            else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
                print("Region inconnue")
                self.ma_selection = None
                self.canevas.delete("marqueur")
            if self.ma_selection_vaisseau is not None:
                if t[0] != self.mon_nom and t[2] != "Flotte":
                    self.ma_selection_vaisseau = None

    def montrer_etoile_selection(self, etoile):
        self.etoile_selectionne = etoile
        if self.label_etoile_or and self.label_etoile_argent and self.label_etoile_bronze and self.label_etoile_hydrogene is not None:
            self.label_etoile_or.grid_forget()
            self.label_etoile_argent.grid_forget()
            self.label_etoile_bronze.grid_forget()
            self.label_etoile_hydrogene.grid_forget()
            self.info_etoile_or.grid_forget()
            self.info_etoile_argent.grid_forget()
            self.info_etoile_bronze.grid_forget()
            self.info_etoile_hydrogene.grid_forget()
            self.label_ress_extraites.grid_forget()
            self.cadre_ress_extraites.pack_forget()
            self.label_etoile_population.grid_forget()
            self.label_etoile_nourriture.grid_forget()
            self.label_pop.grid_forget()
            self.label_nourriture.grid_forget()
            self.label_ress_humaines.grid_forget()
            self.cadre_ress_humaines.pack_forget()

        self.cadreinfochoix.pack(fill=BOTH)
        if not self.liste_options_selection_etoile:
            btn_creer_batiment = Button(self.cadreoutils, text="Creer batiment",
                                        command=lambda: self.afficher_creation_batiment(etoile))
            btn_creer_batiment.bind("<Button-1>")
            self.liste_options_selection_etoile.append(btn_creer_batiment)
            btn_creer_batiment.pack()
            for i in etoile.batiments:
                self.liste_options_selection_etoile.append(
                    Button(self.cadreoutils, text=str(i.type) + " niveau " + str(i.niveau),
                           command=lambda i=i: self.afficher_options_batiment(etoile, i)))
                self.liste_options_selection_etoile[-1].bind("<Button>")
                self.liste_options_selection_etoile[-1].pack()
        self.afficher_ressources_extraites(etoile)

    def afficher_creation_batiment(self, etoile):
        self.retirer_infos_etoile()
        if not self.wigets_creation_batiment:
            taille = etoile.taille
            self.wigets_creation_batiment = []
            taille -= len(etoile.batiments)
            info_msg = Label(self.cadreoutils, text="Quantité restante : " + str(taille))
            info_msg.pack()
            self.wigets_creation_batiment.append(info_msg)
            if taille > 0:
                for i in range(5):
                    if i % 5 == 0:
                        text = "Creer Ferme"
                    elif i % 5 == 1:
                        text = "Creer Residence"
                    elif i % 5 == 2:
                        text = "Creer Mine"
                    elif i % 5 == 3:
                        text = "Creer Usine"
                    else:
                        text = "Creer Tour defensive"
                    boutonbatiment = Button(self.cadreoutils, text=text)
                    boutonbatiment.bind("<Button-1>", self.creer_batiment)
                    self.wigets_creation_batiment.append(boutonbatiment)
                    boutonbatiment.pack()

    def afficher_options_batiment(self, etoile, batiment):
        self.retirer_infos_etoile()
        if not self.options_batiment:
            btn_ameliorer = Button(self.cadreoutils, text=("Ameliorer " + str(batiment.type)),
                                   command=lambda: self.ameliorer_batiment(etoile, batiment))
            btn_ameliorer.bind()
            self.options_batiment.append(btn_ameliorer)
            btn_ameliorer.pack()
            btn_detruire = Button(self.cadreoutils, text="Detruire",
                                  command=lambda: self.detruire_batiment(etoile, batiment))
            btn_detruire.bind()
            self.options_batiment.append(btn_detruire)
            btn_detruire.pack()

    def retirer_infos_etoile(self):
        if self.liste_options_selection_etoile:
            for i in self.liste_options_selection_etoile:
                i.pack_forget()
        self.liste_options_selection_etoile = []
        if self.wigets_creation_batiment:
            for i in self.wigets_creation_batiment:
                i.pack_forget()
        self.wigets_creation_batiment = []
        if self.widgets_batiment:
            for i in self.widgets_batiment:
                i.pack_forget()
        self.widgets_batiment = []
        if self.options_batiment:
            for i in self.options_batiment:
                i.pack_forget()
        if self.label_etoile_or and self.label_etoile_argent and self.label_etoile_bronze and self.label_etoile_hydrogene:
            self.label_etoile_argent.grid_forget()
            self.label_etoile_bronze.grid_forget()
            self.label_etoile_hydrogene.grid_forget()
            self.info_etoile_or.grid_forget()
            self.info_etoile_argent.grid_forget()
            self.info_etoile_bronze.grid_forget()
            self.info_etoile_hydrogene.grid_forget()
            self.label_ress_extraites.grid_forget()
            self.cadre_ress_extraites.pack_forget()
            self.label_etoile_population.grid_forget()
            self.label_etoile_nourriture.grid_forget()
            self.label_pop.grid_forget()
            self.label_nourriture.grid_forget()
            self.label_ress_humaines.grid_forget()
            self.cadre_ress_humaines.pack_forget()
            self.label_etoile_or = None
            self.label_etoile_argent = None
            self.label_etoile_bronze = None
            self.label_etoile_hydrogene = None
            self.label_ress_extraites = None
        self.options_batiment = []

    # def supprimer_btn_options_etoile(self):
    #     if self.liste_options_selection_etoile:
    #         for i in self.liste_options_selection_etoile:
    #             i.pack_forget()
    #     self.liste_options_selection_etoile = []
    #
    # def supprimer_options_batiment(self):
    #     if self.widgets_batiment:
    #         for i in self.widgets_batiment:
    #             i.pack_forget()
    #     self.widgets_batiment = []
    #
    # def supprimer_btn_batiment(self):
    #     if self.btns_batiment:
    #         for i in self.btns_batiment:
    #             i.pack_forget()
    #     self.btns_batiment = []

    def test(self, evt):
        print("Bouton pesé")

    def montrer_flotte_selection(self):
        mod = self.modele
        self.memoire_selection = self.ma_selection_vaisseau[1]
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte.keys():
                for m in i.flotte[k]:
                    v = i.flotte[k][m]
                    if v.id == self.memoire_selection:
                        if isinstance(v, Orion_modele.Explorateur):
                            for j in self.liste_action_explorer:
                                # ameli
                                j.pack()

                        # print(
                        #     v.rayon_de_tir,
                        #     "\n",
                        #     v.id,
                        #     "\n",
                        #     v.proprietaire,
                        #     "\n",
                        #
                        #     v.vie_max,
                        #     "\n",
                        #     v.vie_actuelle,
                        #     "\n",
                        #
                        #     v.espace_cargo,
                        #     "\n",
                        #     v.carburant,
                        #     "\n",
                        #     v.carburant_max,
                        #     "\n",
                        #     v.taille,
                        #     "\n",
                        #     v.vitesse,
                        #     "\n",
                        #
                        #     v.vitesse_tir,
                        #     "\n",
                        #     v.tir_delai,
                        #     "\n",
                        #     v.rayon_de_tir,
                        #     "\n",
                        # )

    def montrer_ennemi_selection(self, tags):
        # print(tags[1])
        self.btn_manipuler.config(command=lambda: self.manipuler(tags[1]))

        self.btn_manipuler.pack()

    # Methodes pour multiselect#########################################################
    def debuter_multiselection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteur_actif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline="red", width=2,
                                                             dash=(2, 2), tags=("", "selecteur", "", ""))

    def afficher_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteur_actif, x1, y1, x2, y2)

    def terminer_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.debutselect = []
            objchoisi = (list(self.canevas.find_enclosed(x1, y1, x2, y2)))
            for i in objchoisi:
                if self.parent.mon_nom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.objets_selectionnes.append(self.canevas.gettags(i)[2])

            self.canevas.delete("selecteur")

    ### FIN du multiselect

    def afficher_projectiles(self):
        mod = self.modele
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte.keys():
                for m in i.flotte[k]:
                    v = i.flotte[k][m]
                    if v.liste_projectiles is not None:
                        for p in v.liste_projectiles:

                            if self.clock < 10:
                                self.canevas.create_oval(p.x - 4, p.y - 4, p.x +4, p.y+4, fill="darkgreen", tag="dynamique")
                            elif 10 <= self.clock < 20:
                                self.canevas.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill="lightgreen",
                                                          tag="dynamique")
                            elif 20 <= self.clock < 30:
                                self.canevas.create_oval(p.x - 2, p.y - 2, p.x + 2, p.y + 2, fill="white",
                                                          tag="dynamique")
                            elif 30 <= self.clock < 40:
                                self.canevas.create_oval(p.x - 1, p.y - 1, p.x + 1, p.y + 1, fill="lightgreen",
                                                          tag="dynamique")
                            elif 40 <= self.clock < 50:
                                self.canevas.create_oval(p.x - 2, p.y - 2, p.x + 2, p.y + 2, fill="darkgreen",
                                                          tag="dynamique")
                            elif 50 <= self.clock < 60:
                                self.canevas.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill="white",
                                                         tag="dynamique")
            for etoile in i.etoilescontrolees:
                for batiment in etoile.batiments:
                    if batiment.type == "Tour defensive":
                        if batiment.projectile is not None:
                            id = etoile.id
                            self.canevas.delete(id)
                            self.canevas.create_line(batiment.projectile.parent.etoile.x,
                                                     batiment.projectile.parent.etoile.y,
                                                     batiment.projectile.x, batiment.projectile.y,
                                                     fill=batiment.projectile.couleurs_hex, width=5, tag="dynamique")
                            t = etoile.taille * self.zoom
                            self.canevas.create_oval(etoile.x - t, etoile.y - t, etoile.x + t, etoile.y + t,
                                                     fill=i.couleur,
                                                     tags=(etoile.proprietaire, str(etoile.id), "Etoile",))

    def afficher_barrevie(self):
        mod = self.modele
        moi = mod.joueurs[self.mon_nom]

        for j in moi.flotte.keys():
            for k in moi.flotte[j]:
                vaisseau = moi.flotte[j][k]
                zone_barre = 100 / 4
                size = 400 * 0.08
                vie_pourcentage = (vaisseau.vie_actuelle / vaisseau.vie_max * 100) / 4
                couleur_enflammee = "green" if vaisseau.stack_enflammees == 0 else "#FF5800"
                self.canevas.create_rectangle(vaisseau.x - zone_barre,
                                              vaisseau.y + 10, vaisseau.x + zone_barre,
                                              vaisseau.y + 13, fill="red", tag="dynamique")

                self.canevas.create_rectangle(vaisseau.x - zone_barre,
                                              vaisseau.y + 10, vaisseau.x - zone_barre + vie_pourcentage * 2,
                                              vaisseau.y + 13, fill=couleur_enflammee, tag="dynamique")
                if vaisseau.bouclier >= 1:
                    if self.clock < 10:
                        self.canevas.create_oval(vaisseau.x - size, vaisseau.y - size, vaisseau.x + size, vaisseau.y + size,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 10 <= self.clock < 20:
                        self.canevas.create_oval(vaisseau.x - size * 0.9, vaisseau.y - size * 0.9, vaisseau.x + size * 0.9,
                                                 vaisseau.y + size * 0.9,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 20 <= self.clock < 30:
                        self.canevas.create_oval(vaisseau.x - size * 0.8, vaisseau.y - size * 0.8, vaisseau.x + size * 0.8,
                                                 vaisseau.y + size * 0.8,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 30 <= self.clock < 40:
                        self.canevas.create_oval(vaisseau.x - size * 0.7, vaisseau.y - size * 0.7, vaisseau.x + size * 0.7,
                                                 vaisseau.y + size * 0.7,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 40 <= self.clock < 50:
                        self.canevas.create_oval(vaisseau.x - size * 0.8, vaisseau.y - size * 0.8, vaisseau.x + size * 0.8,
                                                 vaisseau.y + size * 0.8,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")

                    elif 50 <= self.clock < 60:
                        self.canevas.create_oval(vaisseau.x - size * 0.9, vaisseau.y - size * 0.9, vaisseau.x + size * 0.9,
                                                 vaisseau.y + size * 0.9,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")

        for i in moi.visible:
            if isinstance(i, Orion_modele.Vaisseau):
                zone_barre = 100 / 4
                vie_pourcentage = (i.vie_actuelle / i.vie_max * 100) / 4
                size = 400 * 0.08

                couleur_enflammee = "green" if i.stack_enflammees == 0 else "#FF5800"
                self.canevas.create_rectangle(i.x - zone_barre,
                                              i.y + 10, i.x + zone_barre,
                                              i.y + 13, fill="red", tag="dynamique")
                self.canevas.create_rectangle(i.x - zone_barre,
                                              i.y + 10, i.x - zone_barre + vie_pourcentage * 2,
                                              i.y + 13, fill=couleur_enflammee, tag="dynamique")

                if i.bouclier >= 1:
                    if self.clock < 10:
                        self.canevas.create_oval(i.x - size, i.y - size, i.x + size, i.y + size,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 10 <= self.clock < 20:
                        self.canevas.create_oval(i.x - size * 0.9, i.y - size * 0.9, i.x + size * 0.9,
                                                 i.y + size * 0.9,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 20 <= self.clock < 30:
                        self.canevas.create_oval(i.x - size * 0.8, i.y - size * 0.8, i.x + size * 0.8,
                                                 i.y + size * 0.8,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 30 <= self.clock < 40:
                        self.canevas.create_oval(i.x - size * 0.7, i.y - size * 0.7, i.x + size * 0.7,
                                                 i.y + size * 0.7,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")
                    elif 40 <= self.clock < 50:
                        self.canevas.create_oval(i.x - size * 0.8, i.y - size * 0.8, i.x + size * 0.8,
                                                 i.y + size * 0.8,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")

                    elif 50 <= self.clock < 60:
                        self.canevas.create_oval(i.x - size * 0.9, i.y - size * 0.9, i.x + size * 0.9,
                                                 i.y + size * 0.9,
                                                 width=3,
                                                 outline="lightblue", tag="dynamique")

        # for i in mod.joueurs.keys():
        #     i = mod.joueurs[i]
        #     for k in i.flotte.keys():
        #         for m in i.flotte[k]:
        #             v = i.flotte[k][m]
        #             zone_barre = 100 / 4
        #             vie_pourcentage = (v.vie_actuelle / v.vie_max * 100) / 4
        #
        #             self.canevas.create_rectangle(v.x - zone_barre,
        #                                           v.y + 10, v.x + zone_barre,
        #                                           v.y + 13, fill="red", tag="dynamique")
        #
        #             self.canevas.create_rectangle(v.x - zone_barre,
        #                                           v.y + 10, v.x - zone_barre + vie_pourcentage * 2,
        #                                           v.y + 13, fill="green", tag="dynamique")

    def afficher_carburant(self):
        mod = self.modele
        moi = mod.joueurs[self.mon_nom]

        for j in moi.flotte.keys():
            for k in moi.flotte[j]:
                vaisseau = moi.flotte[j][k]
                zone_barre = 100 / 4
                vie_pourcentage = (vaisseau.carburant / vaisseau.carburant_max * 100) / 4

                self.canevas.create_rectangle(vaisseau.x - zone_barre,
                                              vaisseau.y + 14, vaisseau.x + zone_barre,
                                              vaisseau.y + 17, fill="red", tag="dynamique")

                self.canevas.create_rectangle(vaisseau.x - zone_barre,
                                              vaisseau.y + 14, vaisseau.x - zone_barre + vie_pourcentage * 2,
                                              vaisseau.y + 17, fill="yellow", tag="dynamique")

        for i in moi.visible:
            if isinstance(i, Orion_modele.Vaisseau):
                zone_barre = 100 / 4
                vie_pourcentage = (i.carburant / i.carburant_max * 100) / 4

                self.canevas.create_rectangle(i.x - zone_barre,
                                              i.y + 14, i.x + zone_barre,
                                              i.y + 17, fill="red", tag="dynamique")

                self.canevas.create_rectangle(i.x - zone_barre,
                                              i.y + 14, i.x - zone_barre + vie_pourcentage * 2,
                                              i.y + 17, fill="yellow", tag="dynamique")

                # print(v.carburant)

    # def calculer_ressources(self):
    #     mod = self.modele
    #
    #     for i in mod.joueurs.keys():
    #         i = mod.joueurs[i]
    #         if i.nom == self.mon_nom:
    #             for k in i.ressources.keys():
    #                 print(i.nom, k)

    def calculer_ressources(self):
        mod = self.modele

        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            if i.nom == self.mon_nom:
                self.ressources_population = i.ressources.get('population')
                self.ressources_nourriture = i.ressources.get('nourriture')
                self.ressources_or = i.ressources.get('or')
                self.ressources_argent = i.ressources.get('argent')
                self.ressources_bronze = i.ressources.get('bronze')
                self.ressources_hydrogene = i.ressources.get('hydrogene')

        if self.etoile_selectionne is not None:
            self.etoile_population.set(self.etoile_selectionne.ressources_humaines["population"])
            self.etoile_nourriture.set(self.etoile_selectionne.ressources_humaines["nourriture"])
            self.etoile_or.set(self.etoile_selectionne.ressources_extraites["or"])
            self.etoile_argent.set(self.etoile_selectionne.ressources_extraites["argent"])
            self.etoile_bronze.set(self.etoile_selectionne.ressources_extraites["bronze"])
            self.etoile_hydrogene.set(self.etoile_selectionne.ressources_extraites["hydrogene"])

    def afficher_artefacts(self):
        mod = self.modele
        i = mod.joueurs[self.mon_nom]

        for j in i.artefacts_joueur:
            self.label_artefacts.insert(END, j.nom)

    def retirer_infos_vaisseau(self):
        # self.bouton_explorer.pack_forget()
        if self.btn_manipuler:
            self.btn_manipuler.pack_forget()
        mod = self.modele
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte.keys():
                for m in i.flotte[k]:
                    v = i.flotte[k][m]
                    if v.id == self.memoire_selection:
                        # if v.type == "Explorateur":
                        if isinstance(v, Orion_modele.Explorateur):
                            for j in self.liste_action_explorer:
                                j.pack_forget()

    def exploration(self, evt):
        self.parent.exploration(self.memoire_selection)

    def afficher_ressources_extraites(self, etoile):

        self.goldstr = StringVar()
        self.argentstr = StringVar()
        self.bronzestr = StringVar()
        self.hydrostr = StringVar()
        self.popstr = StringVar()
        self.foodstr = StringVar()
        gold = etoile.ressources_extraites.get('or')
        argent = etoile.ressources_extraites.get('argent')
        bronze = etoile.ressources_extraites.get('bronze')
        hydrogene = etoile.ressources_extraites.get('hydrogene')
        population = etoile.ressources_humaines.get('population')
        nourriture = etoile.ressources_humaines.get('nourriture')

        self.cadre_ress_humaines = Frame(self.cadreoutils, width=200, height=40, bg="darkgrey")
        self.cadre_ress_humaines.pack(side=BOTTOM)
        self.label_ress_humaines = Label(self.cadre_ress_humaines, text='Ressources humaines', bg='darkgrey',
                                         font=("Arial", 16))
        self.label_ress_humaines.grid(row=0, column=0, columnspan=2)
        self.label_etoile_population = Label(self.cadre_ress_humaines, textvariable=self.etoile_population, height=3,
                                             width=6,
                                             relief=SUNKEN)
        self.label_etoile_population.grid(row=1, column=0)

        self.label_etoile_nourriture = Label(self.cadre_ress_humaines, textvariable=self.etoile_nourriture, height=3,
                                             width=6,
                                             relief=SUNKEN)
        self.label_etoile_nourriture.grid(row=1, column=1)
        self.label_pop = Label(self.cadre_ress_humaines, text='Population', bg='darkgrey')
        self.label_pop.grid(row=2, column=0)
        self.label_nourriture = Label(self.cadre_ress_humaines, text='Nourriture', bg='darkgrey')
        self.label_nourriture.grid(row=2, column=1)

        self.cadre_ress_extraites = Frame(self.cadreoutils, width=200, height=40, bg="darkgrey")
        self.cadre_ress_extraites.pack(side=BOTTOM)
        self.label_ress_extraites = Label(self.cadre_ress_extraites, text='Ressources extraites', bg='darkgrey',
                                          font=("Arial", 16))
        self.label_ress_extraites.grid(row=0, column=0, columnspan=4)

        self.label_etoile_or = Label(self.cadre_ress_extraites, textvariable=self.etoile_or, height=3, width=6,
                                     relief=SUNKEN)
        self.label_etoile_or.grid(row=1, column=0)

        self.label_etoile_argent = Label(self.cadre_ress_extraites, textvariable=self.etoile_argent, height=3, width=6,
                                         relief=SUNKEN)
        self.label_etoile_argent.grid(row=1, column=1)

        self.label_etoile_bronze = Label(self.cadre_ress_extraites, textvariable=self.etoile_bronze, height=3, width=6,
                                         relief=SUNKEN)
        self.label_etoile_bronze.grid(row=1, column=2)

        self.label_etoile_hydrogene = Label(self.cadre_ress_extraites, textvariable=self.etoile_hydrogene, height=3,
                                            width=6,
                                            relief=SUNKEN)
        self.label_etoile_hydrogene.grid(row=1, column=3)

        self.info_etoile_or = Label(self.cadre_ress_extraites, text='Or', bg='darkgrey')
        self.info_etoile_or.grid(row=2, column=0)
        self.info_etoile_argent = Label(self.cadre_ress_extraites, text='Argent', bg='darkgrey')
        self.info_etoile_argent.grid(row=2, column=1)
        self.info_etoile_bronze = Label(self.cadre_ress_extraites, text='Bronze', bg='darkgrey')
        self.info_etoile_bronze.grid(row=2, column=2)
        self.info_etoile_hydrogene = Label(self.cadre_ress_extraites, text='Hydrogene', bg='darkgrey')
        self.info_etoile_hydrogene.grid(row=2, column=3)

        self.goldstr.set(str(gold))
        self.argentstr.set(str(argent))
        self.bronzestr.set(str(bronze))
        self.hydrostr.set(str(hydrogene))
        self.popstr.set(str(population))
        self.foodstr.set(str(nourriture))

    def afficher_message(self, objet=None, message=None):
        mod = self.modele
        # mod = self.modele
        # i =
        # for i in mod.joueurs.keys():
        #     i = mod.joueurs[i]
        #     if i.nom == self.mon_nom:
        if objet.proprio == self.mon_nom:
            if isinstance(objet, Orion_modele.GenerateurDeTrouNoir):
                self.afficher_bouton_trou_noir()

            if isinstance(objet, Orion_modele.Artefact):
                textV = "Vous avez découvert l'artefact " + objet.nom + ".\n" + objet.description
                message_label = Label(self.canevas, text=textV, font=("arial", "13"), fg="white", width=1000,
                                      bg="black", image=self.images_joueur[self.mon_nom]["Interface"]["MessageBox"][1],
                                      compound=tkinter.CENTER)
                message_label.pack(side=BOTTOM, anchor=S)
                self.root.after(8000, message_label.pack_forget)

            elif message is not None:
                textV = message
                message_label = Label(self.canevas, text=textV, font=("arial", "13"), fg="white", width=500,
                                      bg="black")
                message_label.pack(side=BOTTOM, anchor=S)
                self.root.after(8000, message_label.pack_forget)

    def afficher_rechargement(self, x, y, liste):
        self.canevas.delete("recharge")
        mod = self.modele
        moi = mod.joueurs[self.mon_nom]
        for i in liste:
            if i in moi.visible:
                if i in self.parent.modele.joueurs[self.mon_nom].visible:
                    for k in mod.joueurs.keys():
                        l = mod.joueurs[k]
                        if l.nom == i.proprietaire:
                            self.canevas.create_line(x, y, i.x, i.y, fill=l.couleur, width=3, tag="recharge", dash=(10))

    def generer_images_joueur(self):
        mod = self.modele
        index = 0
        liste_position = [[0, 0], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
        for i in mod.joueurs.keys():
            j = mod.joueurs[i]

            self.images_joueur[i] = {"Vaisseaux": {"Explorateur": {1: [],
                                                                   2: [],
                                                                   3: [],
                                                                   4: []},
                                                   "Combattant": {1: [],
                                                                  2: [],
                                                                  3: [],
                                                                  4: []},
                                                   "Cargo": {1: [],
                                                             2: [],
                                                             3: [],
                                                             4: []}
                                                   },
                                     "Interface": {"MessageBox": {1: []}
                                                   }
                                     }

            couleur = j.couleur
            C1, C2, C3 = self.trouver_couleur(couleur)

            for niveau in range(0, 4):
                v_niveaux = self.generer_vaisseau_Explorateur(niveau, C1, C2, C3)
                self.images_joueur[i]["Vaisseaux"]["Explorateur"][niveau] = v_niveaux

            for niveau in range(0, 4):
                v_niveaux = self.generer_vaisseau_Combattant(niveau, C1, C2, C3)
                self.images_joueur[i]["Vaisseaux"]["Combattant"][niveau] = v_niveaux

            for niveau in range(0, 4):
                v_niveaux = self.generer_vaisseau_Cargo(niveau, C1, C2, C3)
                self.images_joueur[i]["Vaisseaux"]["Cargo"][niveau] = v_niveaux

            messageBox = self.generer_boite_dialogue(C1, C2, C3, 1000, 200)
            self.images_joueur[i]["Interface"]["MessageBox"][1] = messageBox

            index += 1

    def trouver_couleur(self, couleur):
        C1 = 0
        C2 = 0
        C3 = 0
        if couleur == "red":
            C1 = 255
            C2 = 0
            C3 = 0
        elif couleur == "blue":
            C1 = 0
            C2 = 0
            C3 = 255
        elif couleur == "lightgreen":
            C1 = 144
            C2 = 238
            C3 = 144
        elif couleur == "yellow":
            C1 = 255
            C2 = 255
            C3 = 0
        elif couleur == "lightblue":
            C1 = 173
            C2 = 216
            C3 = 230
        elif couleur == "pink":
            C1 = 255
            C2 = 0
            C3 = 255
        elif couleur == "gold":
            C1 = 255
            C2 = 215
            C3 = 0

        elif couleur == "orange":
            C1 = 255
            C2 = 165
            C3 = 0
        elif couleur == "green":
            C1 = 0
            C2 = 255
            C3 = 0
        elif couleur == "cyan":
            C1 = 0
            C2 = 255
            C3 = 255
        elif couleur == "SeaGreen1":
            C1 = 84
            C2 = 255
            C3 = 159
        elif couleur == "turquoise1":
            C1 = 0
            C2 = 245
            C3 = 255
        elif couleur == "firebrick1":
            C1 = 255
            C2 = 48
            C3 = 48
        else:
            C1 = 128
            C2 = 0
            C3 = 128

        return [C1, C2, C3]

    def generer_vaisseau_Explorateur(self, niveau, C1, C2, C3):
        size = 0.08

        hauteur = math.floor(400 * size)
        largeur = math.floor(400 * size)
        img = Image.new('RGBA', (largeur, hauteur), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, 'RGBA')

        L1 = 255

        S1 = 0
        S2 = 255
        S3 = 255
        SO = 155

        L1 = 255

        if niveau >= 3:
            draw.polygon([(200 * size, 5), (200 * size, 200 * size), (390 * size, 390 * size)],
                         (C1 - 100, C2 - 100, C3 - 100, 255))
            draw.polygon([(200 * size, 200 * size), (200 * size, 5), (5, 390 * size)],
                         (C1 - 100, C2 - 100, C3 - 100, 255))

        if niveau >= 2:
            draw.ellipse((145 * size, 0, 255 * size, 295 * size), (0, 0, 0, L1))
            draw.ellipse((140 * size, 0, 260 * size, 290 * size), (S1, S2, S3, SO))
            draw.ellipse((140 * size, 0, 260 * size, 290 * size), (S1, S2, S3, SO))
            draw.ellipse((150 * size, 5, 250 * size, 300 * size), (C1 - 150, C2 - 150, C3 - 150, 255))

        if niveau >= 1:
            draw.polygon([(205 * size, 0), (200 * size, 135 * size), (390 * size, 390 * size)], (0, 0, 0, L1))
            draw.polygon([(200 * size, 135 * size), (195 * size, 0), (5, 390 * size)], (0, 0, 0, L1))

            draw.polygon([(210 * size, 0), (200 * size, 145 * size), (390 * size, 390 * size)],
                         (S1 + 50, S2 + 50, S3 + 50, SO))
            draw.polygon([(200 * size, 145 * size), (190 * size, 0), (5, 390 * size)], (S1, S2, S3, SO))
            draw.polygon([(210 * size, 0), (200 * size, 145 * size), (390 * size, 390 * size)],
                         (S1 + 50, S2 + 50, S3 + 50, SO))
            draw.polygon([(200 * size, 145 * size), (190 * size, 0), (5, 390 * size)], (S1, S2, S3, SO))

            draw.polygon([(200 * size, 5), (200 * size, 100 * size), (390 * size, 390 * size)], (C1, C2, C3, 255))
            draw.polygon([(200 * size, 100 * size), (200 * size, 5), (5, 390 * size)], (C1, C2, C3, 255))

        draw.ellipse((170 * size, 50 * size, 230 * size, 305 * size), (0, 0, 0, L1))
        draw.ellipse((165 * size, 50 * size, 235 * size, 310 * size), (S1, S2, S3, SO))
        draw.ellipse((165 * size, 50 * size, 235 * size, 310 * size), (S1, S2, S3, SO))
        draw.ellipse((175 * size, 50 * size, 225 * size, 300 * size), (C1 + 55, C2 + 55, C3 + 55, 255))
        draw.ellipse((185 * size, 50 * size, 215 * size, 100 * size), ("lightgrey"))

        out_0 = img.rotate(270)
        images = [ImageTk.PhotoImage(out_0)]
        angle = -9
        for i in range(0, 39):
            result = out_0.rotate(angle, resample=Image.BICUBIC)
            out_1 = ImageTk.PhotoImage(result)
            images.append(out_1)
            angle -= 9
        return images

    def generer_vaisseau_Combattant(self, niveau, C1, C2, C3):

        size = 0.08

        largeur = math.floor(400 * size)
        hauteur = math.floor(400 * size)
        img = Image.new('RGBA', (largeur, hauteur), (0, 0, 0, 0))
        draw = ImageDraw.ImageDraw(img)
        draw.RoundrectPIL = rounded_rectanglePIL

        L1 = 255

        S1 = 0
        S2 = 255
        S3 = 255
        SO = 155

        L1 = 255

        # Charpente
        if niveau >= 2:
            draw.RoundrectPIL(draw, (190 * size, 50 * size, 210 * size, 110 * size), fill=(100, 100, 100, 255),
                              outline="black", width=math.floor(3 * size), radius=math.floor(10 * size))

            draw.polygon([(105 * size, 45 * size), (180 * size, 300 * size), (220 * size, 300 * size),
                          (295 * size, 45 * size), (200 * size, 75 * size)], fill=(C1 - 150, C2 - 150, C3 - 150, 255),
                         outline="black")

        if niveau >= 1:
            draw.polygon([(125 * size, 45 * size), (180 * size, 300 * size), (220 * size, 300 * size),
                          (275 * size, 45 * size), (200 * size, 75 * size)], fill=(C1 - 100, C2 - 100, C3 - 100, 255),
                         outline="black")
        draw.polygon(
            [(145 * size, 45 * size), (180 * size, 300 * size), (220 * size, 300 * size), (255 * size, 45 * size),
             (200 * size, 75 * size)], fill=(C1 + 50, C2 + 50, C3 + 50, 255),
            outline=(C1 - 150, C2 - 150, C3 - 150, 255))

        # Aile gauche

        # #Aile gauche
        if niveau >= 1:
            draw.RoundrectPIL(draw, (275 * size, 100 * size, 295 * size, 200 * size),
                              fill=(100, 100, 100, 255), outline="black", width=math.floor(3 * size),
                              radius=math.floor(10 * size))

        if niveau >= 3:
            draw.RoundrectPIL(draw, (360 * size, 0 * size, 375 * size, 250 * size), fill=(100, 100, 100, 255),
                              outline="black", width=math.floor(3 * size), radius=math.floor(10 * size))
            draw.RoundrectPIL(draw, (335 * size, 55 * size, 400 * size, 195 * size),
                              fill=(C1 - 25, C2 - 25, C3 - 25, 255),
                              outline=(C1 - 150, C2 - 150, C3 - 150, 255),
                              width=math.floor(6 * size), radius=math.floor(20 * size))
            draw.polygon([(305 * size, 45 * size), (305 * size, 135 * size), (335 * size, 175 * size),
                          (335 * size, 75 * size)], fill=(30, 30, 30, 255), outline="black")

        if niveau >= 1:
            draw.RoundrectPIL(draw, (265 * size, 25 * size, 305 * size, 155 * size),
                              fill=(C1 - 25, C2 - 25, C3 - 25, 255),
                              outline=(C1 - 150, C2 - 150, C3 - 150, 255),
                              width=math.floor(6 * size), radius=math.floor(20 * size))
            draw.RoundrectPIL(draw, (265 * size, 25 * size, 305 * size, 155 * size),
                              fill=(C1 - 25, C2 - 25, C3 - 25, 255),
                              outline=(C1 - 150, C2 - 150, C3 - 150, 255),
                              width=math.floor(6 * size), radius=math.floor(20 * size))

        # #AileDroite
        if niveau >= 1:
            draw.RoundrectPIL(draw, (105 * size, 100 * size, 125 * size, 200 * size),
                              fill=(100, 100, 100, 255), outline="black", width=math.floor(3 * size),
                              radius=math.floor(10 * size))

        if niveau >= 3:
            draw.RoundrectPIL(draw, (25 * size, 0 * size, 40 * size, 250 * size), fill=(100, 100, 100, 255),
                              outline="black",
                              width=math.floor(3 * size), radius=math.floor(10 * size))
            draw.RoundrectPIL(draw, (0 * size, 55 * size, 65 * size, 195 * size), fill=(C1 - 25, C2 - 25, C3 - 25, 255),
                              outline=(C1 - 150, C2 - 150, C3 - 150, 255), width=math.floor(6 * size),
                              radius=math.floor(20 * size))
            draw.polygon(
                [(65 * size, 75 * size), (65 * size, 175 * size), (95 * size, 135 * size), (95 * size, 45 * size)],
                fill=(30, 30, 30, 255), outline="black")

        if niveau >= 1:
            draw.RoundrectPIL(draw, (95 * size, 25 * size, 135 * size, 155 * size),
                              fill=(C1 - 25, C2 - 25, C3 - 25, 255),
                              outline=(C1 - 150, C2 - 150, C3 - 150, 255),
                              width=math.floor(6 * size), radius=math.floor(20 * size))

        # #
        draw.polygon([(170 * size, 280 * size), (200 * size, 400 * size), (230 * size, 280 * size)],
                     fill=(30, 30, 30, 255),
                     outline="black")
        draw.RoundrectPIL(draw, (180 * size, 70 * size, 220 * size, 310 * size),
                          fill=(C1 - 100, C2 - 100, C3 - 100, 255),
                          outline="black", width=math.floor(3 * size), radius=math.floor(20 * size))
        draw.RoundrectPIL(draw, (195 * size, 275 * size, 205 * size, 400 * size), fill=(100, 100, 100, 255),
                          outline="black",
                          width=math.floor(3 * size), radius=math.floor(10 * size))

        out_0 = img.rotate(90)
        images = [ImageTk.PhotoImage(out_0)]
        angle = -9
        for i in range(0, 39):
            result = out_0.rotate(angle, resample=Image.BICUBIC, expand=True)
            out_1 = ImageTk.PhotoImage(result)
            images.append(out_1)
            angle -= 9
        return images

    def generer_vaisseau_Cargo(self, niveau, C1, C2, C3):

        size = 0.08
        size2 = size * 0.96


        largeur = math.floor(400 * size)
        hauteur = math.floor(400 * size)
        img = Image.new('RGBA', (largeur, hauteur), (0, 0, 0, 0))
        draw = ImageDraw.ImageDraw(img)
        draw.RoundrectPIL = rounded_rectanglePIL

        L1 = 255

        S1 = 0
        S2 = 255
        S3 = 255
        SO = 155

        L1 = 255

        draw.polygon(
            [(0 * size, 175 * size), (0 * size, 150 * size), (150 * size, 100 * size), (250 * size, 100 * size),
             (400 * size, 150 * size), (400 * size, 175 * size), (250 * size, 225 * size),
             (150 * size, 225 * size)], fill=(0, 0, 0, 255))

        draw.polygon(
            [(0 * size, 175 * size), (0 * size, 150 * size), (150 * size, 100 * size), (250 * size, 100 * size),
             (400 * size, 150 * size), (400 * size, 175 * size), (250 * size, 225 * size),
             (150 * size, 225 * size)], fill=(0, 0, 0, 255))

        draw.polygon(
            [(0 * size, 350 * size), (0 * size, 325 * size), (175 * size, 320 * size), (225 * size, 320 * size),
             (400 * size, 325 * size), (400 * size, 350 * size), (225 * size, 375 * size),
             (175 * size, 375 * size)], fill=(0, 0, 0, 255))

        draw.RoundrectPIL(draw,(60 * size, 120 * size, 340 * size, 210 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(185 * size, 0 * size, 215 * size, 400 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(175 * size, 0 * size, 225 * size, 210 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(175 * size, 300 * size, 225 * size, 400 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(150 * size, 75 * size, 250 * size, 210 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(20 * size, 100 * size, 35 * size, 390 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(10 * size, 100 * size, 45 * size, 210 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(10 * size, 275 * size, 45 * size, 375 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(365 * size, 100 * size, 380 * size, 390 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(355 * size, 100 * size, 390 * size, 210 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(355 * size, 275 * size, 390 * size, 375 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))

        # In

        draw.polygon(
            [(0 * size, 175 * size), (0 * size, 150 * size), (150 * size, 100 * size), (250 * size, 100 * size),
             (400 * size, 150 * size), (400 * size, 175 * size), (250 * size, 225 * size),
             (150 * size, 225 * size)], fill=(C1 - 175, C2 - 175, C3 - 175, 255))

        draw.polygon(
            [(0 * size, 350 * size), (0 * size, 325 * size), (175 * size, 320 * size), (225 * size, 320 * size),
             (400 * size, 325 * size), (400 * size, 350 * size), (225 * size, 375 * size),
             (175 * size, 375 * size)], fill=(C1 - 175, C2 - 175, C3 - 175, 255))

        draw.RoundrectPIL(draw,(60 + 3 * size, 120 + 3 * size, 340 - 3 * size, 210 - 3 * size),
                               fill=(C1 - 75, C2 - 75, C3 - 75, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(185 + 3 * size, 0 + 3 * size, 215 - 3 * size, 400 - 3 * size),
                               fill=(C1 - 100, C2 - 100, C3 - 100, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(175 + 3 * size, 0 + 3 * size, 225 - 3 * size, 210 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(175 + 10 * size, 0 + 10 * size, 225 - 10 * size, 210 - 10 * size),
                               fill=(50, 50, 255, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(175 + 3 * size, 300 + 3 * size, 225 - 3 * size, 400 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(150 + 3 * size, 75 + 3 * size, 250 - 3 * size, 210 - 3 * size),
                               fill=(C1 - 50, C2 - 50, C3 - 50, 255),
                               radius=math.floor(10 * size))

        draw.ellipse((150 * size, 100, 250 * size, 200 * size), (C1 - 150, C2 - 150, C3 - 150, 255))
        draw.ellipse((155 * size, 105, 245 * size, 195 * size), (C1 - 100, C2 - 100, C3 - 100, 255))
        draw.ellipse((160 * size, 110, 240 * size, 190 * size), (C1 - 50, C2 - 50, C3 - 50, 255))

        draw.RoundrectPIL(draw,(10 * size, 150 * size, 390 * size, 160 * size), fill=(0, 0, 0, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(15 * size, 152 * size, 385 * size, 154 * size), fill=(50, 50, 50, 255),
                               radius=math.floor(10 * size))

        draw.ellipse((195 * size, 145, 205 * size, 165 * size), (C1 - 150, C2 - 150, C3 - 150, 255))

        draw.RoundrectPIL(draw,(20 + 3 * size, 100 + 3 * size, 35 - 3 * size, 390 - 3 * size),
                               fill=(C1 - 100, C2 - 100, C3 - 100, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(10 + 3 * size, 100 + 3 * size, 45 - 3 * size, 210 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))
        draw.RoundrectPIL(draw,(10 + 3 * size, 275 + 3 * size, 45 - 3 * size, 375 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(365 + 3 * size, 100 + 3 * size, 380 - 3 * size, 390 - 3 * size),
                               fill=(C1 - 100, C2 - 100, C3 - 100, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(355 + 3 * size, 100 + 3 * size, 390 - 3 * size, 210 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))

        draw.RoundrectPIL(draw,(355 + 3 * size, 275 + 3 * size, 390 - 3 * size, 375 - 3 * size),
                               fill=(100, 100, 100, 255),
                               radius=math.floor(10 * size))

        out_0 = img.rotate(270)
        images = [ImageTk.PhotoImage(out_0)]
        angle = -9
        for i in range(0, 39):
            result = out_0.rotate(angle, resample=Image.BICUBIC, expand=True)
            out_1 = ImageTk.PhotoImage(result)
            images.append(out_1)
            angle -= 9
        return images

    def generer_boite_dialogue(self, C1, C2, C3, hauteur, largeur):
        size = 1
        img = Image.new("RGBA", (hauteur, largeur))
        draw = ImageDraw.ImageDraw(img)
        draw.RoundrectPIL = rounded_rectanglePIL

        opacity = 255

        draw.RoundrectPIL(draw, (0 * size, 0 * size, hauteur, largeur * size),
                          fill=(C1, C2, C3, 100), outline="black", width=math.floor(3 * size),
                          radius=math.floor(10 * size))
        x = 0
        y = 0
        # Case
        for i in range(4):
            draw.RoundrectPIL(draw,
                              ((0 + 5 + x) * size, (0 + 5 + x) * size, (hauteur - 5 - x) * size,
                               (largeur - 5 - x) * size),
                              fill=(C1 + y, C2 + y, C3 + y, 100), outline="black",
                              width=math.floor(3 * size),
                              radius=math.floor(10 * size))
            x += 4
            y += 25
            opacity -= 25

        out_0 = img
        images = [ImageTk.PhotoImage(out_0)]

        return images

    def generer_images_univers(self):
        pass

    def generer_images_interface(self):
        pass

    def afficher_bouton_trou_noir(self):
        self.btn_trou_noir.pack()

    def bouton_trou_noir(self, evt):
        self.btn_trou_noir_actif = True


def rounded_rectanglePIL(self, xy, radius=0, fill=None, outline=None, width=1):
    if isinstance(xy[0], (list, tuple)):
        (x0, y0), (x1, y1) = xy
    else:
        x0, y0, x1, y1 = xy
    d = radius * 2
    full_x = d >= x1 - x0
    if full_x:
        d = x1 - x0
    full_y = d >= y1 - y0
    if full_y:
        d = y1 - y0
    if full_x and full_y:
        return self.ellipse(xy, fill, outline, width)
    if d == 0:
        return self.rectangle(xy, fill, outline, width)
    r = d // 2
    ink, fill = self._getink(outline, fill)

    def draw_corners(pieslice):
        if full_x:
            parts = (((x0, y0, x0 + d, y0 + d), 180, 360), ((x0, y1 - d, x0 + d, y1), 0, 180))
        elif full_y:
            # Draw left and right halves
            parts = (
                ((x0, y0, x0 + d, y0 + d), 90, 270),
                ((x1 - d, y0, x1, y0 + d), 270, 90),
            )
        else:
            # Draw four separate corners
            parts = (
                ((x1 - d, y0, x1, y0 + d), 270, 360),
                ((x1 - d, y1 - d, x1, y1), 0, 90),
                ((x0, y1 - d, x0 + d, y1), 90, 180),
                ((x0, y0, x0 + d, y0 + d), 180, 270),
            )
        for part in parts:
            if pieslice:
                self.draw.draw_pieslice(*(part + (fill, 1)))
            else:
                self.draw.draw_arc(*(part + (ink, width)))

    if fill is not None:
        draw_corners(True)

        if full_x:
            self.draw.draw_rectangle((x0, y0 + r + 1, x1, y1 - r - 1), fill, 1)
        else:
            self.draw.draw_rectangle((x0 + r + 1, y0, x1 - r - 1, y1), fill, 1)
        if not full_x and not full_y:
            self.draw.draw_rectangle((x0, y0 + r + 1, x0 + r, y1 - r - 1), fill, 1)
            self.draw.draw_rectangle((x1 - r, y0 + r + 1, x1, y1 - r - 1), fill, 1)
    if ink is not None and ink != fill and width != 0:
        draw_corners(False)

        if not full_x:
            self.draw.draw_rectangle(
                (x0 + r + 1, y0, x1 - r - 1, y0 + width - 1), ink, 1
            )
            self.draw.draw_rectangle(
                (x0 + r + 1, y1 - width + 1, x1 - r - 1, y1), ink, 1
            )
        if not full_y:
            self.draw.draw_rectangle(
                (x0, y0 + r + 1, x0 + width - 1, y1 - r - 1), ink, 1
            )
            self.draw.draw_rectangle(
                (x1 - width + 1, y0 + r + 1, x1, y1 - r - 1), ink, 1
            )
