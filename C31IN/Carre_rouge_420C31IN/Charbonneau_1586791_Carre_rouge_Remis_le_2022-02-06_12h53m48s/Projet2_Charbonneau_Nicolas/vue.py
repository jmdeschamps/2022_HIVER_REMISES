from tkinter import *


class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.choix_sentinelles = StringVar()
        self.choix_pion = StringVar()
        self.choix_jeu = StringVar()
        self.choix_difficulte = StringVar()
        self.afficher_menu_principal()

    def afficher_menu_principal(self):
        self.creer_cadre_menu_principal()

    def creer_cadre_menu_principal(self):
        self.cadre_menu_principal = Frame(self.root, width=550, height=550, bg="#c6c6c6")
        self.cadre_menu_principal.pack(expand=1, fill=BOTH)
        titre = Label(self.cadre_menu_principal, text="MENU PRINCIPAL", font=("Copperplate Gothic Light", 18),
                      bg="#c6c6c6")
        titre.place(relx=0.5, rely=0.1, anchor=CENTER)
        options_label = Label(self.cadre_menu_principal, text="options", font=("Copperplate Gothic Light", 16),
                              bg="#c6c6c6")
        options_label.place(relx=0.5, rely=0.2, anchor=CENTER)
        dimensions_label = Label(self.cadre_menu_principal, text="dimensions :", font=("Copperplate Gothic Light", 16),
                                 bg="#c6c6c6")
        dimensions_label.place(relx=0.08, rely=0.25)
        sentinelles_label = Label(self.cadre_menu_principal, text="sentinelles :",
                                  font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        sentinelles_label.place(relx=0.12, rely=0.30)
        self.choix_sentinelles.set("2")
        btn_sentinelles_1 = Radiobutton(self.cadre_menu_principal, text="x0.5", variable=self.choix_sentinelles,
                                        value=1, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_sentinelles_1.place(relx=0.14, rely=0.35)
        btn_sentinelles_2 = Radiobutton(self.cadre_menu_principal, text="x1.0", variable=self.choix_sentinelles,
                                        value=2, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_sentinelles_2.place(relx=0.28, rely=0.35)
        btn_sentinelles_3 = Radiobutton(self.cadre_menu_principal, text="x2.0", variable=self.choix_sentinelles,
                                        value=3, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_sentinelles_3.place(relx=0.42, rely=0.35)
        pion_label = Label(self.cadre_menu_principal, text="pion :", font=("Copperplate Gothic Light", 12),
                           bg="#c6c6c6")
        pion_label.place(relx=0.12, rely=0.40)
        self.choix_pion.set("2")
        btn_pion_1 = Radiobutton(self.cadre_menu_principal, text="x0.5", variable=self.choix_pion, value=1,
                                 font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_pion_1.place(relx=0.14, rely=0.45)
        btn_pion_2 = Radiobutton(self.cadre_menu_principal, text="x1.0", variable=self.choix_pion, value=2,
                                 font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_pion_2.place(relx=0.28, rely=0.45)
        btn_pion_3 = Radiobutton(self.cadre_menu_principal, text="x2.0", variable=self.choix_pion, value=3,
                                 font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_pion_3.place(relx=0.42, rely=0.45)
        jeu_label = Label(self.cadre_menu_principal, text="jeu :", font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        jeu_label.place(relx=0.12, rely=0.50)
        self.choix_jeu.set("1")
        btn_jeu_1 = Radiobutton(self.cadre_menu_principal, text="x1.0", variable=self.choix_jeu, value=1,
                                font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_jeu_1.place(relx=0.14, rely=0.55)
        btn_jeu_2 = Radiobutton(self.cadre_menu_principal, text="x1.5", variable=self.choix_jeu, value=2,
                                font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_jeu_2.place(relx=0.28, rely=0.55)
        btn_jeu_3 = Radiobutton(self.cadre_menu_principal, text="x2.0", variable=self.choix_jeu, value=3,
                                font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_jeu_3.place(relx=0.42, rely=0.55)
        difficulte_label = Label(self.cadre_menu_principal, text="difficulté :", font=("Copperplate Gothic Light", 16),
                                 bg="#c6c6c6")
        difficulte_label.place(relx=0.58, rely=0.25)
        self.choix_difficulte.set("4")
        btn_difficulte_1 = Radiobutton(self.cadre_menu_principal, text="facile", variable=self.choix_difficulte,
                                       value=1, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_difficulte_1.place(relx=0.62, rely=0.3)
        btn_difficulte_2 = Radiobutton(self.cadre_menu_principal, text="moyen", variable=self.choix_difficulte, value=2,
                                       font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_difficulte_2.place(relx=0.62, rely=0.35)
        btn_difficulte_3 = Radiobutton(self.cadre_menu_principal, text="difficile", variable=self.choix_difficulte,
                                       value=3, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_difficulte_3.place(relx=0.62, rely=0.40)
        btn_difficulte_4 = Radiobutton(self.cadre_menu_principal, text="progressif", variable=self.choix_difficulte,
                                       value=4, font=("Copperplate Gothic Light", 12), bg="#c6c6c6")
        btn_difficulte_4.place(relx=0.62, rely=0.45)
        btn_voir_session = Button(self.cadre_menu_principal, text="SESSION", command=self.afficher_menu_session,
                                  font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_voir_session.place(width=200, height=60, relx=0.5, rely=0.75, anchor=CENTER)
        btn_demarrer_jeu = Button(self.cadre_menu_principal, text="JOUER", command=self.afficher_menu_jeu,
                                  font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_demarrer_jeu.place(width=200, height=60, relx=0.3, rely=0.9, anchor=CENTER)
        btn_scores = Button(self.cadre_menu_principal, text="SCORES", command=self.afficher_menu_scores,
                            font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_scores.place(width=200, height=60, relx=0.7, rely=0.9, anchor=CENTER)

    def sauvegarder_options(self):
        self.parent.sauvegarder_options(self.choix_sentinelles.get(), self.choix_pion.get(), self.choix_jeu.get(),
                                        self.choix_difficulte.get())

    def afficher_menu_session(self):
        self.enlever_menu_principal()
        self.creer_cadre_session()

    def creer_cadre_session(self):
        self.cadre_menu_session = Frame(self.root, width=550, height=550, bg="#c6c6c6")
        self.cadre_menu_session.pack(expand=1, fill=BOTH)
        self.cadre_menu_session.pack_propagate(False)
        titre = Label(self.cadre_menu_session, text="INFORMATIONS SESSION", font=("Copperplate Gothic Light", 18),
                      bg="#c6c6c6")
        titre.place(relx=0.5, rely=0.1, anchor=CENTER)
        bar_deroulante = Scrollbar(self.cadre_menu_session)
        bar_deroulante.pack(side=RIGHT, fill=Y)
        liste_scores = Listbox(self.cadre_menu_session, yscrollcommand=bar_deroulante.set, font=("Copperplate Gothic Light", 16))
        for score in self.modele.liste_scores:
            liste_scores.insert(END, "Temps:        " + str(score[0] + "        -        Points:        " + str(score[1])))
        liste_scores.place(width=500, height=250, relx=0.5, rely=0.4, anchor=CENTER)
        bar_deroulante.config(command=liste_scores.yview)
        nom_label = Label(self.cadre_menu_session, text="Votre nom:", font=("Copperplate Gothic Light", 14),
                      bg="#c6c6c6")
        nom_label.place(relx=0.2, rely=0.68, anchor=CENTER)
        self.champ_nom = Entry(self.cadre_menu_session, width=40)
        self.champ_nom.place(relx=0.55, rely=0.68, anchor=CENTER)
        btn_sauvegarder_session = Button(self.cadre_menu_session, text="SAUVEGARDER",
                                         command=self.sauvegarder_session, font=("Copperplate Gothic Light", 12),
                                         bg="#228B22")
        btn_sauvegarder_session.place(width=160, height=30, relx=0.35, rely=0.75, anchor=CENTER)
        btn_supprimer_session = Button(self.cadre_menu_session, text="SUPPRIMER",
                                         command=self.supprimer_session, font=("Copperplate Gothic Light", 12),
                                         bg="#228B22")
        btn_supprimer_session.place(width=160, height=30, relx=0.65, rely=0.75, anchor=CENTER)
        btn_sortir_session = Button(self.cadre_menu_session, text="RETOUR", command=self.parent.sortir_menu_session,
                                 font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_sortir_session.place(width=120, height=30, relx=0.70, rely=0.9)

    def sauvegarder_session(self):
        nom = self.champ_nom.get()
        self.parent.sauvegarder_session(nom)
        self.enlever_menu_session()
        self.afficher_menu_session()

    def supprimer_session(self):
        self.parent.supprimer_session()
        self.enlever_menu_session()
        self.afficher_menu_session()

    def afficher_menu_scores(self, donnees=""):
        self.enlever_menu_principal()
        self.creer_cadre_scores(donnees)

    def creer_cadre_scores(self, donnees):
        self.cadre_menu_scores = Frame(self.root, width=550, height=550, bg="#c6c6c6")
        self.cadre_menu_scores.pack(expand=1, fill=BOTH)
        self.cadre_menu_scores.pack_propagate(False)
        titre = Label(self.cadre_menu_scores, text="SCORES", font=("Copperplate Gothic Light", 18),
                      bg="#c6c6c6")
        titre.place(relx=0.5, rely=0.1, anchor=CENTER)
        bar_deroulante = Scrollbar(self.cadre_menu_scores)
        bar_deroulante.pack(side=RIGHT, fill=Y)
        liste_scores = Listbox(self.cadre_menu_scores, yscrollcommand=bar_deroulante.set, font=("Copperplate Gothic Light", 12))
        if donnees == "" :
            donnees = self.parent.lire_scores()
        for donnee in donnees:
            donnee = donnee.split(",")
            liste_scores.insert(END, "Nom: " + str(donnee[0]) + " - Temps: " + str(donnee[1] + " - Points: " + str(donnee[2])))
        liste_scores.place(width=500, height=250, relx=0.5, rely=0.4, anchor=CENTER)
        bar_deroulante.config(command=liste_scores.yview)
        btn_trier_scores = Button(self.cadre_menu_scores, text="TRIER",
                                         command=self.trier_scores, font=("Copperplate Gothic Light", 12),
                                         bg="#228B22")
        btn_trier_scores.place(width=160, height=30, relx=0.35, rely=0.75, anchor=CENTER)
        btn_supprimer_scores = Button(self.cadre_menu_scores, text="EFFACER",
                                         command=self.effacer_scores, font=("Copperplate Gothic Light", 12),
                                         bg="#228B22")
        btn_supprimer_scores.place(width=160, height=30, relx=0.65, rely=0.75, anchor=CENTER)
        btn_sortir_scores = Button(self.cadre_menu_scores, text="RETOUR", command=self.parent.sortir_menu_scores,
                                 font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_sortir_scores.place(width=120, height=30, relx=0.70, rely=0.9)

    def trier_scores(self):
        donnees = self.parent.trier_scores()
        self.enlever_menu_scores()
        self.afficher_menu_scores(donnees)

    def effacer_scores(self):
        self.parent.effacer_scores()
        self.enlever_menu_scores()
        self.afficher_menu_scores()

    def afficher_menu_jeu(self):
        self.sauvegarder_options()
        self.cadre_menu_principal.pack_forget()
        self.creer_cadres_jeu()
        self.afficher_objets()

    def creer_cadres_jeu(self):
        self.creer_cadre_fenetre()
        self.creer_cadre_zone_jeu()

    def creer_cadre_fenetre(self):
        self.cadre_fenetre = Frame(self.root, width=self.modele.largeur_fenetre, height=self.modele.hauteur_fenetre,
                                   bg="black")
        self.cadre_fenetre.pack()

    def creer_cadre_zone_jeu(self):
        self.cadre_zone_jeu = Frame(self.cadre_fenetre, width=self.modele.largeur_zone, height=self.modele.hauteur_zone,
                                    bg="white")
        self.canevas = Canvas(self.cadre_zone_jeu, width=self.modele.largeur_zone, height=self.modele.hauteur_zone,
                              bg="white")
        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.pack()
        self.cadre_zone_jeu.place(relx=.5, rely=.5, anchor=CENTER)

    def afficher_objets(self):
        self.canevas.delete(ALL)
        self.afficher_pion()
        self.afficher_sentinelles()

    def afficher_pion(self):
        pion = self.modele.partie_courante.pion
        delta = pion.largeur / 2
        self.canevas.create_rectangle(pion.position_x - delta, pion.position_y - delta, pion.position_x + delta,
                                      pion.position_y + delta, fill="red", tags="pion")

    def afficher_sentinelles(self):
        for i in self.modele.partie_courante.sentinelles:
            delta_x = i.largeur / 2
            delta_y = i.hauteur / 2
            self.canevas.create_rectangle(i.position_x - delta_x, i.position_y - delta_y, i.position_x + delta_x,
                                          i.position_y + delta_y, fill="blue")

    def debuter_partie(self, event):
        if not self.modele.partie_courante.est_termine:
            self.canevas.tag_unbind("pion", "<Button>")
            self.canevas.bind("<B1-Motion>", self.deplacer_pion)
            self.canevas.bind("<ButtonRelease>", self.relacher_pion)
            self.parent.demarrer_chrono()
            self.parent.jouer()

    def recibler_pion(self, event):
        if not self.modele.partie_courante.est_termine:
            self.canevas.tag_unbind("pion", "<Button>")
            self.canevas.bind("<B1-Motion>", self.deplacer_pion)
            self.canevas.bind("<ButtonRelease>", self.relacher_pion)

    def deplacer_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.deplacer_pion(x, y)

    def relacher_pion(self, evt):
        self.canevas.tag_bind("pion", "<Button>", self.recibler_pion)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def afficher_menu_fin_partie(self):
        self.creer_menu_fin_partie()

    def creer_menu_fin_partie(self):
        self.cadre_fin_partie = Frame(self.cadre_fenetre, width=400, height=200, bg="#c6c6c6",
                                      highlightbackground="black", highlightthickness=5)
        self.cadre_fin_partie.place(relx=.5, rely=.5, anchor=CENTER)
        titre = Label(self.cadre_fin_partie, text="FIN DE PARTIE", font=("Copperplate Gothic Light", 18), bg="#c6c6c6")
        titre.place(width=250, height=20, x=200, y=45, anchor=CENTER)
        duree = "{:.0f}".format(self.modele.partie_courante.duree / 60) + "min" + "{:.0f}".format(
            self.modele.partie_courante.duree % 60) + "sec"
        self.parent.ajouter_score(duree)
        temps = Label(self.cadre_fin_partie, text="Temps écoulé : %s" % duree, font=("Copperplate Gothic Light", 14),
                      bg="#c6c6c6")
        temps.place(relx=0.5, rely=0.5, anchor=CENTER)
        btn_retour_menu = Button(self.cadre_fin_partie, text="MENU", command=self.parent.retour_vers_menu,
                                 font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_retour_menu.place(width=120, height=30, x=70, y=150)
        btn_rejouer = Button(self.cadre_fin_partie, text="REJOUER", command=self.parent.rejouer,
                             font=("Copperplate Gothic Light", 14), bg="#228B22")
        btn_rejouer.place(width=120, height=30, x=210, y=150)

    def enlever_menu_principal(self):
        self.cadre_menu_principal.destroy()

    def enlever_menu_session(self):
        self.cadre_menu_session.destroy()

    def enlever_menu_scores(self):
        self.cadre_menu_scores.destroy()

    def enlever_menu_fin_partie(self):
        self.cadre_fin_partie.destroy()

    def enlever_menu_jeu(self):
        self.cadre_fenetre.destroy()
        self.cadre_zone_jeu.destroy()
