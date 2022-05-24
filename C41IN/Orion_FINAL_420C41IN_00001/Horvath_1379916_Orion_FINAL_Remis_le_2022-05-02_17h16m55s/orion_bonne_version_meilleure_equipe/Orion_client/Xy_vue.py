from tkinter import *
from Orion_vue import *

class Xy_vue():
    def __init__(self, parent):
        self.parent = parent

    def ouvrir_xy(self):
        nouvelle_fenetre = Toplevel(self.parent.root)
        nouvelle_fenetre.geometry("200x200")
        Label(nouvelle_fenetre, text="hello world").grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)
