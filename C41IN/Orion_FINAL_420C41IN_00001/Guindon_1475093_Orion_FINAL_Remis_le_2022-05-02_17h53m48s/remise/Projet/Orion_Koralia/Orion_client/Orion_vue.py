# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math
from systeme_solaire import *
#from Sprite_generator import Picture
from PIL import Image
import random
import re
from PIL import Image, ImageDraw
import os,os.path

class Vue():
    def __init__(self,parent,urlserveur,mon_nom,msg_initial):
        self.toggle_menu_reducteur = True
        self.parent=parent
        self.root=Tk()
        self.root.title("Je suis "+mon_nom)
        self.mon_nom=mon_nom
        # attributs
        self.taille_minimap=150
        self.padding_res_joueurs = 2
        self.width_res_systemes = 0
        self.nbr_cadre_res_systemes = 5
        self.afficher_infrastructure_exist = 0
        self.afficher_vaisseau_exist = 0
        self.couleur_texte_systemes = "yellow"
        self.tableau_systeme = []
        self.objets_selectionnes = []
        self.msg_box = None
        self.img = []
        self.tab_btn_bien = []
        '''
            Dictionnaire d'image selon les joueurs
        '''
        self.red = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.blue = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.lightgreen = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.yellow = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.lightblue = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.pink = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.dict_gold = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }
        self.purple = {
            "explorateur" : [],
            "cargo" : [],
            "combat" : [],
            "etoile" : []
        }

        # couleur d'ai

        self.orange = {
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }

        self.green = {
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }

        self.cyan ={
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }

        self.seagreen = {
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }

        self.turquoise1 = {
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }

        self.firebrick1 = {
            "explorateur": [],
            "cargo": [],
            "combat": [],
            "etoile": []
        }
        # Etoile sans propriétaire

        self.grey = {
            "etoile": []
        }

        self.cjoueur = {
            "red": self.red,
            "blue" : self.blue,
            "lightgreen" : self.lightgreen,
            "yellow" : self.yellow,
            "lightblue" : self.lightblue,
            "pink" : self.pink,
            "gold" : self.dict_gold,
            "purple" : self.purple,
            # ai
            "orange" : self.orange,
            "green" : self.green,
            "cyan" : self.cyan,
            "seagreen" : self.seagreen,
            "turquoise1" : self.turquoise1,
            "firebrick1" : self.firebrick1,
            # Étoile sans propriétaire
            "grey" : self.grey
        }
        '''
            Fin des dictionnaires d'images
        '''
        self.creer_image()  # créer les images pour le jeu
        #self.information_etoile_cadre = None
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
        self.systeme_courant = None
        # arbre de competences
        self.toggle_arbre_comptences_est_affiche= False
        #menu afficher journal
        self.toggle_menu_journal_est_affiche = False

        # bool Menu contruction_
        self.menu_construction_bien_est_affiche = False




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
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="navy")
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

        # image des étoiles
        choix = self.parent.image_splash()
        key_list = list(self.cjoueur.keys())
        self.canevas_splash.create_image(80, 400, image=self.cjoueur.get(key_list[choix[0]]).get("etoile")[0])
        self.canevas_splash.create_image(200, 425, image=self.cjoueur.get(key_list[choix[1]]).get("etoile")[0])
        # set-up l'icone
        self.root.wm_iconphoto(False, self.cjoueur.get("red").get("explorateur")[0])
        # on place les autres boutons
        self.canevas_splash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash

    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self) :
        # le cadre lobby, pour inscription des autres joueurs, remplace le splash
        self.cadrelobby=Frame(self.cadre_app)
        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480,bg="royal blue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby=Listbox(borderwidth=2,relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie=Button(text="Lancer partie",state=DISABLED,command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440,240,window=self.listelobby,width=200,height=400)
        self.canevaslobby.create_window(200,400,window=self.btnlancerpartie,width=100,height=30)
        self.canevaslobby.create_text(150,100, text="Jeu créé par : \n Jean-Christophe Caron \n Korallia Frenette \n Maxence Guindon \n Sebastian Perez \n Karl Robillard-Marchand", fill="white", font="bold")
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


        self.cadrejeu.columnconfigure(0,weight=1)
        self.cadrejeu.rowconfigure(0,weight=1)
        self.canevas.bind("<ButtonPress-1>",self.info_cosmos)
        self.canevas.tag_bind(ALL,"<ButtonPress-1>",self.info_cosmos)
        self.canevas.bind("<ButtonPress-3>",self.event_cosmos)
        self.canevas.tag_bind(ALL,"<ButtonPress-3>",self.event_cosmos)
        self.canevas.bind("<ButtonPress-3>",self.click_cosmos)

        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)

        # bouger sur la map
        self.canevas.bind("<ButtonPress-1>", self.point_depart)
        self.canevas.bind("<B1-Motion>", self.bouger_map)

        self.creer_cadre_outils()

        self.cadrejeu.pack(side=LEFT,expand=1,fill=BOTH)
        return self.cadrepartie

    def uptade_log(self):
        joueur = self.modele.joueurs.get(self.mon_nom)
        if(len(joueur.log)!=0):
            systeme = str(joueur.log[-1][0])
            self.info_liste.delete(0)
            self.info_liste.insert(0, "Systeme solaire "+systeme[2:-2])




    def creer_cadre_outils(self):
        self.cadreoutils=Frame(self.cadrepartie,width=200,height=50,bg="darkgrey")
        self.cadreoutils.pack(side=BOTTOM,fill=X)


        #
        self.cadreinfoliste=Frame(self.cadreoutils)
        # self.label_temp = Label(self.cadreinfoliste, text= "plz donate").pack()
        # self.energie_valeur = Label(self.energie_frame, text="", textvariable=self.energie_sys, bg="black",
        #                             fg="white").pack(side=LEFT)

        ##GROS SCROLL BAR BLANC.

        self.scroll_liste_Y=Scrollbar(self.cadreinfoliste,orient=VERTICAL)
        self.info_liste=Listbox(self.cadreinfoliste,width=20,height=6,yscrollcommand = self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-3>",self.centrer_liste_objet)
        self.info_liste.grid(column=0,row=0,sticky=W+E+N+S)
        self.scroll_liste_Y.grid(column=1,row=0,sticky=N+S)

        #NOTRE CODE #

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

        # ressources Joueur
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

        self.specialistes = StringVar()
        self.specialistes.set("0")

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

        # Cadre ressources en specialiste
        self.specialistes_frame_res = Frame(self.info_etoile_population, bg="grey69")
        self.specialistes_frame_res.pack(side=TOP, padx=self.padding_res_joueurs)
        self.specialistes_titre_res = Label(self.specialistes_frame_res, text="Specialiste : ", bg="grey4",
                                      fg=self.couleur_texte_systemes).pack(side=LEFT)
        self.specialistes_valeur_res = Label(self.specialistes_frame_res, text="", textvariable=self.specialistes, bg="black",
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
        self.cadreinfochoix = Frame(self.cadreinfo, width=150, height=50, bg="grey30")
        self.creer_infra = Button(self.cadreinfochoix, text="Infrastructure")
        self.creer_infra.bind("<Button>", self.afficher_infrastructure)
        self.creer_infra.pack()


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

        self.age = StringVar()
        self.age.set("0")

        self.evtn_contenu = StringVar()
        self.evtn_contenu.set("0")

        # Cadre de pour détacher les ressources des boutons de statistiques à gauche
        self.btn_menu_reductible = Button(self.cadre_ressources_joueur, text="Menu", command = self.afficher_menu_reducteur, bg= "black", fg="white")
        self.btn_menu_reductible.pack(side=LEFT)
        self.cadre_detache = Label(self.cadre_ressources_joueur, width=10, bg="gray69").pack(side=LEFT)

        #cadre event

        self.messageevt = StringVar()
        self.messageevt.set("")


        self.evnt_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.evnt_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.evnt_titre = Label(self.cadre_ressources_joueur, text="Event : ", bg="grey4",
                                fg="white").pack(side=LEFT)
        self.evt_valeur = Label(self.cadre_ressources_joueur,text="", textvariable=self.messageevt,
                                bg="grey40",
                                fg="white").pack(side=LEFT)
        # cadre Age


        #cadre Age
        self.age_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.age_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.age_titre = Label(self.cadre_ressources_joueur, text="Age : ", bg="grey4",
                                        fg="white").pack(side=LEFT)
        self.age_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.age,
                                         bg="grey40",
                                         fg="white").pack(side=LEFT)

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

        # Cadre ressource  en specialistes
        self.specialistes_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
        self.specialistes_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
        self.specialistes_titre = Label(self.cadre_ressources_joueur, text="Specialistes : ", bg="grey4",
                                        fg="white").pack(side=LEFT)
        self.specialistes_valeur = Label(self.cadre_ressources_joueur, text="", textvariable=self.specialistes, bg="grey40",
                                         fg="white").pack(side=LEFT)
        self.creation_menu_lateral_g()

    def creer_boite_information(self, titre, message, joueur, choix=None):
        # exemple : self.creer_boite_information("test", "Voulez-vous vraiment choisir cette étoile", True)
        if joueur == self.mon_nom:
            joueurConcerner = self.modele.joueurs.get(self.mon_nom)
            joueurConcerner.event = message
            self.messageevt.set(message)

            # self.evnt_frame = Frame(self.cadre_ressources_joueur, bg="grey69")
            # self.evnt_frame.pack(side=LEFT, padx=self.padding_res_joueurs)
            # self.evnt_titre = Label(self.cadre_ressources_joueur, text="Event : ", bg="grey4",
            #                         fg="white").pack(side=LEFT)
            # self.evt_valeur = Label(self.cadre_ressources_joueur, text=message,
            #                         bg="grey40",
            #                         fg="white").pack(side=LEFT)
            return 1

    def creer_cadre_contruction(self):
        if self.menu_construction_bien_est_affiche == False:

            joueur = self.liste_joueurs.get(self.mon_nom)
            dict_production = joueur.bien_production

            if len(self.tab_btn_bien) >0 :
                for btn in self.tab_btn_bien:
                    btn.destroy()

            for key in dict_production.keys():
                # recherche_complete_label = Label(recherches_debloques_LF, text=liste_recherches_completees[key], bg="grey4",
                #                                  fg="yellow").pack(side=TOP, fill=BOTH, padx=self.padding_res_joueurs)
                btn_tmp = Button(self.cadreinfochoix, text=key)
                btn_tmp.bind("<Button>", self.creer_bien)
                btn_tmp.pack()
                self.tab_btn_bien.append(btn_tmp)

            self.menu_construction_bien_est_affiche = True


    def afficher_menu_journal(self):
            joueur = self.modele.joueurs.get(self.mon_nom)
            couleur = joueur.couleur

            self.toggle_menu_journal_est_affiche = True
            self.root.afficher_journal = Toplevel()
            self.root.afficher_journal.wm_iconphoto(False, self.cjoueur.get(couleur).get("etoile")[0])
            self.frame_afficher_journal = Frame(self.root.afficher_journal, width =450, height=350, bg ="black")
            self.frame_afficher_journal.pack()
            self.menu_journal_LB = LabelFrame(self.frame_afficher_journal, width=350, height=32,
                                                   text=" Journal", bg="black",
                                                   fg=self.couleur_texte_systemes,
                                                   labelanchor=NE, relief=RAISED)
            self.menu_journal_LB.pack()
            if (len(joueur.log) != 0):
                for log in joueur.log:
                    id = str(log[0])
                    if log [1]!="":
                        action = str(log[1])[2:-2]
                    if str(log[2])[1:-1]!="":
                        cargo = log[2]


                    label_tmp = Label( self.menu_journal_LB , text="START \n "
                                                                   "je suis arrivé sur " + id[2:-2] + action , bg="grey4",
                                        fg="yellow").pack(side=TOP, fill=BOTH, padx=self.padding_res_joueurs)

                    for ressources in cargo:
                        ressource = str(ressources)[2:-3]
                        ressource.replace("'","")
                        label_tmp1 = Label(self.menu_journal_LB, text=ressource , bg="grey4",
                                      fg="yellow").pack(side=TOP, fill=BOTH, padx=self.padding_res_joueurs)

                    label_tmp2 = Label(self.menu_journal_LB, text="OVER \n", bg="grey4",
                                       fg="yellow").pack(side=TOP, fill=BOTH, padx=self.padding_res_joueurs)

        #self.root.afficher_journal.protocol("WM_DELETE_WINDOW", self.fermer_menu_journal)


    def fermer_menu_journal(self):
        self.root.afficher_journal.destroy()
        self.toggle_menu_journal_est_affiche = False




    def afficher_arbre_competence(self ):
        joueur = self.modele.joueurs[self.mon_nom]
        couleur = joueur.couleur
        if not self.toggle_arbre_comptences_est_affiche:
            self.toggle_arbre_comptences_est_affiche = True
            joueur = self.modele.joueurs.get(self.mon_nom)
            joueur.mise_a_jour_recherches()

            dict_recherches_possibles = joueur.recherches_possibles
            liste_recherches_completees = joueur.recherches_completee
            liste_artefacts = joueur.artefacts

            self.root_arbrecompetence = Toplevel()
            self.root_arbrecompetence.wm_iconphoto(False, self.cjoueur.get(couleur).get("etoile")[0])
            self.frame22 = Frame(self.root_arbrecompetence,width=450,height=350, bg ="black")
            self.sous_frame22 = Frame(self.frame22,width=450,height=350, bg ="blue")
            self.frame22.pack()
            self.sous_frame22.pack(side=TOP)
            recherches_debloques_LF = LabelFrame(self.sous_frame22, width=350, height=32,
                                                                text=" Recherches Debloqués", bg="black",
                                                                fg=self.couleur_texte_systemes,
                                                                labelanchor=NE, relief=RAISED)
            recherches_debloques_LF.pack(side = LEFT)
            artefactes_debloques_LF = LabelFrame(self.sous_frame22, width=350, height=32,
                                                 text=" Artefactes Debloqués", bg="black",
                                                 fg=self.couleur_texte_systemes,
                                                 labelanchor=NE, relief=RAISED)
            artefactes_debloques_LF.pack(side = RIGHT, fill = BOTH)

            recherches_disponibles_LF = LabelFrame(self.frame22, width=350, height=32,
                                                 text=" Recherches Disponibles", bg="black",
                                                 fg=self.couleur_texte_systemes,
                                                 labelanchor=NE, relief=RAISED)
            recherches_disponibles_LF.pack()


            for key in range(len(liste_recherches_completees)):
                recherche_complete_label=Label(recherches_debloques_LF,text = liste_recherches_completees[key], bg="grey4",
                                                fg="yellow").pack(side=TOP, fill = BOTH, padx=self.padding_res_joueurs)

            for key in range(len(liste_artefacts)):
                artefacts_label=Label(artefactes_debloques_LF,text = liste_artefacts[key], bg="grey4",
                                                fg="yellow").pack(side=TOP, fill = BOTH, padx=self.padding_res_joueurs)

            for key in dict_recherches_possibles.keys():
                # grey69
                recherche1_frame = Frame(recherches_disponibles_LF, bg="black")
                recherche1_frame.pack(side=TOP, fill = Y)
                recherche1_label = Label(recherche1_frame, text= "debloquer" , bg="grey4",
                                                fg="yellow").pack(side=LEFT, fill = BOTH)

                btn_accept = Button(recherche1_frame, text=key)
                btn_accept.bind("<Button>",self.fonction_click_btn_unlock)
                btn_accept.pack(side = RIGHT, padx=self.padding_res_joueurs+20)

        self.root_arbrecompetence.protocol("WM_DELETE_WINDOW", self.fermer_arbre_competences)






    def fermer_arbre_competences(self):
        self.root_arbrecompetence.destroy()
        self.toggle_arbre_comptences_est_affiche = False

    def fonction_click_btn_unlock(self,evt):
        texte = evt.widget.cget("text")
        choix = str(texte)
        self.parent.creer_recherche(choix)
        self.fermer_arbre_competences()
        # # print(choix)

        # def creer_infrastructure(self, evt):
        #     # commencer à coder la fonction, aide des modeleurs requises
        #     type_infrastructure = str(evt.widget.cget("text"))
        #     type_infrastructure = re.sub(r"\s+", "", type_infrastructure)
        #     print(type_infrastructure)
        #     self.parent.creer_infrastructure(type_infrastructure, self.systeme_courant)
        #     self.ma_selection = None
        #     pass




    def afficher_statistiques(self):
        self.creer_boite_information('Statistiques', 'à venir')


    def afficher_inventaire(self):
        self.creer_boite_information('Inventaire','à venir')

    def afficher_journal(self):
        # self.creer_boite_information('Journal', 'à venir')
        self.afficher_menu_journal()


    def afficher_evenement(self):
        self.creer_boite_information('Événements', 'à venir')

    def afficher_joueurs(self):
        donate = str(self.modele.joueurs.keys())
        joueur = self.liste_joueurs.get(self.mon_nom)
        self.creer_boite_information('Joueurs', donate[11:-2], self.mon_nom )

    def afficher_infrastructure(self, evt):
        if self.afficher_infrastructure_exist:
            self.information_etoile_infrastructure.pack_forget()
        self.afficher_infrastructure_exist = 1
        self.information_etoile_cadre.pack_forget()
        self.information_etoile_infrastructure = LabelFrame(self.cadre_etoile_information, width=150, height=32,
                                                   text=" Créer infrastructure", bg="black", fg=self.couleur_texte_systemes,
                                                   labelanchor=NE, relief=RAISED)

        self.info_mine = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                              text="Mine", bg="black", fg=self.couleur_texte_systemes, labelanchor=N,
                                              relief=RAISED)
        self.info_mine.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_musee = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                          text="Musée", bg="black",
                                          fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_musee.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_ecole = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                                     text="Ecole", bg="black",
                                                     fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_ecole.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_barraques = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                                 text="Barraques", bg="black",
                                                 fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_barraques.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_usine = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                          text="Usine", bg="black",
                                          fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_usine.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_ferme = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                     text="Ferme", bg="black",
                                     fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_ferme.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_usine_traitement_gaz = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                     text="Usine traitement gaz", bg="black",
                                     fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_usine_traitement_gaz.pack(side=LEFT, padx=2, expand=1, fill=BOTH)

        self.info_centrale_nucleaire = LabelFrame(self.information_etoile_infrastructure, width=50, height=32,
                                                    text="Centrale nucleaire", bg="black",
                                                    fg=self.couleur_texte_systemes, labelanchor=N, relief=RAISED)
        self.info_centrale_nucleaire.pack(side=LEFT, padx=2, expand=1, fill=BOTH)


        self.cadre_infrastructure_g = Label(self.info_etoile_infrastructure, bg="black")
        self.cadre_infrastructure_d = Label(self.info_etoile_infrastructure, bg="black")
        self.cadre_infrastructure_g.pack(side=LEFT, expand=1, fill=BOTH)
        self.cadre_infrastructure_d.pack(side=LEFT, expand=1, fill=BOTH)

        # Variable pour la progression des créations d'infrastructures
        # infrastructure
        self.progres_mine = StringVar()
        self.progres_mine.set("0")

        self.progres_musee = StringVar()
        self.progres_musee.set("0")

        self.progres_ecole = StringVar()
        self.progres_ecole.set("0")

        self.progres_barraques = StringVar()
        self.progres_barraques.set("0")

        self.progres_usine = StringVar()
        self.progres_usine.set("0")

        self.progres_ferme = StringVar()
        self.progres_ferme.set("0")

        self.progres_usine_traitement_gaz = StringVar()
        self.progres_usine_traitement_gaz.set("0")

        self.progres_centrale_nucleaire = StringVar()
        self.progres_centrale_nucleaire.set("0")

        # Cadre mine
        self.mine_frame = Frame(self.info_mine, bg="grey69")
        self.mine_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        #Bouton
        self.btn_creer_mine = Button(self.info_mine, text="Mine")
        self.btn_creer_mine.bind("<Button>",self.creer_infrastructure)
        self.btn_creer_mine.pack(side=TOP)

        # Cadre usine
        self.usine_frame = Frame(self.info_usine, bg="grey69")
        self.usine_frame.pack(side=TOP, padx=self.padding_res_joueurs)
        #Bouton
        self.btn_creer_usine = Button(self.info_usine, text="Usine")
        self.btn_creer_usine.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_usine.pack(side=TOP)

        # Cadre ferme
        self.ferme_frame = Frame(self.info_ferme, bg="grey69")
        self.ferme_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_ferme = Button(self.info_ferme, text="Ferme")
        self.btn_creer_ferme.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_ferme.pack(side=TOP)

        # Cadre musee
        self.musee_frame = Frame(self.info_musee, bg="grey69")
        self.musee_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_musee = Button(self.info_musee, text="Musee")
        self.btn_creer_musee.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_musee.pack(side=TOP)

        # Cadre ecole
        self.ecole_frame = Frame(self.info_ecole, bg="grey69")
        self.ecole_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_ecole = Button(self.info_ecole, text="Ecole")
        self.btn_creer_ecole.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_ecole.pack(side=TOP)

        # Cadre barraques
        self.barraques_frame = Frame(self.info_barraques, bg="grey69")
        self.barraques_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_barraques = Button(self.info_barraques, text="Barraques")
        self.btn_creer_barraques.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_barraques.pack(side=TOP)

        # Cadre UsineTraitementGaz
        self.usine_traitement_gaz_frame = Frame(self.info_usine_traitement_gaz, bg="grey69")
        self.usine_traitement_gaz_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_usine_traitement_gaz_frame = Button(self.info_usine_traitement_gaz, text="Usine Traitement Gaz")
        self.btn_creer_usine_traitement_gaz_frame.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_usine_traitement_gaz_frame.pack(side=TOP)

        # Cadre musee
        self.centrale_nucleaire_frame = Frame(self.info_centrale_nucleaire, bg="grey69")
        self.centrale_nucleaire_frame.pack(side=TOP, padx=self.padding_res_joueurs)

        # Bouton
        self.btn_creer_centrale_nucleaire = Button(self.info_centrale_nucleaire, text="Centrale Nucleaire")
        self.btn_creer_centrale_nucleaire.bind("<Button>", self.creer_infrastructure)
        self.btn_creer_centrale_nucleaire.pack(side=TOP)


        self.information_etoile_infrastructure.pack(side=TOP, expand=1, fill=BOTH)
        

    def creation_menu_lateral_g(self):

        self.menu_btn = Frame(self.canevas, bg="grey80", width=100, height=450)

        self.btn_arbre_competences = Button(self.menu_btn, bg="grey50", text="Arbre de compétence", font=2, justify="center", command= lambda : self.afficher_arbre_competence())
        # self.btn_stats = Button(self.menu_btn, bg="grey50", text="Statistiques", font=2, justify="center", command=self.afficher_statistiques)
        # self.btn_inventaire = Button(self.menu_btn, bg="grey50", text="Inventaires", font=2, justify="center", command=self.afficher_inventaire)
        self.btn_journal = Button(self.menu_btn, bg="grey50", text="Journal", font=2, justify="center",command=self.afficher_journal)
        #self.btn_evenement = Button(self.menu_btn, bg="grey50", text="Événements", font=2, justify="center", command=self.afficher_evenement)
        self.btn_joueurs = Button(self.menu_btn, bg="grey50", text="Joueurs", font=2, justify="center", command=self.afficher_joueurs)

        self.btn_arbre_competences.pack(side=TOP, fill=X, pady=5, padx=5)
        # self.btn_stats.pack(side=TOP, fill=X, pady=5, padx=5)
        # self.btn_inventaire.pack(side=TOP,  fill=X, pady=5, padx=5)
        self.btn_journal.pack(side=TOP, fill=X, pady=5, padx=5)
        #self.btn_evenement.pack(side=TOP, fill=X, pady=5, padx=5)
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

    def point_depart(self, evt):
        self.canevas.scan_mark(evt.x, evt.y)

    def bouger_map(self,evt):
        self.canevas.scan_dragto(evt.x, evt.y, gain=1)

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
        self.liste_joueurs = modele.joueurs
        joueur = self.modele.joueurs[self.mon_nom]
        couleur = joueur.couleur
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.root.wm_iconphoto(False, self.cjoueur.get(couleur).get("explorateur")[0])

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)
        self.afficher_decor(modele)
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
        # for i in mod.systemes:
        #     t = i.taille * self.zoom
        #     self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
        #                              fill="grey11", outline="grey11",
        #                              tags=(i.proprietaire, str(i.id), "SystemeSolaire",)) # fill="grey80", outline=col,
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
        self.canevas.itemconfig(id)
        self.canevas.itemconfig(id,tags=(joueur,id, "SystemeSolaire",))

    # ajuster la liste des vaisseaux
    def lister_objet(self,obj,id):
        self.info_liste.insert(END,obj+"; "+id)

    def creer_bien(self,evt):
        type_bien=evt.widget.cget("text")
        # if type_bien == "Destroyer" and not self.destroyer_possible:
        #     self.creer_boite_information("manque de fonds", "vous ne pouvez pas encore acheter ce ben-ci")
        #     return None
        self.parent.creer_bien(type_bien)
        self.ma_selection=None
        self.canevas.delete("marqueur")
        #self.cadreinfochoix.pack_forget()


    def creer_infrastructure(self, evt):
        # commencer à coder la fonction, aide des modeleurs requises
        type_infrastructure = str(evt.widget.cget("text"))
        type_infrastructure = re.sub(r"\s+", "",type_infrastructure)
        print(type_infrastructure)
        self.parent.creer_infrastructure(type_infrastructure,self.systeme_courant)
        self.ma_selection=None
        pass


    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("SystemeSolaire")
        self.canevas.delete("marqueur")
        self.afficher_ressources()
        self.afficher_sys_dans_rayon_mere(mod)

        if self.ma_selection != None:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[0] != "":
                if self.ma_selection[2] == "SystemeSolaire":
                    for i in joueur.systemes_controlees:
                        if i.id == self.ma_selection[1]:
                            x = i.x
                            y = i.y
                            t = 10 * self.zoom
                            self.canevas.create_oval(x - i.get_fog(), y - i.get_fog(), x + i.get_fog(), y + i.get_fog(),
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
                                self.canevas.create_oval(x - i.rayon, y - i.rayon, x + i.rayon, y + i.rayon,
                                                              dash=(2, 2), outline = "gold",
                                                              tags=("multiselection", "marqueur"))

        # afficher asset des joueurs
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            vaisseau_local=[]
            for k in i.flotte:
                for j in i.flotte[k]:
                    j=i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    self.dessiner_vaisseau(j,tailleF,i,k)

        for t in self.modele.trou_de_vers:
            i=t.porte_a
            for i in [t.porte_a,t.porte_b]:
                self.canevas.create_oval(i.x-i.pulse,i.y-i.pulse,
                                         i.x+i.pulse,i.y+i.pulse,outline=i.couleur,width=2,fill="grey15",
                                         tags=("",i.id,"Porte_de_ver","objet_spatial"))

                self.canevas.create_oval(i.x-i.pulse,i.y-i.pulse,
                                         i.x+i.pulse,i.y+i.pulse,outline=i.couleur,width=2,fill="grey15",
                                         tags=("",i.id,"Porte_de_ver","objet_spatial"))

    def dessiner_vaisseau(self, obj, tailleF, joueur, type_obj):
        couleur = joueur.couleur
        t=obj.taille*self.zoom
        a=obj.ang
        x,y=hlp.getAngledPoint(obj.angle_cible,int(t/4*3),obj.x,obj.y)
        dt=t/2

        position = self.position_mouvement(obj)
        if type_obj == "Cargo":
            self.canevas.create_image((obj.x), (obj.y), image=self.cjoueur.get(couleur).get("cargo")[position],
                                      tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        elif type_obj == "Vaisseau":
            self.canevas.create_image((obj.x), (obj.y), image=self.cjoueur.get(couleur).get("explorateur")[position], tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

        elif type_obj == "Combat":
            self.canevas.create_image((obj.x), (obj.y), image=self.cjoueur.get(couleur).get("combat")[position],
                                      tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    def position_mouvement(self, obj):
        angle = (((obj.angle_cible+ 2*math.pi) *180)/math.pi)%360
        pos = 0
        if 23 >= angle > 0 or 360 >= angle >= 338:
            pos = 6
        elif 24 <= angle <= 68:
            pos = 5
        elif 69 <= angle <= 113:
            pos = 4
        elif 114 <= angle <= 158:
            pos = 3
        elif 159 <= angle <= 203:
            pos = 2
        elif 204 <= angle <= 248:
            pos = 1
        elif 249 <= angle <= 293:
            pos = 0
        elif 294 <= angle <= 337:
            pos = 7
        return pos

    def click_cosmos(self, evt):
        print(evt.x, evt.y)
        #return (evt.x, evt.y)

    def info_cosmos(self, evt):
        self.effacer_cadre_info()
        t = self.canevas.gettags(CURRENT)
        if t:  # il y a des tags
            if t[0] == self.mon_nom:  # et
                self.ma_selection = [self.mon_nom, t[1], t[2]]
                if t[2] == "SystemeSolaire":
                    self.afficher_systemes_info(t[1])
                    self.montrer_etoile_selection()
                    #si non ouvert
                    self.creer_cadre_contruction()
                elif t[2] == "Flotte":
                    self.montrer_flotte_selection(t[1])
                    self.information_etoile_cadre.pack_forget()
            else:
                if t[2] == "SystemeSolaire":
                    self.afficher_systemes_info(t[1])
                    self.afficher_information_etoile()
                    self.canevas.delete("marqueur")
                    #self.montrer_etoile_selection()
                    #self.creer_cadre_contruction()
        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.ma_selection = None
            self.effacer_cadre_info()
            self.afficher_information_etoile()
            self.canevas.delete("marqueur")

    def event_cosmos(self, evt):
        t = self.canevas.gettags(CURRENT)
        if self.ma_selection is not None:
            tag = self.ma_selection[2]
            if t:  # il y a des tags
                if tag == "Flotte":
                    self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                self.ma_selection = None
                self.canevas.delete("marqueur")
            else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
                print("Region inconnue")
                self.ma_selection = None
                self.canevas.delete("marqueur")

    def montrer_etoile_selection(self):
        self.cadreinfochoix.pack(side = RIGHT,fill=BOTH)
        self.afficher_information_etoile()

        # if self.menu_construction_bien_est_affich
        ##toggle TEST ici



    def montrer_flotte_selection(self, id):
        self.afficher_information_vaisseau(id)
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

        dict = joueur.systeme_mere.retourner_ressources()

        # Ressources
        #Mettre l'age actuel ici a partir d'un dictionnaire
        self.age.set(str(joueur.age))
        #Mettre log ici



        self.energie.set(int(dict.get('energie')/1000))
        self.nourriture.set(int(dict.get('nourriture')/1000))
        self.gold.set(int(dict.get('or')/1000))
        self.fer.set(int(dict.get('fer')/1000))
        self.cuivre.set(int(dict.get('cuivre')/1000))
        self.titanite.set(int(dict.get('titanite')/1000))
        self.uranium.set(int(dict.get('uranium')/1000))
        self.hydrogene.set(int(dict.get('hydrogene')/1000))
        self.azote.set(int(dict.get('azote')/1000))
        self.xenon.set(int(dict.get('xenon')/1000))

        self.moral.set(int(dict.get('moral')))
        self.population.set(dict.get('population'))
        self.specialistes.set(dict.get('specialiste'))

    def afficher_systemes_info(self, cible):
        joueur = self.modele.joueurs.get(self.mon_nom)
        systeme = 0
        for systemes in joueur.systemes_controlees:
            if systemes.id == cible:
                systeme = systemes
                if systeme.id == joueur.systeme_mere.id:
                    self.creer_cadre_contruction()
                    break

        if systeme == 0:
            for sys in self.modele.systemes:
                if sys.id == cible:
                    systeme = sys
                    self.menu_construction_bien_est_affiche = False
                    break

        dict = systeme.retourner_infrasctructure()
        dict_res = systeme.retourner_ressources()
        self.systeme_courant = systeme
        #print(dict_res)

        if systeme.proprietaire == "":
            self.energie_sys.set(0)
            self.nourriture_sys.set(0)
            self.gold_sys.set(0)
            self.fer_sys.set(0)
            self.cuivre_sys.set(0)
            self.titanite_sys.set(0)
            self.uranium_sys.set(0)
            self.hydrogene_sys.set(0)
            self.azote_sys.set(0)
            self.xenon_sys.set(0)
            self.moral_sys.set(0)
            self.population_sys.set(0)

            self.mine.set(0)
            self.ecole.set(0)
            self.barraques.set(0)
            self.usine.set(0)
            self.ferme.set(0)
            self.usine_traitement_gaz.set(0)
            self.centrale_nucleaire.set(0)
            self.musee.set(0)
        else:
            self.energie_sys.set(int(dict_res.get('energie')/1000))
            self.nourriture_sys.set(int(dict_res.get('nourriture')/1000))
            self.gold_sys.set(int(dict_res.get('or')/1000))
            self.fer_sys.set(int(dict_res.get('fer')/1000))
            self.cuivre_sys.set(int(dict_res.get('cuivre')/1000))
            self.titanite_sys.set(int(dict_res.get('titanite')/1000))
            self.uranium_sys.set(int(dict_res.get('uranium')/1000))
            self.hydrogene_sys.set(int(dict_res.get('hydrogene')/1000))
            self.azote_sys.set(int(dict_res.get('azote')/1000))
            self.xenon_sys.set(int(dict_res.get('xenon')/1000))
            self.moral_sys.set(int(dict_res.get('moral')))
            self.population_sys.set(int(dict_res.get('defense_art')))

            # Infrastructure
            self.mine.set(dict.get("Mine"))
            self.ecole.set(dict.get("Ecole"))
            self.barraques.set(dict.get("Barraques"))
            self.usine.set(dict.get("Usine"))
            self.ferme.set(dict.get("Ferme"))
            self.usine_traitement_gaz.set(dict.get("UsineTraitementGaz"))
            self.centrale_nucleaire.set(dict.get("CentraleNucleaire"))
            self.musee.set(dict.get("Musee"))


    def afficher_information_etoile(self):
        self.information_etoile_cadre.pack(side=TOP, expand=1, fill=BOTH)
        self.root.update()

    def effacer_cadre_info(self):
        if self.afficher_infrastructure_exist:
            self.information_etoile_infrastructure.pack_forget()
        if self.afficher_vaisseau_exist:
            self.info_vaisseau.pack_forget()
        self.cadreinfochoix.pack_forget()

    def afficher_information_vaisseau(self, id):
        if self.afficher_vaisseau_exist:
            self.info_vaisseau.pack_forget()
        self.afficher_vaisseau_exist = 1
        self.information_etoile_cadre.pack_forget()

        tab_info = self.parent.update_v_info(id)

        # Information importante du joueur
        self.v_energie = StringVar()
        self.v_espace = StringVar()
        self.v_type = StringVar()
        self.v_id = StringVar()

        self.v_energie.set(str(tab_info[0]))
        self.v_espace.set(str(tab_info[1]))
        self.v_type.set(str(tab_info[2]))
        nom = str(tab_info[2]) + " " + id[3:]
        self.v_id.set(nom)

        self.info_vaisseau = Frame(self.cadre_etoile_information, bg="black")
        self.v_nom = Label(self.info_vaisseau, text="", textvariable=self.v_id, bg="black", fg=self.couleur_texte_systemes).pack(side=TOP)
        self.v_info_energie = Label(self.info_vaisseau, text="", textvariable=self.v_energie, bg="black", fg=self.couleur_texte_systemes).pack(side=TOP)
        self.v_info_espace = Label(self.info_vaisseau, text="", textvariable=self.v_espace, bg="black",
                                    fg=self.couleur_texte_systemes).pack(side=TOP)
        self.v_info_type = Label(self.info_vaisseau, text="", textvariable=self.v_type, bg="black",
                                    fg=self.couleur_texte_systemes).pack(side=TOP)
        self.info_vaisseau.pack(fill=BOTH)

    def afficher_menu_reducteur(self):
        if self.toggle_menu_reducteur is True :
            self.menu_btn.pack(side=LEFT)
            self.toggle_menu_reducteur = False
            #mettre toggle ici
        else :
            self.menu_btn.pack_forget()
            self.toggle_menu_reducteur = True

    def afficher_sys_dans_rayon_mere(self, mod):
        joueur = mod.joueurs.get(self.mon_nom)
        couleur = joueur.couleur

        sys = joueur.systemes_controlees
        for etoile in sys:
            for i in mod.systemes:
                if etoile.x - etoile.get_fog() <= i.x <= etoile.x + etoile.get_fog():
                    if etoile.y - etoile.get_fog() <= i.y <= etoile.y + etoile.get_fog():
                        if i.proprietaire != "":
                            if i.proprietaire == joueur:
                                t = i.taille * self.zoom
                                self.canevas.create_image(i.x, i.y, image=self.cjoueur.get(couleur).get("etoile")[0],
                                                     tags=(i.proprietaire, str(i.id), "SystemeSolaire",))
                            else:
                                autrej = mod.joueurs.get(i.proprietaire)
                                couleur = autrej.couleur
                                self.canevas.create_image(i.x, i.y, image=self.cjoueur.get(couleur).get("etoile")[0],
                                                          tags=(i.proprietaire, str(i.id), "SystemeSolaire",))
                        else:
                            t = i.taille * self.zoom
                            self.canevas.create_image(i.x, i.y, image=self.cjoueur.get("grey").get("etoile")[0],
                                                     tags=(i.proprietaire, str(i.id),
                                                           "SystemeSolaire",))
    def creer_image(self):

        img_etoile = []
        img_explorateur = []
        img_cargo = []
        img_combat = []

        couleur_p = {
            "red" : (255, 0, 0),
            "blue" :(0,0,255),
            "lightgreen" : (31, 128, 31),
            "yellow" : (189, 173, 36),
            "lightblue" : (44, 111, 121),
            "pink" : (157, 76, 90),
            "gold" : (117, 101, 15),
            "purple" : (128,0,128),
            # AI
            "orange" : (252,150,4),
            "green" : (5,135,64),
            "cyan" : (0, 179, 255),
            "seagreen" : (18,55,34),
            "turquoise1" : (64,224,208),
            "firebrick1" : (70,13,13),
            # Etoile sans propriétaire
            "grey" : (110, 108, 108)
        }
        couleur_s = {
            "red": (252, 86, 86),
            "blue": (74, 171, 255),
            "lightgreen": (144, 238, 144),
            "yellow": (255, 255, 0),
            "lightblue": (173, 216, 230),
            "pink": (255, 192, 203),
            "gold": (255, 215, 0),
            "purple": (230, 12, 230),
            # AI
            "orange" : (252,194,4),
            "green": (0, 176, 80),
            "cyan": (0, 255, 255),
            "seagreen" : (18,110,34),
            "turquoise1": (175,238,238),
            "firebrick1": (153,13,13),
            # Etoile sans propriétaire
            "grey": (148, 145, 145)
        }
        for color in couleur_p.items():
            picture = Picture(color[0], color[1], couleur_s[color[0]])
            img_etoile.append(picture.creer_etoile())
            img_explorateur.append(picture.creer_explorateur())
            img_cargo.append(picture.creer_cargo())
            img_combat.append(picture.creer_combat())

        self.ajouter_img_dans_dict_joueur(img_etoile, img_explorateur, img_cargo, img_combat)


    def ajouter_img_dans_dict_joueur(self, img_etoile, img_explorateur, img_cargo, img_combat):

        tab = ["red", "blue", "lightgreen", "yellow", "lightblue", "pink", "gold", "purple",
            "orange", "green", "cyan", "seagreen", "turquoise1", "firebrick1", "grey"]
        compteur = 0

        for i in tab:
            if i != "grey":
                self.cjoueur[i]["explorateur"] = img_explorateur[compteur]
                self.cjoueur[i]["cargo"] = img_cargo[compteur]
                self.cjoueur[i]["combat"] = img_combat[compteur]
                self.cjoueur[i]["etoile"] = img_etoile[compteur]
            else:
                self.cjoueur[i]["etoile"] = img_etoile[compteur]
            compteur += 1

class Picture:
    def __init__(self, couleur, couleur_primaire, couleur_secondaire):
        # self.image = Image.new('RGBA',(16, 16))
        self.longueur = 16
        self.hauteur = 16
        self.couleur_primaire = couleur_primaire
        self.couleur_secondaire = couleur_secondaire
        self.couleur = couleur
        self.contour_vaisseau = (110, 110, 110, 255)  # gris
        self.blanc = (255, 255, 255, 255)  # blanc
        self.lumiere_vaisseau = (252, 4, 4, 255)  # rouge
        self.vitre = (189, 215, 238, 255)  # bleu poudre
        self.reflet = (221, 235, 247, 255)  # bleu presque blanc
        self.noir = (0, 0, 0, 0)  # couleur noir
        self.size = (32, 32)
        self.lien = []
        self.angle = [45, 90, 135, 180, 225, 270, 315]

    def creer_etoile(self):
        nomf = "img\etoile" + self.couleur + ".png"
        image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))

        # i = y j = x sur un tableau cartésien
        # faire un paramètre couleur qui prends 3 int puis ensuite on passe
        for i in range(self.longueur):
            for j in range(self.hauteur):
                if j == 0 or j == 15:
                    if 11 > i > 4:
                        image.putpixel((i, j), self.couleur_primaire)
                elif j == 1:
                    if 5 > i > 2 or 10 < i < 13:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 4 < i < 11:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 2:
                    if i == 2 or i == 13:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 2 < i < 13:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 3:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 1 < i < 14:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 4:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 1 < i < 14:
                        if i == 4 or i == 5:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 5:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        if 8 < i < 12:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 6:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 7:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        if 4 < i < 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 8:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 9:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        if 11 < i < 14:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 10:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        if 2 < i < 8:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 11:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 1 < i < 14:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 12:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 15:
                        if 6 < i < 11:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 13:
                    if i == 2 or i == 13:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 2 < i < 13:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 14:
                    if 2 < i < 5 or 10 < i < 13:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 4 < i < 11:
                        image.putpixel((i, j), self.couleur_secondaire)
                else:
                    image.putpixel((i, j), self.noir)  # couleur noir

        image = image.resize((64, 64))
        image.save(nomf)
        tkimage = PhotoImage(file=nomf)
        tab_img = []
        tab_img.append(tkimage)
        os.remove(nomf)
        for a in self.angle:
            nom = "img\etoile" + self.couleur + str(a) + ".png"
            image.save(nom)
            img = Image.open(nom)
            img = img.rotate(a)
            img.save(nom)
            tkimage = PhotoImage(file=nom)
            tab_img.append(tkimage)
            del img
            os.remove(nom)
        del image
        return tab_img

    def creer_explorateur(self):
        nomf = "img\explorateur" + self.couleur + ".png"
        image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        # i = y j = x sur un tableau cartésien
        # faire un paramètre couleur qui prends 3 int puis ensuite on passe
        for i in range(self.longueur):
            for j in range(self.hauteur):
                if j == 0:
                    if 5 < i < 10:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 1:
                    if 4 < i < 11:
                        if i == 5 or i == 10:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if 5 < i < 10:
                                if i == 7:
                                    image.putpixel((i, j), self.reflet)
                                else:
                                    image.putpixel((i, j), self.vitre)

                elif j == 2:
                    if 4 < i < 11:
                        if i == 5 or i == 10:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if 5 < i < 10:
                                if i == 8:
                                    image.putpixel((i, j), self.reflet)
                                else:
                                    image.putpixel((i, j), self.vitre)
                elif j == 3:
                    if 3 < i < 12:
                        if i == 4 or i == 11:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if 6 < i < 9:
                                image.putpixel((i, j), self.vitre)
                            else:
                                image.putpixel((i, j), self.couleur_primaire)
                elif j == 4:
                    if 3 < i < 12:
                        if i == 4 or i == 11:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if i == 6 or i == 9:
                                image.putpixel((i, j), self.couleur_secondaire)
                            else:
                                image.putpixel((i, j), self.couleur_primaire)
                elif j == 5:
                    if 1 < i < 14:
                        if 1 < i < 4 or 11 < i < 14:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if i == 4 or i == 11:
                                image.putpixel((i, j), self.couleur_primaire)
                            else:
                                image.putpixel((i, j), self.couleur_secondaire)
                elif j == 6:
                    if 0 < i < 15:
                        if i == 1 or i == 14:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if 1 < i < 4 or 11 < i < 14:
                                image.putpixel((i, j), self.couleur_primaire)
                            else:
                                image.putpixel((i, j), self.couleur_secondaire)

                elif 7 <= j <= 9:
                    if 0 < i < 15:
                        if i == 1 or i == 14:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if i == 2 or i == 13:
                                image.putpixel((i, j), self.couleur_primaire)
                            else:
                                image.putpixel((i, j), self.couleur_secondaire)
                elif j == 10:
                    if 0 < i < 15:
                        if i == 1 or i == 14:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if i == 2 or i == 13:
                                image.putpixel((i, j), self.couleur_primaire)
                            else:
                                if i == 5 or i == 10:
                                    image.putpixel((i, j), self.contour_vaisseau)
                                else:
                                    image.putpixel((i, j), self.couleur_secondaire)
                elif j == 11:
                    if i == 1 or i == 4 or i == 11 or i == 14:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 5 < i < 10:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif i == 2 or i == 13:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif i == 3 or i == 12:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 12:
                    if 0 < i < 4 or 11 < i < 15:
                        if i == 2 or i == 13:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.contour_vaisseau)
                elif j == 13:
                    if 0 < i < 4 or 11 < i < 15:
                        if i == 2 or i == 13:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.contour_vaisseau)
                elif j == 14:
                    if 0 < i < 3 or 12 < i < 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 15:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.contour_vaisseau)
        image = image.resize(self.size)
        image.save(nomf)
        tkimage = PhotoImage(file=nomf)
        tab_img = []
        tab_img.append(tkimage)
        os.remove(nomf)
        for a in self.angle:
            nom = "img\etoile" + self.couleur + str(a) + ".png"
            image.save(nom)
            img = Image.open(nom)
            img = img.rotate(a)
            img.save(nom)
            tkimage = PhotoImage(file=nom)
            tab_img.append(tkimage)
            del img
            os.remove(nom)
        del image
        return tab_img

    def creer_combat(self):
        nomf = "img\combat" + self.couleur + ".png"
        image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        # i = y j = x sur un tableau cartésien
        # faire un paramètre couleur qui prends 3 int puis ensuite on passe
        for i in range(self.longueur):
            for j in range(self.hauteur):
                if j == 0:
                    if 5 < i < 10:
                        image.putpixel((i, j), self.contour_vaisseau)  # Gris la couleur autour des vaisseaux
                elif j == 1:
                    if 13 < i or i < 2:
                        image.putpixel((i, j), self.lumiere_vaisseau)  # rouge lumière du vaisseaux
                    elif i == 2 or i == 13:
                        image.putpixel((i, j), self.blanc)  # blanc lumière du vaisseaux
                    elif i == 5 or i == 10:
                        image.putpixel((i, j), self.contour_vaisseau)  # Gris la couleur autour des vaisseaux
                    elif 5 < i < 10:
                        if i == 8:
                            image.putpixel((i, j), self.reflet)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 2:
                    if i < 3 or i > 12:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif i == 5 or i == 10:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 5 < i < 10:
                        if i == 7:
                            image.putpixel((i, j), self.reflet)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 3:
                    if i == 4 or i == 11:
                        image.putpixel((i, j), self.noir)
                    elif 0 < i < 3 or 12 < i < 15:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 5 < i < 10:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.vitre)
                    else:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 4 or j == 5:
                    if i == 4 or i == 11:
                        image.putpixel((i, j), self.noir)
                    elif 0 < i < 3 or 12 < i < 15:
                        if i == 1 or i == 14:
                            image.putpixel((i, j), self.couleur_secondaire)
                        else:
                            image.putpixel((i, j), self.couleur_primaire)
                    elif 5 < i < 10:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                    else:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 6:
                    if i == 4 or i == 11:
                        image.putpixel((i, j), self.noir)
                    elif 0 < i < 3 or 12 < i < 15:
                        image.putpixel((i, j), self.couleur_secondaire)
                    elif 5 < i < 10:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                    else:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 7:
                    if i == 3 or i == 12:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 3 or 12 < i < 15:
                        image.putpixel((i, j), self.couleur_secondaire)
                    elif 5 < i < 10:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                    else:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 8:
                    if i == 4 or i == 11:
                        image.putpixel((i, j), self.couleur_primaire)
                    elif 0 < i < 4 or 11 < i < 15:
                        image.putpixel((i, j), self.couleur_secondaire)
                    elif 5 < i < 10:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                    else:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 9:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 1 < i < 14:
                        if i == 6 or i == 9:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.couleur_secondaire)
                elif j == 10:
                    if i == 2 or i == 13:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 2 < i < 13:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 11:
                    if 2 < i < 6 or 9 < i < 13:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 5 < i < 10:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 12:
                    if 3 < i < 12:
                        if i == 5:
                            image.putpixel((i, j), self.noir)  # noir
                        elif i == 10:
                            image.putpixel((i, j), self.noir)  # noir
                        else:
                            image.putpixel((i, j), self.contour_vaisseau)
        image = image.resize(self.size)
        image.save(nomf)
        tkimage = PhotoImage(file=nomf)
        tab_img = []
        tab_img.append(tkimage)
        os.remove(nomf)
        for a in self.angle:
            nom = "img\etoile" + self.couleur + str(a) + ".png"
            image.save(nom)
            img = Image.open(nom)
            img = img.rotate(a)
            img.save(nom)
            tkimage = PhotoImage(file=nom)
            tab_img.append(tkimage)
            del img
            os.remove(nom)
        del image
        return tab_img

    def creer_cargo(self):
        nomf = "img\cargo" + self.couleur + ".png"
        image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        # i = y j = x sur un tableau cartésien
        # faire un paramètre couleur qui prends 3 int puis ensuite on passe
        for i in range(self.longueur):
            for j in range(self.hauteur):
                if j == 0:
                    if 2 < i < 13:
                        image.putpixel((i, j), self.contour_vaisseau)
                elif j == 1:
                    if 1 < i < 14:
                        if i == 2 or i == 13:
                            image.putpixel((i, j), self.contour_vaisseau)
                        else:
                            if 1 < i < 12:
                                image.putpixel((i, j), self.vitre)
                            elif i == 12:
                                image.putpixel((i, j), self.reflet)
                elif j == 2:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 1 < i < 14:
                        if i == 4 or i == 11:
                            image.putpixel((i, j), self.reflet)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 3:
                    if i == 1 or i == 14:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 1 < i < 14:
                        if i == 5 or 7 < i < 10:
                            image.putpixel((i, j), self.reflet)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 4:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 0 < i < 15:
                        if i == 1 or i == 14:
                            image.putpixel((i, j), self.couleur_primaire)
                        elif 7 < i < 10:
                            image.putpixel((i, j), self.vitre)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 5:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 0 < i < 15:
                        if 0 < i < 3 or 12 < i < 15:
                            image.putpixel((i, j), self.couleur_primaire)
                        else:
                            image.putpixel((i, j), self.vitre)
                elif j == 6:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif i == 2 or i == 13:
                        image.putpixel((i, j), self.couleur_secondaire)
                    else:
                        image.putpixel((i, j), self.couleur_primaire)
                elif 7 <= j <= 9:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif i == 1 or i == 14:
                        image.putpixel((i, j), self.couleur_primaire)
                    else:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 10:
                    if 0 <= i < 2 or 13 < i <= 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    else:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 11:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 1 < i < 4 or 11 < i < 14:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 3 < i < 12:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 12:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 2 < i < 5 or 10 < i < 13:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 4 < i < 11:
                        image.putpixel((i, j), self.couleur_secondaire)
                elif j == 13:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
                    elif 4 < i < 11:
                        image.putpixel((i, j), self.contour_vaisseau)

                elif j == 14:
                    if i == 0 or i == 15:
                        image.putpixel((i, j), self.contour_vaisseau)
        image = image.resize(self.size)
        image.save(nomf)
        tkimage = PhotoImage(file=nomf)
        tab_img = []
        tab_img.append(tkimage)
        os.remove(nomf)
        for a in self.angle:
            nom = "img\etoile" + self.couleur + str(a) + ".png"
            image.save(nom)
            img = Image.open(nom)
            img = img.rotate(a)
            img.save(nom)
            tkimage = PhotoImage(file=nom)
            tab_img.append(tkimage)
            del img
            os.remove(nom)
        del image
        return tab_img