
from tkinter import *
import time




class Vue():
    def __init__(self, parent):
        self.parent = parent

        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, Version 0.4")

        self.cadres = self.creer_interface()

    def creer_interface(self):

        # cadre HUD affichant la duree

        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()

        # le canevas de jeu
        self.canevas = Canvas(self.root, width=450, height=450, bg="white")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)

        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas.pack()

        self.afficher_partie()

    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")

        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

        self.modele.pion.x = 225
        self.modele.pion.y = 225
        self.modele.sentinelles.clear()
        self.modele.creer_sentinelles()

    def game_over(self):
        self.afficher_partie()

    def recibler_pion(self, evt):
        x = evt.x

        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="darkred", tags=("pion",))

        #CRÉER CADRE DE JEU
        x = self.modele.bordure.x
        y = self.modele.bordure.y
        d = self.modele.bordure.demitaille
        self.canevas.create_rectangle(x - d, y - d, 500 + d, x + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(x - d, y - d, x + d, 500 + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(x - d, 450 - d, 500 + d, 500 + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(450 - d, 450 - d, 500 + d, y + d,
                                      fill="black", tags=("poteau",))

        for i in self.modele.sentinelles:
            x = i.x
            y = i.y
            d1 = i.dt1
            d2 = i.dt2
            self.canevas.create_rectangle(x - d1, y - d2, x + d1, y + d2,
                                          fill="darkblue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.partie_en_cours.duree, 2)))
