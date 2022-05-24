from Pillow import *
from Orion_vue import *
from tkinter import *

class Log_vue():
    def __init__(self, parent):
        self.parent = parent

    def creer_log(self):
        self.nouvelle_fenetre = Toplevel(self.parent.root)
        self.nouvelle_fenetre.geometry("200x200")
        Label(self.nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)
        self.nouvelle_fenetre.protocol("WM_DELETE_WINDOW", self.fermer_log)
        self.nouvelle_fenetre.withdraw()

    def ouvrir_log(self):
        self.nouvelle_fenetre.deiconify()

    def fermer_log(self):
        self.nouvelle_fenetre.iconify()
