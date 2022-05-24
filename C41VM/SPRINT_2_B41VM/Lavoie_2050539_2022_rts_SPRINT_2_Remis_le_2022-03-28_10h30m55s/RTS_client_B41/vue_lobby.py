from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *


class Lobby:
    def __init__(self, view):
        self.view = view
        self.controleur = view.controleur
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(view.cadreapp)
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

    def update_lobby(self, dico):
        self.listelobby.delete(0, END)
        for i in dico:
            self.listelobby.insert(END, i[0])
        if self.controleur.joueur_createur:
            self.btnlancerpartie.config(state=NORMAL)

    def lancer_partie(self):
        self.controleur.lancer_partie()

    def pack(self, expand, fill):
        self.cadrelobby.pack(expand=1, fill=BOTH)

    def pack_forget(self):
        self.cadrelobby.pack_forget()
