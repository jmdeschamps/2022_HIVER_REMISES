from tkinter import *
import time


class Vue():

    def __init__(self, parent):
        self.sentinelle = None
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, P-O Parisien, alpha_0.1")
        self.root.iconbitmap('square-24.ico')
        self.leCarreRouge = None
        self.partie_en_cours = 0
        self.cadres = self.creer_interface()

    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="purple")
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
        self.zone_blanche = self.canevas.create_rectangle(50, 50, self.modele.largeur - 50,
                                                          self.modele.hauteur - 50,
                                                          fill="white")

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion"))

        for s in self.modele.lesSentinelles:
            self.canevas.create_rectangle(s.x1, s.y1, s.x2, s.y2,
                                          fill="blue", tags=("sentinelle"))

        x = self.modele.poteau.x
        y = self.modele.poteau.y
        d = self.modele.poteau.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="black", tags=("poteau",))
        self.var_duree.set(str(round(self.modele.duree, 2)))

    # def rafraichir(self):
    #     if self.parent.partie_en_cours:
    #         for s in self.modele.lesSentinelles:
    #             self.modele.avancer_sentinelles()
    #             self.root.after(10, self.rafraichir)


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.poteau = Poteau(self)
        self.lesSentinelles = []
        s1 = Sentinelle(self, 70, 70, 130, 130, 1, 1)
        s2 = Sentinelle(self, 270, 50, 330, 110, 1, -1)
        s3 = Sentinelle(self, 70, 320, 100, 380, -1, 1)
        s4 = Sentinelle(self, 305, 330, 405, 350, -1, -1)
        self.lesSentinelles.append(s1)
        self.lesSentinelles.append(s2)
        self.lesSentinelles.append(s3)
        self.lesSentinelles.append(s4)

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def avancer_sentinelles(self):
        for s in self.lesSentinelles:
            s.deplacer()


class Poteau():
    def __init__(self, parent):
        self.parent = parent
        self.x = 120
        self.y = 100
        self.demitaille = 5


class Sentinelle():
    def __init__(self, parent, x1, y1, x2, y2, dx, dy):
        self.parent = parent
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = dx
        self.dy = dy
        self.vitesse = 2
        # self.id =id

    def deplacer(self):
        # if
        self.x1 = self.x1 + (self.dx * self.vitesse)
        self.y1 = self.y1 + (self.dy * self.vitesse)
        self.x2 = self.x2 + (self.dx * self.vitesse)
        self.y2 = self.y2 + (self.dy * self.vitesse)
        self.parent.move(self.parent, self.dx * self.vitesse, self.dy * self.vitesse)
        self.rebond()

    def rebond(self):  # collisions avec les bords
        if self.x1 <= 0 or self.x2 >= self.parent.largeur:
            self.dx = -1 * self.dx

        if self.y1 <= 0 or self.y2 >= self.parent.hauteur:
            self.dy = -1 * self.dy

        # lesElements = self.parent.find_overlapping()
        # for i in lesElements:
        #     lesTags = self.parent.gettags(i)
        #     if len(lesTags) > 0:
        #         if lesTags[0] == "carreRouge":  # si le carre rouge lui touche
        #             self.vue.arreter()  ##declancher fin de jeu


class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.x = self.parent.largeur / 2
        self.y = self.parent.hauteur / 2
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

        pot = self.parent.poteau
        potx1 = pot.x - pot.demitaille
        poty1 = pot.y - pot.demitaille
        potx2 = pot.x + pot.demitaille
        poty2 = pot.y + pot.demitaille

        if (x2 > potx1 and x1 < potx2) and (y2 > poty1 and y1 < poty2):
            print("collision", self.parent.duree)

        # collisions avec les bords noirs
        if x1 <= 50 or x2 >= self.parent.largeur - 50:
            print("collision", self.parent.duree)

        if y1 <= 50 or y2 >= self.parent.hauteur - 50:
            print("collision", self.parent.duree)


class Fichier:
    def __init__(self):
        pass

    def ouvrir_fichier(self, nomFichier):
        fichier = open(nomFichier + ".txt")
        donnees = fichier.readlines()
        fichier.close()
        return donnees

    def sauvegarder_fichier(self, nomFicher, donnees):
        fichier = open(nomFicher + ".txt", "w")

        for i in donnees:
            fichier.write(i)

        fichier.close()


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


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
