from tkinter import *
import time


class Vue:
    def __init__(self, parent):
        self.parent = parent

        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.cadres = self.creer_interface()

    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()
        # le canevas de jeu
        self.canevas = Canvas(self.root, width=self.modele.largeur_carre_noir, height=self.modele.hauteur_carre_noir,
                              bg="black")

        self.canevas.create_rectangle(50, 50, 500,
                                      500, fill="white")
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

    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def fin_de_partie(self):
        format_float = "{:.2f}".format(self.parent.modele.duree)
        print(format_float)
        self.parent.modele.liste_poteau.clear()
        self.parent.modele.creer_poteau()
        self.parent.partie_en_cours = 0
        self.parent.modele.pion.x = self.modele.largeur_carre_noir / 2
        self.parent.modele.pion.y = self.modele.hauteur_carre_noir / 2



        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def afficher_partie(self):
        self.canevas.delete(ALL)

        self.canevas.create_rectangle(50, 50, 500, 500,
                                      fill="white")

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))
        for i in self.modele.liste_poteau:
            x = i.x
            y = i.y
            dx = i.demi_taille_x
            dy = i.demi_taille_y
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                          fill="blue", tags=("poteau",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele:
    def __init__(self, parent):
        self.parent = parent

        self.largeur_carre_blanc = 450
        self.hauteur_carre_blanc = 450
        self.carre_blanc_demitaille = self.largeur_carre_blanc / 2
        self.largeur_carre_noir = 550
        self.hauteur_carre_noir = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.liste_poteau = []
        self.creer_poteau()


    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def creer_poteau(self):
        self.liste_poteau = [Poteau(self, 100, 100, 30, 30, 8, 12),
                             Poteau(self, 300, 85, 30, 25, -12, 5),
                             Poteau(self, 85, 350, 15, 30, 8, -12),
                             Poteau(self, 355, 340, 50, 10, -5, -8)]

    def recibler_poteau(self):
        for i in self.liste_poteau:
            i.recibler_poteau()
        self.pion.tester_collision()


class Poteau:
    def __init__(self, parent, x, y, demi_taille_x, demi_taille_y, vitesse_x, vitesse_y):
        self.parent = parent

        self.x = x
        self.y = y
        self.demi_taille_x = demi_taille_x
        self.demi_taille_y = demi_taille_y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y

    def recibler_poteau(self):
        if self.x >= self.parent.largeur_carre_noir:
            self.vitesse_x = -8
        elif self.x <= 0:
            self.vitesse_x = 8
        elif self.y >= self.parent.hauteur_carre_noir:
            self.vitesse_y = -8
        elif self.y <= 0:
            self.vitesse_y = 8

        self.x += self.vitesse_x * self.parent.duree/3
        self.y += self.vitesse_y * self.parent.duree/3


class Pion:
    def __init__(self, parent):
        self.parent = parent

        self.x = self.parent.largeur_carre_noir / 2
        self.y = self.parent.largeur_carre_noir / 2
        self.demitaille = 20

    def recibler(self, x, y):
        self.x = x

        self.y = y

        self.tester_collision()

    def tester_collision(self):

        x1 = self.x - self.demitaille

        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        for i in self.parent.liste_poteau:

            pot = i
            potx1 = pot.x - pot.demi_taille_x
            poty1 = pot.y - pot.demi_taille_y
            potx2 = pot.x + pot.demi_taille_x
            poty2 = pot.y + pot.demi_taille_y

            if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
                self.parent.parent.fin_de_partie()
            elif x2 > self.parent.largeur_carre_noir - 50 or x1 < 50:
                self.parent.parent.fin_de_partie()
            elif y2 > self.parent.hauteur_carre_noir - 50 or y1 < 50:
                self.parent.parent.fin_de_partie()


class Controleur:
    def __init__(self):
        self.partie_en_cours = 0

        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def recibler_poteau(self):
        self.modele.recibler_poteau()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()

        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.recibler_poteau()
            self.vue.root.after(40, self.jouer_partie)
        self.vue.afficher_partie()

    def fin_de_partie(self):
        self.vue.fin_de_partie()


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
