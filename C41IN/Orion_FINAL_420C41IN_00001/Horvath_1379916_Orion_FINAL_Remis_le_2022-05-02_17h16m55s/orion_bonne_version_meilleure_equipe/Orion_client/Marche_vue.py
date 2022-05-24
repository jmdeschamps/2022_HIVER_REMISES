from Orion_vue import *
from Marche import *
class Marche_vue():
    def __init__(self, parent,controleur):
        self.parent = parent
        self.controleur = controleur
        self.taille_police = 7

    def ouvrir_marche(self):
        self.joueurs = self.parent.modele.joueurs.copy()
        self.marche_root = Toplevel(self.parent.root,bg="#333333")
        self.marche_root.geometry("1100x500+550+250")
        self.marche_root.title("Marche")
        self.frame = Frame(self.marche_root,bg="#333333")
        Label(self.frame, text="Ressource Offerte", font=self.taille_police).grid(row=0, column=5, sticky=W, ipadx=15, ipady=15, pady=5,
                                                               padx=5)
        Label(self.frame, text="Quantite Offerte", font=self.taille_police).grid(row=0, column=20, sticky=W, ipadx=15, ipady=15, pady=5,
                                                              padx=5)
        Label(self.frame, text="Ressource Demandé", font=self.taille_police).grid(row=0, column=30, sticky=W, ipadx=15, ipady=15, pady=5,
                                                               padx=5)
        Label(self.frame, text="Quantité Demandé", font=self.taille_police).grid(row=0, column=40, sticky=W, ipadx=15, ipady=15, pady=5,
                                                              padx=5)
        Label(self.frame, text="Joueur", font=self.taille_police).grid(row=0, column=50, sticky=W, ipadx=15, ipady=15, pady=5, padx=5)
        self.marche = self.parent.modele.marche
        self.input_ressource_offerte = Text(self.frame, height=1, width=1)
        self.input_ressource_offerte.grid(row=len(self.parent.modele.marche.liste_echange) + 1, column=5, sticky=W, ipadx=38,
                                          ipady=2, pady=2, padx=20)
        self.input_quantite_offerte = Text(self.frame, height=1, width=1)
        self.input_quantite_offerte.grid(row=len(self.parent.modele.marche.liste_echange) + 1, column=20, sticky=W, ipadx=20,
                                         ipady=2, pady=2, padx=22)
        self.input_ressource_demande = Text(self.frame, height=1, width=1)
        self.input_ressource_demande.grid(row=len(self.parent.modele.marche.liste_echange) + 1, column=30, sticky=W, ipadx=38,
                                          ipady=2, pady=2, padx=20)
        self.input_quantite_demande = Text(self.frame, height=1, width=1)
        self.input_quantite_demande.grid(row=len(self.parent.modele.marche.liste_echange) + 1, column=40, sticky=W, ipadx=20,
                                         ipady=2, pady=2, padx=20)
        Label(self.frame, text=self.parent.mon_nom, font=self.taille_police).grid(row=len(self.parent.modele.marche.liste_echange) + 1, column=50,
                                                        sticky=W, ipadx=15, ipady=15, pady=5, padx=5)
        self.string_var_info_echange = StringVar()
        self.string_var_info_echange.set("Entrez les informations pour l'échange")
        self.label_info_echange = Label(self.frame, textvariable=self.string_var_info_echange).grid(
            row=len(self.parent.modele.marche.liste_echange) + 3, column=30, sticky=W,
            ipadx=15, ipady=15, pady=5, padx=5)
        Button(self.frame, text="ajouter un échange", command=self.ajouter_offre_marche, font=self.taille_police).grid(
            row=len(self.parent.modele.marche.liste_echange) + 2,
            column=0, sticky=W, ipadx=15, ipady=20, pady=20, padx=15)
        compteur_row = 1
        for echange in self.marche.liste_echange:
            if echange.nom == self.parent.mon_nom:
                self.texte_echange = str(compteur_row)+"-retirer"
                temp = Button(self.frame, text=self.texte_echange,command=self.retirer_offre_marche, font=self.taille_police)
                data=[echange,temp.cget('text')]
                temp.grid(row=compteur_row, column=0, sticky=W, ipadx=5, ipady=5, pady=5, padx=5)
            else:
                self.texte_echange = str(compteur_row) + "-accepter"
                temp = Button(self.frame, text=self.texte_echange,command=self.accepter_offre_marche, font=self.taille_police)
                temp.grid(row=compteur_row, column=0, sticky=W, ipadx=5, ipady=5, pady=5, padx=5)
            Label(self.frame, text=str(echange.ressource_offerte), font=self.taille_police).grid(row=compteur_row, column=5, sticky=W,
                                                                              ipadx=15, ipady=15, pady=5, padx=5)
            Label(self.frame, text=str(echange.quantite_offerte), font=self.taille_police).grid(row=compteur_row, column=20, sticky=W,
                                                                             ipadx=15,
                                                                             ipady=15, pady=5, padx=5)
            Label(self.frame, text=str(echange.ressource_demande), font=self.taille_police).grid(row=compteur_row, column=30, sticky=W,
                                                                              ipadx=15, ipady=15, pady=5, padx=5)
            Label(self.frame, text=str(echange.quantite_demande), font=self.taille_police).grid(row=compteur_row, column=40, sticky=W,
                                                                             ipadx=15,
                                                                             ipady=15, pady=5, padx=5)
            Label(self.frame, text=echange.nom, font=self.taille_police).grid(row=compteur_row, column=50, sticky=W, ipadx=15, ipady=15,
                                                           pady=5,
                                                           padx=5)
            compteur_row += 1
        self.frame.pack()



    def accepter_offre_marche(self):
        id = int(self.texte_echange[0:1])
        ressource_offerte = self.marche.liste_echange[id - 1].ressource_offerte
        quantite_offerte = self.marche.liste_echange[id - 1].quantite_offerte
        ressource_demande = self.marche.liste_echange[id - 1].ressource_demande
        quantite_demande = self.marche.liste_echange[id - 1].quantite_demande
        nom_vendeur = self.marche.liste_echange[id-1].nom
        action = [self.parent.mon_nom, "accepter_echange",
                  [ressource_offerte, quantite_offerte,ressource_demande,quantite_demande,id,nom_vendeur]]
        self.controleur.actionsrequises.append(action)


    def retirer_offre_marche(self):
        id = int(self.texte_echange[0:1])
        ressource_offerte = self.marche.liste_echange[id-1].ressource_offerte
        quantite_offerte = self.marche.liste_echange[id-1].quantite_offerte
        action = [self.parent.mon_nom, "retirer_echange",
                  [ressource_offerte, quantite_offerte,id]]
        self.controleur.actionsrequises.append(action)


    def ajouter_offre_marche(self):
        quantite_joueur = 0
        liste_ressource = ["nourriture", "cuivre", "titanium", 'eau', "fer", "energie"]
        try:
            quantite_offerte = int(self.input_quantite_offerte.get("1.0", END)[:-1].lower())
            quantite_demande = int(self.input_quantite_demande.get("1.0", END)[:-1].lower())
        except:
            self.string_var_info_echange.set("Veuillez entrer des chiffres comme quantité")
            quantite_offerte = 0
            quantite_demande = 0
        ressource_offerte = self.input_ressource_offerte.get("1.0", END)[:-1].lower()
        ressource_demande = self.input_ressource_demande.get("1.0", END)[:-1].lower()

        if quantite_offerte > quantite_joueur:
            self.string_var_info_echange.set("Vous n'avez pas assez de ressource")
            self.string_var_info_echange.set("Votre echange est ajouter")
            action =[self.parent.mon_nom,"ajouter_echange",[ressource_offerte,quantite_offerte,ressource_demande,quantite_demande]]
            self.controleur.actionsrequises.append(action)





