import os
from tkinter import *
import time
from tkinter import simpledialog, messagebox


class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carré Rouge, alpha_0.1 par Déric Marchand")
        self.cadres = self.creer_interface()

    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()
        btn_scores = Button(self.cadre_info, text="Afficher scores")
        btn_scores.bind("<Button-1>", self.parent.afficher_score)
        btn_scores.pack()
        # le canevas de jeu
        self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas.pack()
        self.afficher_partie()

    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")
        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        self.canevas.bind("<ButtonRelease>", self.parent.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self, evt=None):
        if evt:
            self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
            self.canevas.unbind("<B1-Motion>")
            self.canevas.unbind("<ButtonRelease>")
        if not evt:
            self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
            self.canevas.unbind("<B1-Motion>")
            self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        # aire jouable
        self.canevas.create_rectangle(0 + (self.modele.largeur - self.modele.aire_jouable.largeur),
                                      0 + (self.modele.hauteur - self.modele.aire_jouable.hauteur),
                                      self.modele.aire_jouable.largeur,
                                      self.modele.aire_jouable.hauteur,
                                      fill="ivory", outline="")
        # pion
        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))

        for sentinelle in self.modele.sentinelles:
            x = sentinelle.x
            y = sentinelle.y
            dx = sentinelle.demi_x
            dy = sentinelle.demi_y
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                          fill="blue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.aire_jouable = Aire_Jouable(self)
        self.pion = Pion(self)
        self.sentinelles = []
        self.creer_sentinelles()

    def creer_sentinelles(self):
        # (self, parent, x, y, demi_x, demi_y, vitesse_x=0, vitesse_y=0):
        self.sentinelles.append(Sentinelle(self, 100, 100, 30, 30, 5, 5))
        self.sentinelles.append(Sentinelle(self, 300, 85, 30, 25, -5, 5))
        self.sentinelles.append(Sentinelle(self, 85, 350, 15, 30, 5, -5))
        self.sentinelles.append(Sentinelle(self, 355, 340, 50, 10, -5, -5))

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

        for sentinelle in self.sentinelles:
            sentinelle.deplacer()
            sentinelle.rebondir()

    def arreter_jeu(self):
        if len(self.sentinelles):
            self.sentinelles.clear()
            self.creer_sentinelles()
        self.pion.x = self.largeur / 2
        self.pion.y = self.largeur / 2


class Aire_Jouable:
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur - 100
        self.hauteur = self.parent.hauteur - 100
        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
        self.demitaille = self.largeur / 2


class Sentinelle:
    def __init__(self, parent, x, y, demi_x, demi_y, vitesse_x=0, vitesse_y=0):
        self.parent = parent
        self.x = x
        self.y = y
        self.demi_x = demi_x
        self.demi_y = demi_y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y

    def deplacer(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir(self):
        x1 = self.x - self.demi_x
        y1 = self.y - self.demi_y
        x2 = self.x + self.demi_x
        y2 = self.y + self.demi_y

        # vérification des collisions avec les limites du cadre
        cx1 = 0
        cy1 = 0
        cx2 = self.parent.largeur
        cy2 = self.parent.hauteur

        if x2 >= cx2 or x1 <= cx1:
            self.vitesse_x = -self.vitesse_x

        if y2 >= cy2 or y1 <= cy1:
            self.vitesse_y = -self.vitesse_y

class Pion:
    def __init__(self, parent):
        self.parent = parent
        self.controleur = parent.parent
        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
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

        # vérification des collisions avec les limites de l'aire de jeu
        a = self.parent.aire_jouable
        ax1 = 0 + (self.parent.largeur - self.parent.aire_jouable.largeur)
        ay1 = 0 + (self.parent.hauteur - self.parent.aire_jouable.hauteur)
        ax2 = self.parent.aire_jouable.largeur
        ay2 = self.parent.aire_jouable.hauteur
        if (x1 <= ax1 or x2 >= ax2) or (y1 <= ay1 or y2 >= ay2):
            self.controleur.arreter_jeu()

        for sentinelle in self.parent.sentinelles:
            s = sentinelle
            sx1 = s.x - s.demi_x
            sy1 = s.y - s.demi_y
            sx2 = s.x + s.demi_x
            sy2 = s.y + s.demi_y
            if (x2 >= sx1 and x1 <= sx2) and (y2 >= sy1 and y1 <= sy2):
                self.parent.parent.arreter_jeu()

class Controleur:
    def __init__(self):
        self.partie_en_cours = False
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.liste_score = []
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.partie_en_cours = True
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.vue.afficher_partie()
            self.vue.root.after(15, self.jouer_partie)

    def arreter_jeu(self, evt=None):
        self.vue.arreter_jeu()
        self.partie_en_cours = False
        self.modele.arreter_jeu()
        self.vue.afficher_partie()
        self.nouveau_score()

    def nouveau_score(self):
        duree = (round(self.modele.duree, 2))
        nom = simpledialog.askstring(f"{duree}!", "Quel est votre nom?",
                                        parent=self.vue.root)
        nom = nom.replace(" ", "")
        if nom is not None or not "":
            with open('score.txt', 'a') as f:
                f.write(f"{duree} {nom}\n")

    def afficher_score(self, scores_affiches=None):
        scores_affiches = ""
        if not os.path.exists('score.txt'):
            with open('score.txt', 'w'):
                pass

        with open('score.txt', 'r') as f:
            for line in f:
                score_entree = line.split()
                score_valeur, score_nom = score_entree
                self.liste_score.append([float(score_valeur), score_nom.strip()])

            self.liste_score = sorted(self.liste_score, key=lambda x: x[0], reverse=True)
            for score in self.liste_score:
                scores_affiches += f"{score[0]:<16} {score[1]}\n"

        messagebox.showinfo("Scores", scores_affiches)
        self.liste_score.clear()


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
