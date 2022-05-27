from tkinter import font
from tkinter.simpledialog import *
from chargeurdimages import *

class MenuFinPartie:
    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def __init__(self, view):
        self.images = chargerimages2()
        self.view = view
        self.cadre = None
        self.canevas = None
        self.font = font.Font(family='freemono', size=11, weight="bold")

    def quitter(self):
        self.view.root.destroy()

    def pack(self, expand, fill):
        controleur = self.view.controleur
        model = controleur.modele

        joueur_mort = model.joueursMorts
        self.cadre = Frame(self.view.cadreapp, width=500, height=400)

        self.canevas = Canvas(self.cadre, width=1280, height=960)

        if controleur.monnom in joueur_mort.keys():
            self.canevas.create_image(0, 0, anchor=NW, image=self.images['fin-defaite'])
            self.canevas.create_text(640, 30, text="YOU DIED", font=self.font)
        else:
            self.canevas.create_image(0, 0, anchor=NW, image=self.images['fin-victoire'])
            self.canevas.create_text(640, 30, text="VICTORY ACHIEVED", font=self.font)

        nb_row = 1
        self.canevas.create_text(640, (nb_row * 20) + 30, text=f"{nb_row}: {model.joueur_winner.nom}", font=self.font)
        nb_row += 1

        for joueur in joueur_mort.keys():
            self.canevas.create_text(640, (nb_row * 20) + 30, text=f"{nb_row}: {joueur}")
            nb_row += 1

        btnurlconnect = Button(self.cadre, text="Quitter", font=("Arial", 12),
                               command=self.quitter)

        self.canevas.create_window(650, 400, window=btnurlconnect, width=400, height=30)

        self.canevas.pack()
        self.cadre.pack(expand=1, fill=BOTH)

    def pack_forget(self):
        self.cadre.pack_forget()
