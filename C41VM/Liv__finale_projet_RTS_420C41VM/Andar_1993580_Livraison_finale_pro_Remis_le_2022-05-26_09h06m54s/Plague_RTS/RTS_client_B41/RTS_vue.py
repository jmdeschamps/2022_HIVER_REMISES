## -*- Encoding: UTF-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *

from typing import Type

from helper import Helper
from RTS_divers import *
from chargeurdimages import *
import RTS_vuecadres


class Vue():
    def __init__(self, parent, urlserveur, monnom, testdispo):
        self.parent = parent
        self.root = Tk()
        self.root.title("PLAGUE RTS - Je suis " + monnom)
        self.root.iconbitmap('images/teams/virus.ico')
        self.monnom = monnom
        # attributs
        self.cadrechaton = 0
        self.textchat = ""
        self.infohud = {}
        self.tailleminicarte = 220

        self.cadreactif = None
        # # objet pour cumuler les manipulations du joueur pour generer une action de jeu
        self.action = Action(self)

        # cadre principal de l'application
        self.cadreapp = Frame(self.root, width=500, height=400, bg="red")
        self.cadreapp.pack(expand=1, fill=BOTH)

        self.images = chargerimages()
        self.gifs = chargergifs()
        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres = {}
        self.creer_cadres(urlserveur, monnom, testdispo)
        self.changer_cadre("splash")

        # self.root.protocol("WM_DELETE_WINDOW", self.demanderabandon)
        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None
        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteuractif = None
        # # images des assets, definies dans le modue loadeurimages

    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre: str):
        cadre = self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif = cadre
        self.cadreactif.pack(expand=1, fill=BOTH)

    ###### LES CADRES ############################################################################################
    def creer_cadres(self, urlserveur: str, monnom: str, testdispo: str):
        self.cadres["splash"] = self.creer_cadre_splash(urlserveur, monnom, testdispo)
        self.cadres["lobby"] = self.creer_cadre_lobby()
        self.cadres["jeu"] = self.creer_cadre_jeu()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def creer_cadre_splash(self, urlserveur: str, monnom: str, testdispo: str) -> Frame:
        self.cadresplash = Frame(self.cadreapp)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevassplash = Canvas(self.cadresplash, width=600, height=480, bg="DarkOliveGreen1")
        self.canevassplash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # self.logo = Label(image=self.images["logo"])
        self.etatdujeu = Label(text=testdispo, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14))
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, monnom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevassplash
        self.canevassplash.create_image(320, 10, image=self.images["logo"])
        self.canevassplash.create_window(320, 200, window=self.etatdujeu, width=400, height=30)
        self.canevassplash.create_window(320, 250, window=self.nomsplash, width=400, height=30)
        self.canevassplash.create_window(240, 300, window=self.urlsplash, width=200, height=30)
        self.canevassplash.create_window(420, 300, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 11), state=DISABLED,
                               command=self.reset_partie)

        # on place les autres boutons
        self.canevassplash.create_window(320, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevassplash.create_window(320, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevassplash.create_window(320, 450, window=self.btnreset, width=200, height=30)

        ############# NOTE le bouton suivant permet de générer un Frame issu d'un autre module et l'intégrer à la vue directement
        # self.btncadretest = Button(text="Cadre test", font=("Arial", 9),  command=self.montrercadretest)
        # on place les autres boutons
        # self.canevassplash.create_window(120, 450, window=self.btncadretest, width=200, height=30)
        ##############

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadresplash

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)

    ###########  cette fonction la creation d'un frame par un autre module - pour fin de test uniquement
    # def montrercadretest(self):
    #     self.cadretest=RTS_vuecadres.Cadre_test(self)
    #     print(self.cadretest.nom)
    #     self.cadretest.grid(in_=self.canevas,row=0,column=0)
    ########## fin fonction test pour auttre module

    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadreapp)
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

    ### cadre de jeu : inclus aire de jeu, le HUD, le cadre_jeu_action
    def creer_cadre_jeu(self):
        # le cadre principal du jeu, remplace le Lobby
        self.cadrepartie = Frame(self.cadreapp, bg="#d36060", width=400, height=400)
        # cadre du jeu et ses scrollbars
        self.creer_aire_de_jeu()
        # cadre pour info sur les ressources du joueur en haut de l'aire de jeu
        self.creer_HUD()
        # cadre pour commandes et infos des objets de jeu, situe a droite
        self.creer_cadre_jeu_action()
        # configuration de la section qui s'etire lorsque la fenetre change de taille
        self.cadrepartie.rowconfigure(0, weight=1)
        self.cadrepartie.columnconfigure(0, weight=1)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrepartie

    def creer_aire_de_jeu(self):
        # definition du cadre avec le canvas de jeu et les scrollbars
        self.cadrecanevas = Frame(self.cadrepartie)
        # on crée les scrollbar AVANT le canevas de jeu car le canevas est dépendant de leur
        self.scrollV = Scrollbar(self.cadrecanevas, orient=VERTICAL)
        self.scrollH = Scrollbar(self.cadrecanevas, orient=HORIZONTAL)
        self.canevas = Canvas(self.cadrecanevas, width=400, height=400, bg="salmon",
                              yscrollcommand=self.scrollV.set,
                              xscrollcommand=self.scrollH.set)
        self.scrollV.config(command=self.canevas.yview)
        self.scrollH.config(command=self.canevas.xview)
        # on visualise utilisant grid (grille)
        # le grid avec 'sticky' indique que l'objet doit s'acroitre pour coller aux 'points cardinaux' (anglais)
        self.canevas.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollV.grid(row=1, column=1, sticky=N + S)
        self.scrollH.grid(row=2, column=0, sticky=E + W)

        # visualise le cadre qui contient le canevas de jeu
        self.cadrecanevas.grid(column=0, row=0, sticky=N + S + E + W)
        # on doit preciser quelle partie de la grille (grid) va s'accroitre, colonne et rangée
        # ici on precise que c'est le canevas et non les scrollbar qui doit s'agrandir
        self.cadrecanevas.rowconfigure(1, weight=1)
        self.cadrecanevas.columnconfigure(0, weight=1)
        self.connecter_event()

    def creer_HUD(self):
        self.cadrejeuinfo = Frame(self.cadrecanevas, bg="blue")
        # des etiquettes d'info
        self.infohud = {"Sang:": None,
                        "Matière Organique:": None,
                        "DNA:": None,
                        "Supply:": None, }

        # fonction interne uniquement pour reproduire chaque info de ressource
        def creer_champ_interne(listechamp):
            titre = Champ(self.cadrejeuinfo, text=i, bg="red", fg="white")
            varstr = StringVar()
            varstr.set(0)
            donnee = Champ(self.cadrejeuinfo, bg="red", fg="white", textvariable=varstr)
            titre.pack(side=LEFT)
            donnee.pack(side=LEFT)
            self.infohud[i] = [varstr, donnee]

        ## on l'appelle pour chaque chose de self.infohud
        for i in self.infohud.keys():
            creer_champ_interne(i)

        varstr = StringVar()
        varstr.set("")
        ### champ supplémentaire pour afficher des messages...
        champmsg = Label(self.cadrejeuinfo, text="", fg="red")
        champmsg.pack(side=LEFT)
        self.infohud["msggeneral"] = [champmsg]

        self.btnchat = Button(self.cadrejeuinfo, text="Chat", command=self.action.chatter)
        self.btnaide = Button(self.cadrejeuinfo, text="Aide", command=self.action.aider)
        self.btnskill = Button(self.cadrejeuinfo, text="Skill", command=self.action.victoire)

        self.btnaide.pack(side=RIGHT)
        self.btnchat.pack(side=RIGHT)
        self.btnskill.pack(side=RIGHT)

        self.cadrejeuinfo.grid(row=0, column=0, sticky=E + W, columnspan=2)

    def creer_cadre_jeu_action(self):
        # Ajout du cadre d'action a droite pour identifier les objets permettant les commandes du joueur
        self.cadreaction = Frame(self.cadrepartie)
        self.cadreaction.grid(row=0, column=1, sticky=N + S)
        self.scrollVaction = Scrollbar(self.cadreaction, orient=VERTICAL)
        self.canevasaction = Canvas(self.cadreaction, width=200, height=300, bg="lightblue",
                                    yscrollcommand=self.scrollVaction.set)

        self.scrollVaction.config(command=self.canevasaction.yview)
        self.canevasaction.grid(row=0, column=0, sticky=N + S)
        self.scrollVaction.grid(row=0, column=1, sticky=N + S)
        # les widgets
        self.canevasaction.create_text(100, 30, text=self.parent.monnom, font=("arial", 18, "bold"), anchor=S,
                                       tags=("nom"))

        # minicarte
        self.minicarte = Canvas(self.cadreaction, width=self.tailleminicarte, height=self.tailleminicarte, bg="salmon",
                                highlightthickness=0)
        self.minicarte.grid(row=2, column=0, columnspan=2)
        self.minicarte.bind("<Button-1>", self.deplacer_carte)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        self.canevasaction.rowconfigure(0, weight=1)
        self.cadreaction.rowconfigure(0, weight=1)

    def connecter_event(self):
        # actions de clics sur la carte
        self.canevas.bind("<Button-1>", self.annuler_action)
        self.canevas.bind("<Button-2>", self.indiquer_position)
        self.canevas.bind("<Button-3>", self.construire_batiment)
        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)
        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)
        self.canevas.bind("<Control-Motion>", self.defiler)

        # acgtions liées aux objets dessinés par tag
        self.canevas.tag_bind("batiment", "<Button-1>", self.ajouter_selection_batiment)
        self.canevas.tag_bind("perso", "<Button-1>", self.ajouter_selection)
        self.canevas.tag_bind("organe", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("eau", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("globuleRouge", "<Button-1>", self.chasser_ressource)

        self.canevas.bind("<Control-Button-1>", self.parent.montrer_stats)

        self.canevas.tag_bind("territoire", "<Button-1>", self.annuler_action)
        self.canevas.tag_bind("territoire", "<Button-2>", self.indiquer_position)
        self.canevas.tag_bind("territoire", "<Button-3>", self.construire_batiment)

        self.canevas.tag_bind("perso", "<Button-2>", self.attaquer)
        self.canevas.tag_bind("batiment", "<Button-2>", self.attaquer)
       # self.canevas.tag_bind("biotope", "<Button-2>", self.attaquer)

### TEST ####
    #     self.canevas.bind("<Shift-Button-2>", self.kill_batiment)
    #
    # def kill_batiment(self, evt):
    #     for j in self.modele.joueurs.keys():
    #         for a in self.modele.joueurs[j].batiments.keys():
    #             for b in self.modele.joueurs[j].batiments[a]:
    #                 self.modele.joueurs[j].batiments[a][b].hp = 0
### FIN TEST ####

    def defiler_vertical(self, evt):
        rep = self.scrollV.get()[0]
        if evt.delta < 0:
            rep = rep + 0.01
        else:
            rep = rep - 0.01
        self.canevas.yview_moveto(rep)

    def defiler_horizon(self, evt):
        rep = self.scrollH.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

    def defiler(self, evt):
        x, y = evt.x, evt.y

        if x < 20:
            delta = -1
            self.canevas.xview('scroll', delta, 'units')

        if x > (self.canevas.winfo_width() - 20):
            delta = 1
            self.canevas.xview('scroll', delta, 'units')

        if y < 20:
            delta = -1
            self.canevas.yview('scroll', delta, 'units')

        if y > (self.canevas.winfo_height() - 20):
            delta = 1
            self.canevas.yview('scroll', delta, 'units')

    ### cadre qui s'Affichera par-dessus le canevas de jeu pour l'aide
    def creer_aide(self):
        self.cadreaide = Frame(self.canevas)
        self.scrollVaide = Scrollbar(self.cadreaide, orient=VERTICAL)
        self.textaide = Text(self.cadreaide, width=50, height=10,
                             yscrollcommand=self.scrollVaide.set)
        self.scrollVaide.config(command=self.textaide.yview)
        self.textaide.pack(side=LEFT)
        self.scrollVaide.pack(side=LEFT, expand=1, fill=Y)
        fichieraide = open("aide.txt")
        monaide = fichieraide.read()
        fichieraide.close()
        self.textaide.insert(END, monaide)
        self.textaide.config(state=DISABLED)

    ### cadre qui affichera un chatbox
    def creer_chatter(self):
        self.cadrechat = Frame(self.canevas, bd=2, bg="orange")
        self.cadrechatlist = Frame(self.cadrechat)

        self.scrollVchat = Scrollbar(self.cadrechatlist, orient=VERTICAL)
        self.textchat = Listbox(self.cadrechatlist, width=30, height=6,
                                yscrollcommand=self.scrollVchat.set)
        self.scrollVchat.config(command=self.textchat.yview)
        self.textchat.pack(side=LEFT)
        self.scrollVchat.pack(side=LEFT, expand=1, fill=Y)
        self.textchat.delete(0, END)
        self.cadrechatlist.pack()
        # inscrire texte et choisir destinataire
        self.cadreparler = Frame(self.cadrechat, bd=2)
        self.joueurs = ttk.Combobox(self.cadreparler,
                                    values=list(self.modele.joueurs.keys()))
        self.entreechat = Entry(self.cadreparler, width=20)
        self.entreechat.bind("<Return>")  # ,self.action.envoyerchat)
        self.joueurs.pack(expand=1, fill=X)
        self.entreechat.pack(expand=1, fill=X)
        self.cadreparler.pack(expand=1, fill=X)

    def cadrevictoire(self):
        self.windowwin = Tk()
        self.cadrevictoire = Frame(self.windowwin, width=500, height=400)
        self.canevasvictoire = Canvas(self.cadrevictoire, width=600, height=480, bg="DarkOliveGreen1")
        self.canevasvictoire.pack()

        # self.condition = ""
        self.windowwin.title("GAME OVER")

        if self.victoireon == 0:
            # self.condition = Label(self.windowwin, text="T'est un WINNER mon chum")
            self.canevasvictoire.create_image(320, 10, image=self.images['win'])
        else:
            # self.condition = Label(self.windowwin, text="LMAOO! T'as pas gagné HAHAHAHAHAH, pleure")
            self.canevasvictoire.create_image(320, 10, image=self.images['lose'])

        # self.condition.config(font=('Comic Sans MS', 20), wraplength=250)
        # self.condition.pack()


    ##### FONCTIONS DU SPLASH #########################################################################
    def creer_partie(self):
        nom = self.nomsplash.get()
        self.parent.creer_partie(nom)

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

    def reset_partie(self):
        rep = self.parent.reset_partie()

    def initialiser_avec_modele(self, modele):
        self.modele = modele
        # on reassigne le nom final localement pour eviter
        # de toujours le requerir du parent
        self.monnom = self.parent.monnom
        # on ajuste la taille du canevas de jeu
        self.canevas.config(scrollregion=(0, 0, self.modele.aireX, self.modele.aireY))
        self.canevasaction.delete("nom")
        self.canevasaction.create_text(100, 30, text=self.monnom, font=("arial", 18, "bold"), anchor=S, tags=("nom"))

        # on cree les cadres affichant les items d'actions du joueur
        # cadre apparaissant si on selectionne un ouvrier
        coul = self.modele.joueurs[self.parent.monnom].couleur
        coul = self.modele.joueurs[self.parent.monnom].couleur
        self.cadrejeuinfo.config(bg=coul[1])
        self.creer_aide()
        self.creer_cadre_ouvrier(coul[0] + "_", ["maison", "watchtower", "barracks", "turrets"])
        self.creer_cadre_maison(coul[0] + "_", "ouvrier")
        self.creer_cadre_barracks(coul[0] + "_", ["druide", "soldat", "ballista"])
        self.creer_chatter()
        # on affiche les maisons, point de depart des divers joueurs
        self.afficher_depart()
        self.root.update()
        # self.centrer_maison()

    def creer_cadre_ouvrier(self, coul, artefacts):
        self.cadreouvrier = Frame(self.canevasaction)
        for i in artefacts:
            if i == "watchtower":
                btn = Button(self.cadreouvrier, text=i, image=self.images[coul + "icon_" + i])
            else:
                btn = Button(self.cadreouvrier, text=i, image=self.images[coul + i])
            btn.bind("<Button>", self.batir_artefact)
            btn.pack()

    # def creer_cadre_batiment(self, coul, artefacts):
    #     self.cadrebatiment = Frame(self.canevasaction)
    #
    #     for i in artefacts:
    #         btn = Button(self.cadrebatiment, text=i, image=self.images[coul + i + "D"])
    #         btn.bind("<Button>", self.batir_artefact)
    #         btn.pack()

    def creer_cadre_maison(self, coul, artefact):
        self.cadremaison = Frame(self.canevasaction)

        btn = Button(self.cadremaison, text=artefact, image=self.images[coul + artefact])
        btn.bind("<Button>", self.creer_entite)
        btn.pack()

    def creer_cadre_barracks(self, coul, artefacts):
        self.cadrebarracks = Frame(self.canevasaction)

        for i in artefacts:
            btn = Button(self.cadrebarracks, text=i, image=self.images[coul + i])
            btn.bind("<Button>", self.creer_entite)
            btn.pack()

    # def creer_cadre_cellules(self, coul, artefacts):
    #     self.cadrecellules = Frame(self.canevasaction)
    #     for i in artefacts:
    #         btn = Button(self.cadrecellules, text=i, image=self.images[coul + i])
    #         btn.bind("<Button>", self.batir_artefact)
    #         btn.pack()

    ##FONCTIONS D'AFFICHAGES##################################
    def afficher_depart(self):
        self.modele.listebiotopes.sort(key=lambda c: c.y)
        for i in self.modele.listebiotopes:
            if i.montype == "globuleRouge":
                monitem = self.canevas.create_image(i.x, i.y, image=self.images[i.img], anchor=S,
                                                    tags=("mobile", "", i.id, "biotope", i.montype, ""))
                # tags=("mobile","",i.id,)
            else:
                monitem = self.canevas.create_image(i.x, i.y, image=self.images[i.img], anchor=S,
                                                    tags=("statique", "", i.id, "biotope", i.montype, ""))
                # tags=("mobile","",i.id,)

        self.modele.listebiotopes = []
        minitaillecase = int(self.tailleminicarte / self.modele.taillecarte)
        couleurs = {0: "",
                    "arbre": "light green",
                    "eau": "light blue",
                    "marais": "orange"}
        for i, t in enumerate(self.modele.regions):
            if t != "plaine":
                for j, c in enumerate(self.modele.regions[t]):
                    for cle, k in self.modele.regions[t][c].dicocases.items():
                        y1 = k.y * minitaillecase
                        y2 = y1 + minitaillecase
                        x1 = k.x * minitaillecase
                        x2 = x1 + minitaillecase
                        self.minicarte.create_rectangle(x1, y1, x2, y2, outline="",
                                                        # fill=couleurs[self.modele.cartecase[k[1]][k[0]].type]),
                                                        fill=couleurs[k.parent.montype])

        # Affichage des batiments intiaux sur l'aire de jeu et sur la minicarte
        px = int(self.tailleminicarte / self.modele.aireX)
        py = int(self.tailleminicarte / self.modele.aireY)

        for j in self.modele.joueurs.keys():
            for k in self.modele.joueurs[j].batiments.keys():
                for i in self.modele.joueurs[j].batiments[k]:

                    m = self.modele.joueurs[j].batiments[k][i]
                    coul = self.modele.joueurs[j].couleur[0]

                    self.canevas.create_image(m.x, m.y, image=self.images[coul + "_maison"],
                                              tags=("statique", j, m.id, "batiment", m.montype, "vivant"))

                    # afficher sur minicarte
                    couleur = self.modele.joueurs[j].couleur[1]
                    x1 = int((m.x / self.modele.aireX) * self.tailleminicarte)
                    y1 = int((m.y / self.modele.aireY) * self.tailleminicarte)
                    self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=couleur,
                                                    tags=(j, m.id, "artefact", "maison"))

    def afficher_bio(self, bio):
        self.canevas.create_image(bio.x, bio.y, image=self.images[bio.img],
                                  tags=("statique", "", bio.id, "biotope", bio.montype, ""))
        x1 = int((bio.x / 4000) * self.tailleminicarte)
        y1 = int((bio.y / 4000) * self.tailleminicarte)
        if bio.montype == "beacon":
            self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="black",
                                            tags=(self.parent.monnom, bio.id, "biotope", bio.montype))
        else:
            self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="red",
                                            tags=(self.parent.monnom, bio.id, "biotope", bio.montype))

    def afficher_batiment(self, joueur, batiment):

        self.canevas.delete(batiment.id)

        print(self.parent.monnom)
        chose = self.canevas.create_image(batiment.x, batiment.y, image=self.images[batiment.image],
                    tags=("statique", joueur, batiment.id, "batiment", batiment.montype, "vivant"))

        x0, y0, x2, y2 = self.canevas.bbox(chose)

        coul = self.modele.joueurs[joueur].couleur[1]
        x1 = int((batiment.x / self.modele.aireX) * self.tailleminicarte)
        y1 = int((batiment.y / self.modele.aireY) * self.tailleminicarte)
        self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=coul,
                                        tags=(joueur, batiment.id, "artefact", batiment.montype))
        return [x0, y0, x2, y2]

    def afficher_jeu(self):

        # On efface tout ce qui est 'mobile' (un tag)
        self.canevas.delete("mobile")

        # on se debarrasse des choses mortes (disparues), le id est dans le tag du dessin
        for i in self.modele.ressourcemorte:
            self.canevas.delete(i.id)

        # commencer par les choses des joueurs
        for j in self.modele.joueurs.keys():
            # ajuster les infos du HUD
            if j == self.parent.monnom:
                self.infohud["Sang:"][0].set(self.modele.joueurs[j].ressources["Sang"])
                self.infohud["Matière Organique:"][0].set(self.modele.joueurs[j].ressources["Matière Organique"])
                self.infohud["DNA:"][0].set(self.modele.joueurs[j].ressources["DNA"])
                self.infohud["Supply:"][0].set(
                    str(self.modele.joueurs[j].current_supply) + "/" + str(self.modele.joueurs[j].total_supply))
                self.infohud["msggeneral"][0].config(text=self.modele.msggeneral)

            # ajuster les constructions de chaque joueur
            for p in self.modele.joueurs[j].batiments['siteconstruction']:
                s = self.modele.joueurs[j].batiments['siteconstruction'][p]
                if s.etat == "attente":
                    self.canevas.create_image(s.x, s.y, anchor=CENTER, image=self.images["siteX"],
                                              tags=("mobile", j, p, "batiment", type(s).__name__, ""))
                    # tags=(j,s.id,"artefact","mobile","siteconstruction","batiments"))
                else:
                    self.canevas.create_image(s.x, s.y, anchor=CENTER, image=self.images["EnConstruction"],
                                              tags=("mobile", j, p, "batiment", type(s).__name__, ""))

            for a in self.modele.joueurs[j].batiments.keys():
                if a == "siteconstruction":
                    continue
                for b in self.modele.joueurs[j].batiments[a]:

                    m = self.modele.joueurs[j].batiments[a][b]

                    self.canevas.create_line(m.x - 50, m.y - 75, (m.x - 50) + 100, m.y - 75, width=10, fill="black",
                                             tags=("mobile"))
                    self.canevas.create_line(m.x - 50, m.y - 75, (m.x - 50) + (m.hp * 5), m.y - 75, width=10, fill="green",
                                             tags=("mobile"))

            # ajuster les persos de chaque joueur et leur dépendance (ici javelots des ouvriers)
            for p in self.modele.joueurs[j].persos.keys():
                for k in self.modele.joueurs[j].persos[p].keys():
                    i = self.modele.joueurs[j].persos[p][k]
                    coul = self.modele.joueurs[j].couleur[0]
                    self.canevas.create_image(i.x, i.y, anchor=S, image=self.images[i.image],
                                              tags=("mobile", j, k, "perso", i.montype, ""))
                    # tags=(j,k,"artefact","mobile","perso",p))
                    self.canevas.create_line(i.x - 15, i.y - 60, (i.x - 15) + 30, i.y - 60, width=10, fill="black",
                                             tags=("mobile"))
                    self.canevas.create_line(i.x - 15, i.y - 60, (i.x - 15) + (i.hp * 15), i.y - 60, width=10, fill="green",
                                             tags=("mobile"))

                    if k in self.action.persochoisi:
                        self.canevas.create_rectangle(i.x - 10, i.y + 5, i.x + 10, i.y + 10, fill="yellow",
                                                      tags=("mobile", j, p, "perso", i.montype, "persochoisi"))
                        # tags=(j,k,"artefact","mobile","persochoisi"))

                    # dessiner javelot de l'ouvrier
                    if p == "ouvrier":
                        for b in self.modele.joueurs[j].persos[p][k].javelots:
                            self.canevas.create_image(b.x, b.y, image=self.images[b.image],
                                                      tags=("mobile", j, b.id, "", type(b).__name__, ""))
                            # tags=(j,b.id,"artefact","mobile","javelot"))

        # ajuster les choses vivantes dependantes de la partie (mais pas des joueurs)
        for j in self.modele.biotopes["globuleRouge"].keys():
            i = self.modele.biotopes["globuleRouge"][j]
            if i.etat == "mort":
                self.canevas.create_image(i.x, i.y, image=self.images["globulerougeMORT"],
                                          tags=("mobile", "", i.id, "biotope", i.montype, ""))
            else:
                self.canevas.create_image(i.x, i.y, image=self.images[i.img],
                                          tags=("mobile", "", i.id, "biotope", i.montype, ""))

            self.canevas.create_line(i.x - 15, i.y - 50, (i.x - 15) + 30, i.y - 50, width=10, fill="black",
                                     tags=("mobile", i.id, "artefact", ""))
            self.canevas.create_line(i.x - 15, i.y - 50, (i.x - 15) + (i.hp * 30), i.y - 50, width=10, fill="green",
                                     tags=("mobile", i.id, "artefact", ""))

        # mettre les chat a jour si de nouveaux messages sont arrives
        if self.textchat and self.modele.joueurs[self.parent.monnom].chatneuf:
            self.textchat.delete(0, END)
            self.textchat.insert(END, *self.modele.joueurs[self.parent.monnom].monchat)
            if self.modele.joueurs[self.parent.monnom].chatneuf and self.action.chaton == 0:
                self.btnchat.config(bg="orange")
            self.modele.joueurs[self.parent.monnom].chatneuf = 0

        # affichage NPC
        for j in self.modele.NPCs["globuleBlanche"].keys():
            i = self.modele.NPCs["globuleBlanche"][j]
            self.canevas.create_image(i.x, i.y, image=self.images[i.image],
                                      tags=("mobile", "", i.id, "perso", type(i).__name__, ""))

    def afficher_ruine(self, batiment):
        self.canevas.create_image(batiment.x, batiment.y, image=self.images[batiment.montype + "MORT"],
                                  tags=("statique", "", "", "ruine", "", "mort"))

    def centrer_maison(self):
        self.root.update()
        cle = list(self.modele.joueurs[self.monnom].batiments["maison"].keys())[0]
        x = self.modele.joueurs[self.monnom].batiments["maison"][cle].x
        y = self.modele.joueurs[self.monnom].batiments["maison"][cle].y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.aireX
        pcty = (y - y1) / self.modele.aireY

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    ##### ACTIONS DU JOUEUR #######################################################################

    def annuler_action(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        if not mestags or "territoire" in mestags:
            self.canevasaction.delete(self.action.widgetsactifs)
            if self.action.btnactif:
                self.action.btnactif.config(bg="SystemButtonFace")
            self.action = Action(self)

    def fermer_chat(self):
        self.textchat = None
        self.fenchat.destroy()

    def ajouter_selection(self, evt):
        self.canevasaction.delete(self.action.widgetsactifs)
        if self.action.btnactif:
            self.action.btnactif.config(bg="SystemButtonFace")
        self.action = Action(self)
        mestags = self.canevas.gettags(CURRENT)
        if self.parent.monnom == mestags[1]:
            if "Ouvrier" == mestags[4] or "ouvrier" == mestags[4]:
                self.action.persochoisi.append(mestags[2])
                self.action.afficher_commande_perso()
            ######
            else:
                self.action.persochoisi.append(mestags[2])

        # BUG quand on attaque
        # elif self.action.persochoisi!= []:
        #     self.action.ciblechoisi=mestags
        #     self.action.attaquer()

    def ajouter_selection_batiment(self, evt):
        self.canevasaction.delete(self.action.widgetsactifs)
        if self.action.btnactif:
            self.action.btnactif.config(bg="SystemButtonFace")
        self.action = Action(self)
        mestags = self.canevas.gettags(CURRENT)
        self.action.derniertagchoisi = mestags
        if mestags[5] == "vivant":
            self.action.posbatiment = [evt.x, evt.y]
            if self.parent.monnom == mestags[1]:
                if "batiment" == mestags[3]:
                    if "maison" == mestags[4]:
                        self.action.batimentchoisi.append(mestags[2])
                        self.action.afficher_commande_maison()
                    elif "barracks" == mestags[4]:
                        self.action.batimentchoisi.append(mestags[2])
                        self.action.afficher_commande_barracks()

    # Methodes pour multiselect
    def debuter_multiselection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteuractif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline="red", width=2,
                                                            dash=(2, 2), tags=("", "selecteur", "", "artefact"))

    def afficher_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteuractif, x1, y1, x2, y2)

    def terminer_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.debutselect = []
            objchoisi = (list(self.canevas.find_enclosed(x1, y1, x2, y2)))
            for i in objchoisi:
                if self.parent.monnom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.action.persochoisi.append(self.canevas.gettags(i)[2])

            if self.action.persochoisi:
                self.action.afficher_commande_perso()
            self.canevas.delete("selecteur")

    # Fin du multiselect

    def ramasser_ressource(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if tag[1] == "" and self.action.persochoisi:
            self.action.ramasser_ressource(tag)
        else:
            print(tag[4])

    def chasser_ressource(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if tag[1] == "" and self.action.persochoisi and tag[4] == "globuleRouge":
            self.action.chasser_ressource(tag)
        else:
            print(tag[3])

    def attaquer(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if self.action.persochoisi:
            self.action.attaquer(tag)

    def indiquer_position(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if (not tag or "territoire" in tag) and self.action.persochoisi:
            x, y = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.position = [x, y]
            self.action.deplacer()

    # Cette fonction permet se se deplacer via un click sur la minicarte
    def deplacer_carte(self, evt):
        x = evt.x
        y = evt.y

        pctx = x / self.tailleminicarte
        pcty = y / self.tailleminicarte

        xl = (self.canevas.winfo_width() / 2) / self.modele.aireX
        yl = (self.canevas.winfo_height() / 2) / self.modele.aireY

        self.canevas.xview_moveto(pctx - xl)
        self.canevas.yview_moveto(pcty - yl)
        xl = self.canevas.winfo_width()
        yl = self.canevas.winfo_height()

    def batir_artefact(self, evt):
        # on obtient l'information du bouton de menu cliquer
        obj = evt.widget
        if self.action.btnactif:  # si un autre bouton etait deja choisi
            if self.action.btnactif != obj:  # et qu'il est different du nouveau
                self.action.btnactif.config(bg="SystemButtonFace")  # change couleur pour deselection du precedent
        # test de cout a cet endroit
        nomsorte = obj.cget("text")  # on utilise pour identifier la sorte de batiment à produire
        self.action.btnactif = obj

        # on valide qu'on a assez de ressources pour construire
        vals = self.parent.trouver_valeurs()
        ok = 1
        for k, val in self.modele.joueurs[self.monnom].ressources.items():
            if val < vals[nomsorte][k]:
                ok = 0  # on indique qu'on a PAS les ressources
                break
        if ok:
            self.action.prochaineaction = obj.cget("text")
            obj.config(bg="lightgreen")
        else:
            self.action.btnactif.config(bg="SystemButtonFace")
            print("VOUS N'AVEZ PAS ASSEZ DE", k)

    def construire_batiment(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        if (not mestags or "territoire" in mestags) and self.action.persochoisi and self.action.prochaineaction:
            pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.construire_batiment(pos)

    def creer_entite(self, evt):
        type_batiment = self.action.derniertagchoisi[4]
        posbatiment = self.action.posbatiment

        if type_batiment == "maison":
            type_unite = "ouvrier"
        elif type_batiment == "barracks":
            obj = evt.widget
            if self.action.btnactif:  # si un autre bouton etait deja choisi
                if self.action.btnactif != obj:  # et qu'il est different du nouveau
                    self.action.btnactif.config(bg="SystemButtonFace")  # change couleur pour deselection du precedent
            type_unite = obj.cget("text")
            self.action.btnactif = obj

        vals = self.parent.trouver_valeurs()
        ok = 1

        if self.parent.monnom in self.action.derniertagchoisi:
            if "batiment" in self.action.derniertagchoisi:
                if "maison" in self.action.derniertagchoisi:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break

                if "barracks" in self.action.derniertagchoisi:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break

                if ok:
                    pos = (posbatiment[0], posbatiment[1])
                    action = [self.parent.monnom, "creerperso",
                              [type_unite, self.action.derniertagchoisi[4], self.action.derniertagchoisi[2], pos]]
                    self.parent.actionsrequises.append(action)
                else:
                    print("VOUS N'AVEZ PAS ASSEZ DE", k)

    def creer_entite1(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        type_batiment = mestags[4]
        if type_batiment == "maison":
            type_unite = "ouvrier"
        elif type_batiment == "watchtower":
            type_unite = "druide"
        elif type_batiment == "barracks":
            type_unite = "soldat"
        elif type_batiment == "turrets":
            type_unite = "ballista"

        vals = self.parent.trouver_valeurs()

        ok = 1

        if self.parent.monnom in mestags:
            if "batiment" in mestags:
                if "maison" in mestags:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break
                if "cellanimal" in mestags:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break
                if "watchtower" in mestags:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break
                if "barracks" in mestags:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break
                if "turrets" in mestags:
                    for k, val in self.modele.joueurs[self.monnom].ressources.items():
                        if val < vals[type_unite][k]:
                            ok = 0
                            break

                if ok:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.parent.monnom, "creerperso", [type_unite, mestags[4], mestags[2], pos]]
                    self.parent.actionsrequises.append(action)
                else:
                    print("VOUS N'AVEZ PAS ASSEZ DE", k)

        ###### les ATTAQUES SUR BATIMENT INACTIFS
        # elif self.action.persochoisi:
        #     self.action.ciblechoisi=mestags
        #     self.action.attaquer()

    # def afficher_nouveau_territoire(self, territoire):
    #     for i in territoire:
    #         self.canevas.create_rectangle(i.x * 20 - 10, i.y * 20 - 10, i.x * 20 + 10, i.y * 20 + 10, outline="",
    #                                       fill="brown", tags=("territoire", "statique"))
    #
    #         x1 = int((i.x * 20 / self.modele.aireX) * self.tailleminicarte)
    #         y1 = int((i.y * 20 / self.modele.aireY) * self.tailleminicarte)
    #
    #         self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, outline="",
    #                                         fill="brown", tags=("territoire", "statique"))
    #         self.canevas.tag_lower("territoire")
    #         self.minicarte.tag_lower("territoire")

    def afficher_nouveau_territoire(self, territoire, coul):

        topleft = territoire[0]
        bottomright = territoire[-1]

        # self.canevas.create_rectangle(topleft.x * 20 - 10, topleft.y * 20 - 10, bottomright.x * 20 + 10, bottomright.y * 20 + 10, outline="",
        #                               fill=coul, tags=("territoire", "statique"))

        self.canevas.create_rectangle(topleft.x * 20, topleft.y * 20, bottomright.x * 20 + 20,
                                      bottomright.y * 20 + 20, outline="",
                                      fill=coul, tags=("territoire", "statique"))

        x1 = int((topleft.x * 20 / self.modele.aireX) * self.tailleminicarte)
        y1 = int((topleft.y * 20 / self.modele.aireY) * self.tailleminicarte)
        x2 = int(((bottomright.x * 20 + 20) / self.modele.aireX) * self.tailleminicarte)
        y2 = int(((bottomright.y * 20 + 20) / self.modele.aireY) * self.tailleminicarte)

        self.minicarte.create_rectangle(x1, y1, x2, y2, outline="",
                                        fill=coul, tags=("territoire", "statique"))
        self.canevas.tag_lower("territoire")
        self.minicarte.tag_lower("territoire")


# Singleton (mais pas automatique) sert a conserver les manipulations du joueur pour demander une action
######   CET OBJET SERVIRA À CONSERVER LES GESTES ET INFOS REQUISES POUR PRODUIRE UNE ACTION DE JEU
class Action():
    def __init__(self, parent):
        self.parent = parent
        self.persochoisi = []
        self.batimentchoisi = []
        self.ciblechoisi = None
        self.position = []
        self.btnactif = None  # le bouton choisi pour creer un batiment
        self.prochaineaction = None  # utiliser pour les batiments seulement
        self.widgetsactifs = []
        self.chaton = 0
        self.aideon = 0
        self.skillon = 0
        self.victoireon = 0
        self.derniertagchoisi = None
        self.posbatiment = None
        # self.images = chargerimages()

    def attaquer(self, evt):
        tag = self.parent.canevas.gettags(CURRENT)
        print("AA")
        if self.persochoisi:
            print("AAA")
            qui = tag[1]
            cible = tag[2]
            sorte = tag[4]
            action = [self.parent.parent.monnom, "attaquer", [self.persochoisi, [qui, cible, sorte]]]
            self.parent.parent.actionsrequises.append(action)

    def mouvementAgressif(self):
        if self.persochoisi:
            qui = self.ciblechoisi[1]
            cible = self.ciblechoisi[2]
            sorte = self.ciblechoisi[5]

            action = [self.parent.parent.monnom, "attaquer", [self.persochoisi, [qui, cible, sorte]]]
            self.parent.parent.actionsrequises.append(action)

    def deplacer(self):
        if len(self.persochoisi) > 1:
            action = [self.parent.parent.monnom, "deplacerGroupe",
                      [self.position, self.persochoisi, len(self.persochoisi)]]
            self.parent.parent.actionsrequises.append(action)

        elif self.persochoisi:
            action = [self.parent.parent.monnom, "deplacer", [self.position, self.persochoisi]]
            self.parent.parent.actionsrequises.append(action)

    def chasser_ressource(self, tag):
        if self.persochoisi:
            action = [self.parent.parent.monnom, "chasserressource", [tag[4], tag[2], self.persochoisi]]
            self.parent.parent.actionsrequises.append(action)

    def ramasser_ressource(self, tag):
        if self.persochoisi:
            action = [self.parent.parent.monnom, "ramasserressource", [tag[4], tag[2], self.persochoisi]]
            self.parent.parent.actionsrequises.append(action)

    def construire_batiment(self, pos):
        self.btnactif.config(bg="SystemButtonFace")
        self.btnactif = None
        action = [self.parent.monnom, "construirebatiment", [self.persochoisi, self.prochaineaction, pos]]
        self.parent.parent.actionsrequises.append(action)

    def afficher_commande_perso(self):
        self.widgetsactifs = self.parent.canevasaction.create_window(100, 60,
                                                                     window=self.parent.cadreouvrier,
                                                                     anchor=N)
        self.parent.root.update()
        fh = self.parent.cadreouvrier.winfo_height()
        ch = int(self.parent.canevasaction.cget("height"))
        if fh + 60 > ch:
            cl = int(self.parent.canevasaction.cget("width"))
            self.parent.canevasaction.config(scrollregion=(0, 0, cl, fh + 60))

    # def afficher_commande_batiment(self):
    #     self.widgetsactifs = self.parent.canevasaction.create_window(100, 60,
    #                                                                  window=self.parent.cadrebatiment,
    #                                                                  anchor=N)
    #     self.parent.root.update()
    #     fh = self.parent.cadrebatiment.winfo_height()
    #     ch = int(self.parent.canevasaction.cget("height"))
    #     if fh + 60 > ch:
    #         cl = int(self.parent.canevasaction.cget("width"))
    #         self.parent.canevasaction.config(scrollregion=(0, 0, cl, fh + 60))

    def afficher_commande_barracks(self):
        self.widgetsactifs = self.parent.canevasaction.create_window(100, 60,
                                                                     window=self.parent.cadrebarracks,
                                                                     anchor=N)
        self.parent.root.update()
        fh = self.parent.cadrebarracks.winfo_height()
        ch = int(self.parent.canevasaction.cget("height"))
        if fh + 60 > ch:
            cl = int(self.parent.canevasaction.cget("width"))
            self.parent.canevasaction.config(scrollregion=(0, 0, cl, fh + 60))

    def afficher_commande_maison(self):
        self.widgetsactifs = self.parent.canevasaction.create_window(100, 60,
                                                                     window=self.parent.cadremaison,
                                                                     anchor=N)
        self.parent.root.update()
        fh = self.parent.cadremaison.winfo_height()
        ch = int(self.parent.canevasaction.cget("height"))
        if fh + 60 > ch:
            cl = int(self.parent.canevasaction.cget("width"))
            self.parent.canevasaction.config(scrollregion=(0, 0, cl, fh + 60))

    def envoyer_chat(self, evt):
        txt = self.parent.entreechat.get()
        joueur = self.parent.joueurs.get()
        if joueur:
            action = [self.parent.monnom, "chatter", [self.parent.monnom + ": " + txt, self.parent.monnom, joueur]]
            self.parent.parent.actionsrequises.append(action)

    def chatter(self):
        if self.chaton == 0:
            x1, x2 = self.parent.scrollH.get()
            x3 = self.parent.modele.aireX * x1
            y1, y2 = self.parent.scrollV.get()
            y3 = self.parent.modele.aireY * y1
            self.parent.cadrechaton = self.parent.canevas.create_window(x3, y3,
                                                                        window=self.parent.cadrechat,
                                                                        anchor=N + W)
            self.parent.btnchat.config(bg="SystemButtonFace")
            self.chaton = 1
        else:
            self.parent.canevas.delete(self.parent.cadrechaton)
            self.parent.cadrechaton = 0
            self.chaton = 0

    def aider(self):
        if self.aideon == 0:
            x1, x2 = self.parent.scrollH.get()
            x3 = self.parent.modele.aireX * x2
            y1, y2 = self.parent.scrollV.get()
            y3 = self.parent.modele.aireY * y1
            self.aideon = self.parent.canevas.create_window(x3, y3,
                                                            window=self.parent.cadreaide,
                                                            anchor=N + E)
        else:
            self.parent.canevas.delete(self.aideon)
            self.aideon = 0

    def skill(self):
        if self.skillon == 0:
            self.windowskill = Tk()
            self.windowskill.title("Skill Tree ")
            self.windowskill.iconbitmap('images/misc/dna.ico')

            self.label = Label(self.windowskill, text="Skill Tree lmao")
            self.button1 = Button(self.windowskill, text="lol")
            # self.btnL = Button(self.label, highlightthickness=0, bd=0, image=self.parent.images["daimMORT"])
            self.label.pack(pady=250, padx=400)
            self.button1.pack()
            # self.btnL.pack()

        else:
            self.parent.canevas.delete(self.skillon)

    def victoire(self):
        self.windowwin = Tk()
        self.cadrevictoire = Frame(self.windowwin, width=500, height=400)
        self.canevasvictoire = Canvas(self.cadrevictoire, width=600, height=480, bg="DarkOliveGreen1")
        self.canevasvictoire.pack()

        self.condition = ""
        self.windowwin.title("GAME OVER")

        if self.victoireon == 0:
            self.condition = Label(self.windowwin, text="T'est un WINNER mon chum")
            # self.canevasvictoire.create_image(320, 10, image=self.images['win'])
        else:
            self.condition = Label(self.windowwin, text="LMAOO! T'as pas gagné HAHAHAHAHAH, pleure")
            # self.canevasvictoire.create_image(320, 10, image=self.images['lose'])

        self.condition.config(font=('Comic Sans MS', 20), wraplength=250)
        self.condition.pack()


    ### FIN des methodes pour lancer la partie


class Champ(Label):
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.config(font=("arial", 13, "bold"))
        self.config(bg="goldenrod3")
