from tkinter import *
import time
import random


class Vue():
    def __init__(self, parent):
        self.parent = parent

        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.9")
        self.cadres = self.creer_interface()

    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()

        # le canevas de jeu
        self.canevas_noir = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        self.canevas = Canvas(self.canevas_noir, width=450, height=450, bg="white")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas_noir.pack()
        self.canevas.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.canevas.pack()
        self.canevas.place(anchor=CENTER, relx=0.5, rely=0.5)

        self.afficher_partie()

    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")
        self.canevas.bind("<B1-Motion>", self.recibler_pion)

        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0

        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")
        self.modele.sentinelles.clear()
        self.modele.pion.x = 225
        self.modele.pion.y = 225
        self.modele.creer_sentinelles()
        self.modele.duree = 0
        self.modele.pion.demitaille = 10

    def recibler_pion(self, evt):
        x = evt.x

        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):

        if not self.modele.pion.alive:
            self.arreter_jeu(self)
            self.modele.pion.alive = True

        self.canevas.delete(ALL)
        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))

        for i in self.modele.sentinelles:
            x = i.x
            y = i.y
            d1 = i.demitaille1
            d2 = i.demitaille2
            self.canevas.create_rectangle(x - d1, y - d2, x + d1, y + d2,
                                          fill="blue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.vue = Vue

        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)

        self.sentinelles = []
        self.creer_sentinelles()

    def creer_sentinelles(self):
        vitesse = 8
        self.sentinelles.append(Sentinelle(self, 100, 100, 30, 30, vitesse, -vitesse))
        self.sentinelles.append(Sentinelle(self, 300, 85, 30, 25, -vitesse, -vitesse))
        self.sentinelles.append(Sentinelle(self, 85, 350, 15, 30, vitesse, vitesse))
        self.sentinelles.append(Sentinelle(self, 355, 340, 50, 10, -vitesse, vitesse))

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut


class Sentinelle():
    def __init__(self, parent, x, y, demitaille1, demitaille2, vitesse_x, vitesse_y):
        self.parent = parent

        self.x = x
        self.y = y
        self.demitaille1 = demitaille1
        self.demitaille2 = demitaille2

        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y

    def bouger(self):
        self.x = self.x + self.vitesse_x
        self.y = self.y - self.vitesse_y

        self.x1 = self.x - self.demitaille1
        self.y1 = self.y - self.demitaille2
        self.x2 = self.x + self.demitaille1
        self.y2 = self.y + self.demitaille2

        if self.x1 <= 0 or self.x2 >= 450:
            self.vitesse_x = self.vitesse_x * -1

        if self.y1 <= 0 or self.y2 >= 450:
            self.vitesse_y = self.vitesse_y * -1


class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.alive = True

        self.x = 225
        self.y = 225
        self.demitaille = 10

    def recibler(self, x, y):
        self.x = x

        self.y = y
        self.tester_collision()

    def tester_collision(self):
        x1 = self.x - self.demitaille

        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        for i in self.parent.sentinelles:
            sentinelle = i
            sentinelle_x1 = sentinelle.x - sentinelle.demitaille1
            sentinelle_y1 = sentinelle.y - sentinelle.demitaille2
            sentinelle_x2 = sentinelle.x + sentinelle.demitaille1
            sentinelle_y2 = sentinelle.y + sentinelle.demitaille2

            if (x2 > sentinelle_x1 and x1 < sentinelle_x2) and (y2 > sentinelle_y1 and y1 < sentinelle_y2):
                self.alive = False

            if x1 < 10 or x2 > 450 or y1 < 10 or y2 > 450:
                self.alive = False


class Controleur():
    def __init__(self):
        self.partie_en_cours = 0

        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            for i in self.modele.sentinelles:
                i.bouger()

            self.modele.pion.demitaille = 10 + self.modele.duree / 2
            self.vue.root.after(40, self.jouer_partie)

        self.modele.pion.tester_collision()
        self.vue.afficher_partie()


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
