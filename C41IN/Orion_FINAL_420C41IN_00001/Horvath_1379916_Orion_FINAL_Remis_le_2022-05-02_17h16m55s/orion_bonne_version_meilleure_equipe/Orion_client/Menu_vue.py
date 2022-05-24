from tkinter import *
from Orion_vue import *


class Menu_vue():
    def __init__(self, parent):
        self.parent = parent
        self.taille_police = 9

    def creer_menu(self):
        self.menu = Toplevel(self.parent.root, bg="#618fad")
        self.menu.title("Menu")
        self.menu.geometry("500x500+600+450")
        self.menu.protocol("WM_DELETE_WINDOW", self.fermer_menu)

        self.btn_quitter = Button(self.menu, text='Quitter', command=self.parent.root.destroy, borderwidth=2,
                                  relief="groove", bg="#45657a", font=self.taille_police).pack(side="bottom", ipadx=15, ipady=10, pady=5)

        self.btn_fenetre = Button(self.menu, text='Fenetre', command=self.mode_fenetre, borderwidth=2, relief="groove",
                                  bg="#45657a", font=self.taille_police).pack(side="bottom", ipadx=15, ipady=10, pady=5)
        self.menu.iconify()

    def ouvrir_menu(self):
        self.menu.deiconify()

    def fermer_menu(self):
        self.menu.iconify()

    def mode_fenetre(self):
        self.parent.root.attributes('-fullscreen', True)
        self.parent.root.wm_attributes('-fullscreen', False)
