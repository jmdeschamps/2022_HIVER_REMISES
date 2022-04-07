from tkinter import *
import time


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
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self,evt):
        self.parent.partie_en_cours = 0

        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def fin_de_partie(self):

        self.df = self.modele.duree
        format_float = "{:.2f}".format(self.df)
        print(format_float)

        self.modele.tableauSentinelle.clear()
        self.modele.pion.x = self.modele.largeur / 2
        self.modele.pion.y = self.modele.hauteur / 2

        self.parent.partie_en_cours = 0
        self.modele.creer_Sentinnelle()
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self, evt):
        x = evt.x

        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        self.canevas.create_rectangle(50, 50, 500, 500, fill="white", tags=("airedejeu"))

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))

        for i in self.modele.tableauSentinelle:
            x = i.x
            y = i.y
            dx = i.demitaillex
            dy = i.demitailley
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                      fill="blue", tags=("poteau",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.ajoutdecalage = 50
        self.vitesse = 3
        self.tableauSentinelle = []
        self.pion = Pion(self)


        self.creer_Sentinnelle()


    def creer_Sentinnelle(self):
        self.tableauSentinelle.append(Poteau(self, 100 + self.ajoutdecalage, 100 + self.ajoutdecalage, 30, 30, 8, 13))
        self.tableauSentinelle.append(Poteau(self, 300 + self.ajoutdecalage, 85 + self.ajoutdecalage, 30, 25, -5, 10))
        self.tableauSentinelle.append(Poteau(self, 85 + self.ajoutdecalage, 300+ self.ajoutdecalage, 15, 30, 10, -8))
        self.tableauSentinelle.append(Poteau(self, 355+ self.ajoutdecalage, 340+ self.ajoutdecalage, 50, 10, -10, -13))

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y,self)


    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def deplacement_sentinnelle(self):
        for i in self.tableauSentinelle:
            i.deplacerSentinelle()
        self.pion.tester_collision(self)



class Poteau():
    def __init__(self, parent, posx, posy, demix, demiy, vx, vy):
        self.parent = parent
        self.x = posx
        self.y = posy
        self.demitaillex = demix
        self.demitailley = demiy
        self.vx = vx
        self.vy = vy

    def deplacerSentinelle(self):

        self.x += self.vx
        self.y += self.vy

        if self.x < 15 or self.x > 535:
                self.vx = -(self.vx)

        if self.y < 15 or self.y > 535:
                self.vy = -(self.vy)




class Pion():
    def __init__(self, parent):
        self.parent = parent

        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
        self.demitaille = 20

    def recibler(self, x, y,parent):
        self.x = x
        self.y = y

        self.tester_collision(parent)

    def tester_collision(self,parent):

        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        for i in parent.tableauSentinelle:
            pot = i
            potx1 = pot.x - pot.demitaillex
            poty1 = pot.y - pot.demitailley
            potx2 = pot.x + pot.demitaillex
            poty2 = pot.y + pot.demitailley

            if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
                self.parent.parent.vue.fin_de_partie()
                print("collision", self.parent.duree)

        if x1 < 50 or y1 < 50 or x2 > 500 or y2 > 500:
            self.parent.parent.vue.fin_de_partie()


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
            self.deplacerSentinnel()
            self.vue.root.after(40, self.jouer_partie)

        self.vue.afficher_partie()

    def deplacerSentinnel(self):
        self.modele.deplacement_sentinnelle()


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")