# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math

import random


class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.technologie_affichees = False
        self.ressources_affichees = False
        self.opt_vaisseau_affichees = True
        self.opt_etoile_affichees = False

        self.aller_retour_bool = False
        self.opt_vaisseau_affichees = False


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
        self.cadres["ressources"] = self.creer_cadre_aff_ressources()
        self.cadres["technologie"] = self.creer_cadre_technologie()
        self.cadres["opt_vaisseau"] = self.creer_cadre_opt_vaisseau()
        self.cadres["opt_etoile"] = self.creer_cadre_opt_etoile()
        self.cadres["opt_vaisseau"].pack_forget()

        # Pour retirer le cadre technologie au demarrage
        self.cadres["technologie"].pack_forget()
        self.cadres["opt_etoile"].pack_forget()

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

        self.canevas.bind("<Button-1>", self.cliquer_cosmos)            # left-click
        self.canevas.tag_bind(ALL,"<Button-3>",self.cliquer_cosmos)     # right-click

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

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="darkgrey")
        self.cadreinfo.pack(fill=BOTH)

        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="grey50")
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planemetemere)
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()
        self.btn_aff_ressources = Button(self.cadreinfogen, command=self.aff_ressources, text="Ressources")
        self.btn_aff_ressources.pack()

        # Bouton pour generer le CADRE TECHNOLOGIQUE
        self.btncreerArbreTechno = Button(self.cadreinfogen, text="Technologie", command=self.aff_technologie)
        self.btncreerArbreTechno.pack()

        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30")

        # Bouton de creation de vaisseau
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)
        self.btncreereclaireur = Button(self.cadreinfochoix, text="Eclaireur")
        self.btncreereclaireur.bind("<Button>", self.creer_vaisseau)
        self.btncreerchasseur = Button(self.cadreinfochoix, text="Chasseur")
        self.btncreerchasseur.bind("<Button>", self.creer_vaisseau)


        # self.btncreervaisseau.pack() ~ a effacer
        self.btncreercargo.pack()
        self.btncreereclaireur.pack()
        self.btncreerchasseur.pack()

        self.cadreinfoliste = Frame(self.cadreinfo, bg="blue")

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

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def aff_ressources(self):
        if self.ressources_affichees:
            self.cadres["ressources"].pack_forget()
            self.ressources_affichees = False
        else:
            self.cadres["ressources"].pack()
            self.ressources_affichees = True

    def creer_cadre_aff_ressources(self):
        self.cadreressources = Frame(self.cadreoutils, height=25, bg="orange")  # packé après la minimap (l.203)
        self.labressources1k = Label(self.cadreressources, text="Metal : ", fg="purple")
        self.labressources1k.pack(side=LEFT)
        self.labressources1v = Label(self.cadreressources,
                                     text="0", fg="purple")
        self.labressources1v.pack(side=LEFT)
        self.labressources2 = Label(self.cadreressources, text="Combustible : ", fg="purple")
        self.labressources2.pack(side=LEFT)
        self.labressources2v = Label(self.cadreressources,
                                     text="0", fg="purple")
        self.labressources2v.pack(side=LEFT)
        self.labressources3 = Label(self.cadreressources, text="Eau : ", fg="purple")
        self.labressources3.pack(side=LEFT)
        self.labressources3v = Label(self.cadreressources,
                                     text="0", fg="purple")
        self.labressources3v.pack(side=LEFT)
        self.labressources4 = Label(self.cadreressources, text="Materiaux : ", fg="purple")
        self.labressources4.pack(side=LEFT)
        self.labressources4v = Label(self.cadreressources,
                                     text="0", fg="purple")
        self.labressources4v.pack(side=LEFT)

        self.cadreressources.pack(side=BOTTOM, fill=X)

        return self.cadreressources

    def aff_technologie(self):
        if self.technologie_affichees:
            self.cadres["technologie"].pack_forget()
            self.technologie_affichees = False
        else:
            self.cadres["technologie"].pack(side=LEFT)
            self.technologie_affichees = True

    def switchButtonState(self, button1, button2):
        if (button2["state"] == tkinter.DISABLED):
            button2["state"] = tkinter.NORMAL
            button1["state"] = tkinter.DISABLED
        else:
            button1["state"] = tkinter.NORMAL
            button2["state"] = tkinter.DISABLED

    def creer_cadre_technologie(self):
        self.cadre_technologie = LabelFrame(self.canevas, height=500, width=8000, bg="green", text="ARBRE TECHNOLOGIQUE")

        self.cadre_nourriture = LabelFrame(self.cadre_technologie, height=125, width=7000, bg="SeaGreen1", text="Nourriture")
        self.cadre_connaissance = LabelFrame(self.cadre_technologie, height=125, width=7000, bg="SeaGreen1", text="Connaissance")
        self.cadre_industrie = LabelFrame(self.cadre_technologie, height=125, width=7000, bg="SeaGreen1", text="Industrielle")

        self.btn_science1A = Button(self.cadre_nourriture, text="Bouffe 1", command=self.science_1A,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science1B = Button(self.cadre_nourriture, text="Bouffe 2", state=DISABLED, command=self.science_1B,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science1C = Button(self.cadre_nourriture, text="Bouffe 2", state=DISABLED, command=self.science_1C,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)

        self.btn_science2A = Button(self.cadre_connaissance, text="Science 1", command=self.science_2A,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science2B = Button(self.cadre_connaissance, text="Science 2", state=DISABLED, command=self.science_2B,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science2C = Button(self.cadre_connaissance, text="Science 2", state=DISABLED, command=self.science_2C,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)

        self.btn_science3A = Button(self.cadre_industrie, text="Minage 1", command=self.science_3A,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science3B = Button(self.cadre_industrie, text="Minage 2", state=DISABLED, command=self.science_3B,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)
        self.btn_science3C = Button(self.cadre_industrie, text="Minage 2", state=DISABLED, command=self.science_3C,
                                             borderwidth=5, width=10, height=5, padx=5, pady=5)

        self.btn_science1A.pack(side=LEFT)
        self.btn_science1B.pack(side=LEFT)
        self.btn_science1C.pack(side=LEFT)

        self.btn_science2A.pack(side=LEFT)
        self.btn_science2B.pack(side=LEFT)
        self.btn_science2C.pack(side=LEFT)

        self.btn_science3A.pack(side=LEFT)
        self.btn_science3B.pack(side=LEFT)
        self.btn_science3C.pack(side=LEFT)

        self.cadre_nourriture.pack()
        self.cadre_connaissance.pack()
        self.cadre_industrie.pack()

        self.cadre_technologie.pack(side=LEFT)

        return self.cadre_technologie

# Ajouter les déblocaque de science
    def science_1A(self):
        self.switchButtonState(self.btn_science1A, self.btn_science1B)
    def science_1B(self):
        self.switchButtonState(self.btn_science1B, self.btn_science1C)
    def science_1C(self):
        pass
    def science_2A(self):
        self.switchButtonState(self.btn_science2A, self.btn_science2B)
    def science_2B(self):
        self.switchButtonState(self.btn_science2B, self.btn_science2C)
    def science_2C(self):
        pass
    def science_3A(self):
        self.switchButtonState(self.btn_science3A, self.btn_science3B)
    def science_3B(self):
        self.switchButtonState(self.btn_science3B, self.btn_science3C)
    def science_3C(self):
        pass

    def creer_cadre_opt_vaisseau(self):
        self.retour_prevu = BooleanVar()
        self.cadre_opt_vaisseau = Frame(self.cadreoutils, height=200, width=200, bg="lightblue")
        self.checkAllerRetour = Checkbutton(self.cadre_opt_vaisseau, variable=self.retour_prevu,
                                            text="Retour", onvalue=True, offvalue=False)
        self.checkAllerRetour.pack()
        self.cadre_opt_vaisseau.pack()

        return self.cadre_opt_vaisseau

    def aff_cadre_opt_vaisseau(self):
        if self.opt_vaisseau_affichees:
            self.cadres["opt_vaisseau"].pack_forget()
            self.opt_vaisseau_affichees = False
        else:
            self.cadres["opt_vaisseau"].pack()
            self.opt_vaisseau_affichees = True

    def aff_cadre_opt_etoile(self):
        if self.opt_etoile_affichees:
            self.cadres["opt_etoile"].pack_forget()
            self.opt_etoile_affichees = False
        else:
            self.cadres["opt_etoile"].pack(side=BOTTOM)
            self.opt_etoile_affichees = True

    def creer_cadre_opt_etoile(self):
        self.cadre_opt_etoile = Canvas(self.canevas, height=150, width=1000, bg="lightblue")
        self.btn_bat_alimentation = Button(self.cadre_opt_etoile, width=10, height=2, text="Alimentation")
        self.btn_bat_science = Button(self.cadre_opt_etoile, width=10, height=2, text="Science")
        self.btn_bat_industrie = Button(self.cadre_opt_etoile, width=10, height=2, text="Industrie")

        self.cadre_opt_etoile.create_text(35, 45, text="niv : ", font=("Helvetica 8 bold"))
        self.cadre_opt_etoile.create_text(200, 20, text="Bâtiments", font=('Helvetica 10 bold'))
        self.cadre_opt_etoile.create_text(35, 119, text="coût : ", font=("Helvetica 8 bold"))
        self.cadre_opt_etoile.create_window(100, 80, window=self.btn_bat_alimentation)
        self.cadre_opt_etoile.create_window(200, 80, window=self.btn_bat_science)
        self.cadre_opt_etoile.create_window(300, 80, window=self.btn_bat_industrie)


        # self.btn_bat_alimentation.pack(side=LEFT)
        # self.btn_bat_science.pack(side=LEFT)
        # self.btn_bat_industrie.pack(side=LEFT)
        self.cadre_opt_etoile.pack(side=BOTTOM)

        return self.cadre_opt_etoile


    def deplacer(self, id_vaisseau_choisi, id_destination, type):
        self.aff_cadre_opt_vaisseau()
        retour_prevu = self.retour_prevu.get()
        self.parent.cibler_flotte(id_vaisseau_choisi, id_destination, type, retour_prevu)

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

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

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
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoilescontrolees:
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

    def afficher_info_ressources(self, obj):
        self.info_liste.delete(0, END)
        if obj.info_rapportee:
            for key, value in obj.ressources.items():
                self.info_liste.insert(END, key + " : " + str(value))

        #self.info_liste.insert(END, obj.ressources)

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

        self.le_cadre_courant.set(str(self.parent.modele.cadre_courant))

        if self.ma_selection != None:
            joueur = mod.joueurs[self.ma_selection[0]]
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoilescontrolees:
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
                    if k == "Vaisseau":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Cargo":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j, tailleF, i, k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))

                    elif k == "Eclaireur":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_eclaireur(j, tailleF, i, k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))

                    elif k == "Chasseur":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_chasseur(j, tailleF, i, k)
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

        self.mettre_a_jour_ressources()
        self.mettre_a_jour_var_construction()

    def mettre_a_jour_ressources(self):
        self.labressources1v.config(text=self.modele.joueurs[self.mon_nom].ressources["metal"])
        self.labressources2v.config(text=self.modele.joueurs[self.mon_nom].ressources["combustible"])
        self.labressources3v.config(text=self.modele.joueurs[self.mon_nom].ressources["eau"])
        self.labressources4v.config(text=self.modele.joueurs[self.mon_nom].ressources["materiaux"])

    def mettre_a_jour_var_construction(self):
        # Affichage niveau batiment
        self.cadre_opt_etoile.create_text(100, 45,
                                          text=str(self.modele.batiment_alimentation.niveau),
                                          font=('Helvetica 8'))
        self.cadre_opt_etoile.create_text(200, 45,
                                          text=str(self.modele.batiment_science.niveau),
                                          font=('Helvetica 8'))
        self.cadre_opt_etoile.create_text(300, 45,
                                          text=str(self.modele.batiment_industrie.niveau),
                                          font=('Helvetica 8'))
        # Affichage coût de construction
        self.cadre_opt_etoile.create_text(100, 120, text=str(self.modele.batiment_alimentation.cout_construction) + " matériaux",
                                          font=('Helvetica 8'))
        self.cadre_opt_etoile.create_text(200, 120, text=str(self.modele.batiment_science.cout_construction) + " matériaux",
                                          font=('Helvetica 8'))
        self.cadre_opt_etoile.create_text(300, 120, text=str(self.modele.batiment_industrie.cout_construction) + " matériaux",
                                        font=('Helvetica 8'))

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

        # Bar de vie
        # sante => relier sante du vaisseau puis changer la couleur du bar selon le % restant
        self.canevas.create_rectangle((x - dt - 10), (y - dt - 25),
                                 (x + dt + 10), (y + dt - 25), fill="red",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

        points1 = [(x-dt), (y-dt), (x+30-dt), (y-dt), (x-dt), (y-30+dt)]
        self.canevas.create_polygon(points1, fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        points2 = [(x - dt), (y - dt), (x - 30 - dt), (y - dt), (x - dt), (y + 30 + dt)]
        self.canevas.create_polygon(points2, fill=joueur.couleur,
                                    tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))


    def dessiner_eclaireur(self, obj, tailleF, joueur, type_obj):
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

        x1, y1 = hlp.getAngledPoint(obj.angle_cible+90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x1 - dt), (y1 - dt),
                                 (x1 + dt), (y1 + dt), fill="blue",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        x1, y1 = hlp.getAngledPoint(obj.angle_cible - 90, int(t / 4 * 3), obj.x, obj.y)
        self.canevas.create_oval((x1 - dt), (y1 - dt),
                                 (x1 + dt), (y1 + dt), fill="blue",
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

        #en donnant des

    def cliquer_cosmos(self, evt):
        t = self.canevas.gettags(CURRENT)
        if t:  # il y a des tags
            if t[0] == self.mon_nom:
                self.ma_selection = [self.mon_nom, t[1], t[2]] # Lorsque l'objet est à moi t[1] id objet t[2] type
                if t[2] == "Etoile":
                    self.aff_cadre_opt_etoile()
                    self.montrer_etoile_selection()
                    for i in self.modele.joueurs[self.mon_nom].etoilescontrolees:
                        if i.id == t[1]:
                            self.afficher_info_ressources(i)


                elif t[2] == "Flotte":
                    self.vaisseau_choisi = self.ma_selection
                    self.aff_cadre_opt_vaisseau()
                    # self.montrer_flotte_selection()

            elif ("Etoile" in t or "Porte_de_ver" in t) and t[0] != self.mon_nom:
                if self.ma_selection:
                    #self.deplacer(self.ma_selection[1], t[1], t[2])  # t = tout les tags de l'objet sélectionné
                    self.deplacer(self.vaisseau_choisi[1], t[1], t[2])
                self.vaisseau_choisi = None
                self.ma_selection = None
                self.canevas.delete("marqueur")

        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.ma_selection = None
            self.canevas.delete("marqueur")

    def montrer_etoile_selection(self):
        self.cadreinfochoix.pack(fill=BOTH)

    # def montrer_flotte_selection(self):
    #     print("À IMPLANTER - FLOTTE de ", self.mon_nom)

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

