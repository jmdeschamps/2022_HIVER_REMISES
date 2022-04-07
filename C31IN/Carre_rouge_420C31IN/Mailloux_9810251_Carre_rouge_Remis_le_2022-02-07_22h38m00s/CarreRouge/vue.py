import tkinter
from tkinter import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.cadres = self.creer_interface()

    def creer_interface(self):

        # Version avec grid

        # cadre HUD affichant la duree
        self.cadre_info = Frame(self.root, bg="lightgreen")
        self.var_duree = StringVar()
        label_titre = Label(self.cadre_info, text="Durée")
        label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        label_titre.grid(row=0, pady=10)
        label_duree.grid(row=1, pady=2)

        # le canevas de jeu noir
        self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)

        # la zone blanche délimitant le déplacement du carré rouge
        self.canevas.create_rectangle(self.modele.bordure, self.modele.bordure,
                                      self.modele.largeur-self.modele.bordure, self.modele.hauteur-self.modele.bordure, fill="white")

        label_scores = Label(self.cadre_info, text="High Scores")
        label_scores.grid(row=2, pady=10)
        self.liste_score = Text(self.cadre_info, width=20, height=20)
        self.liste_score.grid(row=3, pady=2)

        btnReplacer = Button(self.cadre_info, text="Replacer le jeu", command=self.parent.replacer_jeu)
        btnReplacer.grid(row=5, pady=5)

        btnQuitter = Button(self.cadre_info, text="Replacer le jeu", command=self.modele.sauver_scores)
        btnQuitter.grid(row=6, pady=5)

        # visualiser
        self.canevas.grid(row=0, column=0)
        self.cadre_info.grid(row=0, column=1, sticky='ns')
        self.scores_update()
        self.afficher_partie()

        # # cadre HUD affichant la duree
        # self.cadre_info = Frame(self.root, bg="lightgreen")
        # self.var_duree = StringVar()
        # label_duree = Label(self.cadre_info, text="0", textvariable=self.var_duree)
        # label_duree.pack()
        #
        # # le canevas de jeu noir
        # self.canevas = Canvas(self.root, width=self.modele.largeur, height=self.modele.hauteur, bg="black")
        # self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        #
        # # la zone blanche délimitant le déplacement du carré rouge
        # self.canevas.create_rectangle(self.modele.bordure, self.modele.bordure,
        #                               self.modele.largeur - self.modele.bordure,
        #                               self.modele.hauteur - self.modele.bordure, fill="white")
        #
        # self.btnReplacer = Button(self.root, text="Replacer le jeu", command=self.parent.replacer_jeu)
        # self.btnReplacer.pack(side=RIGHT)
        #
        # # visualiser
        # self.cadre_info.pack(expand=1, fill=X)
        # self.canevas.pack()
        # self.afficher_partie()

    # def fenetre_score(self):
    #     self.score = Frame(self.root, bg="lightgreen")


    def debuter_partie(self, evt):
        self.canevas.tag_unbind("pion", "<Button>")
        self.canevas.bind("<B1-Motion>", self.recibler_pion)
        #self.canevas.bind("<ButtonRelease>", self.arreter_jeu)
        self.parent.debuter_partie()

    def rebind(self):  #,evt retiré méthode renommée rebind
        self.parent.partie_en_cours = 0
        self.canevas.tag_bind("pion", "<Button>", self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        #self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self, evt):
        x = evt.x
        y = evt.y
        self.parent.recibler_pion(x, y)

    def scores_update(self):
        self.liste_score.delete("1.0", "end")
        self.modele.high_scores.sort(key = lambda x: x[1], reverse=True)
        for i in self.modele.high_scores:
            pad = len(i[0])
            score = str(i[1]).rjust(20-pad, ".")
            self.liste_score.insert(END, i[0] + score + "\n\n")

    def fenetre_high_score(self):
        nom_var = StringVar()

        def save_close():
                self.modele.high_scores.append([nom_var.get(), round(self.modele.duree, 2)])
                high_score_frame.grid_forget()

        high_score_frame = Frame(self.cadre_info, bg="lightgreen")
        texte1 = Label(high_score_frame, text="Vous êtes dans le top 10!")
        texte2 = Label(high_score_frame, text="Entrez votre nom")
        nom = Entry(high_score_frame, textvariable=nom_var)
        btnOK = Button(high_score_frame, text="Enregistrer", command=save_close)

        high_score_frame.grid(row=4)
        texte1.grid(row=0)
        texte2.grid(row=1)
        nom.grid(row=2)
        btnOK.grid(row=3)


    def afficher_partie(self):
        self.canevas.delete("dynamique")
        x = self.modele.pion.x
        y = self.modele.pion.y
        d = self.modele.pion.demitaille
        self.canevas.create_rectangle(x - d, y - d, x + d, y + d,
                                      fill="red", tags=("pion","dynamique"))
        for i in self.modele.liste_sentinelles:
            x = i.x
            y = i.y
            dx = i.dx
            dy = i.dy
            self.canevas.create_rectangle(x - dx, y - dy, x + dx, y + dy,
                                          fill="blue", tags=("sentinelle","dynamique"))
        self.var_duree.set(str(round(self.modele.duree, 2)))

    def deplacer_sentinelles(self, parent):
        self.parent.deplacer_sentinelles()






