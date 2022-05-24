from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *

from chargeurdimages import *


class Champ(Label):
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.config(font=("arial", 13, "bold"))
        self.config(bg="goldenrod3")

class Jeu:
    ### cadre de jeu : inclus aire de jeu, le HUD, le cadre_jeu_action
    def __init__(self, view):
        self.view = view
        self.controleur = view.controleur
        self.modele = self.controleur.modele

        self.tailleminicarte = 220

        # # images des assets, definies dans le modue loadeurimages
        self.images = chargerimages()

        # # objet pour cumuler les manipulations du joueur pour generer une action de jeu
        self.action = Action(self)

        # le cadre principal du jeu, remplace le Lobby
        self.cadrepartie = Frame(self.view.cadreapp, bg="green", width=400, height=400)

        # cadre du jeu et ses scrollbars
        self.creer_aire_de_jeu()

        # cadre pour info sur les ressources du joueur en haut de l'aire de jeu
        self.creer_HUD()

        # cadre pour commandes et infos des objets de jeu, situe a droite
        self.creer_cadre_jeu_action()

        # configuration de la section qui s'etire lorsque la fenetre change de taille
        self.cadrepartie.rowconfigure(0, weight=1)
        self.cadrepartie.columnconfigure(0, weight=1)

    def pack(self, expand, fill):
        self.cadrepartie.pack(expand=1, fill=BOTH)

    def pack_forget(self):
        self.pack_forget()

    def creer_aire_de_jeu(self):
        # definition du cadre avec le canvas de jeu et les scrollbars
        self.cadrecanevas = Frame(self.cadrepartie)

        # on crée les scrollbar AVANT le canevas de jeu car le canevas est dépendant de leur
        self.scrollV = Scrollbar(self.cadrecanevas, orient=VERTICAL)
        self.scrollH = Scrollbar(self.cadrecanevas, orient=HORIZONTAL)

        self.canevas = Canvas(self.cadrecanevas, width=400, height=400, bg="DarkOliveGreen2",
                              yscrollcommand=self.scrollV.set, xscrollcommand=self.scrollH.set)

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
        self.infohud = {"Or": None}

        ## on l'appelle pour chaque chose de self.infohud

        i = "Or"
        titre = Champ(self.cadrejeuinfo, text=i, bg="blue", fg="white")
        varstr = StringVar()
        varstr.set(0)
        donnee = Champ(self.cadrejeuinfo, bg="red", fg="white", textvariable=varstr)
        donnee.pack(side=LEFT)
        titre.pack(side=LEFT)
        self.infohud[i] = [varstr, donnee]

        varstr = StringVar()
        varstr.set("")
        ### champ supplémentaire pour afficher des messages...
        champmsg = Label(self.cadrejeuinfo, text="", fg="red")
        champmsg.pack(side=LEFT)
        self.infohud["msggeneral"] = [champmsg]

        self.btnchat = Button(self.cadrejeuinfo, text="Chat", command=self.action.chatter)
        self.btnaide = Button(self.cadrejeuinfo, text="Aide", command=self.action.aider)
        self.btnaide.pack(side=RIGHT)
        self.btnchat.pack(side=RIGHT)

        self.cadrejeuinfo.grid(row=0, column=0, sticky=E + W, columnspan=2)

    def creer_cadre_jeu_action(self):
        # Ajout du cadre d'action a droite pour identifier les objets permettant les commandes du joueur
        self.cadreaction = Frame(self.cadrepartie)
        self.cadreaction.grid(row=0, column=1, sticky=N + S)
        self.scrollVaction = Scrollbar(self.cadreaction, orient=VERTICAL)
        self.canevasaction = Canvas(self.cadreaction, width=200, height=300, #bg="red",
                                    yscrollcommand=self.scrollVaction.set)

        self.scrollVaction.config(command=self.canevasaction.yview)
        self.canevasaction.grid(row=0, column=0, sticky=N + S)
        self.scrollVaction.grid(row=0, column=1, sticky=N + S)
        # les widgets
        #self.canevasaction.create_text(100, 30, text=self.controleur.monnom, font=("arial", 18, "bold"), anchor=S,
        #                               tags=("nom"))

        # minicarte
        self.minicarte = Canvas(self.cadreaction, width=self.tailleminicarte, height=self.tailleminicarte, bg="tan1",
                                highlightthickness=0)
        self.minicarte.grid(row=2, column=0, columnspan=2)
        self.minicarte.bind("<Button-1>", self.deplacer_carte)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        self.canevasaction.rowconfigure(0, weight=1)
        self.cadreaction.rowconfigure(0, weight=1)

    def connecter_event(self):
        # actions de clics sur la carte
        self.canevas.tag_bind("case", "<Button-1>", self.annuler_action)
        self.canevas.tag_bind("zone_controle", "<Button-1>", self.annuler_action)
        #self.canevas.tag_bind("case", "<Button-2>", self.deplacement_perso_choisi)
        self.canevas.tag_bind("zone_controle", "<Button-2>", self.deplacement_perso_choisi)
        self.canevas.bind("<Button-3>", self.deplacement_perso_choisi)
        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)
        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)

        # actions liées aux objets dessinés par tag
        self.canevas.tag_bind("batiment", "<Button-1>", self.creer_entite)
        self.canevas.tag_bind("perso", "<Button-1>", self.ajouter_selection)

        self.canevas.bind("<Control-Button-1>", self.montrer_stats)

    def initialiser_avec_modele(self, modele):
        self.modele = modele

        # on reassigne le nom final localement pour eviter
        # de toujours le requerir du parent
        self.monnom = self.controleur.monnom

        # on ajuste la taille du canevas de jeu
        self.canevas.config(scrollregion=(0, 0, self.modele.aireX, self.modele.aireY))
        #self.canevasaction.delete("nom")
        #self.canevasaction.create_text(100, 30, text=self.monnom, font=("arial", 18, "bold"), anchor=S, tags=("nom"))

        couleur_cases = {
            "arbre": "green",
            "roche": "grey",
            "plaine": "white",
            "eau": "blue",
            "batiment": "red"
        }

        # creation de la grid de jeu
        for line in range(0, self.modele.aireX, 72):  # range(start, stop, step)
            self.canevas.create_line([(line, 0), (line, self.modele.aireY)], fill='black', tags='grid_line_w')
        for line in range(0, self.modele.aireY, 72):
            self.canevas.create_line([(0, line), (self.modele.aireX, line)], fill='black', tags='grid_line_h')

        # creer des cases selon leur type
        for caseX in range(0, len(self.modele.cartecase), 1):
            for caseY in range(0, len(self.modele.cartecase), 1):
                self.canevas.create_rectangle(caseX * 72, caseY * 72, caseX * 72 + 72, caseY * 72 + 72,
                                              fill=couleur_cases[self.modele.cartecase[caseY][caseX].montype], tags='case')
                self.canevas.create_text(caseX * 72 + (72/2), caseY * 72 + (72/2), text="{},{}".format(caseX, caseY))

        # on cree les cadres affichant les items d'actions du joueur
        # cadre apparaissant si on selectionne un ouvrier
        coul = self.modele.joueurs[self.controleur.monnom].couleur
        #print(coul, "alloooo!!!!!!")
        self.cadrejeuinfo.config(bg=coul[1])
        self.creer_aide()
        print(coul[0])
        self.creer_cadre_ouvrier(coul[0] + "_", ["Village", "Caserne", "Ferme", "Scierie", "tour", "pecherie", "mine"])
        self.creer_chatter()
        # on affiche les maisons, point de depart des divers joueurs
        self.afficher_depart()
        self.view.update()
        # self.centrer_maison()

    def centrer_village(self):
        self.view.update()
        cle = list(self.modele.joueurs[self.monnom].batiments["Village"].keys())[0]
        x = self.modele.joueurs[self.monnom].batiments["Village"][cle].x
        y = self.modele.joueurs[self.monnom].batiments["Village"][cle].y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.aireX
        pcty = (y - y1) / self.modele.aireY

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    # fab: créer les cadre

    ### cadre qui s'Affichera par-dessus le canevas de jeu pour l'aide
    def creer_aide(self):
        self.cadreaide = Frame(self.canevas)
        self.scrollVaide = Scrollbar(self.cadreaide, orient=VERTICAL)
        self.textaide = Text(self.cadreaide, width=50, height=10, yscrollcommand=self.scrollVaide.set)
        self.scrollVaide.config(command=self.textaide.yview)
        self.textaide.pack(side=LEFT)
        self.scrollVaide.pack(side=LEFT, expand=1, fill=Y)
        fichieraide = open("aide.txt")
        monaide = fichieraide.read()
        fichieraide.close()
        self.textaide.insert(END, monaide)
        self.textaide.config(state=DISABLED)

    def creer_cadre_ouvrier(self, coul, artefacts):
        self.cadreouvrier = Frame(self.canevasaction)
        for i in artefacts:
            print("i", i)

            if i in ["Village", "Caserne", "Ferme", "Scierie", "tour", "pecherie", "mine"]:
                btn = Button(self.cadreouvrier, text=i, justify=LEFT, width=16, height=1)
            else:
                btn = Button(self.cadreouvrier, text=i, image=self.images[coul + i])
            btn.bind("<Button>", self.batir_artefact)
            #print("ici!!")
            btn.pack()
        self.cadreouvrier.pack()

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

    ##FONCTIONS D'AFFICHAGES##################################
    def afficher_depart(self):
        self.modele.listebiotopes.sort(key=lambda c: c.y)
        for i in self.modele.listebiotopes:
            monitem = self.canevas.create_image(i.x, i.y, image=self.images[i.img], anchor=S,
                                                tags=("statique", "", i.id, "biotope", i.montype, ""))
            # tags=("mobile","",i.id,)

        self.modele.listebiotopes = []
        minitaillecase = int(self.tailleminicarte / self.modele.taillecarte)
        couleurs = {0: "",
                    "arbre": "light green",
                    "eau": "light blue",
                    "roche": "gray30"}
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
                                                        fill=couleurs[k.controleur.montype])

        # Affichage des batiments intiaux sur l'aire de jeu et sur la minicarte
        px = int(self.tailleminicarte / self.modele.aireX)
        py = int(self.tailleminicarte / self.modele.aireY)

        for j in self.modele.joueurs.keys():
            for i in self.modele.joueurs[j].batiments["Village"].keys():
                village_initiale = self.modele.joueurs[j].batiments["Village"][i]
                coul = self.modele.joueurs[j].couleur[1]
                case = village_initiale.case
                batiment_label = village_initiale.montype[0]
                print(case)
                self.canevas.create_rectangle(case.x * 72, case.y * 72, case.x * 72 + 72, case.y * 72 + 72,
                                              fill="red",
                                              tags=(
                                                  "statique", j, village_initiale.id, "batiment",
                                                  village_initiale.montype,
                                                  ""))
                # self.canevas.create_image(m.x,m.y,image=self.images[coul+"_maison"],
                # tags=("statique",j,m.id,"batiment",m.montype,""))
                # tags=("mobile","",i.id,)

                # code pour print cordordenée sur batiment
                self.canevas.create_text(case.x * 72 + (72 / 2), case.y * 72 + (72 / 2), text=batiment_label,
                                         font=("arial", 18, "bold"), anchor=CENTER,
                                         tags=(
                                             "statique", j, village_initiale.id, "batiment", village_initiale.montype,
                                             ""))

                # Affichage de la zone de controle
                for zdc in village_initiale.zone_controle:
                    if zdc.x == case.x and zdc.y == case.y:
                        pass
                    else:
                        self.canevas.create_rectangle(zdc.x * 72, zdc.y * 72, zdc.x * 72 + 72, zdc.y * 72 + 72,
                                                      fill=coul, stipple="gray12", tags=('zone_controle', village_initiale.id))

                # afficher sur minicarte
                coul = self.modele.joueurs[j].couleur[1]
                x1 = int((village_initiale.x / self.modele.aireX) * self.tailleminicarte)
                y1 = int((village_initiale.y / self.modele.aireY) * self.tailleminicarte)
                self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=coul,
                                                tags=(j, village_initiale.id, "artefact", "maison"))

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

        self.action.prochaineaction = obj.cget("text")
        obj.config(bg="lightgreen")

    def afficher_jeu(self):

        # On efface tout ce qui est 'mobile' (un tag)
        self.canevas.delete("mobile")

        #if self.modele.joueurs

        moi = self.modele.joueurs[self.monnom]
        if self.action.batiment_selectioner is not None:
            pass

        if len(self.action.persochoisi) != 0:
            self.cadreouvrier.pack()
        else:
            self.cadreouvrier.pack_forget()

        # on se debarrasse des choses mortes (disparues), le id est dans le tag du dessin
        for i in self.modele.ressourcemorte:
            self.canevas.delete(i.id)

        for batiment in self.modele.batimentmort:
            self.canevas.delete(batiment.id)

        # commencer par les choses des joueurs
        for nom_joueur in self.modele.joueurs.keys():
            # ajuster les infos du HUD
            if nom_joueur == self.controleur.monnom:
                # self.infohud["Nourriture"][0].set(self.modele.joueurs[j].ressources["nourriture"])
                # self.infohud["Bois"][0].set(self.modele.joueurs[j].ressources["arbre"])
                # self.infohud["Roche"][0].set(self.modele.joueurs[j].ressources["roche"])
                self.infohud["Or"][0].set(self.modele.joueurs[nom_joueur].Or)
                self.infohud["msggeneral"][0].config(text=self.modele.msggeneral)

            # ajuster les constructions de chaque joueur
            for type_perso in self.modele.joueurs[nom_joueur].batiments['siteconstruction']:
                s = self.modele.joueurs[nom_joueur].batiments['siteconstruction'][type_perso]
                self.canevas.create_image(s.x, s.y, anchor=CENTER, image=self.images["siteX"],
                                          tags=("mobile", nom_joueur, type_perso, "batiment", type(s).__name__, ""))
                # tags=(j,s.id,"artefact","mobile","siteconstruction","batiments"))

            self.afficher_perso(nom_joueur)

            self.afficher_fleche(nom_joueur)

        # ajuster les choses vivantes dependantes de la partie (mais pas des joueurs)
        for nom_joueur in self.modele.biotopes["eau"].keys():
            i = self.modele.biotopes["eau"][nom_joueur]
            if i.sprite:
                self.canevas.create_image(i.x, i.y, image=self.gifs[i.sprite][i.spriteno],
                                          tags=("mobile", "", i.id, "biotope", type(i).__name__, ""))
                # tags=("",i.id,"artefact","eau","mobile"))

        # mettre les chat a jour si de nouveaux messages sont arrives
        if self.textchat and self.modele.joueurs[self.controleur.monnom].chatneuf:
            self.textchat.delete(0, END)
            self.textchat.insert(END, *self.modele.joueurs[self.controleur.monnom].monchat)
            if self.modele.joueurs[self.controleur.monnom].chatneuf and self.action.chaton == 0:
                self.btnchat.config(bg="orange")
            self.modele.joueurs[self.controleur.monnom].chatneuf = 0

    def afficher_perso(self, nom_joueur):
        # ajuster les persos de chaque joueur et leur dépendance
        for type_perso in self.modele.joueurs[nom_joueur].persos.keys():
            for id_perso in self.modele.joueurs[nom_joueur].persos[type_perso].keys():
                perso = self.modele.joueurs[nom_joueur].persos[type_perso][id_perso]
                coul = self.modele.joueurs[nom_joueur].couleur[0]
                self.canevas.create_image(perso.x, perso.y, anchor=S, image=self.images[perso.image],
                                          tags=("mobile", nom_joueur, id_perso, "perso", type_perso, ""))
                # tags=(j,k,"artefact","mobile","perso",p))
                if id_perso in self.action.persochoisi:
                    self.canevas.create_rectangle(perso.x - 10, perso.y + 5, perso.x + 10, perso.y + 10, fill="yellow",
                                                  tags=("mobile", nom_joueur, type_perso, "perso", type(perso).__name__,
                                                        "persochoisi"))
                    # tags=(j,k,"artefact","mobile","persochoisi"))

    def afficher_fleche(self, nom_joueur):
        for id_tour in self.modele.joueurs[nom_joueur].batiments["Tour"].keys():
            for fleche in self.modele.joueurs[nom_joueur].batiments["tour"][id_tour].fleches:
                self.canevas.create_image(fleche.x, fleche.y, image=self.images[fleche.image],
                                        tags=("mobile", nom_joueur, fleche.id, "", type(fleche).__name__, ""))

    def afficher_batiment(self, joueur, batiment):
        coul = self.modele.joueurs[joueur].couleur[1]

        case = batiment.case
        batiment_label = batiment.montype[0]
        # t = VarString()
        self.canevas.delete(batiment.id)
        self.canevas.create_rectangle(case.x * 72, case.y * 72, case.x * 72 + 72, case.y * 72 + 72, fill="red",
                                      tags=(
                                          "statique", self.controleur.monnom, batiment.id, "batiment", batiment.montype,
                                          ""))

        self.canevas.create_text(case.x * 72 + (72 / 2), case.y * 72 + (72 / 2), font=("arial", 18, "bold"),
                                 text=batiment_label, tags=(batiment.id))
        # self.canevas.create_text(case.x*72 - 36, case.y*72 - 36, text=batiment_type, font=("arial",18,"bold"),anchor=CENTER,
        #                         tags=("statique",self.parent.monnom,batiment.id,"batiment",batiment.montype,""))


        # Affichage de la zone de controle
        for zdc in batiment.zone_controle:
            if zdc.montype == "batiment":
                pass
            else:
                self.canevas.create_rectangle(zdc.x * 72, zdc.y * 72, zdc.x * 72 + 72, zdc.y * 72 + 72,
                                              fill=coul, stipple="gray12", tags=('zone_controle', batiment.id))

        print(self.controleur.monnom)
        # chose=self.canevas.create_image(batiment.x,batiment.y,image=self.images["caseRed"],
        #                          tags=("statique",self.parent.monnom,batiment.id,"batiment",batiment.montype,""))

        # x0, y0, x2, y2 = self.canevas.bbox(chose)

        couleurs = {0: "",
                    1: "light green",
                    2: "light blue",
                    3: "tan",
                    4: "gray30",
                    5: "orange"}
        coul = self.modele.joueurs[joueur].couleur[1]
        x1 = int((batiment.x / self.modele.aireX) * self.tailleminicarte)
        y1 = int((batiment.y / self.modele.aireY) * self.tailleminicarte)
        self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=coul,
                                        tags=(self.controleur.monnom, batiment.id, "artefact", batiment.montype))
        # return [x0, y0, x2, y2]

    def afficher_bio(self, bio):
        self.canevas.create_image(bio.x, bio.y, image=self.images[bio.img],
                                  tags=("statique", "", bio.id, "biotope", bio.montype, ""))

    ##### ACTIONS DU JOUEUR #######################################################################

    def annuler_action(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        #if not mestags:
        #self.canevasaction.delete(self.action.widgetsactifs)
        if self.action.btnactif:
            self.action.btnactif.config(bg="SystemButtonFace")
        self.action = Action(self)

    def fermer_chat(self):
        self.textchat = None
        self.fenchat.destroy()

    def ajouter_selection(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        if self.controleur.monnom == mestags[1]:
            if "Ouvrier" == mestags[4]:
                self.action.persochoisi.append(mestags[2])
            ######
            else:
                self.action.persochoisi.append(mestags[2])
            # BUG quand on attaque
        elif self.action.persochoisi != []:
            self.action.ciblechoisi=mestags
            self.action.attaquer()

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
                if self.controleur.monnom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.action.persochoisi.append(self.canevas.gettags(i)[2])

            self.canevas.delete("selecteur")

    ### FIN du multiselect

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

    def deplacement_perso_choisi(self, evt):
        tag = self.canevas.gettags(CURRENT)
        #if not tag and
        if self.action.persochoisi and self.action.btnactif is not None:
            pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.construire_batiment(pos)
        elif self.action.persochoisi:
            x, y = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.position = [x, y]
            self.action.deplacer()

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

    def creer_entite(self, evt):
        x, y = evt.x, evt.y
        mestags = self.canevas.gettags(CURRENT)
        if self.controleur.monnom in mestags:
            action = None
            if "batiment" in mestags:
                if "Village" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.controleur.monnom, "creerperso", ["ouvrier", mestags[4], mestags[2], pos]]
                if "Caserne" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.controleur.monnom, "creerperso", ["soldat", mestags[4], mestags[2], pos]]

                if (action is not None):
                    self.controleur.actionsrequises.append(action)
        ###### les ATTAQUES SUR BATIMENT INACTIFS
        # elif self.action.persochoisi:
        #     self.action.ciblechoisi=mestags
        #     self.action.attaquer()

    # afficher la nombre de batiment et de perso total dans la partie
    # est ativer par controler click
    def montrer_stats(self, evt):
        self.controleur.modele.calc_stats()


