from tkinter import *
from tkinter.simpledialog import *


class MenuPrincipal:
    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def __init__(self, view, urlserveur: str, monnom: str, testdispo: str):
        self.view = view
        self.controleur = view.controleur
        self.cadresplash = Frame(view.cadreapp)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevassplash = Canvas(self.cadresplash, width=600, height=480, bg="royal blue")
        self.canevassplash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=testdispo, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14))
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, monnom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevassplash
        self.canevassplash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevassplash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevassplash.create_window(240, 250, window=self.urlsplash, width=200, height=30)
        self.canevassplash.create_window(420, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)

        # on place les autres boutons
        self.canevassplash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevassplash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevassplash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        ############ ## NOTES : ceci est un exemple pour ajouter des options au cadresplash
        # ## POUR CHOIX CIVILISATION, 4 OPTIONS
        # # LA VARIABLE DONT LA VALEUR CHANGERA AU FIL DES CLICK
        # self.valciv = StringVar(self.cadresplash, "1")
        # # LES 4 BTN RADIO
        # radciv1 = Radiobutton(text="Azteque", variable=self.valciv, value="Azteque")
        # radciv2 = Radiobutton(text="Congolaise", variable=self.valciv, value="Congolaise")
        # radciv3 = Radiobutton(text="Russe", variable=self.valciv, value="Russe")
        # radciv4 = Radiobutton(text="Maya", variable=self.valciv, value="Maya")
        # radciv5 = Radiobutton(text="Magyar", variable=self.valciv, value="Magyar")
        # # LE PLACEMENTS DES BTN RADIOS
        # self.canevassplash.create_window(220, 350, window=radciv1, width=180, height=30)
        # self.canevassplash.create_window(220, 380, window=radciv2, width=180, height=30)
        # self.canevassplash.create_window(220, 410, window=radciv3, width=180, height=30)
        # self.canevassplash.create_window(220, 440, window=radciv4, width=180, height=30)
        # self.canevassplash.create_window(220, 470, window=radciv5, width=180, height=30)
        # ## ##########    FIN de l'exemple des choix de civilisations

        ############# NOTE le bouton suivant permet de générer un Frame issu d'un autre module et l'intégrer à la vue directement
        # self.btncadretest = Button(text="Cadre test", font=("Arial", 9),  command=self.montrercadretest)
        # on place les autres boutons
        # self.canevassplash.create_window(120, 450, window=self.btncadretest, width=200, height=30)
        ##############

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.controleur.connecter_serveur(url_serveur)

    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="ERREUR - un probleme est survenu")

    def inscrire_joueur(self):
        nom = self.nomsplash.get()
        urljeu = self.urlsplash.get()
        self.controleur.inscrire_joueur(nom, urljeu)

    def creer_partie(self):
        nom = self.nomsplash.get()
        self.controleur.creer_partie(nom)

    def reset_partie(self):
        rep = self.controleur.reset_partie()

    def pack(self, expand, fill):
        self.cadresplash.pack(expand=1, fill=BOTH)

    def pack_forget(self):
        self.cadresplash.pack_forget()
