from tkinter import *
import time

class Vue:
    def __init__(self, parent):
        self.root = Tk()
        self.parent = parent
        self.modele = self.parent.modele
        self.root.title("Carre Rouge, alpha_0.3")
        self.cadres = self.creer_interface()

    def creer_interface(self):
        #affichage du temps
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()

        #Espace de jeu
        self.carre_noir = Frame(self.root, width=self.parent.modele.width, height=self.parent.modele.height, bg="black")
        self.carre_blanc = Canvas(self.carre_noir, width=self.parent.modele.width_interne,
                                  height=self.parent.modele.height_interne, bg="white")
        self.carre_blanc.pack(padx=(self.parent.modele.width - self.parent.modele.width_interne)/2,  pady=(self.parent.modele.height - self.parent.modele.height_interne)/2)
        self.carre_blanc.tag_bind("carre", "<Button>", self.debuter_partie)

        #Affichage
        self.cadre_info.pack(expand=1, fill=X)
        self.carre_noir.pack(expand=1, fill=X)
        self.afficher_partie()

    def debuter_partie(self, evt):
        self.carre_blanc.tag_unbind("carre", "<Button>")
        self.carre_blanc.bind("<B1-Motion>", self.recibler_pion)
        self.carre_blanc.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.carre_blanc.tag_bind("carre", "<Button>", self.debuter_partie)
        self.carre_blanc.unbind("<B1-Motion>")
        self.carre_blanc.unbind("<ButtonRelease>")
        # if evt is None:
        #self.afficher_score()

    def afficher_partie(self):
        self.carre_blanc.delete(ALL)

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.carre_blanc.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("carre",))

        for i in self.modele.sentinelle:
            x1 = i.x1
            y1 = i.y1
            x2 = i.x2
            y2 = i.y2

            self.carre_blanc.create_rectangle(x1, y1, x2, y2, fill= "blue", tags=("sentinelle"))

        self.var_duree.set(str(round(self.modele.duree, 2)))

    def afficher_score(self):
        print("Je suis valide chummy")
        strVar = self.parent.modele.duree
        self.carre_blanc.create_rectangle(50, 50, 400, 400, fill="Lightblue", tags="fin")
        self.carre_blanc.create_text(200, 100, text="Votre Score est : ", fill="black",  font=('Helvetica 15 bold'))
        self.carre_blanc.create_text(200, 150, text=strVar, fill="black", font=('Helvetica 15 bold'))
        self.parent.modele.pion.x = self.parent.modele.width / 3
        self.parent.modele.pion.y = self.parent.modele.height / 2
        self.carre_blanc.tag_bind("fin", "<Button>", self.debuter_partie)


    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)


class Jeu:
    def __init__(self, parent):
        self.width = 550
        self.height = 550
        self.width_interne = 450
        self.height_interne = 450
        self.parent = parent
        self.debut = None
        self.duree = 0
        self.pion = Carre(self)
        self.sentinelle = []
        self.partie = None

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def creer_sentinelle(self):
        self.sentinelle.append(Sentinelle(self, 300, 280, 340, 380))
        self.sentinelle.append(Sentinelle(self, 320, 20, 340, 220))
        self.sentinelle.append(Sentinelle(self, 30, 50, 80, 150))
        self.sentinelle.append(Sentinelle(self, 50, 340, 180, 400))

    def deplacement(self):
        self.vitesse = 0

        if self.parent.partie_en_cours:
            self.vitesse = 5
            self.vitesse += self.duree/2

            for i in self.sentinelle:
                sent = i
                sentx1 = sent.x1
                senty1 = sent.y1
                sentx2 = sent.x2
                senty2 = sent.y2

                if sentx1 < 0:
                    i.inverse_x = False

                elif sentx2 > self.width_interne:
                    i.inverse_x = True

                elif senty1 < 0:
                    i.inverse_y = False

                elif senty2 > self.height_interne:
                    i.inverse_y = True

                if i.inverse_x:
                    i.x1 -= self.vitesse
                    i.x2 -= self.vitesse
                elif not i.inverse_x:
                    i.x1 += self.vitesse
                    i.x2 += self.vitesse

                if i.inverse_y:
                    i.y1 -= self.vitesse
                    i.y2 -= self.vitesse
                elif not i.inverse_y:
                    i.y1 += self.vitesse
                    i.y2 += self.vitesse

    def fin_partie(self):
        self.parent.fin_partie()

class Score:
    def __init__(self):
        self.temps = 0
        self.nom = ""

class Sentinelle:
    def __init__(self, parent, x1, y1, x2, y2):
        self.parent = parent
        self.taille = 0
        self.couleur = ""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.inverse_x = True
        self.inverse_y = True

class Carre:
    def __init__(self, parent):
        self.parent = parent
        self.x = self.parent.width / 2
        self.y = self.parent.width / 2
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

        for i in self.parent.sentinelle:

            sentx1 = i.x1
            senty1 = i.y1
            sentx2 = i.x2
            senty2 = i.y2

            if (x2 > sentx1 and x1 < sentx2) and (y2 > senty1 and y1 < senty2):
                print("collision avec ", i, self.parent.duree)
                self.parent.fin_partie()

        if (x2 > self.parent.width_interne) or (x1 < 0) or (y2 > self.parent.height_interne) or (y1 < 0):
            print("collision avec mur", self.parent.duree)
            self.parent.fin_partie()

class Controleur:
    def __init__(self):
        self.modele = Jeu(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def recibler_pion(self, x, y):
        self.modele.recibler_pion(x, y)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.modele.sentinelle.clear()
        self.modele.creer_sentinelle()
        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.modele.deplacement()
            self.modele.pion.tester_collision()
            self.vue.root.after(40, self.jouer_partie)
        self.vue.afficher_partie()

    def fin_partie(self):
        self.vue.afficher_score()
        self.vue.arreter_jeu(evt) # je sais qu'il y a une erreur ici, mais si je ne la laisse pas là, mon menu de fin ne s'affiche pas
        #self.partie_en_cours = 0

if __name__ == '__main__':
    c = Controleur()