# Singleton (mais pas automatique) sert a conserver les manipulations du joueur pour demander une action
# CET OBJET SERVIRA À CONSERVER LES GESTES ET INFOS REQUISES POUR PRODUIRE UNE ACTION DE JEU
class Action:
    def __init__(self, parent):
        self.parent = parent
        self.persochoisi = []
        self.batiment_selectioner = None
        self.ciblechoisi = None
        self.position = []
        self.btnactif = None  # le bouton choisi pour creer un batiment
        self.prochaineaction = None  # utiliser pour les batiments seulement
        self.widgetsactifs = []
        self.chaton = 0
        self.aideon = 0

    def attaquer(self):
        if self.persochoisi:
            qui = self.ciblechoisi[1]
            cible = self.ciblechoisi[2]
            sorte = self.ciblechoisi[4]
            action = [self.parent.controleur.monnom, "attaquer", [self.persochoisi, [qui, cible, sorte]]]
            self.parent.controleur.actionsrequises.append(action)

    def deplacer(self):
        if self.persochoisi:
            action = [self.parent.controleur.monnom, "deplacer", [self.position, self.persochoisi]]
            self.parent.controleur.actionsrequises.append(action)

    def ramasser_ressource(self, tag):
        if self.persochoisi:
            action = [self.parent.controleur.monnom, "ramasserressource", [tag[4], tag[2], self.persochoisi]]
            self.parent.controleur.actionsrequises.append(action)

    def construire_batiment(self, pos):
        self.btnactif.config(bg="SystemButtonFace")
        self.btnactif = None
        action = [self.parent.monnom, "construirebatiment", [self.persochoisi, self.prochaineaction, pos]]
        self.parent.controleur.actionsrequises.append(action)

    def envoyer_chat(self, evt):
        txt = self.parent.entreechat.get()
        joueur = self.parent.joueurs.get()
        if joueur:
            action = [self.parent.monnom, "chatter", [self.parent.monnom + ": " + txt, self.parent.monnom, joueur]]
            self.parent.controleur.actionsrequises.append(action)

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

    ### FIN des methodes pour lancer la partie