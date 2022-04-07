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
        self.canevas = Canvas(self.root, width=550, height=550, bg="black")
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


    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)


    def afficher_partie(self):
        self.canevas.delete(ALL)
        self.canevas.create_rectangle(50, 50, self.modele.largeur, self.modele.hauteur, fill="white")
        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                        fill="red", tags=("pion",))


        for sentinelle in self.modele.sentinelle_list:
            x = sentinelle.x
            y = sentinelle.y
            dX = sentinelle.demitailleX
            dY = sentinelle.demitailleY
            self.canevas.create_rectangle(x - dX, y - dY, x + dX, y + dY,
                                        fill="blue", tags=("sentinelle",)) #Ajouter un tag pour chaque rectangle?
        self.var_duree.set(str(round(self.modele.duree, 2)))

    def menu_mort(self):
       self.cadre_mort = Frame(self.root, bg="red")
       self.var_score = self.modele.score
       label_mort = Label(self.cadre_mort, text="0", textvariable=self.var_duree)
       label_mort.pack()

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 500
        self.hauteur = 500
        self.debut = None
        self.duree = 0
        self.score = 0
        self.vitesse = 0
        self.augmentation = 0.0005
        self.pion = Pion(self)
        self.isOver = False
        self.sentinelle_list = []
        self.sentinelle_list.append(Sentinelle(self, 100, 100, 30, 30, 1))
        self.sentinelle_list.append(Sentinelle(self, 300, 85, 30, 25, 2))
        self.sentinelle_list.append(Sentinelle(self, 85, 350, 15, 30, 3))
        self.sentinelle_list.append(Sentinelle(self, 405, 390, 50, 10, 4))


    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def tour_de_garde_sentinelles(self):
        for i in self.sentinelle_list:
            i.tour_de_garde()
            i.vitesse += self.vitesse

    def finir_partie(self):
            self.score = self.duree
            self.pion.recentrer()
            for i in self.sentinelle_list:
                i.replacer()




class Sentinelle():
    def __init__(self, parent, x, y, demitailleX, demitailleY, id):
        self.parent = parent
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.id = id
        self.vitesse = 4
        self.demitailleX = demitailleX
        self.demitailleY = demitailleY
        self.cibleX = 0
        self.cibleY = 0

    def tour_de_garde(self):

        if self.id == 1:
            self.x = self.x + self.vitesse
            self.y = self.y + self.vitesse
        elif self.id == 2:
            self.x = self.x - self.vitesse
            self.y = self.y + self.vitesse
        elif self.id == 3:
            self.x = self.x + self.vitesse
            self.y = self.y - self.vitesse
        elif self.id == 4:
            self.x = self.x - self.vitesse
            self.y = self.y - self.vitesse

        if self.x + self.demitailleX >= 500 or self.x - self.demitailleX <= 50 or self.y + self.demitailleY >= 500 or self.y - self.demitailleY <= 50:
            if self.vitesse != -4:
                self.vitesse = -4
                self.parent.augmentation = self.parent.augmentation * -1
            else:
                self.vitesse = 4


    def replacer(self):
        self.x = self.original_x
        self.y = self.original_y
        self.vitesse = 3



class Pion(): #carré rouge
    def __init__(self, parent):
        self.parent = parent
        self.x = (self.parent.largeur + 50) / 2
        self.y = (self.parent.hauteur + 50) / 2
        self.demitaille = 20


    def recentrer(self):
        self.x = (self.parent.largeur + 50) / 2
        self.y = (self.parent.hauteur + 50) / 2

    def recibler(self, x, y):
        self.x = x
        self.y = y
        self.tester_collision()

    def tester_collision(self):
        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille
        for i in self.parent.sentinelle_list:
            sentx1 = i.x - i.demitailleX
            senty1 = i.y - i.demitailleY
            sentx2 = i.x + i.demitailleX
            senty2 = i.y + i.demitailleY
            if (x2 > sentx1 and x1 < sentx2) and (y2 > senty1 and y1 < senty2):
                self.parent.isOver = True

        if self.x - self.demitaille <= 50 or self.x + self.demitaille >= 450 or self.y + self.demitaille <= 50 or self.y - self.demitaille >= 450:
            self.parent.isOver = True


class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def deplacer_sentinelles(self):
        self.modele.tour_de_garde_sentinelles()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if not self.modele.isOver:
            self.modele.jouer_tour()
            self.modele.tour_de_garde_sentinelles()
            self.vue.afficher_partie()
            self.vue.root.after(40, self.jouer_partie)
        else:
            self.finir_partie()

    def finir_partie(self):
        self.modele.finir_partie()
        print(self.modele.score)
        self.vue.menu_mort()
        self.vue.afficher_partie()
        self.partie_en_cours = 0





if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")