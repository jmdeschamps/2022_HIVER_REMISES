from Pillow import *
from Orion_vue import *
from tkinter import *

class Senat_vue():
    def __init__(self, parent):
        self.parent = parent

    def ouvrir_senat(self):
        self.historique_lois = []  # aller chercher liste des lois votées.
        senat_root = Toplevel(self.parent.root,bg="#e1ccad")
        senat_root.title('Sénat')

        senat_root.geometry("500x500+1000+130")

        frame_senat = Frame(senat_root,borderwidth=2, relief="ridge",bg="#333333")
        compteur_row = 1

        Label(frame_senat, text="PROCHAINE LOI VOTÉE SERA PROPOSÉE PAR : ").grid(row=5, column=5, sticky=W, ipadx=15,
                                                                                 ipady=15,
                                                                                 pady=5, padx=5)
        self.joueur_vote = Label(frame_senat, text=" ").grid(row=5, column=15, sticky=W, ipadx=15, ipady=15,
                                                             pady=20, padx=5)
        frame_historique_lois = Frame(senat_root,borderwidth=2, relief="ridge",bg="#333333")

        Label(frame_historique_lois, text="LOIS VOTÉS").grid(row=10, column=5, sticky=W, ipadx=15,
                                                             ipady=15,
                                                             pady=15, padx=5)
        Label(frame_historique_lois, text="Description : ").grid(row=10, column=10, sticky=W,
                                                                 ipadx=15,
                                                                 ipady=15,
                                                                 pady=5, padx=5)
        for loi in historique_lois:
            Label(frame_historique_lois, text=str(loi.nom)).grid(row=compteur_row, column=5, sticky=W,
                                                                 ipadx=15, ipady=15, pady=5, padx=5)
            Label(frame_historique_lois, text=str(loi.description)).grid(row=compteur_row, column=10, sticky=W,
                                                                         ipadx=15,
                                                                         ipady=15, pady=5, padx=5)
            compteur_row += 1

        frame_senat.pack(fill="x")
        frame_historique_lois.pack(fill="x")

