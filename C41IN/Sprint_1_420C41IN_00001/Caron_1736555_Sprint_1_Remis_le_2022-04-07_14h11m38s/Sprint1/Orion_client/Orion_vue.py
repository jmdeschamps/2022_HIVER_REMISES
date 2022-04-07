# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math
from systeme_solaire import *
import random


class Vue():
    def __init__(self,parent,urlserveur,mon_nom,msg_initial):
        self.parent=parent
        self.root=Tk()
        self.root.title("Je suis "+mon_nom)
        self.mon_nom=mon_nom
        # attributs
        self.taille_minimap=150
        self.padding_res_joueurs = 2
        self.width_res_systemes = 0
        self.nbr_cadre_res_systemes = 5
        self.couleur_texte_systemes = "yellow"
        self.information_etoile_cadre = None
        self.zoom=2
        self.ma_selection=None
        self.cadre_actif=None
        # cadre principal de l'application
        self.cadre_app=Frame(self.root,width=500,height=400,bg="red")
        self.cadre_app.pack(expand=1,fill=BOTH)
        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres={}
        self.creer_cadres(urlserveur,mon_nom,msg_initial)
        self.changer_cadre("splash")
        # PROTOCOLE POUR INTERCEPTER LA FERMETURE DU ROOT - qui termine l'application
        #self.root.protocol("WM_DELETE_WINDOW", self.demander_abandon)

        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele=None
        # # variable pour suivre le trace du multiselect
        self.debut_selection=[]
        self.selecteur_actif=None


    def demander_abandon(self):
        rep=askokcancel("Vous voulez vraiment quitter?")
        if rep:
            self.root.after(500, self.root.destroy)

