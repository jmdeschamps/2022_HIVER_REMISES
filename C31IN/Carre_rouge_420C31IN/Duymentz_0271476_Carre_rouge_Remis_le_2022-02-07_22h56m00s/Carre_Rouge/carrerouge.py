from tkinter import *
from tkinter import messagebox
import time


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.cadres = self.creer_interface()
        self.canevas.config(cursor="hand2")


    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree, width=24, cursor="hand1")
        label_duree.pack(side=RIGHT)

        # le canevas de jeu et sa bordure bleue
        self.cadre_canevas = Frame(self.root, width=self.modele.largeur, height=self.modele.hauteur,
                                   bg="lightblue", bd=12)
        self.canevas = Canvas(self.cadre_canevas, width=self.modele.largeur, height=self.modele.hauteur,
                              bg="white", highlightthickness=0)
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)

        # visualiser
        self.cadre_info.pack(fill=X)
        self.cadre_canevas.pack()
        self.canevas.pack()

        self.afficher_partie()              # le MAINLOOP a pas encore été créé; cet appel précéde le tick et arrive juste 1 fois

    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")     #Dès que partie débute, on unbind la handler fct
        self.canevas.bind("<B1-Motion>", self.recibler_pion)    #puis on bind sur motion (sous-entendu onhold)
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)  #puis arreter onrelease, on spécifie pas de tag ?
        self.parent.debuter_partie()

    def arreter_jeu(self, evt):
        self.parent.partie_en_cours = 0
        self.recibler_pion(evt)
        self.recibler_sentinelle(evt)
        messagebox.showinfo("Fin de partie", self.parent.modele.duree)

        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)  #rebind pour debuter, unbind etc.
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")


    def recibler_pion(self, evt):
        if self.parent.partie_en_cours:
            pionx = evt.x
            piony = evt.y
        else:
            pionx = self.parent.modele.largeur / 2
            piony = self.parent.modele.largeur / 2
        self.parent.recibler_pion(pionx, piony, evt)

    def recibler_sentinelle(self, evt):
        sentinellex = 50
        sentinelley = 100
        self.parent.recibler_sentinelle(sentinellex, sentinelley, evt)

    def afficher_partie(self):
        self.canevas.delete(ALL)
        x = self.modele.pion.x
        y = self.modele.pion.y
#########   Curseur style
        if ((self.root.winfo_pointerx() <= (x + self.root.winfo_rootx() + 12 + self.parent.modele.pion.demitaille)) and
            (self.root.winfo_pointerx() >= (x + self.root.winfo_rootx() + 12 - self.parent.modele.pion.demitaille))):
                if(((self.root.winfo_pointery() > (y + self.root.winfo_rootx() + 56 + self.parent.modele.pion.demitaille)) or
                    (self.root.winfo_pointery() < (y + self.root.winfo_rootx() + 56 - self.parent.modele.pion.demitaille)))):
                        self.canevas.config(cursor="hand2")
                else:
                    self.canevas.config(cursor="pirate")
        else:
            self.canevas.config(cursor="hand2")
#########
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion",))
        x = self.modele.sentinelle.x
        y = self.modele.sentinelle.y
        dx = self.modele.sentinelle.demitaillex
        dy = self.modele.sentinelle.demitailley
        self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                      fill="black", tags=("sentinelle",))

        self.var_duree.set(str(round(self.modele.duree, 2)))


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 400
        self.hauteur = 400
        self.debut = None
        self.duree = 0
        self.pion = Pion(self)
        self.sentinelle = Sentinelle(self)

    def recibler_pion(self, x, y, evt):
        self.pion.recibler(x, y)

    def recibler_sentinelle(self, x, y, evt):
        self.sentinelle.recibler(x, y)

    def jouer_tour(self):
        self.duree = time.time() - self.debut

    def bouger_sentinelle(self):
        self.sentinelle.bouger()


