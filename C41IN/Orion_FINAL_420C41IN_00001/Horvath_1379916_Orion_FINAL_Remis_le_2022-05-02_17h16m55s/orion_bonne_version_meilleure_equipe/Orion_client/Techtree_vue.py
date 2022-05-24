from Pillow import *
from Orion_vue import *
from tkinter import *
from Orion_modele import *

from idlelib.tooltip import Hovertip


class Techtree_vue():
    def __init__(self, parent):
        self.parent = parent
        self.dico_ameliorations_militaire = []
        self.dico_ameliorations_economie = []
        self.dico_ameliorations_diplomatie = []
        self.dico_ameliorations_exploitation = []

    def creer_techtree(self):
        self.ecran_largeur = self.parent.root.winfo_screenwidth() / 2
        self.ecran_hauteur = self.parent.root.winfo_screenheight() / 2
        self.point_depart_x = 400
        self.point_depart_y = self.ecran_hauteur / 5

        self.valeur_incrementation_y = 100
        self.tech_root = Toplevel(self.parent.root)
        self.tech_root.geometry("1805x600+50+250")
        self.tech_root.title("TechTree")
        self.tech_root.bind_all("")
        frame_techtree = Frame(self.tech_root, width=self.ecran_largeur, height=self.ecran_hauteur)
        tech_canvas = Canvas(frame_techtree, bg="black")
        self.tech_root.protocol("WM_DELETE_WINDOW", self.fermer_techtree)
        self.frame_description = Frame(frame_techtree, width=250, height=100, bg="#618fad")
        self.label_description = Label(self.frame_description, text=" ",bg="#618fad")

        # Améliorations Militaire
        Label(tech_canvas, text="MILITAIRE", relief="ridge", borderwidth=4, bg="tan1").grid(row=self.point_depart_x,
                                                                                            column=10, sticky=W,
                                                                                            ipadx=15, ipady=15, pady=5,
                                                                                            padx=15)
        b = Button(tech_canvas, text="Spacefighter I", relief="ridge", borderwidth=4, bg="#618fad")
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Rage de Vivre", relief="ridge", borderwidth=4, bg="#618fad")
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Spacefighter II", relief="ridge", borderwidth=4, bg="#618fad")
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Flotte Renforcee", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Satellite: Defense I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=10, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Satellite: Defense II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=10, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Colonisateur I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=15, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Figure: General I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=15, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Destroyer I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=15, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Figure: General II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=15, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Destroyer II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 250, column=15, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)

        # Ameliorations Exploration
        Label(tech_canvas, text="EXPLORATION", relief="ridge", borderwidth=4, bg="tan1", ).grid(row=self.point_depart_x,
                                                                                              column=30, sticky=W,
                                                                                              ipadx=15, ipady=15,
                                                                                              pady=5, padx=15)
        b = Button(tech_canvas, text="Scout II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=25, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Scout III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=25, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Pyramide d'Argent", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=25, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)


        b = Button(tech_canvas, text="Figure: Scientifique I", relief="ridge", borderwidth=4, bg="#618fad")
        b = Button(tech_canvas, text="Figure: Scientifique I", relief="ridge", borderwidth=4, bg="#618fad", )

        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=30, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Laboratoire II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=30, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Figure: Scientifique II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=30, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Laboratoire III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=30, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Grande Universite", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 250, column=30, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Satellite: Vision I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=35, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Intrication Quantique", relief="ridge", borderwidth=4,
                   bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=35, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Satellite: Vision II", relief="ridge", borderwidth=4,
                   bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=35, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)

        # Améliorations Diplomatie
        Label(tech_canvas, text="DIPLOMATIE", relief="ridge", borderwidth=4, bg="tan1", ).grid(row=self.point_depart_x,
                                                                                             column=50, sticky=W,
                                                                                             ipadx=15, ipady=15, pady=5,
                                                                                             padx=15)
        b = Button(tech_canvas, text="Democratie", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=45, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Marche Cosmique", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=45, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Figure: Marchand I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=45, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Bazaar Eternel", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 250, column=45, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Figure: Politicien I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=50, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Alliances", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=50, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Figure: Politicien II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=50, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Autocratie", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=55, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Usine II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=55, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)
        b = Button(tech_canvas, text="Usine III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=55, sticky=W, ipadx=15, ipady=15, pady=5,
               padx=15)

        # Ameliorations Exploitation
        Label(tech_canvas, text="EXPLOITATION", relief="ridge", borderwidth=4, bg="tan1", ).grid(row=self.point_depart_x,
                                                                                               column=70, sticky=W,
                                                                                               ipadx=15, ipady=15,
                                                                                               pady=5, padx=15)
        b = Button(tech_canvas, text="Cargo II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=65, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Raffinerie II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=65, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Cargo III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=65, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Raffinerie III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=65, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        b = Button(tech_canvas, text="Ferme II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 50, column=70, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Conservation I", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 100, column=70, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Ferme III", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 150, column=70, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Conservation II", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 200, column=70, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)
        b = Button(tech_canvas, text="Jardin d'Eden", relief="ridge", borderwidth=4, bg="#618fad", )
        b.bind("<Button>", self.acquerir_tech)
        b.bind("<Enter>", self.afficher_description)
        b.grid(row=self.point_depart_x - 250, column=70, sticky=W, ipadx=15, ipady=15, pady=5, padx=15)

        self.frame_description.pack(fill=BOTH,side=BOTTOM, expand=True)
        self.label_description.pack(fill=BOTH, expand=True,anchor=CENTER)

        tech_canvas.pack(fill=BOTH, expand=True)
        frame_techtree.pack(fill=BOTH, expand=True)
        self.tech_root.iconify()

    def acquerir_tech(self, evt):
        # print(self.b.bindtags())
        btn = evt.widget
        txt = btn.cget("text")
        joueur = self.parent.mon_nom
        resultat = self.parent.modele.technologies[txt].verif_acquerir(self.parent.modele.joueurs[self.parent.mon_nom])
        if resultat:
            btn.config(bg="#2ba180")
            action = [joueur, "acquerir_tech", [txt]]
            self.parent.parent.actionsrequises.append(action)

    def afficher_description(self, evt):
        btn = evt.widget
        txt = btn.cget("text")
        self.description_tech = self.parent.modele.technologies[txt].description
        self.label_description.config(text=self.description_tech)

    # def des améliorations ici + ajouter à la fin def amelioration_accepte afin de changer l'apparence
    # du bouton

    def amelioration_accepte(self):
        pass

    def ouvrir_techtree(self):
        self.tech_root.deiconify()

    def fermer_techtree(self):
        self.tech_root.iconify()
