from tkinter import *
import time

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.afficher_menu()
        self.cadres = self.creer_interface()


    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        btn_menu = Button(self.cadre_info, text="Afficher menu", command=self.afficher_menu)
        btn_score = Button(self.cadre_info, text="Afficher score", command=self.afficher_score)
        btn_menu.pack(side=RIGHT)
        btn_score.pack(side=RIGHT)
        label_duree.pack()
        # le canevas de jeu
        self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="white")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas.pack()
        self.afficher_partie()

    def afficher_menu(self):
        # Le canevas des options
        self.option = Tk()
        self.option.title("Niveau de difficulté")
        self.option.attributes('-topmost', 1)
        self.canevas_option = Canvas(self.option, width=300, height=600, bg="white")
        btn_debutant = Button(self.canevas_option, text="Débutant", width=30, height=2, command=self.niveau_debutant)
        btn_intermediaire = Button(self.canevas_option, text="Intermédiaire", width=30, height=2, command=self.niveau_intermediaire)
        btn_expert = Button(self.canevas_option, text="Expert", width=30, height=2, command=self.niveau_expert)
        self.canevas_option.pack()
        btn_debutant.pack(side=TOP)
        btn_intermediaire.pack(side=TOP)
        btn_expert.pack(side=TOP)

    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")
        self.modele.pion.en_vie = True
        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.parent.recibler_tout()

        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        self.canevas.create_rectangle(0, 0, 550, 550, fill="black")
        self.canevas.create_rectangle(50, 50, 500, 500, fill="white")

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))

        for i in self.modele.sentinelles:
            self.canevas.create_rectangle(i.x, i.y, i.x + i.largeur, i.y + i.hauteur, fill="blue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))

    def afficher_score(self):
        self.win_score = Tk()
        self.win_score.title("Scores")
        self.canevas_score = Text(self.win_score, width=30, height=10)
        self.canevas_score.pack()

        self.canevas_score.insert(END, "SCORES: \n\n")
        for i in self.parent.high_score:
            if i > 1:
                self.canevas_score.insert(END, f"{i:.2f} secondes\n")
            else:
                self.canevas_score.insert(END, f"{i:.2f} seconde\n")

    def niveau_debutant(self):
        self.modele.vitesse = 2
        self.modele.creer_sentinelles()
    def niveau_intermediaire(self):
        self.modele.vitesse = 6
        self.modele.creer_sentinelles()
    def niveau_expert(self):
        self.modele.vitesse = 8
        self.modele.creer_sentinelles()

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 550
        self.hauteur = 550
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.vitesse = 2
        self.sentinelles_jettable = []
        self.creer_sentinelles()

    def creer_sentinelles(self):
        self.sentinelles = []
        self.sentinelles.append(Sentinelle(self, 100, 100, 60, 60, 1, self.vitesse))
        self.sentinelles.append(Sentinelle(self, 300, 85, 60, 50, 2, self.vitesse))
        self.sentinelles.append(Sentinelle(self, 85, 350, 30, 60, 3, self.vitesse))
        self.sentinelles.append(Sentinelle(self, 355, 340, 100, 20, 4, self.vitesse))

    def recibler_sentinelles(self):
        self.sentinelles_jettable = self.sentinelles
        self.sentinelles = []

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def avancer_sentinelles(self):
        for i in self.sentinelles:
            i.avancer_sentinelles()

    def verifier_collision_cadre(self):
        for i in self.sentinelles:
            i.verifier_collision_cadre()

class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.x = self.parent.largeur / 2
        self.y = self.parent.largeur / 2
        self.demitaille = 10
        self.en_vie = True

    def recibler(self, x, y):
        self.x = x
        self.y = y
        self.tester_collision()
        self.verifier_collision_cadre()

    def tester_collision(self):
        x1 = self.x - self.demitaille
        y1 = self.y - self.demitaille
        x2 = self.x + self.demitaille
        y2 = self.y + self.demitaille

        for i in self.parent.sentinelles:
            if (x2 > i.x and x1 < i.x + i.largeur) and (y2 > i.y and y1 < i.y + i.hauteur):
                self.en_vie = False

    def verifier_collision_cadre(self):
        if self.x >= 500 - self.demitaille or self.x <= 50 + self.demitaille or self.y >= 500 - self.demitaille or self.y <= 50 + self.demitaille:
            self.en_vie = False


class Sentinelle():
    def __init__(self, parent, x, y, hauteur, largeur, id, vitesse):
        self.parent = parent
        self.x = x
        self.y = y
        self.hauteur = hauteur
        self.largeur = largeur
        self.demitaille_largeur = self.largeur / 2
        self.demitaille_hauteur = self.hauteur / 2
        self.vitesse = vitesse
        self.directionX = 1
        self.directionY = 1
        self.id = id

    def avancer_sentinelles(self):
        if self.id == 1:
            self.x = self.x + self.vitesse * self.directionX
            self.y = self.y + self.vitesse * self.directionY
        elif self.id == 2:
            self.x = self.x - self.vitesse * self.directionX
            self.y = self.y + self.vitesse * self.directionY
        elif self.id == 3:
            self.x = self.x + self.vitesse * self.directionX
            self.y = self.y - self.vitesse * self.directionY
        elif self.id == 4:
            self.x = self.x - self.vitesse * self.directionX
            self.y = self.y - self.vitesse * self.directionY

    def verifier_collision_cadre(self):
        if self.x + self.largeur >= 550 or self.x <= 0:
            if self.directionX != -1:
                self.directionX = -1
            else:
                self.directionX = 1
        if self.y + self.hauteur >= 550 or self.y <= 0:
            if self.directionY != -1:
                self.directionY = -1
            else:
                self.directionY = 1

class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.high_score = []
        self.en_jeu = False
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()

        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if not self.en_jeu:
            self.en_jeu = True
            self.jouer_partie2()

    def jouer_partie2(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.modele.avancer_sentinelles()
            self.modele.verifier_collision_cadre()
            self.modele.pion.tester_collision()
            if not self.modele.pion.en_vie:
                self.high_score.append(self.modele.duree)
                self.partie_en_cours = 0
                self.vue.arreter_jeu(self)
        self.vue.afficher_partie()
        self.vue.root.after(40, self.jouer_partie2)

    def recibler_tout(self):
        self.modele.pion.recibler(self.modele.largeur / 2, self.modele.largeur / 2)
        self.modele.recibler_sentinelles()
        self.modele.creer_sentinelles()

if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
