# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
from functools import partial
import math

import random
import Orion_modele


class Vue:
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.label_etoile_or = None
        self.or_extrait = None
        self.stats_bronze = None
        self.stats_argent = None
        self.stats_or = None
        self.stats_hydrogene = None
        self.stats_nourriture = None
        self.stats_population = None
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
        self.root.title("Je suis " + mon_nom)
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
        # self.canevas.bind("<Button>", self.cliquer_cosmos)
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
        return self.cadrepartie

    def creer_cadre_outils(self):
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="darkgrey")
        self.cadreoutils.pack(side=LEFT, fill=Y)

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

        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="grey30")
        self.btncreerexplorateur = Button(self.cadreinfochoix, text="Explorateur")
        self.btncreerexplorateur.bind("<Button>", self.creer_vaisseau)
        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)
        self.btncreercombattant = Button(self.cadreinfochoix, text="Combattant")
        self.btncreercombattant.bind("<Button>", self.creer_vaisseau)

        self.bouton_explorer = Button(self.cadreoutils, text="Explorer")
        self.bouton_explorer.bind("<Button>", self.exploration)

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
                                      bg="pink")
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

        self.stats_population.set(self.ressources_population)
        self.stats_nourriture.set(self.ressources_nourriture)
        self.stats_hydrogene.set(self.ressources_hydrogene)
        self.stats_or.set(self.ressources_or)
        self.stats_argent.set(self.ressources_argent)
        self.stats_bronze.set(self.ressources_bronze)

        self.cadre_ressources = Frame(self.canevas, bg="pink")

        # self.frame_ress_pop = Frame(self.cadre_ressources, height=50, width=100, bg="gray")
        # self.frame_ress_pop.pack(side=LEFT)
        self.label_pop = Label(self.cadre_ressources, textvariable=self.stats_population, height=2, width=10,
                               relief=SUNKEN)
        self.label_pop.pack(fill=Y, side=LEFT)

        self.label_nourriture = Label(self.cadre_ressources, textvariable=self.stats_nourriture, height=2, width=10,
                                      relief=SUNKEN)
        self.label_nourriture.pack(fill=Y, side=LEFT)

        self.label_hydrogene = Label(self.cadre_ressources, textvariable=self.stats_hydrogene, height=2, width=10,
                                     relief=SUNKEN)
        self.label_hydrogene.pack(fill=Y, side=LEFT)

        self.label_or = Label(self.cadre_ressources, textvariable=self.stats_or, height=2, width=10, relief=SUNKEN)
        self.label_or.pack(fill=Y, side=LEFT)

        self.label_argent = Label(self.cadre_ressources, textvariable=self.stats_argent, height=2, width=10,
                                  relief=SUNKEN)
        self.label_argent.pack(fill=Y, side=LEFT)

        self.label_bronze = Label(self.cadre_ressources, textvariable=self.stats_bronze, height=2, width=10,
                                  relief=SUNKEN)
        self.label_bronze.pack(fill=Y, side=LEFT)

        self.cadre_ressources.pack(side=TOP, anchor=NW)

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
                # if j in mod.joueurs[i].visible:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill="grey80",
                                         tags=(j.proprietaire, str(j.id), "Etoile"))

                # on affiche dans minimap
                # minix = j.x / self.modele.largeur * self.taille_minimap
                # miniy = j.y / self.modele.hauteur * self.taille_minimap
                # self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                #                                       fill=mod.joueurs[i].couleur,
                #                                       tags=(j.proprietaire, str(j.id), "Etoile"))
                t = j.taille * self.zoom
                if j in mod.joueurs[i].visible:
                    if self.mon_nom == mod.joueurs[i].nom:
                        print(mod.joueurs[i].visible)
                        self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                                 fill=mod.joueurs[i].couleur,
                                                 tags=(j.proprietaire, str(j.id), "Etoile"))
                    # on affiche dans minimap

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
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            vaisseau_local = []
            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    if k == "Explorateur":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Cargo":
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j, tailleF, i, k)

                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
                    elif k == "Combattant":
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

        self.afficher_projectiles()
        self.afficher_barrevie()
        self.calculer_ressources()
        self.afficher_carburant()

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
                        self.ma_selection_vaisseau = None
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
                self.canevas.delete("marqueur")
            else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
                print("Region inconnue")
                self.ma_selection = None
                self.canevas.delete("marqueur")
            if self.ma_selection_vaisseau is not None:
                if t[0] != self.mon_nom and t[2] != "Flotte":
                    self.ma_selection_vaisseau = None

    def montrer_etoile_selection(self, etoile):

        if self.label_etoile_or and self.label_etoile_argent and self.label_etoile_bronze and self.label_etoile_hydrogene is not None:
            self.label_etoile_or.pack_forget()
            self.label_etoile_argent.pack_forget()
            self.label_etoile_bronze.pack_forget()
            self.label_etoile_hydrogene.pack_forget()
            self.label_ress_extraites.pack_forget()

        self.cadreinfochoix.pack(fill=BOTH)
        if not self.liste_options_selection_etoile:
            btn_creer_batiment = Button(self.cadreoutils, text="Creer batiment",
                                        command=lambda: self.afficher_creation_batiment(etoile))
            btn_creer_batiment.bind("<Button-1>")
            self.liste_options_selection_etoile.append(btn_creer_batiment)
            btn_creer_batiment.pack()
            for i in etoile.batiments:
                btn_batiment_existant = Button(self.cadreoutils, text=str(i.type) + " niveau " + str(i.niveau),
                                               command=lambda: self.afficher_options_batiment(etoile, i))
                btn_batiment_existant.bind("<Button>")
                self.liste_options_selection_etoile.append(btn_batiment_existant)
                btn_batiment_existant.pack()

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
                for i in range(4):
                    if i % 4 == 0:
                        text = "Creer Ferme"
                    elif i % 4 == 1:
                        text = "Creer Residence"
                    elif i % 4 == 2:
                        text = "Creer Mine"
                    else:
                        text = "Creer Usine"
                    boutonbatiment = Button(self.cadreoutils, text=text)
                    boutonbatiment.bind("<Button-1>", self.creer_batiment)
                    self.wigets_creation_batiment.append(boutonbatiment)
                    boutonbatiment.pack()

    def afficher_options_batiment(self, etoile, batiment):
        self.retirer_infos_etoile()
        if not self.options_batiment:
            btn_ameliorer = Button(self.cadreoutils, text="Ameliorer",
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
            self.label_etoile_or.pack_forget()
            self.label_etoile_argent.pack_forget()
            self.label_etoile_bronze.pack_forget()
            self.label_etoile_hydrogene.pack_forget()
            self.label_ress_extraites.pack_forget()
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

    def montrer_ennemi_selection(self):
        print()

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
                            self.canevas.create_rectangle(p.x - 5, p.y - 5, p.x + 5, p.y + 5, fill="darkgrey",
                                                          tag="dynamique")

    def afficher_barrevie(self):
        mod = self.modele
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte.keys():
                for m in i.flotte[k]:
                    v = i.flotte[k][m]
                    zone_barre = 100 / 4
                    vie_pourcentage = (v.vie_actuelle / v.vie_max * 100) / 4

                    self.canevas.create_rectangle(v.x - zone_barre,
                                                  v.y + 10, v.x + zone_barre,
                                                  v.y + 13, fill="red", tag="dynamique")

                    self.canevas.create_rectangle(v.x - zone_barre,
                                                  v.y + 10, v.x - zone_barre + vie_pourcentage * 2,
                                                  v.y + 13, fill="green", tag="dynamique")

    def afficher_carburant(self):
        mod = self.modele
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte.keys():
                for m in i.flotte[k]:
                    v = i.flotte[k][m]
                    zone_barre = 100 / 4
                    carburant_pourcentage = ((v.carburant / v.carburant_max) * 100) / 2

                    self.canevas.create_rectangle(v.x - zone_barre,
                                                  v.y + 14, v.x + zone_barre,
                                                  v.y + 17, fill="red", tag="dynamique")

                    self.canevas.create_rectangle(v.x - zone_barre,
                                                  v.y + 14, v.x - zone_barre + carburant_pourcentage,
                                                  v.y + 17, fill="yellow", tag="dynamique")

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

    def retirer_infos_vaisseau(self):
        # self.bouton_explorer.pack_forget()
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

        gold = etoile.ressources_extraites.get('or')
        argent = etoile.ressources_extraites.get('argent')
        bronze = etoile.ressources_extraites.get('bronze')
        hydrogene = etoile.ressources_extraites.get('hydrogene')

        self.label_ress_extraites = Label(self.cadreoutils, text='Ressources Extraites', bg='darkgrey')
        self.label_ress_extraites.pack(side=TOP, expand=1, anchor=S)

        self.label_etoile_or = Label(self.cadreoutils, textvariable=self.goldstr, height=3, width=6, relief=SUNKEN)
        self.label_etoile_or.pack(side=LEFT, expand=1, anchor=S)

        self.label_etoile_argent = Label(self.cadreoutils, textvariable=self.argentstr, height=3, width=6,
                                         relief=SUNKEN)
        self.label_etoile_argent.pack(side=LEFT, expand=1, anchor=S)

        self.label_etoile_bronze = Label(self.cadreoutils, textvariable=self.bronzestr, height=3, width=6,
                                         relief=SUNKEN)
        self.label_etoile_bronze.pack(side=LEFT, expand=1, anchor=S)

        self.label_etoile_hydrogene = Label(self.cadreoutils, textvariable=self.hydrostr, height=3, width=6,
                                            relief=SUNKEN)
        self.label_etoile_hydrogene.pack(side=LEFT, expand=1, anchor=S)

        self.goldstr.set(str(gold))
        self.argentstr.set(str(argent))
        self.bronzestr.set(str(bronze))
        self.hydrostr.set(str(hydrogene))