####### INTERFACES GRAPHIQUES
    def changer_cadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadre_actif:
            self.cadre_actif.pack_forget()
        self.cadre_actif=cadre
        self.cadre_actif.pack(expand=1,fill=BOTH)


    def bougerMap(self,evt):
        self.canevas.bind("<B1-button>",self.defiler_horizon)
        self.canevas.bind("<B1-button>",self.defiler_vertical)
        self.bougerMap(evt)




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
        self.urlsplash = Entry(font=("Arial", 14),width=42)
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
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED, command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED, command=self.reset_partie)

        # on place les autres boutons
        self.canevas_splash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash



    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby=Frame(self.cadre_app)
        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480,bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby=Listbox(borderwidth=2,relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie=Button(text="Lancer partie",state=DISABLED,command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440,240,window=self.listelobby,width=200,height=400)
        self.canevaslobby.create_window(200,400,window=self.btnlancerpartie,width=100,height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    def creer_cadre_partie(self):
        self.cadrepartie=Frame(self.cadre_app,width=600,height=200, bg="yellow")
        self.cadrejeu=Frame(self.cadrepartie,width=600,height=200,bg="teal")

        self.scrollX=Scrollbar(self.cadrejeu,orient=HORIZONTAL)
        self.scrollY=Scrollbar(self.cadrejeu,orient=VERTICAL)
        self.canevas=Canvas(self.cadrejeu,width=800,height=600,
                            xscrollcommand = self.scrollX.set,
                            yscrollcommand = self.scrollY.set,bg="grey11")

        self.scrollX.config(command=self.canevas.xview)
        self.scrollY.config(command=self.canevas.yview)

        self.canevas.grid(column=0,row=0,sticky=W+E+N+S)
        self.scrollX.grid(column=0,row=1,sticky=W+E)
        self.scrollY.grid(column=1,row=0,sticky=N+S)

        self.cadrejeu.columnconfigure(0,weight=1)
        self.cadrejeu.rowconfigure(0,weight=1)
        self.canevas.bind("<Button>",self.cliquer_cosmos)
        self.canevas.tag_bind(ALL,"<Button>",self.cliquer_cosmos)

        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)

        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)

        self.creer_cadre_outils()

        self.cadrejeu.pack(side=LEFT,expand=1,fill=BOTH)
        return self.cadrepartie
        
    def creer_cadre_outils(self):
        self.cadreoutils=Frame(self.cadrepartie,width=200,height=50,bg="darkgrey")
        self.cadreoutils.pack(side=BOTTOM,fill=X)

        self.cadreinfoliste=Frame(self.cadreoutils)

        ##GROS SCROLL BAR BLANC.

        self.scroll_liste_Y=Scrollbar(self.cadreinfoliste,orient=VERTICAL)
        self.info_liste=Listbox(self.cadreinfoliste,width=20,height=6,yscrollcommand = self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-3>",self.centrer_liste_objet)
        self.info_liste.grid(column=0,row=0,sticky=W+E+N+S)
        self.scroll_liste_Y.grid(column=1,row=0,sticky=N+S)

        self.cadreinfoliste.columnconfigure(0,weight=1)
        self.cadreinfoliste.rowconfigure(0,weight=1)

        self.cadreinfoliste.pack(side=LEFT ,fill=BOTH)

        self.cadre_etoile_information = Frame(self.cadreoutils, height=50, bg="grey69")
        self.cadre_etoile_information.pack(side=LEFT, expand=1, fill=BOTH)

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=50, bg="black")
        self.cadreinfo.pack(side=LEFT, fill=BOTH)

        self.information_etoile_cadre = LabelFrame(self.cadre_etoile_information, width=150, height=32,
                                                   text="Système", bg="black", fg=self.couleur_texte_systemes,
                                                   labelanchor=NE, relief=RAISED)

        self.info_etoile_energie = LabelFrame(self.information_etoile_cadre, width=self.width_res_systemes, height=32,
                                              text="Énergie", bg="black", fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_etoile_energie.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_etoile_met = LabelFrame(self.information_etoile_cadre, width=self.width_res_systemes, height=32,
                                          text="Métaux", bg="black",
                                          fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_etoile_met.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_etoile_infrastructure = LabelFrame(self.information_etoile_cadre, width=100, height=32,
                                                     text="infrastructures", bg="black",
                                                     fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_etoile_infrastructure.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_etoile_population = LabelFrame(self.information_etoile_cadre, width=50, height=32,
                                                 text="Populations", bg="black",
                                                 fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_etoile_population.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_etoile_gaz = LabelFrame(self.information_etoile_cadre, width=50, height=32,
                                          text="Gaz", bg="black",
                                          fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_etoile_gaz.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.cadre_infrastructure_g = Label(self.info_etoile_infrastructure, bg="black")
        self.cadre_infrastructure_d = Label(self.info_etoile_infrastructure, bg="black")
        self.cadre_infrastructure_g.pack(side=LEFT,expand=1, fill=BOTH)
        self.cadre_infrastructure_d.pack(side=LEFT, expand=1, fill=BOTH)

        # ressources sys
        self.energie_sys = StringVar()
        self.energie_sys.set("0")

        self.nourriture_sys = StringVar()
        self.nourriture_sys.set("0")

        self.gold_sys = StringVar()
        self.gold_sys.set("0")

        self.fer_sys = StringVar()
        self.fer_sys.set("0")

        self.cuivre_sys = StringVar()
        self.cuivre_sys.set("0")

        self.titanite_sys = StringVar()
        self.titanite_sys.set("0")

        self.uranium_sys = StringVar()
        self.uranium_sys.set("0")

        self.hydrogene_sys = StringVar()
        self.hydrogene_sys.set("0")

        self.azote_sys = StringVar()
        self.azote_sys.set("0")

        self.xenon_sys = StringVar()
        self.xenon_sys.set("0")

        self.moral_sys = StringVar()
        self.moral_sys.set("0")

        self.population_sys = StringVar()
        self.population_sys.set("0")

        self.defense_art_sys = StringVar()
        self.defense_art_sys.set("0")

        # infrastructure
        self.mine = StringVar()
        self.mine.set("0")

        self.musee = StringVar()
        self.musee.set("0")

        self.ecole = StringVar()
        self.ecole.set("0")

        self.barraques = StringVar()
        self.barraques.set("0")

        self.usine = StringVar()
        self.usine.set("0")

        self.ferme = StringVar()
        self.ferme.set("0")

        self.usine_traitement_gaz = StringVar()
        self.usine_traitement_gaz.set("0")

        self.centrale_nucleaire = StringVar()
        self.centrale_nucleaire.set("0")

        # Cadre ressource en Énergie
        self.energie_frame = Frame(self.info_etoile_energie, bg="grey69")
        self.energie_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.energie_titre = Label(self.energie_frame, text="Énergie : ", bg="grey4", fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.energie_valeur = Label(self.energie_frame, text="", textvariable=self.energie_sys, bg="black",
                                    fg="white").pack(side=LEFT)
        # Cadre ressource en nourriture
        self.nourriture_frame = Frame(self.info_etoile_population, bg="grey69")
        self.nourriture_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.nourriture_titre = Label(self.nourriture_frame, text="nourriture : ", bg="grey4",
                                      fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.nourriture_valeur = Label(self.nourriture_frame, text="", textvariable=self.nourriture_sys, bg="black",
                                       fg="white").pack(side=LEFT)
        # Cadre ressource en or
        self.or_frame = Frame(self.info_etoile_met, bg="grey69")
        self.or_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.or_titre = Label(self.or_frame, text="or : ", bg="grey4",
                              fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.or_valeur = Label(self.or_frame, text="", textvariable=self.gold_sys, bg="black",
                               fg="white").pack(side=LEFT)
        # Cadre ressource en fer
        self.fer_frame = Frame(self.info_etoile_met, bg="grey69")
        self.fer_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.fer_titre = Label(self.fer_frame, text="fer : ", bg="grey4",
                               fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.fer_valeur = Label(self.fer_frame, text="", textvariable=self.fer_sys, bg="black",
                                fg="white").pack(side=LEFT)
        # Cadre ressource en cuivre
        self.cuivre_frame = Frame(self.info_etoile_met, bg="grey69")
        self.cuivre_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.cuivre_titre = Label(self.cuivre_frame, text="cuivre : ", bg="grey4",
                                  fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.cuivre_valeur = Label(self.cuivre_frame, text="", textvariable=self.cuivre_sys, bg="black",
                                   fg="white").pack(side=LEFT)
        # Cadre ressource en titanite
        self.titanite_frame = Frame(self.info_etoile_met, bg="grey69")
        self.titanite_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.titanite_titre = Label(self.titanite_frame, text="titanite : ", bg="grey4",
                                    fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.titanite_valeur = Label(self.titanite_frame, text="", textvariable=self.titanite_sys, bg="black",
                                     fg="white").pack(side=LEFT)
        # Cadre ressource en uranium
        self.uranium_frame = Frame(self.info_etoile_energie, bg="grey69")
        self.uranium_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.uranium_titre = Label(self.uranium_frame, text="uranium : ", bg="grey4",
                                   fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.uranium_valeur = Label(self.uranium_frame, text="", textvariable=self.uranium_sys, bg="black",
                                    fg="white").pack(side=LEFT)
        # Cadre ressource en hydrogene
        self.hydrogene_frame = Frame(self.info_etoile_gaz, bg="grey69")
        self.hydrogene_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.hydrogene_titre = Label(self.hydrogene_frame, text="hydrogene : ", bg="grey4",
                                     fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.hydrogene_valeur = Label(self.hydrogene_frame, text="", textvariable=self.hydrogene_sys, bg="black",
                                      fg="white").pack(side=LEFT)
        # Cadre ressource en azote
        self.azote_frame = Frame(self.info_etoile_gaz, bg="grey69")
        self.azote_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.azote_titre = Label(self.azote_frame, text="azote : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.azote_valeur = Label(self.azote_frame, text="", textvariable=self.azote_sys, bg="black",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en xenon
        self.xenon_frame = Frame(self.info_etoile_gaz, bg="grey69")
        self.xenon_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.xenon_titre = Label(self.xenon_frame, text="Xenon : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.xenon_valeur = Label(self.xenon_frame, text="", textvariable=self.xenon_sys, bg="black",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en Moral
        self.moral_frame = Frame(self.info_etoile_population, bg="grey69")
        self.moral_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        self.moral_titre = Label(self.moral_frame, text="Moral : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.moral_valeur = Label(self.moral_frame, text="", textvariable=self.moral_sys, bg="black",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en defense artificielle
        self.defense_art = Frame(self.info_etoile_population, bg="grey69")
        self.defense_art.pack(side=TOP, padx=self.padding_res_joueurs)
        self.def_art = Label(self.defense_art, text="Defense Artificielle : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.def_art = Label(self.defense_art, text="", textvariable=self.population_sys, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure mine
        self.frame_mine = Frame(self.cadre_infrastructure_g, bg="grey69")
        self.frame_mine.pack(side=TOP, padx=self.padding_res_joueurs)

        self.label_mine = Label(self.frame_mine, text="Mine : ", bg="grey4",
                             fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_mine = Label(self.frame_mine, text="", textvariable=self.mine, bg="black",
                             fg="white").pack(side=LEFT)

        # Cadre infrastructure usine
        self.frame_usine = Frame(self.cadre_infrastructure_g, bg="grey69")
        self.frame_usine.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_usine = Label(self.frame_usine, text="Usine : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_usine = Label(self.frame_usine, text="", textvariable=self.usine, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure ferme
        self.frame_ferme = Frame(self.cadre_infrastructure_g, bg="grey69")
        self.frame_ferme.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_ferme = Label(self.frame_ferme, text="Ferme : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_ferme = Label(self.frame_ferme, text="", textvariable=self.ferme, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure usine_traitement_gaz
        self.frame_usine_traitement_gaz = Frame(self.cadre_infrastructure_g, bg="grey69")
        self.frame_usine_traitement_gaz.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_usine_traitement_gaz = Label(self.frame_usine_traitement_gaz, text="Usine traitement gaz : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_usine_traitement_gaz = Label(self.frame_usine_traitement_gaz, text="", textvariable=self.usine_traitement_gaz, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure musee
        self.frame_musee = Frame(self.cadre_infrastructure_d, bg="grey69")
        self.frame_musee.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_musee = Label(self.frame_musee, text="Musee : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_musee = Label(self.frame_musee, text="", textvariable=self.musee, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure ecole
        self.frame_ecole = Frame(self.cadre_infrastructure_d, bg="grey69")
        self.frame_ecole.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_ecole = Label(self.frame_ecole, text="Ecole : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_ecole = Label(self.frame_ecole, text="", textvariable=self.ecole, bg="black",
                                 fg="white").pack(side=LEFT)

        # Cadre infrastructure barraques
        self.frame_barraques = Frame(self.cadre_infrastructure_d, bg="grey69")
        self.frame_barraques.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_barraques = Label(self.frame_barraques, text="barraques : ", bg="grey4",
                                     fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_barraques = Label(self.frame_barraques, text="", textvariable=self.barraques, bg="black",
                                     fg="white").pack(side=LEFT)

        # Cadre infrastructure centrale_nucleaire
        self.frame_centrale_nucleaire = Frame(self.cadre_infrastructure_d, bg="grey69")
        self.frame_centrale_nucleaire.pack(side=TOP, padx=self.padding_res_joueurs)
        self.label_centrale_nucleaire = Label(self.frame_centrale_nucleaire, text="Centrale Nucleaire : ", bg="grey4",
                                 fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.label_centrale_nucleaire = Label(self.frame_centrale_nucleaire, text="", textvariable=self.centrale_nucleaire, bg="black",
                                 fg="white").pack(side=LEFT)

        ##JAJA et MINI USER.
        self.cadreinfogen = Frame(self.cadreinfo,width=150, height=50, bg="gray30")
        self.cadreinfogen.pack(side=RIGHT, fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()

        ##APPARAIT QUAND TU CLICK SUR UNE PLANÈTE
        self.cadreinfochoix = Frame(self.cadreinfo, width=150, height=50, bg="gray30")
        self.btncreervaisseau = Button(self.cadreinfochoix, text="Vaisseau")
        self.btncreervaisseau.bind("<Button>", self.creer_bien)
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_bien)

        self.btncreervaisseau.pack()
        self.btncreercargo.pack()


    #      Minimap
        self.cadreminimap=Frame(self.cadreoutils,width=150,height=50,bg="black")
        self.canevas_minimap=Canvas(self.cadreminimap,width=self.taille_minimap,height=self.taille_minimap,bg="slategrey")
        self.canevas_minimap.bind("<Button>",self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=RIGHT, fill=X)

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)


    # Cadre des ressources du joueurs (haut du GUI)
        self.cadre_ressources_joueur = Frame(self.cadrepartie, height=25,  bg="grey69")
        self.cadre_ressources_joueur.pack(side=TOP,fill=X)

        self.energie = StringVar()
        self.energie.set("0")

        self.nourriture = StringVar()
        self.nourriture.set("0")

        self.gold = StringVar()
        self.gold.set("0")

        self.fer = StringVar()
        self.fer.set("0")

        self.cuivre = StringVar()
        self.cuivre.set("0")

        self.titanite = StringVar()
        self.titanite.set("0")

        self.uranium = StringVar()
        self.uranium.set("0")

        self.hydrogene = StringVar()
        self.hydrogene.set("0")

        self.azote = StringVar()
        self.azote.set("0")

        self.xenon = StringVar()
        self.xenon.set("0")

        self.moral = StringVar()
        self.moral.set("0")

        self.population = StringVar()
        self.population.set("0")

        self.defense_art = StringVar()
        self.defense_art.set("0")

        # Cadre de pour détacher les ressources des boutons de statistiques à gauche
        self.cadre_détaché = Label(self.cadre_ressources_joueur, width=20, bg="grey69").pack(side=LEFT)


        # Cadre ressource en Énergie
        self.energie_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.energie_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.energie_titre = Label(self.energie_frame, text="Énergie : ", bg="grey4", fg="white").pack(side=LEFT)
        self.energie_valeur = Label(self.energie_frame, text="", textvariable=self.energie, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en nourriture
        self.nourriture_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.nourriture_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.nourriture_titre = Label(self.nourriture_frame, text="nourriture : ", bg="grey4",
                                      fg="white").pack(side=LEFT)
        self.nourriture_valeur = Label(self.nourriture_frame, text="", textvariable=self.nourriture, bg="grey40",
                                       fg="white").pack(side=LEFT)
        # Cadre ressource en or
        self.or_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.or_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.or_titre = Label(self.cadre_ressources_joueur, text="or : ", bg="grey4",
                                   fg="white").pack(side=LEFT)
        self.or_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.gold, bg="grey40",
                                    fg="white").pack(side=LEFT)
        # Cadre ressource en fer
        self.fer_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.fer_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.fer_titre = Label(self.cadre_ressources_joueur, text="fer : ", bg="grey4",
                                   fg="white").pack(side=LEFT)
        self.fer_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.fer, bg="grey40",
                                    fg="white").pack(side=LEFT)
        # Cadre ressource en cuivre
        self.cuivre_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.cuivre_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.cuivre_titre = Label(self.cadre_ressources_joueur, text="cuivre : ", bg="grey4",
                                   fg="white").pack(side=LEFT)
        self.cuivre_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.cuivre, bg="grey40",
                                    fg="white").pack(side=LEFT)
        # Cadre ressource en titanite
        self.titanite_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.titanite_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.titanite_titre = Label(self.cadre_ressources_joueur, text="titanite : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.titanite_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.titanite, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en uranium
        self.uranium_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.uranium_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.uranium_titre = Label(self.cadre_ressources_joueur, text="uranium : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.uranium_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.uranium, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en hydrogene
        self.hydrogene_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.hydrogene_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.hydrogene_titre = Label(self.cadre_ressources_joueur, text="hydrogene : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.hydrogene_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.hydrogene, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en azote
        self.azote_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.azote_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.azote_titre = Label(self.cadre_ressources_joueur, text="azote : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.azote_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.azote, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en xenon
        self.xenon_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.xenon_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.xenon_titre = Label(self.cadre_ressources_joueur, text="Xenon : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.xenon_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.xenon, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en Moral
        self.moral_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.moral_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.moral_titre = Label(self.cadre_ressources_joueur, text="Moral : ", bg="grey4",
                                 fg="white").pack(side=LEFT)
        self.moral_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.moral, bg="grey40",
                                  fg="white").pack(side=LEFT)
        # Cadre ressource en Population
        self.population_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.population_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.population_titre = Label(self.cadre_ressources_joueur, text="Population : ", bg="grey4",
                                 fg="white").pack(side=LEFT,)
        self.population_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.population, bg="grey40",
                                  fg="white").pack(side=LEFT)
        self.creation_menu_lateral_g()

    def creer_boite_information(self, titre, message):
        messagebox.showinfo(titre, message)

    def afficher_arbre_competence(self):
        # self.creer_boite_information('Arbre de comptences', ' à venir')
        ttk.Style().configure("Treeview", background="purple",
                              foreground="red", fieldbackground="blue")
        root = Tk()
        columns = ('1','2','3')
        tree = ttk.Treeview(root, columns = columns, show = 'headings')

        tree.heading('1', text = 'Militaire')
        tree.heading('2', text = 'Diplomatique')
        tree.heading('3', text = 'Scienctifique ')

        tree.pack()










    def afficher_statistiques(self):
        self.creer_boite_information('Statistiques', 'à venir')


    def afficher_inventaire(self):
        self.creer_boite_information('Inventaire','à venir')

    def afficher_journal(self):
        self.creer_boite_information('Journal', 'à venir')

    def afficher_evenement(self):
        self.creer_boite_information('Événements', 'à venir')

    def afficher_joueurs(self):
        donate = str(self.modele.joueurs.keys())
        self.creer_boite_information('Joueurs', donate[11:-2] )








    def creation_menu_lateral_g(self):
        self.menu_btn = Frame(self.canevas, bg="grey80", width=100, height=450)
        self.menu_btn.pack(side=LEFT)

        self.btn_arbre_competences = Button(self.menu_btn, bg="grey50", text="Arbre de compétence", font=2, justify="center", command=self.afficher_arbre_competence)
        self.btn_stats = Button(self.menu_btn, bg="grey50", text="Statistiques", font=2, justify="center", command=self.afficher_statistiques)
        self.btn_inventaire = Button(self.menu_btn, bg="grey50", text="Inventaires", font=2, justify="center", command=self.afficher_inventaire)
        self.btn_journal = Button(self.menu_btn, bg="grey50", text="Journal", font=2, justify="center",command=self.afficher_journal)
        self.btn_evenement = Button(self.menu_btn, bg="grey50", text="Événements", font=2, justify="center", command=self.afficher_evenement)
        self.btn_joueurs = Button(self.menu_btn, bg="grey50", text="Joueurs", font=2, justify="center", command=self.afficher_joueurs)

        self.btn_arbre_competences.pack(side=TOP, fill=X, pady=5, padx=5)
        self.btn_stats.pack(side=TOP, fill=X, pady=5, padx=5)
        self.btn_inventaire.pack(side=TOP,  fill=X, pady=5, padx=5)
        self.btn_journal.pack(side=TOP, fill=X, pady=5, padx=5)
        self.btn_evenement.pack(side=TOP, fill=X, pady=5, padx=5)
        self.btn_joueurs.pack(side=TOP, fill=X,pady=5, padx=5)

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur=self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    def centrer_liste_objet(self,evt):
        info=self.info_liste.get(self.info_liste.curselection())
        print(info)
        liste_separee=info.split(";")
        type_vaisseau=liste_separee[0]
        id=liste_separee[1][1:]
        obj=self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        self.centrer_objet(obj)

    def calc_objets(self,evt):
        print("Univers = ",len(self.canevas.find_all()))

    def defiler_vertical(self, evt):
        # rep = self.scrollY.get()[0]
        rep = evt.y
        if evt.delta < 0:
            rep = rep + 0.01
        else:
            rep = rep - 0.01
        self.canevas.yview_moveto(rep)

    def defiler_horizon(self, evt):
        # rep = self.scrollX.get()[0]
        rep = evt.x
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

##### FONCTIONS DU SPLASH #########################################################################

    ###  FONCTIONS POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self,etat):
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
        rep=self.parent.reset_partie()

    def creer_partie(self):
        nom = self.nomsplash.get()
        self.parent.creer_partie(nom)


    ##### FONCTION DU LOBBY #############
    def update_lobby(self,dico):
        self.listelobby.delete(0,END)
        for i in dico:
            self.listelobby.insert(END,i[0])
        if self.parent.joueur_createur:
            self.btnlancerpartie.config(state=NORMAL)

    def inscrire_joueur(self):
        nom=self.nomsplash.get()
        urljeu=self.urlsplash.get()
        self.parent.inscrire_joueur(nom,urljeu)

    def lancer_partie(self):
        self.parent.lancer_partie()

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

        # self.afficher_ressources()
####################################################################################################

    def positionner_minicanevas(self,evt):
        x=evt.x
        y=evt.y

        pctx=x/self.taille_minimap
        pcty=y/self.taille_minimap

        xl=(self.canevas.winfo_width()/2)/self.modele.largeur
        yl=(self.canevas.winfo_height()/2)/self.modele.hauteur

        self.canevas.xview_moveto(pctx-xl)
        self.canevas.yview_moveto(pcty-yl)
        xl=self.canevas.winfo_width()
        yl=self.canevas.winfo_height()

    def afficher_decor(self, mod):
        # on cree un arriere fond de petites etoieles NPC pour le look
        for i in range(len(mod.systemes) * 50):
            x = random.randrange(int(mod.largeur))
            y = random.randrange(int(mod.hauteur))
            n = random.randrange(3) + 1
            col = random.choice(["LightYellow", "azure1", "pink"])
            self.canevas.create_oval(x, y, x + n, y + n, fill=col, tags=("fond",))
        # affichage des etoiles
        for i in mod.systemes:
            t = i.taille * self.zoom
            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80", outline=col,
                                     tags=(i.proprietaire, str(i.id), "SystemeSolaire",))
        # affichage des etoiles possedees par les joueurs
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].systemes_controlees:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=mod.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id),  "SystemeSolaire"))
                # on affiche dans minimap
                minix=j.x/self.modele.largeur*self.taille_minimap
                miniy=j.y/self.modele.hauteur*self.taille_minimap
                self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                                         fill=mod.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id), "SystemeSolaire"))

    def afficher_mini(self,evt): #univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.systemes:
                minix=j.x/self.modele.largeur*self.taille_minimap
                miniy=j.y/self.modele.hauteur*self.taille_minimap
                self.canevas_minimap.create_rectangle(minix, miniy, minix + 0, miniy + 0,
                                         fill="black",
                                         tags=("mini", "SystemeSolaire"))
        # # affichage des etoiles possedees par les joueurs
        # for i in mod.joueurs.keys():
        #     for j in mod.joueurs[i].etoilescontrolees:
        #         t = j.taille * self.zoom
        #         self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
        #                                  fill=mod.joueurs[i].couleur,
        #                                  tags=(j.proprietaire, str(j.id),  "SystemeSolaire"))



    def centrer_planemetemere(self,evt):
        self.centrer_objet(self.modele.joueurs[self.mon_nom].systeme_mere)

    def centrer_objet(self,objet):
        # permet de defiler l'écran jusqu'à cet objet
        x=objet.x
        y=objet.y

        x1=self.canevas.winfo_width()/2
        y1=self.canevas.winfo_height()/2

        pctx=(x-x1)/self.modele.largeur
        pcty=(y-y1)/self.modele.hauteur

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    # change l'appartenance d'une etoile et donc les propriétés des dessins les représentants
    def afficher_etoile(self,joueur,cible):
        joueur1=self.modele.joueurs[joueur]
        id=cible.id
        couleur=joueur1.couleur
        self.canevas.itemconfig(id,fill=couleur)
        self.canevas.itemconfig(id,tags=(joueur,id, "SystemeSolaire",))

    # ajuster la liste des vaisseaux
    def lister_objet(self,obj,id):
        self.info_liste.insert(END,obj+"; "+id)

    def creer_bien(self,evt):
        type_vaisseau=evt.widget.cget("text")
        self.parent.creer_bien(type_vaisseau)
        self.ma_selection=None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.afficher_ressources()



        if self.ma_selection != None:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[2] == "SystemeSolaire":
                for i in joueur.systemes_controlees:
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
                        i=joueur.flotte[j][i]
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
            vaisseau_local=[]
            for k in i.flotte:
                for j in i.flotte[k]:
                    j=i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    if k=="Vaisseau":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                      tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
                    elif k=="Cargo":
                        #self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j,tailleF,i,k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
        for t in self.modele.trou_de_vers:
            i=t.porte_a
            for i in [t.porte_a,t.porte_b]:
                self.canevas.create_oval(i.x-i.pulse,i.y-i.pulse,
                                         i.x+i.pulse,i.y+i.pulse,outline=i.couleur,width=2,fill="grey15",
                                         tags=("",i.id,"Porte_de_ver","objet_spatial"))

                self.canevas.create_oval(i.x-i.pulse,i.y-i.pulse,
                                         i.x+i.pulse,i.y+i.pulse,outline=i.couleur,width=2,fill="grey15",
                                         tags=("",i.id,"Porte_de_ver","objet_spatial"))

    def dessiner_cargo(self,obj,tailleF,joueur,type_obj):
        t=obj.taille*self.zoom
        a=obj.ang
        x,y=hlp.getAngledPoint(obj.angle_cible,int(t/4*3),obj.x,obj.y)
        dt=t/2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="yellow",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    def dessiner_cargo1(self,j,tailleF,i,k):
        self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                                 (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                 tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
    def cliquer_cosmos(self,evt):
        t=self.canevas.gettags(CURRENT)
        if t: # il y a des tags
            if t[0]==self.mon_nom: # et
                self.ma_selection=[self.mon_nom,t[1],t[2]]
                if t[2] == "SystemeSolaire":
                    self.afficher_systemes_info(t[1])
                    self.montrer_etoile_selection()
                elif t[2] == "Flotte":
                    self.montrer_flotte_selection()
                    self.information_etoile_cadre.pack_forget()
            elif ("SystemeSolaire" in t or "Porte_de_ver" in t ) and t[0]!=self.mon_nom:
                if self.ma_selection:
                    self.parent.cibler_flotte(self.ma_selection[1],t[1],t[2])
                self.ma_selection=None
                self.canevas.delete("marqueur")
        else: # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.ma_selection=None
            self.canevas.delete("marqueur")

    def montrer_etoile_selection(self):
        self.cadreinfochoix.pack(side = RIGHT,fill=BOTH)
        self.afficher_information_etoile()


    def montrer_flotte_selection(self):
        print("À IMPLANTER - FLOTTE de ",self.mon_nom)

    # Methodes pour multiselect#########################################################
    def debuter_multiselection(self,evt):
        self.debutselect=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
        x1,y1=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
        self.selecteur_actif=self.canevas.create_rectangle(x1,y1,x1+1,y1+1,outline="red",width=2,
                                                          dash=(2,2),tags=("","selecteur","",""))


    def afficher_multiselection(self,evt):
        if self.debutselect:
            x1,y1=self.debutselect
            x2,y2=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteur_actif,x1,y1,x2,y2)

    def terminer_multiselection(self,evt):
        if self.debutselect:
            x1,y1=self.debutselect
            x2,y2=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.debutselect=[]
            objchoisi=(list(self.canevas.find_enclosed(x1,y1,x2,y2)))
            for i in objchoisi:
                if self.parent.mon_nom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.objets_selectionnes.append(self.canevas.gettags(i)[2])

            self.canevas.delete("selecteur")

    ### FIN du multiselect

    # Fonction pour aller chercher les ressources du joueurs
    def afficher_ressources(self):
        joueur = self.modele.joueurs.get(self.mon_nom)

        # Ressources
        self.energie.set(str(joueur.systeme_mere.ressources.get('energie')))
        self.nourriture.set(str(joueur.systeme_mere.ressources.get('nourriture')))
        self.gold.set(str(joueur.systeme_mere.ressources.get('or')))
        self.fer.set(str(joueur.systeme_mere.ressources.get('fer')))
        self.cuivre.set(str(joueur.systeme_mere.ressources.get('cuivre')))
        self.titanite.set(str(joueur.systeme_mere.ressources.get('titanite')))
        self.uranium.set(str(joueur.systeme_mere.ressources.get('uranium')))
        self.hydrogene.set(str(joueur.systeme_mere.ressources.get('hydrogene')))
        self.azote.set(str(joueur.systeme_mere.ressources.get('azote')))
        self.xenon.set(str(joueur.systeme_mere.ressources.get('xenon')))
        self.moral.set(str(joueur.systeme_mere.ressources.get('moral')))
        self.population.set(str(joueur.systeme_mere.population))

    def afficher_systemes_info(self, cible):

        # print(cible + str(systeme))
        joueur = self.modele.joueurs.get(self.mon_nom)
        systeme = 0
        for systemes in joueur.systemes_controlees:
            if systemes.id == cible:
                systeme = systemes
                break

        # jooueur
        #
        # Ressources
        self.energie_sys.set(str(systeme.ressources.get('energie')))
        self.nourriture_sys.set(str(systeme.ressources.get('nourriture')))
        self.gold_sys.set(str(systeme.ressources.get('or')))
        self.fer_sys.set(str(systeme.ressources.get('fer')))
        self.cuivre_sys.set(str(systeme.ressources.get('cuivre')))
        self.titanite_sys.set(str(systeme.ressources.get('titanite')))
        self.uranium_sys.set(str(systeme.ressources.get('uranium')))
        self.hydrogene_sys.set(str(systeme.ressources.get('hydrogene')))
        self.azote_sys.set(str(systeme.ressources.get('azote')))
        self.xenon_sys.set(str(systeme.ressources.get('xenon')))
        self.moral_sys.set(str(systeme.ressources.get('moral')))
        self.population_sys.set(str(systeme.ressources.get('defense_art')))

        # Nom système
        nom = (str(joueur.systeme_mere.id))

        print("Système " + nom[3:])

        # Infrastructureà
        self.mine.set(str(len(systeme.infrastructures.get(Mine))))
        self.ecole.set(str(len(systeme.infrastructures.get(Ecole))))
        self.barraques.set(str(len(systeme.infrastructures.get(Barraques))))
        self.usine.set(str(len(systeme.infrastructures.get(Usine))))
        self.ferme.set(str(len(systeme.infrastructures.get(Ferme))))
        self.usine_traitement_gaz.set(str(len(systeme.infrastructures.get(UsineTraitementGaz))))
        self.centrale_nucleaire.set(str(len(systeme.infrastructures.get(CentraleNucleaire))))
        self.musee.set(str(len(systeme.infrastructures.get(Musee))))


    def afficher_information_etoile(self):
        self.information_etoile_cadre.pack(side=TOP, expand=1, fill=BOTH)
        self.root.update()








