# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import random
from tkinter.messagebox import *
from tkinter import *

from Chat_vue import *
from Civilisation_vue import *
from Log_vue import *
from Marche_vue import *
from Menu_vue import *
from Senat_vue import *
from Techtree_vue import *
from Xy_vue import *
from helper import Helper as hlp


class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.test = parent.vaisseau_vue
        self.selection_vaisseau = None
        self.selection_batiment = None
        self.selection_satellite = None
        self.selection_merveille = None
        self.test = parent.vaisseau_vue
        self.menu_vue = Menu_vue(self)
        self.Xy_vue = Xy_vue(self)
        self.log_vue = Log_vue(self)
        self.techtree_vue = Techtree_vue(self)
        self.senat_vue = Senat_vue(self)
        self.civilisation_vue = Civilisation_vue(self)
        self.marche_vue = Marche_vue(self, parent)

        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + mon_nom)
        self.root.overrideredirect(True)
        self.root.overrideredirect(False)
        self.root.attributes('-fullscreen', True)
        self.root.wm_attributes('-fullscreen', True)
        self.ecran_largeur = self.root.winfo_screenwidth()
        self.ecran_hauteur = self.root.winfo_screenheight()
        self.centre_x = self.ecran_largeur / 2
        self.centre_y = self.ecran_hauteur / 2
        self.mon_nom = mon_nom
        # attributs
        self.lebon = 0
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None
        self.cadre_actif = None
        self.nombre_joueur = 0
        self.vaisseau_actif = {"type": None, "vie": None, "degats": None, "energie": None, "nb_capsules": None,
                               "ressource": None}
        self.chat_vue = Chat_vue(self, parent)
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
        self.joueurs = []

        self.famille_police_cadre_outils = "Arial"
        self.taille_police_cadre_outils = 20

    def demander_abandon(self):
        rep = askokcancel("Quitter?")
        if rep:
            self.root.after(500, self.root.destroy)

    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadre_actif:
            self.cadre_actif.pack_forget()
        self.cadre_actif = cadre
        self.cadre_actif.pack(expand=True, fill=BOTH)

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
        self.canevas_splash = Canvas(self.cadre_splash, bg="#45657a")
        self.canevas_splash.pack(fill=BOTH, expand=True)

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14), width=42)
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)

        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(self.centre_x, self.centre_y - 250, window=self.etatdujeu, width=400,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y - 200, window=self.nomsplash, width=400,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y - 150, window=self.urlsplash, width=360,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y - 50, window=self.btnurlconnect, width=100,
                                          height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)
        self.btn_quitter = Button(text='Quitter', font=("Arial", 9), command=self.demander_abandon)

        # on place les autres boutons
        self.canevas_splash.create_window(self.centre_x, self.centre_y + 50, window=self.btncreerpartie, width=200,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y + 100, window=self.btninscrirejoueur, width=200,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y + 150, window=self.btnreset, width=200,
                                          height=30)
        self.canevas_splash.create_window(self.centre_x, self.centre_y + 200, window=self.btn_quitter, width=200,
                                          height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash

    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadre_app)
        self.canevaslobby = Canvas(self.cadrelobby, bg="#333333")
        self.canevaslobby.pack(fill=BOTH, expand=True)
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.titre = Label(self.cadrelobby, font="Rockwell", fg="black", relief="groove",
                           text="ORION UN NOUVEL HORIZON")
        self.aide = Label(self.cadrelobby, font="Rockwell", fg="black", relief="groove",
                           text="Pour construire des vaisseaux, veuillez construire une usine !")
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(self.centre_x + 500, self.centre_y - 100, window=self.listelobby, width=200,
                                        height=400)
        self.canevaslobby.create_window(self.centre_x + 500, self.centre_y + 150, window=self.btnlancerpartie,
                                        width=100, height=30)
        self.canevaslobby.create_window(self.centre_x / 2, self.centre_y / 4, window=self.titre, width=500, height=100)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        self.lobby_decor()
        return self.cadrelobby

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.joueur_actif = self.modele.joueurs[self.mon_nom]
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom, font=9)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

    def creer_cadre_partie(self):
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="#333333")
        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="#333333")

        self.scrollX = Scrollbar(self.cadrejeu, orient=HORIZONTAL)
        self.scrollY = Scrollbar(self.cadrejeu, orient=VERTICAL)
        self.canevas = Canvas(self.cadrejeu, width=800, height=600,
                              xscrollcommand=self.scrollX.set,
                              yscrollcommand=self.scrollY.set, bg="#333333")

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

    def creer_cadre_outils(self):
        # --- Cadre qui tient tout ---#
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="grey", borderwidth=2, relief="solid")
        self.cadreoutils.pack(side=LEFT, fill=Y)

        # --- Cadre qui tient les informations ---#
        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="grey", borderwidth=2, relief="solid")
        self.cadreinfo.pack(fill=BOTH)

        # --- information joueur---#
        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="grey", borderwidth=2, relief="solid")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu", borderwidth=2, relief="solid", font=9)
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI", borderwidth=2, relief="solid", font=9)
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()
        # self.btn_chat = Button(self.cadreinfogen, text="CHAT",borderwidth=2, relief="solid")
        # self.btn_chat.bind("<Button>")
        # self.btn_chat.pack()

        # --- Creation vaisseaux ---#
        taille_police_creation_vaisseaux = 15
        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30", borderwidth=2, relief="solid")
        self.btncreerbatiment = Button(self.cadreinfochoix, text="Batiment", borderwidth=2, relief="solid", font=taille_police_creation_vaisseaux)
        self.btncreersatellite = Button(self.cadreinfochoix, text="Satellite", borderwidth=2, relief="solid", font=taille_police_creation_vaisseaux)
        self.btncreermerveille = Button(self.cadreinfochoix, text="Merveille", borderwidth=2, relief="solid", font=taille_police_creation_vaisseaux)
        self.btncreerfigure = Button(self.cadreinfochoix, text="Figure", borderwidth=2, relief="solid", font=taille_police_creation_vaisseaux)
        self.btncreervaisseau = Button(self.cadreinfochoix, text="Vaisseau", borderwidth=2, relief="solid", font=taille_police_creation_vaisseaux)

        self.btncreerbatiment.bind("<Button>", self.aller_cadre_batiment)
        self.btncreersatellite.bind("<Button>", self.aller_cadre_satellite)
        self.btncreermerveille.bind("<Button>", self.creer_merveille)
        self.btncreerfigure.bind("<Button>", self.creer_figure)
        self.btncreervaisseau.bind("<Button>", self.aller_cadre_vaisseau)

        self.btncreerbatiment.pack(fill="x", pady=5, ipady=10)
        self.btncreersatellite.pack(fill="x", pady=5, ipady=10)
        self.btncreermerveille.pack(fill="x", pady=5, ipady=10)
        self.btncreerfigure.pack(fill="x", pady=5, ipady=10)
        self.btncreervaisseau.pack(fill="x", pady=5, ipady=10)

        # --- frame info clic---#
        self.cadreinfoclic = Frame(self.cadreoutils, bg="grey")
        self.cadreinfoclic.pack(expand=True, fill=BOTH)

        # --- Frame Etoile ---#
        taille_police_statistiques = 9
        self.cadre_etoile_mere = Frame(self.cadreinfoclic, bg="white", borderwidth=2, relief="solid")
        self.id_etoile = Label(self.cadre_etoile_mere, text="Identifiant: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.hp_etoile = Label(self.cadre_etoile_mere, text="Vie: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.habitable_etoile = Label(self.cadre_etoile_mere, text="Habitable: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.population = Label(self.cadre_etoile_mere, text="Population: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.batiment_etoile = Label(self.cadre_etoile_mere, text="batiments: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.merveille_etoile = Label(self.cadre_etoile_mere, text="Merveilles: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.figure_important = Label(self.cadre_etoile_mere, text="Figures d'importance", borderwidth=2,
                                      relief="solid", font=taille_police_statistiques)
        self.ressources_etoile = Label(self.cadre_etoile_mere, text="Ressources: ", borderwidth=2, relief="solid", font=taille_police_statistiques)
        self.energie_etoile = Label(self.cadre_etoile_mere, text="Energie: ", borderwidth=2, relief="solid", font=taille_police_statistiques)

        self.id_etoile.pack(fill="x", pady=5, ipady=10)
        self.hp_etoile.pack(fill="x", pady=5, ipady=10)
        self.habitable_etoile.pack(fill="x", pady=5, ipady=10)
        self.population.pack(fill="x", pady=5, ipady=10)
        self.batiment_etoile.pack(fill="x", pady=5, ipady=10)
        self.merveille_etoile.pack(fill="x", pady=5, ipady=10)
        self.figure_important.pack(fill="x", pady=5, ipady=10)
        self.ressources_etoile.pack(fill="x", pady=5, ipady=10)
        self.energie_etoile.place()
        # --- Frame Vaisseau ---#
        taille_police_frame_vaisseau = 9
        self.cadre_vaisseau = Frame(self.cadreinfoclic, bg="white", borderwidth=2, relief="solid", width=120)
        self.type_vaisseau = Label(self.cadre_vaisseau, text=self.vaisseau_actif["type"], borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)
        self.vie = Label(self.cadre_vaisseau, text=self.vaisseau_actif["vie"], borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)
        self.degats = Label(self.cadre_vaisseau, text=self.vaisseau_actif["degats"], borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)
        self.energie = Label(self.cadre_vaisseau, text=self.vaisseau_actif["energie"], borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)
        self.nb_capsules = Label(self.cadre_vaisseau, text=self.vaisseau_actif["nb_capsules"], borderwidth=2,
                                 relief="solid", font=taille_police_frame_vaisseau)
        self.ressource_vaisseau = Label(self.cadre_vaisseau, text="ressources", borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)
        self.slot_energie_vaisseau = Label(self.cadre_vaisseau, text="Energie cargo: ", borderwidth=2, relief="solid", font=taille_police_frame_vaisseau)

        self.type_vaisseau.pack(fill="x", pady=5, ipady=10)
        self.vie.pack(fill="x", pady=5, ipady=10)
        self.degats.pack(fill="x", pady=5, ipady=10)
        self.energie.pack(fill="x", pady=5, ipady=10)
        self.nb_capsules.pack(fill="x", pady=5, ipady=10)
        self.ressource_vaisseau.pack(fill="x", pady=5, ipady=10)
        self.slot_energie_vaisseau.pack(fill="x")

        # --- Cadre information flotte (haut) ---#
        self.cadreinfoliste = Frame(self.cadreinfo, borderwidth=2, relief="solid")
        self.scroll_liste_Y = Scrollbar(self.cadreinfoliste, orient=VERTICAL, borderwidth=2, relief="solid")
        self.info_liste = Listbox(self.cadreinfoliste, width=20, height=6, yscrollcommand=self.scroll_liste_Y.set,
                                  borderwidth=2, relief="solid")
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
        taille_police_ressource = 9
        self.label_moral = Label(self.cadrehud, text="moral : 0 ", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_moral.grid(row=0, column=0, sticky=W, ipadx=20, ipady=10, pady=5, padx=5)
        self.label_diplomatie = Label(self.cadrehud, text="diplomatie : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_diplomatie.grid(row=0, column=5, sticky=W, ipadx=10, ipady=10, pady=5, padx=5)
        self.label_nourriture = Label(self.cadrehud, text="nourriture : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_nourriture.grid(row=0, column=10, sticky=W, ipadx=10, ipady=10, pady=5, padx=5)
        self.label_energie = Label(self.cadrehud, text="energie : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_energie.grid(row=0, column=15, sticky=W, ipadx=17, ipady=10, pady=5, padx=5)
        self.label_militaire = Label(self.cadrehud, text="militaire : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_militaire.grid(row=0, column=20, sticky=W, ipadx=11, ipady=10, pady=5, padx=5)
        self.label_science = Label(self.cadrehud, text="science : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_science.grid(row=0, column=25, sticky=W, ipadx=13, ipady=10, pady=5, padx=5)
        self.label_eau = Label(self.cadrehud, text="eau : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_eau.grid(row=1, column=0, sticky=W, ipadx=25, ipady=10, pady=5, padx=5)
        self.label_fer = Label(self.cadrehud, text="fer : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_fer.grid(row=1, column=5, sticky=W, ipadx=28, ipady=10, pady=5, padx=5)
        self.label_titanium = Label(self.cadrehud, text="titanium : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_titanium.grid(row=1, column=10, sticky=W, ipadx=16, ipady=10, pady=5, padx=5)
        self.label_cuivre = Label(self.cadrehud, text="cuivre : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_cuivre.grid(row=1, column=15, sticky=W, ipadx=22, ipady=10, pady=5, padx=5)
        self.label_credits = Label(self.cadrehud, text="credits : 0", borderwidth=2, relief="ridge", bg="#618fad", font=taille_police_ressource)
        self.label_credits.grid(row=1, column=20, sticky=W, ipadx=14, ipady=10, pady=5, padx=5)


        # ---- BOUTONS  TEST ----#
        taille_police_boutons = 9

        self.btnmarche = Button(self.cadrehud, text="marche", command=self.marche_vue.ouvrir_marche, borderwidth=2,
                                relief="groove", bg="#45657a", font=taille_police_boutons)
        self.btnmarche.grid(row=0, rowspan=5, column=110, sticky=W, ipadx=18, ipady=30, padx=5)
        self.btncivilisations = Button(self.cadrehud, text="civilisations",
                                       command=self.civilisation_vue.ouvrir_civilisation,
                                       borderwidth=2, relief="groove", bg="#45657a", font=taille_police_boutons)
        self.btncivilisations.grid(row=0, rowspan=5, column=120, sticky=W, ipadx=18, ipady=30, padx=5)
        self.btntechtree = Button(self.cadrehud, text="techtree", command=self.techtree_vue.ouvrir_techtree,
                                  borderwidth=2,
                                  relief="groove", bg="#45657a", font=taille_police_boutons)
        self.btntechtree.grid(row=0, rowspan=5, column=130, sticky=W, ipadx=10, ipady=30, padx=5)

        self.bouton_menu = Button(self.cadrehud, text="Menu", command=self.menu_vue.ouvrir_menu,
                               borderwidth=2,
                               relief="groove", bg="#45657a", font=taille_police_boutons)
        self.bouton_menu.grid(row=0, rowspan=5, column=140, sticky=W, ipadx=10, ipady=30, padx=5)


        self.cadrehud.pack(side=TOP, fill=BOTH)
        self.menu_vue.creer_menu()
        self.techtree_vue.creer_techtree()

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

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

    def lobby_decor(self):
        for i in range(100):
            x = random.randrange(self.ecran_largeur)
            y = random.randrange(self.ecran_hauteur)
            n = random.randrange(3) + 1

            self.canevaslobby.create_oval(x, y, x + n, y + n, fill="white", tags=("fond",))

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
        # affichage des etoiles possedees par les joueurs
        for i in self.parent.modele.joueurs.keys():
            for j in self.parent.modele.joueurs[i].etoiles_controlees:
                minixx = j.x / self.parent.modele.largeur * self.taille_minimap
                miniyy = j.y / self.parent.modele.largeur * self.taille_minimap
                self.canevas_minimap.create_rectangle(minixx, miniyy, minixx + 3, miniyy + 3,
                                                      fill=self.parent.modele.joueurs[i].couleur,
                                                      tags=("mini", j.proprietaire, str(j.id), "Etoile"))

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
        try:
            self.selection_vaisseau = self.ma_selection[1]
        except:
            pass
        self.parent.creer_vaisseau(type_vaisseau, self.selection_vaisseau)
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()

    def aller_cadre_batiment(self, evt):
        taille_police_cadre_batiment = 9

        self.cadreinfochoix.pack_forget()
        self.cadreinfobatiment = Frame(self.cadreinfo, height=200, width=200, bg="#333333", borderwidth=2, relief="solid")

        self.btncreer_raffinerie = Button(self.cadreinfobatiment, text="Raffinerie", borderwidth=2, relief="solid", font=taille_police_cadre_batiment)
        self.btncreer_raffinerie.bind("<Button>", self.creer_batiment)
        self.btncreer_ferme = Button(self.cadreinfobatiment, text="Ferme", borderwidth=2, relief="solid", font=taille_police_cadre_batiment)
        self.btncreer_ferme.bind("<Button>", self.creer_batiment)
        self.btncreer_laboratoire = Button(self.cadreinfobatiment, text="Laboratoire", borderwidth=2, relief="solid", font=taille_police_cadre_batiment)
        self.btncreer_laboratoire.bind("<Button>", self.creer_batiment)
        self.btncreer_usine = Button(self.cadreinfobatiment, text="Usine", borderwidth=2, relief="solid", font=taille_police_cadre_batiment)
        self.btncreer_usine.bind("<Button>", self.creer_batiment)

        self.btncreer_raffinerie.pack(fill="x", pady=5, ipady=10)
        self.btncreer_ferme.pack(fill="x", pady=5, ipady=10)
        self.btncreer_laboratoire.pack(fill="x", pady=5, ipady=10)
        self.btncreer_usine.pack(fill="x", pady=5, ipady=10)
        self.cadreinfobatiment.pack(fill="x")

    def aller_cadre_satellite(self, evt):
        taille_police_cadre_satellite = 9

        self.cadreinfochoix.pack_forget()
        self.cadreinfosatellite = Frame(self.cadreinfo, height=200, width=200, bg="grey", borderwidth=2, relief="solid")

        self.btncreer_sat_defensif = Button(self.cadreinfosatellite, text="SAT Defensif", borderwidth=2, relief="solid", font=taille_police_cadre_satellite)
        self.btncreer_sat_defensif.bind("<Button>", self.creer_satellite)
        self.btncreer_sat_vision = Button(self.cadreinfosatellite, text="SAT Vision", borderwidth=2, relief="solid", font=taille_police_cadre_satellite)
        self.btncreer_sat_vision.bind("<Button>", self.creer_satellite)
        self.btncreer_sat_kamikaze = Button(self.cadreinfosatellite, text="SAT Kamikaze", borderwidth=2, relief="solid", font=taille_police_cadre_satellite)
        self.btncreer_sat_kamikaze.bind("<Button>", self.creer_satellite)

        self.btncreer_sat_defensif.pack(fill="x", pady=5, ipady=10)
        self.btncreer_sat_vision.pack(fill="x", pady=5, ipady=10)
        self.btncreer_sat_kamikaze.pack(fill="x", pady=5, ipady=10)
        self.cadreinfosatellite.pack(fill="x")

    def creer_batiment(self, evt):
        type_batiment = evt.widget.cget("text")
        try:
            self.selection_batiment = self.ma_selection[1]
        except:
            pass
        self.parent.creer_batiment(type_batiment, self.selection_batiment)
        self.ma_selection = None
        self.canevas.delete("marqueur")

    def creer_satellite(self, evt):
        type_satellite = evt.widget.cget("text")
        try:
            self.selection_satellite = self.ma_selection[1]
        except:
            pass
        self.parent.creer_satellite(type_satellite, self.selection_satellite)
        self.ma_selection = None
        self.canevas.delete("marqueur")

    def creer_merveille(self, evt):
        type_merveille = evt.widget.cget("text")
        try:
            self.selection_merveille = self.ma_selection[1]
        except:
            pass
        self.parent.creer_merveille(type_merveille, self.selection_merveille)
        self.ma_selection = None
        self.canevas.delete("marqueur")

    def creer_figure(self, evt):
        type_figure = evt.widget.cget("text")
        self.parent.creer_figure(type_figure)
        self.ma_selection = None
        self.canevas.delete("marqueur")

    def aller_cadre_vaisseau(self, evt):
        taille_police_cadre_vaisseau = 9

        self.cadreinfochoix.pack_forget()
        self.cadreinfovaisseau = Frame(self.cadreinfo, height=200, width=120, bg="grey45")

        # --- Cadre Creation vaisseaux ---#

        self.btncreercargo = Button(self.cadreinfovaisseau, text="Cargo", borderwidth=2, relief="solid", font=taille_police_cadre_vaisseau)
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)
        self.btncreerScout = Button(self.cadreinfovaisseau, text="Scout", borderwidth=2, relief="solid", font=taille_police_cadre_vaisseau)
        self.btncreerScout.bind("<Button>", self.creer_vaisseau)
        self.btncreerSpaceFighter = Button(self.cadreinfovaisseau, text="Spacefighter", borderwidth=2, relief="solid", font=taille_police_cadre_vaisseau)
        self.btncreerSpaceFighter.bind("<Button>", self.creer_vaisseau)
        self.btncreerColonisateur = Button(self.cadreinfovaisseau, text="Colonisateur", borderwidth=2, relief="solid", font=taille_police_cadre_vaisseau)
        self.btncreerColonisateur.bind("<Button>", self.creer_vaisseau)
        self.btncreerDestroyer = Button(self.cadreinfovaisseau, text="Destroyer", borderwidth=2, relief="solid", font=taille_police_cadre_vaisseau)
        self.btncreerDestroyer.bind("<Button>", self.creer_vaisseau)

        self.btncreervaisseau.pack(fill="x", pady=5, ipady=10)
        self.btncreercargo.pack(fill="x", pady=5, ipady=10)
        self.btncreerColonisateur.pack(fill="x", pady=5, ipady=10)
        self.btncreerScout.pack(fill="x", pady=5, ipady=10)
        self.btncreerDestroyer.pack(fill="x", pady=5, ipady=10)
        self.btncreerSpaceFighter.pack(fill="x", pady=5, ipady=10)
        self.cadreinfovaisseau.pack(fill="x")

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("annonce")
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

            ## afficher barre de vie

            for y in i.flotte.keys():
                for z in i.flotte[y]:
                    mon_vaisseau = i.flotte[y][z]
                    ma_barre_vie = 100 / 6
                    vie = (mon_vaisseau.hp / mon_vaisseau.max_hp * 100) / 6
                    ma_barre_energie = 100 / 6
                    energie = i.energie.quantite / 10

                    self.canevas.create_rectangle(mon_vaisseau.x - ma_barre_energie, mon_vaisseau.y - 16,
                                                  mon_vaisseau.x + ma_barre_energie, mon_vaisseau.y - 19, fill="orange",
                                                  tag="artefact")
                    self.canevas.create_rectangle(mon_vaisseau.x - ma_barre_energie, mon_vaisseau.y - 16,
                                                  mon_vaisseau.x - ma_barre_energie + energie * 2, mon_vaisseau.y - 19,
                                                  fill="black", tag="artefact")

                    self.canevas.create_rectangle(mon_vaisseau.x - ma_barre_vie, mon_vaisseau.y - 12,
                                                  mon_vaisseau.x + ma_barre_vie, mon_vaisseau.y - 15, fill="red",
                                                  tag="artefact")
                    self.canevas.create_rectangle(mon_vaisseau.x - ma_barre_vie, mon_vaisseau.y - 12,
                                                  mon_vaisseau.x - ma_barre_vie + vie * 2, mon_vaisseau.y - 15,
                                                  fill="green", tag="artefact")

            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    if j.angle_cible < 0:
                        angle = 360 + (j.angle_cible * 57.2957795)
                    else:
                        angle = j.angle_cible * 57.2957795
                    positionid = round(angle / 45)

                    if k == "Vaisseau":
                        if i.id in self.test.id_vaisseau1:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau1[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau2:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau2[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau3:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau3[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau4:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau4[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau5:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau5[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau6:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau6[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau7:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau7[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau8:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau8[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Destroyer":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill="pink",
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Scout":
                        if i.id in self.test.id_vaisseau1:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout1[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau2:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout2[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau3:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout3[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau4:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout4[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau5:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout5[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau6:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout6[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau7:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout7[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau8:
                            self.canevas.create_image(j.x, j.y, image=self.test.scout8[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Colonisateur":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill="blue",
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Spacefighter":
                        if i.id in self.test.id_vaisseau1:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau1[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau2:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau2[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau3:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau3[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau4:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau4[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau5:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau5[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau6:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau6[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau7:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau7[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif i.id in self.test.id_vaisseau8:
                            self.canevas.create_image(j.x, j.y, image=self.test.vaisseau8[positionid],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Cargo":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j, tailleF, i, k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
            for satk in i.satel:
                for satj in i.satel[satk]:
                    satj = i.satel[satk][satj]
                    tailleS = satj.taille * self.zoom

                    if satk == "SAT Defensif":
                        self.canevas.create_oval((satj.x - tailleS), (satj.y - tailleS),
                                                 (satj.x + tailleS), (satj.y + tailleS), fill="pink",
                                                 tags=(satj.proprietaire, str(satj.id), "Satellite", satk, "artefact"))
                    elif satk == "SAT Vision":
                        self.canevas.create_oval((satj.x - tailleS), (satj.y - tailleS),
                                                 (satj.x + tailleS), (satj.y + tailleS), fill="orange",
                                                 tags=(satj.proprietaire, str(satj.id), "Satellite", satk, "artefact"))
                    elif satk == "SAT Kamikaze":
                        self.canevas.create_oval((satj.x - tailleS), (satj.y - tailleS),
                                                 (satj.x + tailleS), (satj.y + tailleS), fill="purple",
                                                 tags=(satj.proprietaire, str(satj.id), "Satellite", satk, "artefact"))
                        if satj.detruit:
                            self.canevas.delete(satj.id)

        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

            if self.joueur_actif.annonce:
                self.canevas.create_text(self.joueur_actif.annonce.x, self.joueur_actif.annonce.y,
                                         text=self.joueur_actif.annonce.message,
                                         fill="OrangeRed2", font=('Helvetica', 25), tags=("", "annonce"),
                                         anchor="center")
                self.canevas.create_text(self.joueur_actif.annonce.x, self.joueur_actif.annonce.y - 2,
                                         text=self.joueur_actif.annonce.message,
                                         fill="LightGoldenrod2", font=('Helvetica', 25), tags=("", "annonce"),
                                         anchor="center")

        # --affichage ressources hud--#
        taille_police_affichage_ressources = 9
        self.label_moral.config(text=("Moral : " + str(self.joueur_actif.moral)), font=taille_police_affichage_ressources)
        self.label_diplomatie.config(text=("Diplomatie : " + str(self.joueur_actif.diplomatie)), font=taille_police_affichage_ressources)
        self.label_nourriture.config(text=("Nourriture : " + str(self.joueur_actif.nourriture.quantite)), font=taille_police_affichage_ressources)
        self.label_energie.config(text=("Energie : " + str(self.joueur_actif.energie.quantite)), font=taille_police_affichage_ressources)
        self.label_militaire.config(text=("Militaire : " + str(self.joueur_actif.militaire)), font=taille_police_affichage_ressources)
        self.label_science.config(text=("Science : " + str(self.joueur_actif.science)), font=taille_police_affichage_ressources)
        self.label_eau.config(text=("Eau : " + str(self.joueur_actif.eau.quantite)), font=taille_police_affichage_ressources)
        self.label_fer.config(text=("Fer : " + str(self.joueur_actif.fer.quantite)), font=taille_police_affichage_ressources)
        self.label_titanium.config(text=("Titanium : " + str(self.joueur_actif.titanium.quantite)), font=taille_police_affichage_ressources)
        self.label_cuivre.config(text=("Cuivre : " + str(self.joueur_actif.cuivre.quantite)), font=taille_police_affichage_ressources)
        self.label_credits.config(text=("Credits : " + str(self.joueur_actif.credits)), font=taille_police_affichage_ressources)

        self.canevas.delete("PROJECTILE")

        for joueur in mod.joueurs:
            # afficher projectiles depuis tous flottes
            for nom_flotte in mod.joueurs[joueur].flotte.keys():
                for id_flotte in mod.joueurs[joueur].flotte.get(nom_flotte):
                    for projectile in mod.joueurs[joueur].flotte.get(nom_flotte).get(id_flotte).projectiles:
                        self.__afficher_projectiles(projectile)
            # afficher projectiles depuis tous satellites
            for nom_satel in mod.joueurs[joueur].satel.keys():
                for id_satel in mod.joueurs[joueur].satel.get(nom_satel):
                    for projectile in mod.joueurs[joueur].satel.get(nom_satel).get(id_satel).projectiles:
                        self.__afficher_projectiles(projectile)

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
                    print(self.ma_selection[1])
                    print(t[1])
                    print(t[2])
                self.ma_selection = [self.mon_nom, t[1], t[2]]
                if t[2] == "Etoile":
                    try:
                        self.cadreinfovaisseau.pack_forget()
                    except:
                        pass
                    try:
                        self.cadreinfobatiment.pack_forget()
                    except:
                        pass
                    try:
                        self.cadreinfosatellite.pack_forget()
                    except:
                        pass

                    self.update_etoile_actif(t[1])
                    self.montrer_etoile_selection()
                    self.cadre_vaisseau.pack_forget()
                elif t[2] == "Flotte":
                    self.update_vaisseau_actif(t[1], t[3])
                    self.montrer_flotte_selection()
                    self.cadre_etoile_mere.pack_forget()
            else:
                nom_joueur = t[0]
                id_objet = t[1]
                type_objet = t[2]
                if self.ma_selection:
                    self.parent.cibler_flotte(self.ma_selection[1], id_objet, type_objet)

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
        taille_police_vaisseau_actif = 9

        vaisseau = self.joueur_actif.flotte[type_vaisseau][id]
        self.type_vaisseau.config(text=("Type : " + str(vaisseau.type)), font=taille_police_vaisseau_actif)
        self.vie.config(text=("Points de vie : " + str(vaisseau.hp)), font=taille_police_vaisseau_actif)
        # self.attaque.config(text=("Attaque : " + str(vaisseau.attaque)))
        self.degats.config(text=("Dégâts : " + str(vaisseau.degat)), font=taille_police_vaisseau_actif)
        self.energie.config(text=("Energie : " + str(vaisseau.energie)), font=taille_police_vaisseau_actif)
        self.nb_capsules.config(text=("Capsules : " + str(len(vaisseau.capsules))), font=taille_police_vaisseau_actif)
        if type_vaisseau == "Cargo":
            try:
                self.slot_energie_vaisseau.config(text=("Energie: " + str(vaisseau.slot_energie.quantite)), font=taille_police_vaisseau_actif)
            except:
                self.slot_energie_vaisseau.config(text=("Energie: " + str(0)), font=taille_police_vaisseau_actif)
            try:
                self.ressource_vaisseau.config(text=("Ressources : " + str(vaisseau.slot_ressources.nom) + " " + str(
                    vaisseau.slot_ressources.quantite)), font=taille_police_vaisseau_actif)
            except:
                self.ressource_vaisseau.config(text=("Ressources : " + str(0)), font=taille_police_vaisseau_actif)

    # self.vaisseau_actif["ressources"] = vaisseau.ressources

    def update_etoile_actif(self, id):
        taille_police_etoile_actif = 9

        # il faut implementer la verification de si on possede la capsule pour voir les ressources
        batiment_temp = ""
        batiment_niveau = ""
        merveille_temp = ""
        try:
            if id in self.joueur_actif.capsules_ouvertes:
                etoile = self.joueur_actif.capsules_ouvertes[id]
            elif id == self.joueur_actif.etoile_mere.id:
                etoile = self.joueur_actif.etoile_mere
                etoile.ressource.nom = ""
                etoile.ressource.quantite = 0
            self.id_etoile.config(text=("Identifiant étoile: " + str(etoile.id)), font=taille_police_etoile_actif)
            self.hp_etoile.config(text=("Points de vie : " + str(etoile.hp)), font=taille_police_etoile_actif)
            self.habitable_etoile.config(text=("Habitable: " + str(etoile.habitable)), font=taille_police_etoile_actif)
            self.population.config(text=("Population : " + str(etoile.population)), font=taille_police_etoile_actif)

            for i, j in etoile.parent.joueurs.items():
                if i == etoile.proprietaire:
                    #for batiment in j.batiment.items():
                    #    for b1, b2 in batiment[1].items():
                     #       batiment_niveau = " " + str(b2.niveau)
                      #      batiment_temp += "\n" + b2.nom_batiment + batiment_niveau

                    #for merveil in j.merveille.items():
                     #   for b3, b4 in merveil[1].items():
                      #      merveille_temp += "\n" + b4.nom_merveille
                      
                    for etoile in j.etoiles_controlees:
                        if etoile.id == self.ma_selection[1]:
                            for batiment in etoile.batiment.items():
                                for b1, b2 in batiment[1].items():
                                    batiment_niveau = " " + str(b2.niveau)
                                    batiment_temp += "\n" + b2.nom_batiment + batiment_niveau

                            for merveil in etoile.merveille.items():
                                for b3, b4 in merveil[1].items():
                                    merveille_temp += "\n" + b4.nom_merveille

            self.batiment_etoile.config(text=("Batiment: " + batiment_temp), font=taille_police_etoile_actif)
            self.merveille_etoile.config(text=("Merveille: " + merveille_temp), font=taille_police_etoile_actif)

            # self.figure_important.config(text=("Figure Importante : " + str(vaisseau.energie)))
            self.ressources_etoile.config(
                text=("Ressoures : " + str(etoile.ressource.nom) + " " + str(etoile.ressource.quantite)), font=taille_police_etoile_actif)
            self.energie_etoile.config(
                text=("Ressoures : " + str(etoile.energie.nom) + " " + str(etoile.energie.quantite)), font=taille_police_etoile_actif)
        except:
            self.id_etoile.config(text=("Identifiant: " + "?????"), font=taille_police_etoile_actif)
            self.hp_etoile.config(text=("Points de vie : " + "?????"), font=taille_police_etoile_actif)
            self.habitable_etoile.config(text=("Habitable: " + "?????"), font=taille_police_etoile_actif)
            self.population.config(text=("Population : " + "?????"), font=taille_police_etoile_actif)
            self.batiment_etoile.config(text=("Batiment: " + "?????"), font=taille_police_etoile_actif)
            self.figure_important.config(text=("Figure Importante : " + "?????"), font=taille_police_etoile_actif)
            self.merveille_etoile.config(text=("Merveille: " + "?????"), font=taille_police_etoile_actif)
            self.ressources_etoile.config(text=("Ressoures : " + "?????"), font=taille_police_etoile_actif)
            self.energie_etoile.config(text=("Energie : " + "?????"), font=taille_police_etoile_actif)

    def __afficher_projectiles(self, projectile):
        projectile.attaque_cible()
        self.canevas.create_rectangle(
            projectile.x, projectile.y
            , projectile.x + projectile.largeur, projectile.y + projectile.longueur
            , fill=projectile.couleur
            , tag="PROJECTILE"
        )

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

    ## FIN du multiselect
