import math
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

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self, evt):
        x = evt.x

        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)
        self.canevas.create_rectangle(self.modele.largeur - 50, 50, 50, self.modele.hauteur - 50,
                                      fill="white", tags=("bordure",))

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))


        for sentienelle in self.modele.sentinelle_list:
            self.canevas.create_rectangle(sentienelle.x - sentienelle.demi_tailleX,
                                          sentienelle.y - sentienelle.demi_tailleY,
                                          sentienelle.x + sentienelle.demi_tailleX,
                                          sentienelle.y + sentienelle.demi_tailleY,
                                          fill="blue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)

        self.sentinelle_list =[]
        self.sentinelle_list.append(Sentinelle(self,100,100,30,30,"++",4))
        self.sentinelle_list.append(Sentinelle(self,300,85,30,25,"+-",4))
        self.sentinelle_list.append(Sentinelle(self,85,350,15,30,"--",4))
        self.sentinelle_list.append(Sentinelle(self,355,340,50,10,"-+",4))

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)
    def mouvement_toutes_sentienelle(self):
        for sentinelle in self.sentinelle_list:
            sentinelle.mouvement()
            sentinelle.tester_collision()

    def jouer_tour(self):
        self.duree = time.time() - self.debut





class Pion():
    def __init__(self, parent):
        self.parent = parent

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


        #collision avec bordure
        if (self.x -self.demitaille < 55 or self.x -self.demitaille>=455 or self.y -self.demitaille>455 or self.y -self.demitaille < 55):
            self.parent.parent.partie_en_cours=0
class Sentinelle():
    def __init__(self,parent,x,y,demi_tailleX,demi_tailleY,cible,vitesse):
        self.parent =parent
        self.x=x
        self.y=y
        self.demi_tailleX=demi_tailleX
        self.demi_tailleY=demi_tailleY
        self.cible =cible
        self.vitesse = vitesse

    def mouvement(self):

        self.vitesse += self.parent.duree/100
        if self.cible == "++":
            self.x += self.vitesse
            self.y += self.vitesse
            if(self.x >=self.parent.largeur):
                self.cible = "-+"
        elif self.cible == "-+":
            self.x -= self.vitesse
            self.y += self.vitesse
            if (self.y >self.parent.hauteur):
                self.cible = "--"
        elif self.cible == "--":
            self.x -= self.vitesse
            self.y -= self.vitesse
            if (self.x <0):
                self.cible = "+-"
        elif self.cible == "+-":
            self.x += self.vitesse
            self.y -= self.vitesse
            if (self.y <0):
                self.cible = "++"
    def tester_collision(self):
        x1 = self.x - self.demi_tailleX

        y1 = self.y - self.demi_tailleY
        x2 = self.x + self.demi_tailleX
        y2 = self.y + self.demi_tailleY

        pion = self.parent.pion
        pionx1 = pion.x - pion.demitaille
        piony1 = pion.y - pion.demitaille
        pionx2 = pion.x + pion.demitaille
        piony2 = pion.y + pion.demitaille

        if (x2 > pionx1 and x1 < pionx2) and (y2 > piony1 and y1 < piony2):
            self.parent.parent.partie_en_cours = 0
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
            self.vue.afficher_partie()
            self.modele.mouvement_toutes_sentienelle()
            self.vue.root.after(40, self.jouer_partie)


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")