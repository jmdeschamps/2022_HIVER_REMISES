import tkinter.messagebox
from tkinter import *
from tkinter import simpledialog
import time
import re


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, Vers1.0")
        self.creer_interface()

    def creer_interface(self):
        self.cadre_info = Frame(self.root, bg="#9FE2BF")
        self.cadre_menu = Frame(self.root, bg="#9FE2BF")

        label_instructions = Label(self.cadre_menu, bg="#9FE2BF", text="1. Cliquez et tenez le carré rouge;\n"
                                                                     "2. Évitez les Sentinelles;\n"
                                                                     "3. Gagnez la gloire.\n")
        label_score = Label(self.cadre_menu, bg="#9FE2BF")
        btnScore = Button(label_score, text="Meilleur score", command=self.afficher_meilleur_score)
        self.var_duree = StringVar()
        self.best_time_vue = StringVar()
        self.best_time_entree = StringVar()
        label_duree = Label(self.cadre_info, text=" 0 ", textvariable=self.var_duree, bg="#cdf0e1", font=('Times',24), borderwidth=1, relief="solid")
        label_temps = Label(self.cadre_info, text="Temps:", bg="#9FE2BF" )

        label_duree_record = Label(self.cadre_info, text=" 0 ", textvariable=self.best_time_vue, bg="#cdf0e1", font=('Times',18), fg= "darkred", borderwidth=1, relief="solid")
        label_temps_record = Label(self.cadre_info, text="\nTemps record: ", bg="#9FE2BF" )
        label_record_entree = Label(self.cadre_info, text="-", textvariable=self.best_time_entree, bg="#9FE2BF" , font=('Times',14, 'bold'))

        label_temps.pack()
        label_duree.pack()


        label_temps_record.pack(side=TOP)
        label_duree_record.pack(side=TOP)

        label_record_entree.pack()

        # le canevas de jeu
        self.canevas = Canvas(self.root, width=450, height=450, bg="white")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)

        # visualiser
        self.cadre_info.pack(expand=1, fill=X)
        self.canevas.pack()
        self.cadre_menu.pack(expand=1, fill=X)

        label_instructions.pack()
        label_score.pack()
        btnScore.pack()

        self.afficher_partie()

    def afficher_meilleur_score(self):
        best_time = ""
        with open("scores.txt", "r") as file1:
            best_time = file1.read()
        self.best_time_entree.set(str(best_time))

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

        self.modele.pion.x = 225
        self.modele.pion.y = 225
        self.modele.sentinelles.clear()
        self.modele.creer_sentinelles()

    def game_over(self):
        self.afficher_partie()

    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def afficher_partie(self):
        self.canevas.delete(ALL)

        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="darkred", tags=("pion",))

        #AFFICHER BORDURE NOIRE
        x = self.modele.poteau.x
        y = self.modele.poteau.y
        d = self.modele.poteau.demitaille
        self.canevas.create_rectangle(0 - d, 0 - d, 500 + d, 0 + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(x - d, y - d, x + d, 500 + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(0 - d, 450 - d, 500 + d, 500 + d,
                                      fill="black", tags=("poteau",))
        self.canevas.create_rectangle(450 - d, 450 - d, 500 + d, 0 + d,
                                      fill="black", tags=("poteau",))

        #AFFICHER SENTINELLES
        for i in self.modele.sentinelles:
            x = i.x
            y = i.y
            d1 = i.dt1
            d2 = i.dt2
            self.canevas.create_rectangle(x - d1, y - d2, x + d1, y + d2,
                                          fill="darkblue", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))
        self.best_time_vue.set(str(round(self.modele.best_time, 2)))


class Modele():
    def __init__(self, parent):
        self.parent = parent

        self.largeur = 450
        self.hauteur = 450
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.poteau = Cadre(self)
        self.sentinelles = []
        self.creer_sentinelles()
        self.determine_best_time()

    def recibler_pion(self, x, y):
        self.pion.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def creer_sentinelles(self):
        self.sentinelles.append(Sentinelles(self, 100, 100, 30, 30, 5, -5))
        self.sentinelles.append(Sentinelles(self, 300, 85, 30, 25, -5, -5))
        self.sentinelles.append(Sentinelles(self, 85, 350, 15, 30, 5, 5))
        self.sentinelles.append(Sentinelles(self, 350, 340, 50, 10, -5, 5))

    def determine_best_time(self):
        with open("scores.txt", "r") as file1:
            best_time = file1.read()
        matches = re.findall("[+-]?\d+\.\d+", best_time)
        self.best_time = float(matches[0])
        return self.best_time

    def reset_partie_pop_up(self):
        best_time = ""
        with open("scores.txt", "r") as file1:
            best_time = file1.read()


        matches = re.findall("[+-]?\d+\.\d+", best_time)
        self.best_time = float(matches[0])

        answer1 = tkinter.simpledialog.askstring("Score", "Quel est ton nom?",
                                                 parent=self.parent.vue.root)
        if answer1 is not None:
            nice_try = answer1 + " t'as survecu " + str(round(self.duree, 2)) + ' secondes, bel essai!'
            self.parent.vue.best_time_entree.set(str(nice_try))


        if self.duree > self.best_time:
            self.best_time = self.duree
            self.parent.vue.best_time_entree.set(str("NOUVEAU RECORD!"))
            with open("scores.txt", "w") as file1:
                nouveau_record = answer1 + " a survecu " + str(round(self.duree, 2)) + ' secondes!'
                file1.write(nouveau_record)

        tkinter.messagebox.showinfo('Game over...', 'Pèse sur le carré rouge pour recommencer...',
                                    parent=self.parent.vue.root)

    def reset_partie(self):

        self.pion.x = 225
        self.pion.y = 225
        self.sentinelles.clear()
        self.creer_sentinelles()


# CADRE NOIR
class Cadre():
    def __init__(self, parent):
        self.parent = parent
        self.x = 0
        self.y = 0
        self.demitaille = 50


class Pion():
    def __init__(self, parent):
        self.parent = parent
        self.x = 225
        self.y = 225
        self.demitaille = 20
        self.isCollision = False

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
        pot_top_x1 = pot.x - pot.demitaille
        pot_top_y1 = pot.y - pot.demitaille
        pot_top_x2 = 500 + pot.demitaille
        pot_top_y2 = pot.y + pot.demitaille

        pot_bottom_x1 = pot.x - pot.demitaille
        pot_bottom_y1 = 450 - pot.demitaille
        pot_bottom_x2 = 500 + pot.demitaille
        pot_bottom_y2 = 500 + pot.demitaille

        pot_left_x1 = pot.x - pot.demitaille
        pot_left_y1 = pot.y - pot.demitaille
        pot_left_x2 = pot.x + pot.demitaille
        pot_left_y2 = 500 + pot.demitaille

        pot_right_x1 = 450 - pot.demitaille
        pot_right_y1 = pot.y - pot.demitaille
        pot_right_x2 = 500 + pot.demitaille
        pot_right_y2 = 500 + pot.demitaille

        for i in self.parent.sentinelles:
            i_x1 = i.x - i.dt1
            i_y1 = i.y - i.dt2
            i_x2 = i.x + i.dt1
            i_y2 = i.y + i.dt2

            if (x2 > i_x1 and x1 < i_x2) and (y2 > i_y1 and y1 < i_y2):
                self.isCollision = True

        if (x2 > pot_top_x1 and x1 < pot_top_x2) and (y2 > pot_top_y1 and y1 < pot_top_y2):
            self.isCollision = True

        if (x2 > pot_bottom_x1 and x1 < pot_bottom_x2) and (y2 > pot_bottom_y1 and y1 < pot_bottom_y2):
            self.isCollision = True

        if (x2 > pot_left_x1 and x1 < pot_left_x2) and (y2 > pot_left_y1 and y1 < pot_left_y2):
            self.isCollision = True

        if (x2 > pot_right_x1 and x1 < pot_right_x2) and (y2 > pot_right_y1 and y1 < pot_right_y2):
            self.isCollision = True


class Sentinelles():
    def __init__(self, parent, x, y, dt1, dt2, vitesse_x, vitesse_y):
        self.parent = parent
        self.x = x
        self.y = y
        self.dt1 = dt1
        self.dt2 = dt2
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y

    def move(self):

        self.x += self.vitesse_x
        self.y -= self.vitesse_y

        self.x1 = self.x - self.dt1
        self.y1 = self.y - self.dt2
        self.x2 = self.x + self.dt1
        self.y2 = self.y + self.dt2

        if self.x1 <= 0 or self.x2 >= 450:
            self.vitesse_x *= -1
        if self.y1 <= 0 or self.y2 >= 450:
            self.vitesse_y *= -1

    def incrementer_vitesse(self):
        absX = abs(self.vitesse_x)
        absY = abs(self.vitesse_y)

        absX += 0.01
        absY += 0.01

        if self.vitesse_x < 0:
            self.vitesse_x = absX * -1
        else:
            self.vitesse_x = absX

        if self.vitesse_y < 0:
            self.vitesse_y = absY * -1
        else:
            self.vitesse_y = absY


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
        self.modele.pion.isCollision = False
        self.jouer_partie()

    def reset_partie(self):

        self.modele.reset_partie()

    def reset_partie_pop_up(self):
        self.modele.reset_partie_pop_up()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            for i in self.modele.sentinelles:
                i.move()
                i.incrementer_vitesse()

        self.vue.afficher_partie()

        if (self.modele.pion.isCollision):
            self.reset_partie_pop_up()
            self.reset_partie()
            self.modele.pion.isCollision = False
            self.vue.arreter_jeu(self)
            self.partie_en_cours = 0

        if self.partie_en_cours:
            self.vue.root.after(40, self.jouer_partie)


if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")
