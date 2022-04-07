# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *

from Pillow import *
from PIL import ImageTk, Image

from helper import Helper as hlp, Helper
import math

import random


class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + mon_nom)
        self.mon_nom = mon_nom
        # attributs
        self.lebon = 0
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None
        self.cadre_actif = None
        self.nombre_joueur = 0
        self.angle = [270,225,180,135,90,0,360,315,270]
        self.id_vaisseau1 = []
        self.id_vaisseau2 = []
        self.id_vaisseau3 = []
        self.id_vaisseau4 = []
        self.id_vaisseau5 = []
        self.id_vaisseau6 = []
        self.id_vaisseau7 = []
        self.id_vaisseau8 = []
        self.vaisseau1 = {}
        self.vaisseau2 = {}
        self.vaisseau3 = {}
        self.vaisseau4 = {}
        self.vaisseau5 = {}
        self.vaisseau6 = {}
        self.vaisseau7 = {}
        self.vaisseau8 = {}
        self.scout1 = {}
        self.scout2 = {}
        self.scout3 = {}
        self.scout4 = {}
        self.scout5 = {}
        self.scout6 = {}
        self.scout7 = {}
        self.scout8 = {}

        self.vaisseau_actif = {"type": None, "vie": None, "attaque": None, "energie": None, "nb_capsules": None,
                               "ressource": None}

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
        self.joueur_actif = None

    def creercouleurVaisseau(self):
        mod = self.modele
        for i in mod.joueurs.keys():
            compteur = 0
            self.nombre_joueur += 1
            i = mod.joueurs[i]

            if self.nombre_joueur == 1:
                for h in self.angle:
                    self.vaisseau1[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout1[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau1.append(i.id)
                compteur = 0

            if self.nombre_joueur == 2:
                for h in self.angle:
                    self.vaisseau2[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout2[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau2.append(i.id)

            if self.nombre_joueur == 3:
                for h in self.angle:
                    self.vaisseau3[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout3[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau3.append(i.id)

            if self.nombre_joueur == 4:
                for h in self.angle:
                    self.vaisseau4[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout4[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau4.append(i.id)
            if self.nombre_joueur == 5:
                for h in self.angle:
                    self.vaisseau5[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout5[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau5.append(i.id)

            if self.nombre_joueur == 6:
                for h in self.angle:
                    self.vaisseau6[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout6[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau6.append(i.id)

            if self.nombre_joueur == 7:
                for h in self.angle:
                    self.vaisseau7[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout7[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau7.append(i.id)

            if self.nombre_joueur == 8:
                for h in self.angle:
                    self.vaisseau8[compteur] = VaisseauGuerre(i.couleur, h)
                    self.scout8[compteur] = VaisseauScout(i.couleur, h)
                    compteur += 1
                self.id_vaisseau8.append(i.id)
        pass

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
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="pink")
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
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.joueur_actif = self.modele.joueurs[self.mon_nom]
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

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
        return self.cadrepartie

    def ouvrir_civilisation(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def ouvrir_marche(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def ouvrir_senat(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def ouvrir_techtree(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def ouvrir_log(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def ouvrir_xy(self):
        nouvelle_fenetre = Toplevel(self.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)

    def creer_cadre_outils(self):
        # --- Cadre qui tient tout ---#
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="grey")
        self.cadreoutils.pack(side=LEFT, fill=Y)

        # --- Cadre qui tient les informations ---#
        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="grey")
        self.cadreinfo.pack(fill=BOTH)

        # --- information joueur---#
        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="grey")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()

        # --- Creation vaisseaux ---#
        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30")
        self.btncreervaisseau = Button(self.cadreinfochoix, text="Vaisseau")
        self.btncreervaisseau.bind("<Button>", self.creer_vaisseau)
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)
        self.btncreerScout = Button(self.cadreinfochoix, text="Scout")
        self.btncreerScout.bind("<Button>", self.creer_vaisseau)
        self.btncreerSpaceFighter = Button(self.cadreinfochoix, text="Spacefighter")
        self.btncreerSpaceFighter.bind("<Button>", self.creer_vaisseau)
        self.btncreerColonisateur = Button(self.cadreinfochoix, text="Colonisateur")
        self.btncreerColonisateur.bind("<Button>", self.creer_vaisseau)
        self.btncreerDestroyer = Button(self.cadreinfochoix, text="Destroyer")
        self.btncreerDestroyer.bind("<Button>", self.creer_vaisseau)

        self.btncreervaisseau.pack()
        self.btncreercargo.pack()
        self.btncreerColonisateur.pack()
        self.btncreerScout.pack()
        self.btncreerDestroyer.pack()
        self.btncreerSpaceFighter.pack()

        # --- frame info clic---#
        self.cadreinfoclic = Frame(self.cadreoutils, bg="grey")
        self.cadreinfoclic.pack(expand=True, fill=BOTH)

        # --- Frame Etoile ---#
        self.cadre_etoile_mere = Frame(self.cadreinfoclic, bg="white")
        self.id_etoile = Label(self.cadre_etoile_mere, text="Identifiant: ")
        self.hp_etoile = Label(self.cadre_etoile_mere, text="Vie: ")
        self.habitable_etoile = Label(self.cadre_etoile_mere, text="Habitable: ")
        self.population = Label(self.cadre_etoile_mere, text="Population: ")
        self.figure_important = Label(self.cadre_etoile_mere, text="Figures d'importance")
        self.ressources_etoile = Label(self.cadre_etoile_mere, text="Ressources: ")

        self.id_etoile.pack()
        self.hp_etoile.pack()
        self.habitable_etoile.pack()
        self.population.pack()
        self.figure_important.pack()
        self.ressources_etoile.pack()
        # --- Frame Vaisseau ---#
        self.cadre_vaisseau = Frame(self.cadreinfoclic, bg="white")
        self.type_vaisseau = Label(self.cadre_vaisseau, text=self.vaisseau_actif["type"])
        self.vie = Label(self.cadre_vaisseau, text=self.vaisseau_actif["vie"])
        self.attaque = Label(self.cadre_vaisseau, text=self.vaisseau_actif["attaque"])
        self.energie = Label(self.cadre_vaisseau, text=self.vaisseau_actif["energie"])
        self.nb_capsules = Label(self.cadre_vaisseau, text=self.vaisseau_actif["nb_capsules"])
        self.ressources_vaisseau = Label(self.cadre_vaisseau, text="ressources")

        self.type_vaisseau.pack()
        self.vie.pack()
        self.attaque.pack()
        self.energie.pack()
        self.nb_capsules.pack()
        self.ressources_vaisseau.pack()

        # --- Cadre information flotte (haut) ---#
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
                                      bg="black")
        self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=BOTTOM)

        # ---- HUD ----#
        self.cadrehud = Frame(self.cadrepartie, width=200, height=45, bg="black")
        # --- RESSOURCES ---#
        self.label_moral = Label(self.cadrehud, text="moral : 0 ")
        self.label_moral.grid(row=0, column=0, sticky=W, ipadx=20, ipady=10, pady=5, padx=5)
        self.label_diplomatie = Label(self.cadrehud, text="diplomatie : 0")
        self.label_diplomatie.grid(row=0, column=5, sticky=W, ipadx=10, ipady=10, pady=5, padx=5)
        self.label_nourriture = Label(self.cadrehud, text="nourriture : 0")
        self.label_nourriture.grid(row=0, column=10, sticky=W, ipadx=10, ipady=10, pady=5, padx=5)
        self.label_energie = Label(self.cadrehud, text="energie : 0")
        self.label_energie.grid(row=0, column=15, sticky=W, ipadx=17, ipady=10, pady=5, padx=5)
        self.label_militaire = Label(self.cadrehud, text="militaire : 0")
        self.label_militaire.grid(row=0, column=20, sticky=W, ipadx=11, ipady=10, pady=5, padx=5)
        self.label_science = Label(self.cadrehud, text="science : 0")
        self.label_science.grid(row=0, column=25, sticky=W, ipadx=19, ipady=10, pady=5, padx=5)
        self.label_eau = Label(self.cadrehud, text="eau : 0")
        self.label_eau.grid(row=1, column=0, sticky=W, ipadx=25, ipady=10, pady=5, padx=5)
        self.label_fer = Label(self.cadrehud, text="fer : 0")
        self.label_fer.grid(row=1, column=5, sticky=W, ipadx=28, ipady=10, pady=5, padx=5)
        self.label_titanium = Label(self.cadrehud, text="titanium : 0")
        self.label_titanium.grid(row=1, column=10, sticky=W, ipadx=16, ipady=10, pady=5, padx=5)
        self.label_cuivre = Label(self.cadrehud, text="cuivre : 0")
        self.label_cuivre.grid(row=1, column=15, sticky=W, ipadx=22, ipady=10, pady=5, padx=5)
        self.label_credits = Label(self.cadrehud, text="credits : 0")
        self.label_credits.grid(row=1, column=20, sticky=W, ipadx=14, ipady=10, pady=5, padx=5)
        self.bouton_aide = Button(self.cadrehud, text="aide")
        self.bouton_aide.grid(row=1, column=25, sticky=W, ipadx=33, ipady=8, pady=8, padx=5)

        #--- annonce ---#
        self.label_annonces = Label(self.cadrehud, text="Annonces du jour")
        self.label_annonces.grid(row=0,rowspan=3, column=35, columnspan=70, sticky=W, ipadx=200, ipady=25, pady=5, padx=5)

        # ---- BOUTONS  TEST ----#
        self.btncivilisations = Button(self.cadrehud, text="civilisations", command=self.ouvrir_civilisation)
        self.btncivilisations.grid(row=0, rowspan=5, column=105, sticky=W, ipadx=10, ipady=30, padx=5)
        self.btnmarche = Button(self.cadrehud, text="marche", command=self.ouvrir_marche)
        self.btnmarche.grid(row=0, rowspan=5, column=110, sticky=W, ipadx=18, ipady=30, padx=5)
        self.btnsenat = Button(self.cadrehud, text="senat", command=self.ouvrir_senat)
        self.btnsenat.grid(row=0, rowspan=5, column=120, sticky=W, ipadx=18, ipady=30, padx=5)
        self.btntechtree = Button(self.cadrehud, text="techtree", command=self.ouvrir_techtree)
        self.btntechtree.grid(row=0, rowspan=5, column=130, sticky=W, ipadx=10, ipady=30, padx=5)
        self.btnlog = Button(self.cadrehud, text="log", command=self.ouvrir_log)
        self.btnlog.grid(row=0, rowspan=5, column=140, sticky=W, ipadx=20, ipady=30, padx=5)
        self.btnxy = Button(self.cadrehud, text="x,y", command=self.ouvrir_xy)
        self.btnxy.grid(row=0, rowspan=5, column=150, sticky=W, ipadx=18, ipady=30, padx=5)

        self.cadrehud.pack(side=TOP, fill=BOTH)

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def creer_label_figure(self):
        self.valeur_label = None

        colonne = 0

        for i in range(8):
            lb_figure = Label(self.cadreinfo, text=self.valeur_label)
            lb_figure.grid(row=1, column=colonne)

        self.label_moral.config(text=("Moral : " + str(self.joueur_actif.moral)))

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    def centrer_liste_objet(self, evt):
        info = self.info_liste.get(self.info_liste.curselection())
        print(info)
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
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoiles_controlees:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=mod.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id), "Etoile"))
                # on affiche dans minimap
                minix = j.x / self.modele.largeur * self.taille_minimap
                miniy = j.y / self.modele.hauteur * self.taille_minimap
                self.canevas_minimap.create_oval(minix, miniy, minix + 3, miniy + 3,
                                                 fill=mod.joueurs[i].couleur,
                                                 tags=(j.proprietaire, str(j.id), "Etoile"))

    def afficher_mini(self, evt):  # univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.taille_minimap
            miniy = j.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 2, miniy + 2,
                                                  fill=j.couleur,
                                                  tags=("mini", "Etoile"))
        # # affichage des etoiles possedees par les joueurs
        for i in evt.joueurs.keys():
            for j in evt.joueurs[i].etoiles_controlees:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=evt.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id), "Etoile"))

    def centrer_planemetemere(self, evt):
        self.centrer_objet(self.modele.joueurs[self.mon_nom].etoile_mere)

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

    # change l'appartenance d'une planète et donc les propriétés des dessins les représentants
    # def afficher_planete(self, joueur, cible):
    #     joueur1 = self.modele.joueurs[joueur]
    #     id = cible.id
    #     couleur = joueur1.couleur
    #     self.canevas.itemconfig(id, fill=couleur)
    #     self.canevas.itemconfig(id, tags=(joueur, id, "Planete",))

    # ajuster la liste des vaisseaux
    def lister_objet(self, obj, id):
        self.info_liste.insert(END, obj + "; " + id)

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau)
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("marqueur")

        if self.ma_selection != None:
            joueur = mod.joueurs[self.ma_selection[0]]
            # if self.ma_selection[2] == "Planete":
            #     for i in joueur.planetes_conquises:
            #         if i.id == self.ma_selection[1]:
            #             x = i.x
            #             y = i.y
            #             t = 10 * self.zoom
            #             self.canevas.create_rectangle(x - t, y - t, x + t, y + t,
            #                                           dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
            #                                           tags=("multiselection", "marqueur"))
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoiles_controlees:
                    if i.id == self.ma_selection[1]:
                        x = i.x
                        y = i.y
                        t = 10 * self.zoom
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
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            vaisseau_local = []
            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    salut = 0
                    if j.angle_cible < 0:
                        angle = 360 + (j.angle_cible * 57.2957795)
                    else:
                        angle = j.angle_cible * 57.2957795
                    salut = round(angle/45)

                    if k == "Vaisseau":
                        if i.id in self.id_vaisseau1:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau1[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau2:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau2[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau3:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau3[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau4:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau4[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau5:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau5[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau6:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau6[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau7:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau7[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau8:
                            self.canevas.create_image(j.x, j.y, image=self.vaisseau8[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Destroyer":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill="pink",
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Scout":
                        if i.id in self.id_vaisseau1:
                            self.canevas.create_image(j.x, j.y, image=self.scout1[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau2:
                            self.canevas.create_image(j.x, j.y, image=self.scout2[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau3:
                            self.canevas.create_image(j.x, j.y, image=self.scout3[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau4:
                            self.canevas.create_image(j.x, j.y, image=self.scout4[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau5:
                            self.canevas.create_image(j.x, j.y, image=self.scout5[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau6:
                            self.canevas.create_image(j.x, j.y, image=self.scout6[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau7:
                            self.canevas.create_image(j.x, j.y, image=self.scout7[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.id_vaisseau8:
                            self.canevas.create_image(j.x, j.y, image=self.scout8[salut],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Colonisateur":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill="blue",
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Spacefighter":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill="yellow",
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Cargo":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j, tailleF, i, k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))
        # --affichage ressources hud--#
        self.label_moral.config(text=("Moral : " + str(self.joueur_actif.moral)))
        self.label_diplomatie.config(text=("Diplomatie : " + str(self.joueur_actif.diplomatie)))
        self.label_nourriture.config(text=("Nourriture : " + str(self.joueur_actif.nourriture.quantite)))
        self.label_energie.config(text=("Energie : " + str(self.joueur_actif.energie.quantite)))
        self.label_militaire.config(text=("Militaire : " + str(self.joueur_actif.militaire)))
        self.label_science.config(text=("Science : " + str(self.joueur_actif.science)))
        self.label_eau.config(text=("Eau : " + str(self.joueur_actif.eau.quantite)))
        self.label_fer.config(text=("Fer : " + str(self.joueur_actif.fer.quantite)))
        self.label_titanium.config(text=("Titanium : " + str(self.joueur_actif.titanium.quantite)))
        self.label_cuivre.config(text=("Cuivre : " + str(self.joueur_actif.cuivre.quantite)))
        self.label_credits.config(text=("Credits : " + str(self.joueur_actif.credits)))

    def dessiner_cargo(self, obj, tailleF, joueur, type_obj):
        t = obj.taille * self.zoom
        a = obj.ang
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="yellow",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    def dessiner_cargo1(self, j, tailleF, i, k):
        self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                                 (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                 tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

    def cliquer_cosmos(self, evt):
        t = self.canevas.gettags(CURRENT)
        if t:  # il y a des tags
            if t[0] == self.mon_nom:  # et
                if self.ma_selection:
                    self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                self.ma_selection = [self.mon_nom, t[1], t[2]]
                if t[2] == "Etoile":
                    self.update_etoile_actif(t[1])
                    self.montrer_etoile_selection()
                    self.cadre_vaisseau.pack_forget()
                elif t[2] == "Flotte":
                    self.update_vaisseau_actif(t[1], t[3])
                    self.montrer_flotte_selection()
                    self.cadre_etoile_mere.pack_forget()

            if ("Etoile" in t or "Porte_de_ver" in t) and t[0] != self.mon_nom:
                if self.ma_selection:
                    self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                self.ma_selection = None
                self.canevas.delete("marqueur")
        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.ma_selection = None
            self.canevas.delete("marqueur")
            self.cadre_vaisseau.pack_forget()
            self.cadre_etoile_mere.pack_forget()

    def montrer_etoile_selection(self):
        self.cadreinfochoix.pack(fill=BOTH)
        self.cadre_etoile_mere.pack(expand=True, fill=BOTH)

    def montrer_flotte_selection(self):
        print("À IMPLANTER - FLOTTE de ", self.mon_nom)
        self.cadre_vaisseau.pack(expand=True, fill=BOTH)

    def update_vaisseau_actif(self, id, type_vaisseau):
        vaisseau = self.joueur_actif.flotte[type_vaisseau][id]
        self.type_vaisseau.config(text=("Type : " + str(vaisseau.type)))
        self.vie.config(text=("Points de vie : " + str(vaisseau.hp)))
        self.attaque.config(text=("Attaque : " + str(vaisseau.attaque)))
        self.energie.config(text=("Energie : " + str(vaisseau.energie)))
        self.nb_capsules.config(text=("Capsules : " + str(len(vaisseau.capsules))))

    # self.vaisseau_actif["ressources"] = vaisseau.ressources

    def update_etoile_actif(self,id):
        #il faut implementer la verification de si on possede la capsule pour voir les ressources
        ressources_temp = ""
        try:
            if id in self.joueur_actif.capsules_ouvertes:
                etoile = self.joueur_actif.capsules_ouvertes[id]
            elif id == self.joueur_actif.etoile_mere.id:
                etoile = self.joueur_actif.etoile_mere
            self.id_etoile.config(text=("Identifiant: " + str(etoile.id)))
            self.hp_etoile.config(text=("Points de vie : " + str(etoile.hp)))
            self.habitable_etoile.config(text=("Habitable: " + str(etoile.habitable)))
            self.population.config(text=("Population : " + str(etoile.population)))
            for ressource in etoile.ressources:
                temp = ressource.nom + ": " + str(ressource.quantite) + " \n"
                ressources_temp += temp
            # self.figure_important.config(text=("Figure Importante : " + str(vaisseau.energie)))
            self.ressources_etoile.config(text=("Ressoures : " + ressources_temp))
        except:
            self.id_etoile.config(text=("Identifiant: " + "?????"))
            self.hp_etoile.config(text=("Points de vie : " + "?????"))
            self.habitable_etoile.config(text=("Habitable: " + "?????"))
            self.population.config(text=("Population : " + "?????"))
            self.figure_important.config(text=("Figure Importante : " + "?????"))
            self.ressources_etoile.config(text=("Ressoures : " + "?????"))




    # def montrer_planete_selection(self):
    #     self.cadreinfochoix.pack(fill=BOTH)

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

