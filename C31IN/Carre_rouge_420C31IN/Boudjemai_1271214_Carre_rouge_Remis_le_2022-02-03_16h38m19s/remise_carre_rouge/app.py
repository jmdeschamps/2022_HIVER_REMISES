from tkinter import *
import time
from tkinter.font import BOLD
from tkinter import simpledialog, messagebox
from datetime import date

class Sentinelle:
    def __init__(self, id, largeur, hauteur, position_x, position_y, vitesse):
        self.id = id
        self.largeur = largeur
        self.hauteur = hauteur
        self.position_x = position_x
        self.position_y = position_y
        self.vitesse = vitesse
        self.direction_x_renversee = False
        self.direction_y_renversee = False

    def determine_sa_direction(self, cadre_largeur, cadre_hauteur):
        if self.position_x < cadre_largeur/2:
            if self.position_y < cadre_hauteur/2:
                self.direction_x_renversee = False
                self.direction_y_renversee = False
            else:
                self.direction_x_renversee = False
                self.direction_y_renversee = True
        elif self.position_x > cadre_largeur/2:
            if self.position_y < cadre_hauteur / 2:
                self.direction_x_renversee = True
                self.direction_y_renversee = False
            else:
                self.direction_x_renversee = True
                self.direction_y_renversee = True

    def se_deplace(self, cadre_largeur, cadre_hauteur):
        if self.position_x < cadre_largeur and not self.direction_x_renversee:
            if self.position_x > cadre_largeur - self.largeur:
                self.direction_x_renversee = True
            else:
                self.position_x += self.vitesse
        elif self.direction_x_renversee:
            if self.position_x < 0:
                self.direction_x_renversee = False
            else:
                self.position_x -= self.vitesse

        if self.position_y < cadre_hauteur and not self.direction_y_renversee:
            if self.position_y > cadre_hauteur - self.hauteur:
                self.direction_y_renversee = True
            else:
                self.position_y += self.vitesse
        elif self.direction_y_renversee:
            if self.position_y < 0:
                self.direction_y_renversee = False
            else:
                self.position_y -= self.vitesse

class Pion:
    def __init__(self):
        self.largeur = 40
        self.hauteur = 40
        self.position_x = 255
        self.position_y = 255

    def se_recible(self, position_x, position_y):
        self.position_x = position_x - self.largeur/2
        self.position_y = position_y - self.hauteur/2

class Partie:
    def __init__(self, jeu, numero_partie):
        self.jeu = jeu
        self.numero_partie = numero_partie
        self.pion = Pion()
        self.sentinelles = self.creer_sentinelles()
        self.temps_debut_partie: None
        self.duree_partie = None

    def creer_sentinelles(self):
        vitesse_determinee = self.determiner_vitesse_sentinelles()

        tableau_sentinelles = []
        tableau_sentinelles.append(
            Sentinelle(
                1, 60, 60, 100, 100, vitesse_determinee
            )
        )
        tableau_sentinelles.append(
            Sentinelle(
                2, 60, 50, 300, 85, vitesse_determinee
            )
        )
        tableau_sentinelles.append(
            Sentinelle(
                3, 30, 60, 85, 350, vitesse_determinee
            )
        )
        tableau_sentinelles.append(
            Sentinelle(
                4, 100, 20, 355, 340, vitesse_determinee
            )
        )
        return tableau_sentinelles

    def determiner_vitesse_sentinelles(self):
        mode_difficulte_choisi = self.jeu.mode_difficulte
        mode_difficulte = {
            "f": 7,
            "m": 9,
            "d": 11,
            "p": 7
        }
        if mode_difficulte_choisi in mode_difficulte.keys():
            return mode_difficulte.get(mode_difficulte_choisi)
        else:
            return 7

    def configurer_debut_partie(self, cadre_largeur, cadre_hauteur):
        for sentinelle in self.sentinelles:
            sentinelle.determine_sa_direction(cadre_largeur, cadre_hauteur)

    def rouler_partie(self, cadre_largeur, cadre_hauteur):
        self.duree_partie = time.time() - self.temps_debut_partie
        for sentinelle in self.sentinelles:
            if self.jeu.mode_difficulte == "p":
                if self.duree_partie % 5 >= 0 and self.duree_partie %5 <= 0.1:
                    sentinelle.vitesse += 1
            sentinelle.se_deplace(cadre_largeur, cadre_hauteur)

    def est_terminee(self):
        pion_position_x = self.pion.position_x
        pion_position_y = self.pion.position_y
        pion_largeur = self.pion.largeur
        pion_hauteur = self.pion.hauteur
        for sentinelle in self.sentinelles:
            if sentinelle.position_x >= pion_position_x - pion_largeur and sentinelle.position_x <= pion_position_x + pion_largeur:
                if sentinelle.position_y >= pion_position_y - pion_hauteur and sentinelle.position_y <= pion_position_y + pion_hauteur:
                    return True
        if pion_position_x <= (self.jeu.largeur - self.jeu.limites_largeur)/2:
            return True
        if pion_position_x >= self.jeu.largeur - (self.jeu.largeur - self.jeu.limites_largeur)/2 - pion_largeur:
            return True
        if pion_position_y <= (self.jeu.hauteur - self.jeu.limites_hauteur)/2:
            return True
        if pion_position_y >= self.jeu.hauteur - (self.jeu.hauteur - self.jeu.limites_hauteur)/2 - pion_hauteur:
            return True
        return False

    def terminer_partie(self):
        del self.pion
        for sentinelle in self.sentinelles:
            self.sentinelles.remove(sentinelle)

