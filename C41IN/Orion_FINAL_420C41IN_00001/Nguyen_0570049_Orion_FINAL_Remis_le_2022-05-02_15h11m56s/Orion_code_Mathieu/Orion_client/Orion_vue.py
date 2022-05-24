# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import random
import math

import random

# Jessica Chan, Mathieu Mailloux, Pierre-Olivier Parisien, Jacques Duymentz, Pierre Long Nguyen
class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.technologie_affichees = False
        self.opt_etoile_affichees = False
        self.aller_retour_bool = False
        self.opt_vaisseau_affichees = False
        self.opt_action_affichees = False
        self.vaisseau_clique = None
        self.cadre_dubas_affichees = False

        self.id_derniere_etoile_select = None

        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + mon_nom)
        self.mon_nom = mon_nom
        # attributs
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None

        self.vaisseau_choisi = None
        self.vaisseau_attaque = None

        self.cadre_actif = None
        self.le_cadre_courant = StringVar()
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

    def demander_abandon(self):
        rep = askokcancel("Vous voulez vraiment quitter?")
        if rep:
            self.root.after(500, self.root.destroy)

    def avertir_findepartie(self, objet):
        pop = self.parent.modele.joueurs[objet.proprietaire].population_limite
        bouffe = self.parent.modele.joueurs[objet.proprietaire].ressources["nourriture"]
        rep = showinfo(title="Fin de partie", message=objet.proprietaire + " a gagné la partie\n" +
                        "avec " + str(pop) + " de population et " + str(int(bouffe)) + " de nourriture   :-| ")

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
        self.cadres["cadre_dubas"] = self.creer_cadre_dubas()
        # Actions
        self.cadres["action_cargo"] = self.creer_cadre_action_cargo()
        self.cadres["action_chasseur"] = self.creer_cadre_action_chasseur()
        self.cadres["action_explo"] = self.creer_cadre_action_explo()
        self.cadres["action_cargo"].pack_forget()
        self.cadres["action_chasseur"].pack_forget()
        self.cadres["action_explo"].pack_forget()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def creer_cadre_splash(self, urlserveur, mon_nom, msg_initial):
        self.cadre_splash = Frame(self.cadre_app)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="purple4")
        self.canevas_splash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE,
                               bg='black', fg='green1')
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14), width=42)
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur,
                                    activebackground='green1')
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevas_splash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevas_splash.create_window(210, 250, window=self.urlsplash, width=360, height=30)
        self.canevas_splash.create_window(480, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie,
                                     activebackground='green1')
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur, activebackground='green1')
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie, activebackground='green1')

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
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="midnight blue")
        self.canevaslobby.pack()

        ##Étoiles background
        points = [100, 140, 110, 110, 140, 100, 110, 90, 100, 60, 90, 90, 60, 100, 90, 110]
        for _ in range(30):
            random_number = random.randint(-100, 600)
            points1 = [x + random_number for x in points]
            self.canevaslobby.create_polygon(points1, outline='black',
                                             fill='yellow', width=3)

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

    def creer_cadre_partie(self):
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="pink")

        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="white")

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

        self.canevas.bind("<Button-1>", self.cliquer_cosmos)  # left-click
        self.canevas.tag_bind(ALL, "<Button-2>", self.cliquer_cosmos)  # right-click

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

        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="purple")
        self.cadreoutils.pack(side=LEFT, fill=Y)

        self.le_cadre_courant.set("0")

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="black")
        self.cadreinfo.pack(fill=BOTH)

        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="yellow")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        # Juste un exemple du prof , ce bouton MINI
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()

        # Infos Ressources
        self.cadreressources = Frame(self.cadreinfogen, height=25, bg="black")  # packé après la minimap (l.203)

        self.titre_ress_globales = Label(self.cadreressources, text="\nRessources globales\n", background="black",
                                         foreground="white")

        self.framenourriture = Frame(self.cadreressources, height=25)
        self.framecombustible = Frame(self.cadreressources, height=25)
        self.framepopulation = Frame(self.cadreressources, height=25)
        self.framemateriaux = Frame(self.cadreressources, height=25)

        self.titre_ress_globales.pack(anchor="w")
        self.labressources1k = Label(self.framenourriture, text="Nourriture : ", background="black", foreground="white")
        self.labressources1k.pack(side=LEFT)
        self.labressources1v = Label(self.framenourriture, text="0", background="black", foreground="white")
        self.labressources1v.pack(side=LEFT)

        self.labressources2 = Label(self.framecombustible, text="Combustible : ", background="black",
                                    foreground="white")
        self.labressources2.pack(side=LEFT)
        self.labressources2v = Label(self.framecombustible, text="0", background="black", foreground="white")
        self.labressources2v.pack(side=LEFT)

        self.labressources3 = Label(self.framepopulation, text="Population disponible : ", background="black",
                                    foreground="white")
        self.labressources3.pack(side=LEFT)
        self.labressources3v = Label(self.framepopulation, text="0", background="black", foreground="white")
        self.labressources3v.pack(side=LEFT)

        self.labressources4 = Label(self.framemateriaux, text="Materiaux : ", background="black", foreground="white")
        self.labressources4.pack(side=LEFT)
        self.labressources4v = Label(self.framemateriaux, text="0", background="black", foreground="white")
        self.labressources4v.pack(side=LEFT)

        self.cadreressources.pack(side=BOTTOM, fill=X)
        self.framenourriture.pack(side=BOTTOM, anchor="w")
        self.framecombustible.pack(side=BOTTOM, anchor="w")
        self.framepopulation.pack(side=BOTTOM, anchor="w")
        self.framemateriaux.pack(side=BOTTOM, anchor="w")

        # Liste des vaisseaux
        self.cadrelistevaisseau = Frame(self.cadreinfo, height=200)
        self.titre_liste_vaisseau = Label(self.cadreinfo, text="\nVaisseaux en jeu\n", background="black",
                                          foreground="white")
        self.titre_liste_vaisseau.pack(anchor="w")

        self.scroll_liste_vaisseau = Scrollbar(self.cadrelistevaisseau, orient=VERTICAL)
        self.info_vaisseau = Listbox(self.cadrelistevaisseau, width=20, height=6,
                                     yscrollcommand=self.scroll_liste_vaisseau.set)
        self.info_vaisseau.bind("<Button-3>", self.centrer_liste_objet)
        self.info_vaisseau.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_vaisseau.grid(column=1, row=0, sticky=N + S)

        self.cadrelistevaisseau.columnconfigure(0, weight=1)
        self.cadrelistevaisseau.rowconfigure(0, weight=1)

        self.cadrelistevaisseau.pack(expand=1, fill=BOTH)

        # Liste des planètes conquises
        self.cadre_planetes_conquises = Frame(self.cadreinfo, height=200)
        self.titre_planetes_conquises = Label(self.cadreinfo, text="\nPlanètes conquises\n", background="black",
                                              foreground="white")
        self.titre_planetes_conquises.pack(anchor="w")

        self.scroll_liste_planetes = Scrollbar(self.cadre_planetes_conquises, orient=VERTICAL)
        self.info_planete_conquises = Listbox(self.cadre_planetes_conquises, width=20, height=6,
                                    yscrollcommand=self.scroll_liste_planetes.set)
        self.info_planete_conquises.bind("<Button-3>", self.centrer_liste_planete)
        self.info_planete_conquises.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_planetes.grid(column=1, row=0, sticky=N + S)

        self.cadre_planetes_conquises.columnconfigure(0, weight=1)
        self.cadre_planetes_conquises.rowconfigure(0, weight=1)

        self.cadre_planetes_conquises.pack(expand=1, fill=BOTH)

        # Titre actions
        self.titre_actions = Label(self.cadreinfo, text="\nActions\n", background="black", foreground="white")
        self.titre_actions.pack(anchor="w")

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def creer_cadre_dubas(self):
        # Cadre du Bas
        self.cadreoutils_dubas = Frame(self.cadrepartie, width=200, height=200, bg="orange")
        # self.cadreoutils_dubas.pack(side=BOTTOM, fill=BOTH)

        self.titre_dubas = Label(self.cadreoutils_dubas, text="Aucune étoile sélectionnée")
        self.titre_dubas.pack(side=TOP, anchor="w")

        self.cadre_vaiss_plan_batim = Frame(self.cadreoutils_dubas, height=200, width=200, bg="white")
        self.cadre_vaiss_plan_batim.pack(side=BOTTOM, fill=BOTH)

        self.cadre_creer_vaiss = Frame(self.cadre_vaiss_plan_batim, height=200, width=150, bg="white")
        self.cadre_creer_vaiss.pack(side=LEFT, fill=Y)

        self.cadre_infos_planete = Frame(self.cadre_vaiss_plan_batim, height=200, width=150, bg="white")
        self.cadre_infos_planete.pack(side=LEFT, fill=Y)

        self.cadre_creer_batiment = Frame(self.cadre_vaiss_plan_batim, height=200, width=250, bg="white")
        self.cadre_creer_batiment.pack(side=LEFT, fill=Y)

        # info planètes
        self.cadreinfoliste = Frame(self.cadre_infos_planete, bg="blue")

        self.titre_info_planete = Label(self.cadre_infos_planete, text="Info planete \n")

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
                                      bg="pink")
        self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=BOTTOM)

        self.titre_info_planete.pack()

        # Bouton de creation de vaisseau
        self.cadreinfochoix = Frame(self.cadre_creer_vaiss, height=200, width=200, bg="white")

        self.titre_creer_vaiss = Label(self.cadre_creer_vaiss, text="Créer vaisseaux \n")

        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)

        self.prixcargo = Label(self.cadreinfochoix, text="10m 10p")

        self.btncreerexplorateur = Button(self.cadreinfochoix, text="Explorateur")
        self.btncreerexplorateur.bind("<Button>", self.creer_vaisseau)

        self.prixexplorateur = Label(self.cadreinfochoix, text="10m 5p")

        self.btncreerchasseur = Button(self.cadreinfochoix, text="Chasseur")
        self.btncreerchasseur.bind("<Button>", self.creer_vaisseau)

        self.prixchasseur = Label(self.cadreinfochoix, text="10m 15p")

        # self.btncreervaisseau.pack() ~ a effacer
        self.titre_creer_vaiss.pack(anchor="w")
        self.btncreercargo.pack()
        self.prixcargo.pack()
        self.btncreerexplorateur.pack()
        self.prixexplorateur.pack()
        self.btncreerchasseur.pack()
        self.prixchasseur.pack()
        self.cadreinfochoix.pack()

        # Batiments
        # self.cadre_batiment = Frame(self.cadre_creer_batiment, height=150, width=200, bg="lightblue")
        self.titre_bat_planete = Label(self.cadre_creer_batiment, text="Bâtiments de la planète \n")
        self.cadre_alimentation = Frame(self.cadre_creer_batiment, height=150, width=200, bg="white")
        self.btn_bat_alimentation = Button(self.cadre_alimentation, width=10, height=1, text="Alimentation")
        self.btn_bat_alimentation.bind("<Button>", self.creer_batiment)
        self.qte_niv1_al = Label(self.cadre_alimentation, text="niv1 :")
        self.qte_niv1_al_value = Label(self.cadre_alimentation, text="qte")
        self.qte_niv2_al = Label(self.cadre_alimentation, text="niv2 :")
        self.qte_niv2_al_value = Label(self.cadre_alimentation, text="qte")
        self.qte_niv3_al = Label(self.cadre_alimentation, text="niv3 :")
        self.qte_niv3_al_value = Label(self.cadre_alimentation, text="qte")
        self.prix_alimentation = Label(self.cadre_creer_batiment, text="8m 10p")

        self.cadre_science = Frame(self.cadre_creer_batiment, height=150, width=200, bg="white")
        self.btn_bat_science = Button(self.cadre_science, width=10, height=1, text="Science")
        self.btn_bat_science.bind("<Button>", self.creer_batiment)
        self.qte_niv1_sci = Label(self.cadre_science, text="niv1 :")
        self.qte_niv1_sci_value = Label(self.cadre_science, text="qte")
        self.qte_niv2_sci = Label(self.cadre_science, text="niv2 :")
        self.qte_niv2_sci_value = Label(self.cadre_science, text="qte")
        self.qte_niv3_sci = Label(self.cadre_science, text="niv3 :")
        self.qte_niv3_sci_value = Label(self.cadre_science, text="qte")
        self.prix_science = Label(self.cadre_creer_batiment, text="10m 10p")

        self.cadre_industrie = Frame(self.cadre_creer_batiment, height=150, width=200, bg="white")
        self.btn_bat_industrie = Button(self.cadre_industrie, width=10, height=1, text="Industrie")
        self.btn_bat_industrie.bind("<Button>", self.creer_batiment)
        self.qte_niv1_ind = Label(self.cadre_industrie, text="niv1 :")
        self.qte_niv1_ind_value = Label(self.cadre_industrie, text="qte")
        self.qte_niv2_ind = Label(self.cadre_industrie, text="niv2 :")
        self.qte_niv2_ind_value = Label(self.cadre_industrie, text="qte")
        self.qte_niv3_ind = Label(self.cadre_industrie, text="niv3 :")
        self.qte_niv3_ind_value = Label(self.cadre_industrie, text="qte")
        self.prix_industrie = Label(self.cadre_creer_batiment, text="12m 10p")

        self.cadre_habitation = Frame(self.cadre_creer_batiment, height=150, width=200, bg="white")
        self.btn_bat_habitation = Button(self.cadre_habitation, width=10, height=1, text="Habitation")
        self.btn_bat_habitation.bind("<Button>", self.creer_batiment)
        self.qte_niv1_hab = Label(self.cadre_habitation, text="niv1 :")
        self.qte_niv1_hab_value = Label(self.cadre_habitation, text="qte")
        self.qte_niv2_hab = Label(self.cadre_habitation, text="niv2 :")
        self.qte_niv2_hab_value = Label(self.cadre_habitation, text="qte")
        self.qte_niv3_hab = Label(self.cadre_habitation, text="niv3 :")
        self.qte_niv3_hab_value = Label(self.cadre_habitation, text="qte")
        self.prix_habitation = Label(self.cadre_creer_batiment, text="8m")

        self.titre_bat_planete.pack()
        self.cadre_alimentation.pack()
        self.btn_bat_alimentation.pack(side=LEFT)
        self.prix_alimentation.pack(anchor="w")
        self.qte_niv1_al.pack(side=LEFT)
        self.qte_niv1_al_value.pack(side=LEFT)
        self.qte_niv2_al.pack(side=LEFT)
        self.qte_niv2_al_value.pack(side=LEFT)
        self.qte_niv3_al.pack(side=LEFT)
        self.qte_niv3_al_value.pack(side=LEFT)

        self.cadre_science.pack()
        self.btn_bat_science.pack(side=LEFT)
        self.prix_science.pack(anchor="w")
        self.qte_niv1_sci.pack(side=LEFT)
        self.qte_niv1_sci_value.pack(side=LEFT)
        self.qte_niv2_sci.pack(side=LEFT)
        self.qte_niv2_sci_value.pack(side=LEFT)
        self.qte_niv3_sci.pack(side=LEFT)
        self.qte_niv3_sci_value.pack(side=LEFT)

        self.cadre_industrie.pack()
        self.btn_bat_industrie.pack(side=LEFT)
        self.prix_industrie.pack(anchor="w")
        self.qte_niv1_ind.pack(side=LEFT)
        self.qte_niv1_ind_value.pack(side=LEFT)
        self.qte_niv2_ind.pack(side=LEFT)
        self.qte_niv2_ind_value.pack(side=LEFT)
        self.qte_niv3_ind.pack(side=LEFT)
        self.qte_niv3_ind_value.pack(side=LEFT)

        self.cadre_habitation.pack()
        self.btn_bat_habitation.pack(side=LEFT)
        self.prix_habitation.pack(anchor="w")
        self.qte_niv1_hab.pack(side=LEFT)
        self.qte_niv1_hab_value.pack(side=LEFT)
        self.qte_niv2_hab.pack(side=LEFT)
        self.qte_niv2_hab_value.pack(side=LEFT)
        self.qte_niv3_hab.pack(side=LEFT)
        self.qte_niv3_hab_value.pack(side=LEFT)

        return self.cadreoutils_dubas

    def switchButtonState(self, button1, button2):
        if (button2["state"] == tkinter.DISABLED):
            button2["state"] = tkinter.NORMAL
            button1["state"] = tkinter.DISABLED
        else:
            button1["state"] = tkinter.NORMAL
            button2["state"] = tkinter.DISABLED

    def creer_cadre_action_cargo(self):
        self.var_cargo = IntVar()
        self.retour_prevu_cargo = BooleanVar()
        self.cadre_actions_cargo = Frame(self.cadreinfo, height=200, background="black")

        self.checkAllerRetour = Checkbutton(self.cadre_actions_cargo, variable=self.retour_prevu_cargo, text="Retour",
                                            onvalue=True, offvalue=False)
        self.action_rec_nourr = Radiobutton(self.cadre_actions_cargo, variable=self.var_cargo, text="Récolter nourriture", value=1, background="lightblue")
        self.action_rec_comb = Radiobutton(self.cadre_actions_cargo, variable=self.var_cargo, text="Récolter combustible", value=2, background="lightblue")
        self.action_rec_mat = Radiobutton(self.cadre_actions_cargo, variable=self.var_cargo, text="Récolter matériaux", value=3, background="lightblue")

        self.checkAllerRetour.pack()
        self.action_rec_nourr.pack(side=BOTTOM, anchor="w")
        self.action_rec_comb.pack(side=BOTTOM, anchor="w")
        self.action_rec_mat.pack(side=BOTTOM, anchor="w")
        self.cadre_actions_cargo.pack(expand=1, fill=BOTH)

        return self.cadre_actions_cargo

    def creer_cadre_action_chasseur(self):
        self.var_chasseur = IntVar()
        self.retour_prevu_chasseur = BooleanVar()
        self.cadre_actions_chasseur = Frame(self.cadreinfo, height=200, background="white")

        self.checkAllerRetour = Checkbutton(self.cadre_actions_chasseur, variable=self.retour_prevu_chasseur, text="Retour",
                                            onvalue=True, offvalue=False)
        self.action_attaquer = Radiobutton(self.cadre_actions_chasseur, text="Attaquer", variable=self.var_chasseur, value=2, background="lightblue")
        self.action_escorter = Radiobutton(self.cadre_actions_chasseur, text="Escorter", variable=self.var_chasseur, value=3, background="lightblue")

        self.action_escorter.pack(side=BOTTOM, anchor="w")
        self.action_attaquer.pack(side=BOTTOM, anchor="w")
        # self.action_aller_retour.pack(side=BOTTOM, anchor="w")
        self.checkAllerRetour.pack()
        self.cadre_actions_chasseur.pack(expand=1, fill=BOTH)

        return self.cadre_actions_chasseur

    def creer_cadre_action_explo(self):
        self.var_explo = IntVar()
        self.retour_prevu_explo = BooleanVar()
        self.cadre_actions_explo = Frame(self.cadreinfo, height=200, background="black")
        self.checkAllerRetour = Checkbutton(self.cadre_actions_explo, variable=self.retour_prevu_explo, text="Retour",
                                            onvalue=True, offvalue=False)
        self.checkAllerRetour.pack()

        self.cadre_actions_explo.pack(expand=1, fill=BOTH)

        return self.cadre_actions_explo

    def creer_cadre_opt_vaisseau(self):
        self.retour_prevu = BooleanVar()
        self.cadre_opt_vaisseau = Frame(self.cadreoutils, height=200, width=200, bg="lightblue")
        self.checkAllerRetour = Checkbutton(self.cadre_opt_vaisseau, variable=self.retour_prevu, text="Retour",
                                            onvalue=True, offvalue=False)
        self.checkAllerRetour.pack()
        self.cadre_opt_vaisseau.pack()

        return self.cadre_opt_vaisseau

    def aff_cadre_opt_vaisseau(self):
        if self.opt_vaisseau_affichees:
            self.cadres["opt_vaisseau"].pack_forget()
            self.opt_vaisseau_affichees = False

    def aff_cadre_dubas(self):
        if self.cadre_dubas_affichees:
            self.cadres["cadre_dubas"].pack_forget()
            self.cadre_dubas_affichees = False
        else:
            self.cadres["cadre_dubas"].pack(side=BOTTOM)
            self.cadre_dubas_affichees = True
            self.cadre_creer_batiment.pack()

    def aff_cadre_action_cargo(self):
        if self.opt_action_affichees:
            self.cadres["action_cargo"].pack_forget()
            self.cadres["action_chasseur"].pack_forget()
            self.cadres["action_explo"].pack_forget()
            self.opt_action_affichees = False
        else:
            self.cadres["action_cargo"].pack()
            self.opt_action_affichees = True

    def aff_cadre_action_chasseur(self):
        if self.opt_action_affichees:
            self.cadres["action_cargo"].pack_forget()
            self.cadres["action_chasseur"].pack_forget()
            self.cadres["action_explo"].pack_forget()
            self.opt_action_affichees = False
        else:
            self.cadres["action_chasseur"].pack()
            self.opt_action_affichees = True

    def aff_cadre_action_explo(self):
        if self.opt_action_affichees:
            self.cadres["action_cargo"].pack_forget()
            self.cadres["action_chasseur"].pack_forget()
            self.cadres["action_explo"].pack_forget()
            self.opt_action_affichees = False
        else:
            self.cadres["action_explo"].pack()
            self.opt_action_affichees = True

    def deplacer(self, id_vaisseau_choisi, id_destination, type, nom_joueur):
        # self.aff_cadre_opt_vaisseau()
        self.aff_cadre_action_cargo()
        self.aff_cadre_action_chasseur()
        self.aff_cadre_action_explo()

        # Choix de ressource pour le cargo
        self.choisir_ressource()

        retour_prevu = False
        if self.retour_prevu_chasseur.get():
            retour_prevu = self.retour_prevu_chasseur.get()
        elif self.retour_prevu_cargo.get():
            retour_prevu = self.retour_prevu_cargo.get()
        elif self.retour_prevu_explo.get():
            retour_prevu = self.retour_prevu_explo.get()

        self.parent.cibler_flotte(id_vaisseau_choisi, id_destination, type, nom_joueur, retour_prevu)


    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    # centrer vaisseaux
    def centrer_liste_objet(self, evt):
        info = self.info_vaisseau.get(self.info_vaisseau.curselection())
        liste_separee = info.split(";")
        type_vaisseau = liste_separee[0]
        id = liste_separee[1][1:]
        obj = self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        self.centrer_objet(obj)

    def centrer_liste_planete(self, evt):
        info = self.info_planete_conquises.get(self.info_planete_conquises.curselection())
        liste_separee = info.split(";")
        id = liste_separee[1][1:]
        for etoile in self.modele.joueurs[self.mon_nom].etoiles_controlees:
            if etoile.id == id:
                self.centrer_objet(etoile)

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

        self.afficher_decor(modele)
        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2
        xl = (self.canevas.winfo_width() / 2) / self.modele.largeur
        yl = (self.canevas.winfo_height() / 2) / self.modele.hauteur
        self.centrer_planemetemere(self.modele.joueurs[self.mon_nom].etoilemere)

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

        ##cadre rouge de la mini-map
        ratio_x = 800*(self.canevas_minimap.winfo_width() / self.canevas.winfo_width())
        ratio_y = 600*(self.canevas_minimap.winfo_height() / self.canevas.winfo_height())
        self.canevas_minimap.delete("cadre_rouge")
        ## taille du cadre hard-coded... rendre sa taille ajustable en fonction de la taille de self.canevas
        self.canevas_minimap.create_rectangle(x - 12, y + 8,
                                              x + 12, y - 8, outline="red", width=3, fill="",
                                              tags="cadre_rouge")

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
                self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                                                      fill=mod.joueurs[i].couleur,
                                                      tags=(j.proprietaire, str(j.id), "Etoile"))

    def afficher_mini(self, evt):  # univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.taille_minimap
            miniy = j.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 0, miniy + 0,
                                                  fill="black",
                                                  tags=("mini", "Etoile"))

    def centrer_planemetemere(self, evt):
        self.centrer_objet(self.modele.joueurs[self.mon_nom].etoilemere)



    def centrer_objet(self, objet):
        # permet de defiler l'écran jusqu'à cet objet
        x = objet.x
        y = objet.y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = ((x - x1) / self.modele.largeur)-0.04
        pcty = ((y - y1) / self.modele.hauteur)-0.04

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
        self.info_vaisseau.insert(END, obj + "; " + id)

    def lister_planetes_conquises(self, obj, id):
        deja_la = False
        for i in self.info_planete_conquises.get(first=0, last=self.info_planete_conquises.size()):
            if i == obj + "; " + id:
                deja_la = True
                break
        if not deja_la:
            self.info_planete_conquises.insert(END, obj + "; " + id)


    def afficher_info_ressources(self, obj):
        self.info_liste.delete(0, END)
        if obj in self.modele.joueurs[self.mon_nom].etoiles_connues:
            for key, value in obj.ressources.items():
                self.info_liste.insert(END, key + " : " + str(value))

        # self.info_liste.insert(END, obj.ressources)

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau)
        self.vaisseau_clique = type_vaisseau
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadre_creer_batiment.pack_forget()
        # self.cadreinfochoix.pack_forget()

    def creer_batiment(self, evt):
        type_batiment = evt.widget.cget("text")
        self.parent.creer_batiment(type_batiment, self.id_derniere_etoile_select)

    def choisir_ressource(self):
        type_ressource = self.var_cargo.get()
        self.parent.choisir_ressource(type_ressource)

    def afficher_jeu(self):
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("mobile")

        self.le_cadre_courant.set(str(self.parent.modele.cadre_courant))

        if self.ma_selection != None:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoiles_controlees:
                    if i.id == self.ma_selection[1]:
                        x = i.x
                        y = i.y
                        t = 10 * self.zoom
                        self.canevas.create_oval(x - t, y - t, x + t, y + t,
                                                 dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                 tags=("multiselection", "marqueur"))
                        self.mettre_a_jour_titre_dubas(self.ma_selection[1]) # Titre dubas (affiche id de l'étoile sélectionnée)
                        self.id_derniere_etoile_select = self.ma_selection[1] # Pour la construction de bâtiments
                        self.mettre_a_jour_var_construction(i)
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


        # afficher mes assets
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            if i.nom == self.mon_nom:
                vaisseau_local = []
                for k in i.flotte:
                    for j in i.flotte[k]:
                        j = i.flotte[k][j]
                        tailleF = j.taille * self.zoom

                        if k == "Vaisseau":
                            self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                          tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                        elif k == "Cargo":
                            self.dessiner_cargo(j, tailleF, i, k)

                        elif k == "Explorateur":
                            self.dessiner_explorateur(j, tailleF, i, k)

                        elif k == "Chasseur":
                            self.dessiner_chasseur(j, tailleF, i, k)


        for missile in mod.missiles:
            if not missile.cible_atteinte:
                x = missile.x
                y = missile.y
                d = missile.demitaille
                self.canevas.create_oval(x - d, y - d, x + d, y + d, fill="white", outline="",
                                         tags="mobile")


        for i in mod.joueurs[self.mon_nom].vaisseaux_vus:
            joueur = i.parent
            tailleF = i.taille * self.zoom
            if i.mon_type == "Vaisseau":
                self.canevas.create_rectangle((i.x - tailleF), (i.y - tailleF),
                                              (i.x + tailleF), (i.y + tailleF), fill=joueur.couleur,
                                              tags=(i.proprietaire, str(i.id), "Flotte", k, "artefact"))
            elif i.mon_type == "Cargo":
                self.dessiner_cargo(i, tailleF, joueur, "Cargo")

            elif i.mon_type == "Explorateur":
                self.dessiner_explorateur(i, tailleF, joueur, "Explorateur")

            elif i.mon_type == "Chasseur":
                self.dessiner_chasseur(i, tailleF, joueur, "Chasseur")



        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

        self.mettre_a_jour_ressources()
        self.mettre_a_jour_prix()


    def mettre_a_jour_titre_dubas(self, id_etoile):
        self.titre_dubas.config(text="Etoile " + id_etoile)

    def mettre_a_jour_ressources(self):

        self.labressources1v.config(text=round(self.modele.joueurs[self.mon_nom].ressources["nourriture"]))
        self.labressources2v.config(text=self.modele.joueurs[self.mon_nom].ressources["combustible"])
        self.labressources3v.config(text=round(self.modele.joueurs[self.mon_nom].population_inactive))
        self.labressources4v.config(text=self.modele.joueurs[self.mon_nom].ressources["materiaux"])

    def mettre_a_jour_var_construction(self, etoile):
        self.qte_niv1_al_value.config(text=etoile.parc_immobilier["Alimentation"]["niv1"])
        self.qte_niv1_sci_value.config(text=etoile.parc_immobilier["Science"]["niv1"])
        self.qte_niv1_ind_value.config(text=etoile.parc_immobilier["Industrie"]["niv1"])
        self.qte_niv1_hab_value.config(text=etoile.parc_immobilier["Habitation"]["niv1"])

        self.qte_niv2_al_value.config(text=etoile.parc_immobilier["Alimentation"]["niv2"])
        self.qte_niv2_sci_value.config(text=etoile.parc_immobilier["Science"]["niv2"])
        self.qte_niv2_ind_value.config(text=etoile.parc_immobilier["Industrie"]["niv2"])
        self.qte_niv2_hab_value.config(text=etoile.parc_immobilier["Habitation"]["niv2"])

        self.qte_niv3_al_value.config(text=etoile.parc_immobilier["Alimentation"]["niv3"])
        self.qte_niv3_sci_value.config(text=etoile.parc_immobilier["Science"]["niv3"])
        self.qte_niv3_ind_value.config(text=etoile.parc_immobilier["Industrie"]["niv3"])
        self.qte_niv3_hab_value.config(text=etoile.parc_immobilier["Habitation"]["niv3"])

    def mettre_a_jour_prix(self):
        self.prix_alimentation.config(
            text=str(self.modele.cout_alimentation_m) + "m " + str(self.modele.cout_alimentation_p) + "p")
        self.prix_science.config(
            text=str(self.modele.cout_science_m) + "m " + str(self.modele.cout_science_p) + "p")
        self.prix_industrie.config(
            text=str(self.modele.cout_industrie_m) + "m " + str(self.modele.cout_industrie_p) + "p")
        self.prix_habitation.config(
            text=str(self.modele.cout_habitation_m) + "m")
        self.prixcargo.config(
            text=str(self.modele.cout_cargo) + "m " + str(self.modele.cout_equipage_cargo) + "p")
        self.prixchasseur.config(
            text=str(self.modele.cout_chasseur) + "m " + str(self.modele.cout_equipage_chasseur) + "p")
        self.prixexplorateur.config(
            text=str(self.modele.cout_explo) + "m " + str(self.modele.cout_equipage_explo) + "p")

        # Faire la même chose pour les couts de vaisseaux ici ->

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

        x1, y1 = hlp.getAngledPoint(obj.angle_cible + 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x1 - dt), (y1 - dt),
                                 (x1 + dt), (y1 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        x2, y2 = hlp.getAngledPoint(obj.angle_cible - 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x2 - dt), (y2 - dt),
                                 (x2 + dt), (y2 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    def dessiner_explorateur(self, obj, tailleF, joueur, type_obj):
        t = obj.taille * self.zoom
        a = obj.ang
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        dta = t * 50
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="deep pink",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

        x1, y1 = hlp.getAngledPoint(obj.angle_cible + 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x1 - dt), (y1 - dt),
                                 (x1 + dt), (y1 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        x2, y2 = hlp.getAngledPoint(obj.angle_cible - 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x2 - dt), (y2 - dt),
                                 (x2 + dt), (y2 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))



    def dessiner_chasseur(self, obj, tailleF, joueur, type_obj):
        t = obj.taille * self.zoom
        a = obj.ang
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="grey",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        x1, y1 = hlp.getAngledPoint(obj.angle_cible + 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x1 - dt), (y1 - dt),
                                 (x1 + dt), (y1 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        x2, y2 = hlp.getAngledPoint(obj.angle_cible - 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x2 - dt), (y2 - dt),
                                 (x2 + dt), (y2 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

        d = obj.rayon_attaque
        self.canevas.create_oval(x - d, y - d, x + d, y + d, outline="white", dash=6, width=1, tags=("", obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))



    def cliquer_cosmos(self, evt):
        t = self.canevas.gettags(CURRENT)
        if t:  # il y a des tags

            if t[0] == self.mon_nom:
                self.ma_selection = [self.mon_nom, t[1], t[2]]  # Lorsque l'objet est à moi t[1] id objet t[2] type
                if t[2] == "Etoile":
                    self.aff_cadre_dubas()
                    for i in self.modele.joueurs[self.mon_nom].etoiles_controlees:
                        if i.id == t[1]:
                            self.afficher_info_ressources(i)
                            if self.vaisseau_choisi:
                                self.deplacer(self.vaisseau_choisi[1], t[1], t[2], None)
                                self.vaisseau_choisi = None

                elif t[2] == "Flotte":
                    self.cadre_creer_batiment.pack_forget()
                    self.vaisseau_choisi = self.ma_selection
                    if self.vaisseau_clique == "Cargo":
                        self.aff_cadre_action_cargo()
                    elif self.vaisseau_clique == "Chasseur":
                        self.aff_cadre_action_chasseur()
                    elif self.vaisseau_clique == "Explorateur":
                        self.aff_cadre_action_explo()

            elif ("Etoile" in t or "Porte_de_ver" in t) and t[0] != self.mon_nom:
                if self.ma_selection and self.vaisseau_choisi:
                    self.deplacer(self.vaisseau_choisi[1], t[1], t[2], None)
                    self.vaisseau_choisi = None
                self.ma_selection = None
                self.canevas.delete("marqueur")


            if self.ma_selection and self.vaisseau_choisi:
                for id in self.modele.joueurs[self.mon_nom].flotte["Chasseur"]:
                    if id == self.vaisseau_choisi[1]:
                        nom_joueur = self.ma_selection[0]
                        id_ennemi = self.ma_selection[1]
                        self.deplacer(self.vaisseau_choisi[1], id_ennemi, "Vaisseau_etranger", nom_joueur)

        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            self.ma_selection = None
            self.canevas.delete("marqueur")


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
