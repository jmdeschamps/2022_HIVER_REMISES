from tkinter import *
from tkinter.simpledialog import *


class MenuFinPartie:
    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def __init__(self, view):
        self.view = view
        self.cadre = None

    def quitter(self):
        quit()
        self.view.changer_cadre("splash")

    def pack(self, expand, fill):
        controleur = self.view.controleur
        model = controleur.modele

        joueur_mort = model.joueursMorts
        self.cadre = Frame(self.view.cadreapp, width=500, height=400)

        self.cadre.grid_rowconfigure(0, weight=100)

        self.cadre.grid_columnconfigure(0, weight=100)
        self.cadre.grid_columnconfigure(1, weight=100)

        if controleur.monnom in joueur_mort.keys():
            label = Label(self.cadre, text="YOU DIED")
        else:
            label = Label(self.cadre, text="VICTORY ACHIEVED")

        label.grid(row=0, columnspan=3, column=0, sticky="news")

        nb_row = 1
        label = Label(self.cadre, text=f"{nb_row}: {model.joueur_winner.nom}")
        label.grid(row=nb_row, column=1, sticky="nw")
        nb_row += 1

        for joueur in joueur_mort.keys():
            label = Label(self.cadre, text=f"{nb_row}: {joueur}")
            label.grid(row=nb_row, column=1, sticky="nw")
            nb_row += 1

        self.cadre.grid_rowconfigure(nb_row, weight=10)
        self.cadre.grid_rowconfigure(nb_row + 1, weight=100)

        btnurlconnect = Button(self.cadre, text="Quitter", font=("Arial", 12),
                               command=self.quitter)
        btnurlconnect.grid(row=nb_row + 1, column=1, sticky="w")
        self.cadre.pack(expand=1, fill=BOTH)

    def pack_forget(self):
        self.cadre.pack_forget()