class Jeu:
    def __init__(self):
        self.largeur = 550
        self.hauteur = 550
        self.limites_largeur = 450
        self.limites_hauteur = 450
        self.parties = []
        self.nombre_parties = 0
        self.mode_difficulte = None

    def configurer_mode_difficulte(self, reponse):
        self.mode_difficulte = reponse

    def debuter_partie(self):
        self.nombre_parties += 1
        self.parties.append(Partie(self, self.nombre_parties))

class Vue:
    def __init__(self, parent):
        self.controleur = parent
        self.modele = self.controleur.modele
        self.cadre_info = None
        self.duree_partie = None
        self.label_duree_partie = None
        self.cadre_jeu_externe = None
        self.canvas = None
        self.root = Tk()
        self.creer_cadres()
        self.requerir_mode_difficulte()

    def creer_cadres(self):
        self.creer_cadre_info()
        self.creer_cadre_jeu_externe()

    def creer_cadre_info(self):
        self.cadre_info = Frame(
            self.root,
            width=self.modele.jeu.largeur,
            bg="turquoise"
        )
        self.creer_chronometre()
        self.creer_bouton_statistiques()
        self.cadre_info.pack(expand=1, fill=X)

    def creer_cadre_jeu_externe(self):
        self.cadre_jeu_externe = Frame(
            self.root,
            width=self.modele.jeu.largeur,
            height=self.modele.jeu.hauteur,
            bg="black"
        )
        self.cadre_jeu_externe.pack()
        self.canvas = Canvas(
            self.cadre_jeu_externe,
            width=self.modele.jeu.largeur,
            height=self.modele.jeu.hauteur,
            bg="black"
        )
        self.canvas.pack()
        self.creer_cadre_limites_interne()

    def creer_cadre_limites_interne(self):
        self.canvas.create_rectangle(
            50,
            50,
            450+50,
            450+50,
            fill="white"
        )
        self.creer_pion(255, 255, 40, 40)
        self.creer_sentinelles()

    def creer_pion(self, position_x, position_y, largeur, hauteur):
        self.canvas.create_rectangle(
            position_x,
            position_y,
            position_x + largeur,
            position_y + hauteur,
            fill="red",
            tag="pion"
        )
        if self.controleur.partie_en_cours == False:
            self.canvas.tag_bind("pion", "<Button-1>", self.debuter_partie)

    def creer_sentinelles(self):
        if self.controleur.partie_en_cours == False:
            self.canvas.create_rectangle(
                100,
                100,
                100+60,
                100+60,
                fill="blue"
            )
            self.canvas.create_rectangle(
                300,
                85,
                300+60,
                85+50,
                fill="blue"
            )
            self.canvas.create_rectangle(
                85,
                350,
                85 + 30,
                350 + 60,
                fill="blue"
            )
            self.canvas.create_rectangle(
                355,
                340,
                355 + 100,
                340 + 20,
                fill="blue"
            )
        else:
            self.canvas.create_rectangle(
                self.modele.jeu.parties[-1].sentinelles[0].position_x,
                self.modele.jeu.parties[-1].sentinelles[0].position_y,
                self.modele.jeu.parties[-1].sentinelles[0].position_x + self.modele.jeu.parties[-1].sentinelles[0].largeur,
                self.modele.jeu.parties[-1].sentinelles[0].position_y + self.modele.jeu.parties[-1].sentinelles[0].hauteur,
                fill="blue"
            )
            self.canvas.create_rectangle(
                self.modele.jeu.parties[-1].sentinelles[1].position_x,
                self.modele.jeu.parties[-1].sentinelles[1].position_y,
                self.modele.jeu.parties[-1].sentinelles[1].position_x + self.modele.jeu.parties[-1].sentinelles[1].largeur,
                self.modele.jeu.parties[-1].sentinelles[1].position_y + self.modele.jeu.parties[-1].sentinelles[1].hauteur,
                fill="blue"
            )
            self.canvas.create_rectangle(
                self.modele.jeu.parties[-1].sentinelles[2].position_x,
                self.modele.jeu.parties[-1].sentinelles[2].position_y,
                self.modele.jeu.parties[-1].sentinelles[2].position_x + self.modele.jeu.parties[-1].sentinelles[2].largeur,
                self.modele.jeu.parties[-1].sentinelles[2].position_y + self.modele.jeu.parties[-1].sentinelles[2].hauteur,
                fill="blue"
            )
            self.canvas.create_rectangle(
                self.modele.jeu.parties[-1].sentinelles[3].position_x,
                self.modele.jeu.parties[-1].sentinelles[3].position_y,
                self.modele.jeu.parties[-1].sentinelles[3].position_x + self.modele.jeu.parties[-1].sentinelles[3].largeur,
                self.modele.jeu.parties[-1].sentinelles[3].position_y + self.modele.jeu.parties[-1].sentinelles[3].hauteur,
                fill="blue"
            )

    def creer_chronometre(self):
        self.duree_partie = StringVar()
        self.duree_partie.set("Cliques sur le pion rouge, 😉")
        self.label_duree_partie = Label(
            self.cadre_info,
            textvariable=self.duree_partie,
            pady=20,
            bg="turquoise",
            font=BOLD
        )
        self.label_duree_partie.pack()

    def creer_bouton_statistiques(self):
        bouton_statistiques = Button(self.cadre_info, text="Afficher statistiques")
        bouton_statistiques.bind("<Button-1>", self.ouvrir_fichier_statistiques)
        bouton_statistiques.pack(side=RIGHT)

    def debuter_partie(self, evt):
        self.canvas.tag_unbind("pion", "<Button-1>")
        self.canvas.bind("<B1-Motion>", self.recibler_pion)
        self.controleur.debuter_partie()

    def afficher_partie(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(
            50,
            50,
            450 + 50,
            450 + 50,
            fill="white"
        )
        self.creer_pion(
            self.modele.jeu.parties[-1].pion.position_x,
            self.modele.jeu.parties[-1].pion.position_y,
            self.modele.jeu.parties[-1].pion.largeur,
            self.modele.jeu.parties[-1].pion.hauteur
        )
        self.creer_sentinelles()
        self.duree_partie.set(str(round(self.modele.jeu.parties[-1].duree_partie, 2)))

    def recibler_pion(self, evt):
        position_x = evt.x
        position_y = evt.y
        self.controleur.recibler_pion(position_x, position_y)

    def afficher_message_fin_partie(self):
        mode_difficulte = {
            "f": "FACILE",
            "m": "MOYEN",
            "d": "DIFFICILE",
            "p": "PROGRESSIF"
        }
        if self.modele.jeu.mode_difficulte in mode_difficulte.keys():
            mode_a_afficher = mode_difficulte.get(self.modele.jeu.mode_difficulte)

        temps_jeu_ecoule = round(self.modele.jeu.parties[-1].duree_partie, 2)

        utilisateur_veut_sauvegarder_resultat = messagebox.askyesno(">>> FIN DE PARTIE <<<", f'''
Temps de jeu écoulé (score):  {temps_jeu_ecoule} secondes
Mode de difficulté de la partie: {mode_a_afficher}

Voulez-vous sauvegarder vos résultats? (YES)   
''')
        if utilisateur_veut_sauvegarder_resultat:
            self.requerir_information_utilisateur(temps_jeu_ecoule, mode_a_afficher)
        else:
            return

    def requerir_information_utilisateur(self, temps_jeu_ecoule, mode_a_afficher):
        nom_utilisateur = simpledialog.askstring(">>> QUEL EST VOTRE NOM? <<<", '''
Quel est votre nom? ''')

        if nom_utilisateur == None:
            return
        elif len(nom_utilisateur) > 0:
            return self.controleur.sauvegarder_resultat_dans_fichier(nom_utilisateur, temps_jeu_ecoule, mode_a_afficher)
        else:
            messagebox.showinfo("ERREUR D'ÉNTRÉE", "Entrer au moins un caractère")
            return self.requerir_information_utilisateur(temps_jeu_ecoule, mode_a_afficher)

    def terminer_partie(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(
            50,
            50,
            450+50,
            450+50,
            fill="white"
        )
        self.creer_pion(255, 255, 40, 40)
        self.creer_sentinelles()
        self.requerir_mode_difficulte()

    def requerir_mode_difficulte(self):
        reponse = simpledialog.askstring("Choisir le mode de difficulté, 🕹", '''
Choisis ton mode de difficulté:

> FACILE (f)
> MOYEN (m)
> DIFFICILE (d)
> PROGRESSIF (p)

Le mode de difficulté choisi a de l'influence sur la vitesse des sentinelles, 🍃

Évidemment; ... plus le jeu est difficile, plus les sentinelles se déplacent rapidement, 😉

* Attention: lettre entrée doit absolument être en minuscule
* Recommendation du programmeur: le mode PROGRESSIF car ça rend le jeu très immersif, 🍀
        ''', parent=self.root)

        if reponse in "fmdp":
            self.controleur.configurer_mode_difficulte(reponse)
        else:
            self.requerir_mode_difficulte()

    def ouvrir_fichier_statistiques(self, evt):
        fichier = open("mes-resultats.txt", "r")
        messagebox.showinfo("STATISTIQUES", f'''
{fichier.read()}''')

class Modele:
    def __init__(self, parent):
        self.controleur = parent
        self.jeu = Jeu()

class Controleur:
    def __init__(self):
        self.partie_en_cours = False
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def configurer_mode_difficulte(self, reponse):
        self.modele.jeu.configurer_mode_difficulte(reponse)

    def debuter_partie(self):
        self.modele.jeu.debuter_partie()
        self.modele.jeu.parties[-1].configurer_debut_partie(self.modele.jeu.largeur, self.modele.jeu.hauteur)
        self.modele.jeu.parties[-1].temps_debut_partie = time.time()
        self.partie_en_cours = True
        self.animer_partie()

    def animer_partie(self):
        if self.partie_en_cours:
            self.modele.jeu.parties[-1].rouler_partie(self.modele.jeu.largeur, self.modele.jeu.hauteur)
            if self.modele.jeu.parties[-1].est_terminee():
                self.partie_en_cours = False
                self.vue.afficher_message_fin_partie()
                self.modele.jeu.parties[-1].terminer_partie()
                self.vue.terminer_partie()
            else:
                self.vue.afficher_partie()
                self.vue.root.after(40, self.animer_partie)

    def recibler_pion(self, position_x, position_y):
        self.modele.jeu.parties[-1].pion.se_recible(position_x, position_y)

    def sauvegarder_resultat_dans_fichier(self, nom_utilisateur, temps_jeu_ecoule, mode_a_afficher):
        today_date = date.today()
        fichier = open("mes-resultats.txt", "a")
        fichier.write(f'''
En date du {today_date.strftime("%B %d, %Y")}
--- --- --- --- --- --- --- --- ---
Nom du joueur: {nom_utilisateur}
Temps de jeu écoulé (score): {temps_jeu_ecoule} secondes
Mode de difficulté de la partie: {mode_a_afficher}

''')
        fichier.close()

if __name__ == '__main__':
    c = Controleur()