class Sentinelle():
    def __init__(self, parent):
        self.parent = parent
        self.x = 50
        self.y = 100
        self.demitaillex = 10
        self.demitailley = 20
        self.vitessex = 1
        self.vitessey = 3

    def bouger(self):
        self.x += self.vitessex
        self.y += self.vitessey
        self.tester_collision()

    def recibler(self, x, y):
        self.x = x
        self.y = y
        self.vitessex = 1
        self.vitessey = 3

    def tester_collision(self):
        x1 = self.x - self.demitaillex
        y1 = self.y - self.demitailley
        x2 = self.x + self.demitaillex
        y2 = self.y + self.demitailley

        if (x1 < 0):
            self.vitessex *= -1
        if (x2 > self.parent.largeur):
            self.vitessex *= -1
        if (y1 < 0):
            self.vitessey *= -1
        if (y2 > self.parent.hauteur):
            self.vitessey *= -1

        pion = self.parent.pion
        pionx1 = pion.x - pion.demitaille
        piony1 = pion.y - pion.demitaille
        pionx2 = pion.x + pion.demitaille
        piony2 = pion.y + pion.demitaille

        if (x2 > pionx1 and x1 < pionx2) and (y2 > piony1 and y1 < piony2):
            print("collision de sentinelle", self.parent.duree)
            self.parent.parent.partie_en_cours = 0
            self.recibler(50, 100)
            self.parent.pion.recibler(self.parent.largeur/2, self.parent.largeur/2)

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

        sent = self.parent.sentinelle
        sentx1 = sent.x - sent.demitaillex
        senty1 = sent.y - sent.demitailley
        sentx2 = sent.x + sent.demitaillex
        senty2 = sent.y + sent.demitailley

        if (x2 > sentx1 and x1 < sentx2) and (y2 > senty1 and y1 < senty2):
            print("collision à sentinelle", self.parent.duree)
            self.parent.sentinelle.recibler(50, 100)
            self.recibler(self.parent.largeur / 2, self.parent.largeur / 2)
            self.parent.parent.partie_en_cours = 0
        if ((x1 < 0) or (x2 > self.parent.largeur) or (y1 < 0) or (y2 > self.parent.hauteur)):
            print("sortie du root", self.parent.duree)
            self.parent.sentinelle.recibler(50, 100)
            self.recibler(self.parent.largeur/2, self.parent.largeur/2)
            self.parent.parent.partie_en_cours = 0



class Controleur():
    def __init__(self):
        self.partie_en_cours = 0
        self.modele = Modele(self)              # Fait l'INIT, après avoir fait le Modele
        self.vue = Vue(self)                    # Appelle la fct Tk() qui part l'engin graphique
        self.vue.root.mainloop()                #C'EST LÀ QUE LE PROGRAMME ROULE 1ERE FOIS, APRES INIT,
                                                # sur tout ce qui touche root, dont le after(le tick),
                                                # par jouer_partie, par débuter_partie, par vue.debuter_partie,
                                                # par canevas, par tag_bind <bouton> "pion", par create_rectangle tags="pion",
                                                # de afficher_partie de vue, qui est callée quand on fait la vue une première fois et
                                                # ensuite toujours dans le TICK, idès dans le after de jouer_partie qui
                                                # s'appelle par recurrence dans son after/tick après avoir appellé afficher_partie,
                                                # qui lui va toucher tout ce qui a rapport avec root et par qui ça a commencé init.
                                                # on sort du tick en mettant partie_en_cours à 0.

    def recibler_pion(self, x, y, evt):
        self.modele.recibler_pion(x, y, evt)

    def recibler_sentinelle(self, x, y, evt):
        self.modele.recibler_sentinelle(x, y, evt)

    def debuter_partie(self):
        self.modele.debut = time.time()
        self.partie_en_cours = 1
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.modele.bouger_sentinelle()
            self.vue.root.after(40, self.jouer_partie)              # LE TICK TRÈS IMPORTANT
        self.vue.afficher_partie()                                  # de le subordonner à variable partie_en_cours
                                                                    # if partie_cours pour pas qu'il continue
                                                                    # sans jamais recommencer et incrémente la vitesse tjrs...
if __name__ == '__main__':
    c = Controleur()
    print("L'application se termine")