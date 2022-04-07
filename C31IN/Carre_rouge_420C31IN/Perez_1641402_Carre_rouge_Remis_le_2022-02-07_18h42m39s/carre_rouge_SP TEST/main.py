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
        # le canevas de jeux
        self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="white")

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


    def arreter_jeu(self): # il y avait un parametre evt ici
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

        self.canevas.create_rectangle(0, 0, self.modele.largeur, self.modele.hauteur, fill="black", tags=("fond_noir",))
        self.canevas.create_rectangle(30 , 30, self.modele.largeur-30, self.modele.hauteur-30, fill="white", tags=("fond_blanc",))
        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))

        for i in self.modele.liste_sentinelles:
            x = i.x
            y = i.y
            dx = i.demitaille_x
            dy = i.demitaille_y
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy, fill="blue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))

class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)

        self.liste_sentinelles = []
        self.sentinelle1 = Sentinelle(self, 100, 100, 30, 30,1,1,1)
        self.liste_sentinelles.append(self.sentinelle1)
        self.sentinelle2 = Sentinelle(self, 300, 85, 30, 25,2,-1,1)
        self.liste_sentinelles.append(self.sentinelle2)
        self.sentinelle3 = Sentinelle(self, 85, 350, 15, 30,3,1,-1)
        self.liste_sentinelles.append(self.sentinelle3)
        self.sentinelle4 = Sentinelle(self, 355, 340, 50, 10,4,-1,-1)
        self.liste_sentinelles.append(self.sentinelle4)

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut
        self.marcher_sentinelle()

    def marcher_sentinelle(self):
        for i in self.liste_sentinelles:
            i.marcher()

    # def debuter_partie(self):
    #     self.parent.debuter_partie

    def arreter_jeu(self):
        self.parent.arreter_jeu()



class Sentinelle():

    def __init__(self, parent, x, y, dx, dy, id, dirx, diry):
        self.parent=parent

        self.id = id
        self.x = x
        self.y = y
        self.demitaille_x = dx
        self.demitaille_y = dy
        self.vitesse = 8
        self.dirx = dirx
        self.diry = diry


    def marcher(self):

        self.x+=self.vitesse*self.dirx

        if self.x > self.parent.largeur:
            self.dirx = -1
        elif self.x<0 :
            self.dirx = 1


        self.y += self.vitesse * self.diry

        if self.y > self.parent.hauteur:
            self.diry = -1

        elif self.y < 0:
            self.diry = 1












        # if(self.id == 1):
        #     self.x += (self.vitesse * self.dirx)
        #     self.y += (self.vitesse * self.diry)
        #
        # elif(self.id == 2):
        #     self.x -=  (self.vitesse * self.dirx)
        #     self.y +=  (self.vitesse * self.diry)
        #
        # elif(self.id == 3):
        #     self.x += (self.vitesse * self.dirx)
        #     self.y -= (self.vitesse * self.diry)
        #
        # elif(self.id == 4):
        #     self.x -=(self.vitesse * self.dirx)
        #     self.y -=(self.vitesse * self.diry)

        #si ceci est actif, le sentinelle sort de du rectagle noir du coté oppossé
        # a celui specifié dans le lissez-moi

        # if (self.y >= self.parent.hauteur - 30):
        #     self.vitesse *= -1

        #le 60 est la valeur hard-codé pour que les carrées
        # rebondisent plus ou moins à l'interieur du carré blac

        #le *=-1 est pour inerser la direction dans
        # laquelle le sentinelle se deplace.

        # if(self.x>= self.parent.largeur-60):
        #     self.vitesse*=-1
        #
        #
        # if(self.x <= 60):
        #     self.vitesse*=-1
        #
        # if(self.y <=60):
        #     self.vitesse*=-1

        # if(self.dirx>0 and (self.x+self.demitaille_x) >= self.parent.largeur):
        #     self.dirx = self.dirx*-1
        #
        # if(self.dirx<0 and (self.x-self.demitaille_x)<=0):
        #     self.dirx = self.dirx * -1
        #
        # if (self.diry > 0 and (self.y + self.demitaille_y) >= self.parent.hauteur):
        #         self.dirx = self.diry * -1
        #
        # if (self.diry < 0 and (self.y - self.demitaille_y) <= 0):
        #         self.diry = self.diry * -1
class Pion():
    def __init__(self, parent):
        self.parent = parent

        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
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

        for i in self.parent.liste_sentinelles:
            potx1 = i.x - i.demitaille_x
            poty1 = i.y - i.demitaille_y
            potx2 = i.x + i.demitaille_x
            poty2 = i.y + i.demitaille_y

            if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
                print("collision", self.parent.duree)
                self.parent.arreter_jeu()


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
            self.vue.root.after(40, self.jouer_partie)

    def marcher_sentinelles(self):
        self.modele.marcher_sentinelle()

    def arreter_jeu(self):
        self.vue.arreter_jeu()

if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")