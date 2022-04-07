from tkinter import *
import time
from tkinter import ttk


class Vue():
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

        # Bouton choisir niveau
        self.liste_niveaux = ["Facile (3)", "Intermédiaire (9)", "Difficile (15)"]
        self.bouton_niveaux = ttk.Combobox(self.cadre_info, values=self.liste_niveaux)
        self.bouton_niveaux.current(0)
        self.bouton_niveaux.pack()

        #ajouter score

        self.bouton_ajoutScore = Button(self.cadre_info, text="Enlever toutes les bibittes", )
        self.bouton_ajoutScore.bind("<Button-1>", self.ajouterScore)

        # le canevas de jeu
        self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)

        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas.pack()

        self.afficher_partie()

    def ajouterScore(self):
        self.parent.modele.ajouterScore("")

    def debuter_partie(self, evt):
        self.verifier_vitesse()
        self.canevas.tag_unbind("pion", "<Button>")
        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")
        self.parent.modele.pion.x = self.parent.modele.largeur / 2
        self.parent.modele.pion.y = self.parent.modele.largeur / 2
        mod = self.parent.modele
        mod.supprimerRectangle()
        mod.creerRectangle()


    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        self.canevas.create_rectangle(50, 50, 500, 500, fill="white", tags=("aireDeJeu"))

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))
        for i in self.modele.rectangles:
            x = i.x
            y = i.y
            dx = i.demiX
            dy = i.demiY
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                          fill="blue", tags=("poteau1",))
        self.var_duree.set(str(round(self.modele.duree, 2)))

    def verifier_vitesse(self):
        vitesse = 15
        if (self.bouton_niveaux.get() == "Facile (3)"):
            vitesse = 3
        if (self.bouton_niveaux.get() == "Intermédiaire (9)"):
            vitesse = 9
        self.parent.modele.vitesse_Rectangle(vitesse)


class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.vitesse = 15;
        self.tableauScores = []
        self.rectangles = []
        self.creerRectangle()

    def ajouterScore(self, nom=""):
        pass

    def creerRectangle(self):
        self.rectangles.append(Poteau(self, 150, 150, 30, 30, 1, (-2)))
        self.rectangles.append(Poteau(self, 350, 135, 30, 25, 1, 2))
        self.rectangles.append(Poteau(self, 135, 400, 15, 30, (-1), (-2)))
        self.rectangles.append(Poteau(self, 405, 390, 50, 10, (-1), 2))

    def vitesse_Rectangle(self, vitesse):
        for i in self.rectangles:
            i.vitesseX *= vitesse
            i.vitesseY *= vitesse

    def supprimerRectangle(self):
        self.rectangles.clear()

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def deplacementRectangle(self):
        for i in self.rectangles:
            pot = i
            potx1 = pot.x - pot.demiX
            poty1 = pot.y - pot.demiY
            potx2 = pot.x + pot.demiX
            poty2 = pot.y + pot.demiY

            if (potx1 < 0 or potx2 > 550):
                i.vitesseX = -(i.vitesseX)
            if (poty1 < 0 or poty2 > 550):
                i.vitesseY = -(i.vitesseY)
            i.x += i.vitesseX
            i.y += i.vitesseY
            i.tester_collision(self)

    def jouer_tour(self):
        self.duree = time.time() - self.debut


class Poteau():
    def __init__(self, parent, x, y, dx, dy, vitesseX, vitesseY):
        self.parent = parent
        self.xDepart = x
        self.yDepart = y
        self.x = x
        self.y = y
        self.demiX = dx
        self.demiY = dy
        self.vitesseX = vitesseX
        self.vitesseY = vitesseY

    def tester_collision(self, parent):
        x1 = self.x - self.demiX
        y1 = self.y - self.demiY
        x2 = self.x + self.demiX
        y2 = self.y + self.demiY

        pot = parent.pion
        potx1 = pot.x - pot.demitaille
        poty1 = pot.y - pot.demitaille
        potx2 = pot.x + pot.demitaille
        poty2 = pot.y + pot.demitaille

        if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
            print("collision", self.parent.duree)
            self.parent.parent.vue.arreter_jeu(0)


class Pion():
    def __init__(self, parent):
        self.parent = parent

        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
        self.demitaille = 20

    def recibler(self, x, y):
        self.x = x
        self.y = y
        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille
        if (x1 < 50 or x2 > 500 or y1 < 50 or y2 > 500):
            self.parent.parent.vue.arreter_jeu(0)


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
            self.modele.deplacementRectangle()
            self.vue.root.after(40, self.jouer_partie)
        self.vue.afficher_partie()


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
