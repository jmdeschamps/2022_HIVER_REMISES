## -*- Encoding: UTF-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *

from RTS_client_B41.vue_jeu import Jeu
from RTS_client_B41.vue_lobby import Lobby
from RTS_client_B41.vue_menu_principal import MenuPrincipal

from RTS_main_2022 import Controleur
from chargeurdimages import *

class Vue:
    def __init__(self, controleur, urlserveur: str, monnom: str, testdispo: str):
        self.controleur = controleur
        self.root = Tk()
        self.root.title("Je suis " + monnom)
        self.monnom = monnom

        # attributs
        self.cadrechaton = 0
        self.textchat = ""
        self.infohud = {}

        self.cadreactif = None

        # cadre principal de l'application
        self.cadreapp = Frame(self.root, width=500, height=400, bg="red")
        self.cadreapp.pack(expand=1, fill=BOTH)

        # self.root.protocol("WM_DELETE_WINDOW", self.demanderabandon)
        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None

        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteuractif = None

        self.gifs = chargergifs()

        self.menu_principal = MenuPrincipal(self, urlserveur, monnom, testdispo)
        self.lobby = Lobby(self)
        self.jeu = Jeu(self)

        self.changer_cadre("splash")

    def update(self):
        self.root.update()

    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre: str):
        cadre = {
            "splash": self.menu_principal,
            "lobby": self.lobby,
            "jeu": self.jeu
        }[nomcadre]

        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif = cadre
        self.cadreactif.pack(expand=1, fill=BOTH)



    ###  FONCTIONS POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self, etat):
        self.menu_principal.update_splash(etat)

    ##### FONCTION DU LOBBY #############
    def update_lobby(self, dico):
        self.lobby.update_lobby(dico)

    def initialiser_avec_modele(self, modele):
        self.jeu.initialiser_avec_modele(modele)


    def afficher_batiment(self, joueur, batiment):
        self.jeu.afficher_batiment(joueur, batiment)

    def afficher_jeu(self):
        self.jeu.afficher_jeu()

    def centrer_village(self):
        self.jeu.centrer_village()
