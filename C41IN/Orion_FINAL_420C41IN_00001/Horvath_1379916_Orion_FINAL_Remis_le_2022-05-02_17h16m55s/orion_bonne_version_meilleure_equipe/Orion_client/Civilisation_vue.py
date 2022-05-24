from tkinter import *
from Chat_vue import *


class Civilisation_vue():
    def __init__(self, parent):
        self.parent = parent
        self.taille_police = 7

    def ouvrir_civilisation(self):

        self.joueurs = self.parent.modele.joueurs.copy()
        self.text = StringVar()
        self.text.set("Proposer alliance")
        self.civilisation_root = Toplevel(self.parent.root, bg="#333333")
        self.civilisation_root.title("Civilisation")
        self.civilisation_root.geometry("1900x800+0+150")

        contour_civilisation = Frame(self.civilisation_root, bg="#333333")
        self.frame_civilisation = Canvas(self.civilisation_root, bg="#333333")

        contour_joueur_actif = Frame(self.frame_civilisation, bg="#45657a")
        frame_joueur_actif = Frame(contour_joueur_actif, bg="#618fad")

        # self.btn_demande_alliance = Button(self.frame_civilisation,text="Alliance",command=self.demande_alliance)
        # self.btn_rompre_alliance = Button(self.frame_civilisation, text="Rompre",command=self.rompre_alliance)

        self.nom_joueur_actif = Label(frame_joueur_actif, text="nom joueur actif", relief="ridge", borderwidth=4,
                                      bg="#618fad", font=self.taille_police)

        self.nourriture_joueur_actif = Label(frame_joueur_actif, text="nourriture joueur actif", relief="ridge",
                                             borderwidth=4, bg="#618fad", font=self.taille_police)
        self.moral_joueur_actif = Label(frame_joueur_actif, text="moral joueur actif", relief="ridge", borderwidth=4,
                                        bg="#618fad", font=self.taille_police)
        self.militaire_joueur_actif = Label(frame_joueur_actif, text="militaire joueur actif", relief="ridge",
                                            borderwidth=4, bg="#618fad", font=self.taille_police)
        self.energie_joueur_actif = Label(frame_joueur_actif, text="energie joueur actif", relief="ridge",
                                          borderwidth=4, bg="#618fad", font=self.taille_police)
        self.diplomatie_joueur_actif = Label(frame_joueur_actif, text="diplomatie joueur actif", relief="ridge",
                                             borderwidth=4, bg="#618fad", font=self.taille_police)
        self.science_joueur_actif = Label(frame_joueur_actif, text="science joueur actif", relief="ridge",
                                          borderwidth=4, bg="#618fad", font=self.taille_police)
        self.credits_joueur_actif = Label(frame_joueur_actif, text="credits joueur actif", relief="ridge",
                                          borderwidth=4, bg="#618fad", font=self.taille_police)
        self.nom_joueur_actif.grid(row=1, column=1, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.nourriture_joueur_actif.grid(row=2, column=1, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.moral_joueur_actif.grid(row=2, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.militaire_joueur_actif.grid(row=3, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.energie_joueur_actif.grid(row=3, column=1, sticky=W, ipadx=25, ipady=15, pady=5, padx=5)
        self.diplomatie_joueur_actif.grid(row=2, column=10, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.science_joueur_actif.grid(row=4, column=1, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        self.credits_joueur_actif.grid(row=4, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)

        self.nom_joueur_actif.config(text=(str(self.parent.mon_nom) + " (VOUS)"), font=self.taille_police)
        self.nourriture_joueur_actif.config(text=("Nourriture : " + str(self.parent.joueur_actif.nourriture.quantite)), font=self.taille_police)
        self.moral_joueur_actif.config(text=("Moral : " + str(self.parent.joueur_actif.moral)), font=self.taille_police)
        self.militaire_joueur_actif.config(text=("Militaire : " + str(self.parent.joueur_actif.militaire)), font=self.taille_police)
        self.energie_joueur_actif.config(text=("Energie : " + str(self.parent.joueur_actif.energie.quantite)), font=self.taille_police)
        self.diplomatie_joueur_actif.config(text=("Diplomatie : " + str(self.parent.joueur_actif.diplomatie)), font=self.taille_police)
        self.science_joueur_actif.config(text=("Science : " + str(self.parent.joueur_actif.science)), font=self.taille_police)
        self.credits_joueur_actif.config(text=("Credits : " + str(self.parent.joueur_actif.credits)), font=self.taille_police)

        frame_alliance = Frame(frame_joueur_actif, bg='#618fad')

        Label(frame_joueur_actif, text=" Vos demandes d'alliance :",bg='#618fad',relief="ridge",
                                          borderwidth=4, font=self.taille_police).grid(row=5, column=15, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)

        if len(self.parent.joueur_actif.demandes_alliances) == 0:
            Label(frame_joueur_actif, text=" Pas de demande en ce moment ",bg='#618fad',relief="ridge",
                                          borderwidth=4, font=self.taille_police).grid(row=6, column=15, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
        else:
            compteur_row = 1
            for demande in self.parent.joueur_actif.demandes_alliances:
                Label(frame_joueur_actif, text=demande + " vous demande en alliance", font=self.taille_police).grid(row=6, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                bouton_temp = Button(frame_joueur_actif, text="Accepter l'alliance avec " + demande, relief="ridge",
                                     borderwidth=4, bg="#618fad", font=self.taille_police)
                bouton_temp.bind("<Button>", self.accepter_alliance)
                bouton_temp.grid(row=8, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                bouton_temp = Button(frame_joueur_actif, text="Refuser l'alliance avec " + demande, relief="ridge",
                                     borderwidth=4, bg="#618fad", font=self.taille_police)
                bouton_temp.bind("<Button>", self.refuser_alliance)
                bouton_temp.grid(row=10, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)

        frame_alliance.grid(row=5, column=5, sticky=W)
        frame_joueur_actif.pack(fill=BOTH, side=TOP, padx=10, pady=10, anchor=NW)
        contour_joueur_actif.pack(fill=BOTH, side=TOP, padx=10, pady=10, anchor=NW)


        self.lignes = 1
        frame_joueurs = Frame(self.frame_civilisation, bg="#963c31")

        frames = []

        for i in self.joueurs:
            frame = Frame(frame_joueurs, bg="#c24d3f")
            contour = Frame(frame, bg="#618fad")
            self.joueur = self.joueurs[i]
            if self.joueur.nom != self.parent.mon_nom:
                Label(contour, text=str(self.joueur.nom), relief="ridge", borderwidth=4, bg="#618fad", font=self.taille_police).grid(
                    row=self.lignes, column=1, sticky=W,
                    ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Nourriture : " + str(self.joueur.nourriture.quantite)), relief="ridge",
                      borderwidth=4, bg="#618fad", font=self.taille_police).grid(row=2, column=1, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Moral : " + str(self.joueur.moral)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=2, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Militaire : " + str(self.joueur.militaire)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=3, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Energie : " + str(self.joueur.energie.quantite)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=3, column=1, sticky=W, ipadx=25, ipady=15, pady=5, padx=5)
                Label(contour, text=("Diplomatie : " + str(self.joueur.diplomatie)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=2, column=6, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Science : " + str(self.joueur.science)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=4, column=1, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                Label(contour, text=("Credits : " + str(self.joueur.credits)), relief="ridge", borderwidth=4,
                      bg="#618fad", font=self.taille_police).grid(row=4, column=5, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                if self.parent.mon_nom not in self.joueur.alliances:
                    temp = Button(contour, text="Proposer alliance avec " + self.joueur.nom, relief="ridge",
                                  borderwidth=4, bg="#618fad", font=self.taille_police)
                    temp.bind("<Button>", self.proposer_alliance)
                    temp.grid(row=10, column=6, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                else:
                    temp = Button(contour, text="Rompre alliance avec " + self.joueur.nom, relief="ridge",
                                  borderwidth=4, bg="#618fad", font=self.taille_police)
                    temp.bind("<Button>", self.rompre_alliance)
                    temp.grid(row=10, column=6, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                    chat = Button(contour, text="Contacter " + self.joueur.nom, relief="ridge", borderwidth=4,
                                  bg="#618fad", command=self.parent.chat_vue.ouvrir_chat, font=self.taille_police)
                    chat.grid(row=6, column=6, sticky=W, ipadx=20, ipady=15, pady=5, padx=5)
                frame.pack(fill=BOTH, side=LEFT, padx=10, pady=10, anchor=NW)
                contour.pack(fill=BOTH, side=LEFT, padx=10, pady=10, anchor=NW)
                frames.append(frame)

        frame_joueurs.pack()
        self.frame_civilisation.pack(fill=BOTH)
        contour_civilisation.pack(fill=BOTH, side=TOP, padx=10, pady=10, anchor=NW)

    def rompre_alliance(self, evt):
        btn = evt.widget
        txt = btn.cget("text")
        nom_joueur = txt[21:]
        action = [self.parent.mon_nom, "rompre_alliance",
                  [self.parent.mon_nom, nom_joueur]]
        self.parent.parent.actionsrequises.append(action)

    def proposer_alliance(self, evt):
        btn = evt.widget
        txt = btn.cget("text")
        nom_joueur = txt[23:]
        action = [self.parent.mon_nom, "proposer_alliance",
                  [self.parent.mon_nom, nom_joueur]]
        self.parent.parent.actionsrequises.append(action)

    def accepter_alliance(self, evt):
        btn = evt.widget
        txt = btn.cget("text")
        nom_joueur = txt[25:]
        action = [self.parent.mon_nom, "accepter_alliance",
                  [self.parent.mon_nom, nom_joueur]]
        self.parent.parent.actionsrequises.append(action)

    def refuser_alliance(self, evt):
        btn = evt.widget
        txt = btn.cget("text")
        nom_joueur = txt[24:]
        action = [self.parent.mon_nom, "refuser_alliance",
                  [self.parent.mon_nom, nom_joueur]]
        self.parent.parent.actionsrequises.append(action)

