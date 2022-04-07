from tkinter import *

class Jeu_Vue:
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.marge = 0
        self.aire_externe = None
        self.menu_jeu()

    def menu_jeu(self):
        self.menu = Frame(self.root,
                          width=self.parent.modele.largeur,
                          height=self.parent.modele.hauteur,
                          bg="black")
        self.menu.pack_propagate(0)
        self.menu.pack(expand=True, fill="both")
        self.bouton_debuter = Button(self.menu,
                                     width=20,
                                     height=5,
                                     font=10,
                                     bg="gray",
                                    text="Nouvelle Partie",
                                    command=self.parent.nouvelle_partie)
        self.bouton_debuter.place(in_=self.menu, anchor="center", relx=.5, rely=.5)

    def nouvelle_partie(self):
        if not self.parent.premiere_partie:
            self.aire_externe.destroy()
        self.menu.destroy()
        self.marge = self.parent.modele.partie.aire_de_jeu.marge
        self.afficher_aire_jeu()
        self.afficher_partie()

    def afficher_aire_jeu(self):
        self.aire_jeu = self.parent.modele.partie.aire_de_jeu
        ####### Création de l'aire de Jeu ###########
        self.aire_externe = Frame(self.root,
                                  width=self.aire_jeu.largeur_externe,
                                  height=self.aire_jeu.hauteur_externe,
                                  bg=self.aire_jeu.couleur_externe)
        self.aire_externe.pack_propagate(False)
        self.aire_externe.pack(expand=True, fill="both")
        ####### Création du Timer #######
        self.cadre_info = Frame(self.aire_externe, bg="black")
        self.var_duree = StringVar()
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_duree.pack()
        self.cadre_info.pack(expand=1, fill=X)
        ####### Création du Canevas #######
        self.canevas = Canvas(self.aire_externe,
                             width=self.aire_jeu.largeur_externe,
                             height=self.aire_jeu.hauteur_externe,
                             bg=self.aire_jeu.couleur_externe)
        self.canevas.pack()

    def afficher_partie(self):
        self.canevas.delete(ALL)
        self.canevas.create_rectangle(self.marge, self.marge,
                                     self.aire_jeu.largeur_interne+self.marge, self.aire_jeu.hauteur_interne+self.marge,
                                     fill=self.aire_jeu.couleur_interne)
        self.afficher_joueur()
        self.canevas.tag_bind("joueur", "<Button>", self.debuter_partie)
        self.afficher_sentinelles()
        self.var_duree.set(str(round(self.parent.modele.partie.duree, 2)))

    def afficher_joueur(self):
        joueur = self.parent.modele.partie.joueur
        l = joueur.largeur/2
        h = joueur.hauteur/2
        self.canevas.create_rectangle(joueur.x-l, joueur.y+h, joueur.x+l, joueur.y-h, tags=("joueur"), fill=joueur.couleur)

    def afficher_sentinelles(self):
        for i in self.parent.modele.partie.sentinellesListe:
            l=i.demitailleX
            h=i.demitailleY
            self.canevas.create_rectangle(i.x-l+self.marge, i.y+h+self.marge, i.x+l+self.marge, i.y-h+self.marge, fill=i.couleur)

    def debuter_partie(self,evt=None):
        self.canevas.tag_unbind("joueur", "<Button>")
        self.canevas.bind("<B1-Motion>", self.recibler_joueur)
        self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def arreter_jeu(self):
        self.parent.partie_en_cours = False
        self.canevas.tag_bind("joueur", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def recibler_joueur(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_joueur(x, y)

    def fin_partie(self):
        self.canevas.delete(ALL)
        self.cadre_info.destroy()
        self.score_zone = self.canevas.create_rectangle(self.marge,
                                                        self.marge,
                                                        self.aire_jeu.largeur_interne+self.marge,
                                                        self.aire_jeu.hauteur_interne+self.marge,
                                                        fill="black")
        self.score_text = Label(self.aire_externe,
                                bg="gray",
                                fg="white",
                                font=20,
                                text="Votre Score: " + str(round(self.parent.modele.partie.duree, 2)) + " secondes")
        self.score_text.place(x=self.aire_jeu.largeur_interne/2-self.marge, y=self.aire_jeu.hauteur_interne/2-self.marge)
        self.bouton_debuter = Button(self.aire_externe,
                                     width=20,
                                     height=5,
                                     font=10,
                                     bg="gray",
                                     text="Nouvelle Partie",
                                     command=self.parent.nouvelle_partie)
        self.bouton_debuter.place(in_=self.aire_externe, anchor="center", relx=.5, rely=.5)
