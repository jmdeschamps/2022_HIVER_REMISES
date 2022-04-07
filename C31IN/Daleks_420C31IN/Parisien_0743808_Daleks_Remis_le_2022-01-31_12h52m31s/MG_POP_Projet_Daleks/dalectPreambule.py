import Daleks_Vue
import random

class Jeu():
    def __init__(self):
        self.largeur = 8
        self.hauteur = 6
        self.partie_courante = None

    def demarer_partie(self):
        self.partie_courante = Partie(self)


    def changer_option(self,largeur = 8, hauteur = 6):
        self.largeur = largeur

class Partie():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = self.parent.largeur
        self.hauteur = self.parent.hauteur
        self.niveau = 0
        self.nb_dalek_par_niveau = 5
        self.daleks = []
        self.docteur = Docteur(int(self.largeur / 2), int(self.hauteur / 2))
        self.creer_niveau()



    def creer_niveau(self):
        self.niveau += 1
        nb_daleks = self.niveau * self.nb_dalek_par_niveau
        positions = [[self.docteur.x,self.docteur.y]]

        while nb_daleks : # s'il est 0 c'est faux, sinon c'est vrai, "" est aussi égal à faux
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            if [x,y] not in positions:
                positions.append([x,y])
                nb_daleks -= 1

        positions.pop(0)

        for i in positions:
            self.daleks.append(Dalek(i[0],i[1]))

    def mouvement_daleks(self):
        for i in self.daleks :
            #Docteur à droite
            if self.docteur.x > i.x:
                #Docteur plus bas
                if self.docteur.y > i.y:
                    i.x += 1
                    i.y += 1
                #Docteur plus gaut
                elif self.docteur.y < i.y:
                    i.x += 1
                    i.y += -1
                # Docteur sur la même largeur
                elif self.docteur.y == i.y:
                    i.x += 1
                    i.y += 0

            #plus gauche
            elif self.docteur.x < i.x:
                #Docteur plus bas
                if self.docteur.y > i.y:
                    i.x += -1
                    i.y += 1
                #Docteur plus gaut
                elif self.docteur.y < i.y:
                    i.x += -1
                    i.y += -1
                # Docteur sur la même largeur
                elif self.docteur.y == i.y:
                    i.x += -1
                    i.y += 0
            # Docteur sur la même longueur
            elif self.docteur.x == i.x:
                #bas
                if self.docteur.y > i.y:
                    i.x += 0
                    i.y += 1
                #haut
                elif self.docteur.y < i.y:
                    i.x += 0
                    i.y += -1



    def mouvement_docteur(self, args):

        #avoir un état du docteur

        if (self.docteur.x + args[0] < 0) or (self.docteur.y + args[1] < 0) :
             print("Mouvement illégale")
        elif (self.docteur.x + args[0] > self.largeur) or (self.docteur.y + args[1] > self.hauteur):
             print("Mouvement illégale")
        else :  
            self.docteur.x += args[0]
            self.docteur.y += args[1]
            self.mouvement_daleks()



class Docteur():
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y

class Dalek():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Controleur(): #sert à controler le logiciel
    def __init__(self):
        self.modele = Jeu()
        self.vue = Daleks_Vue.Vue()
        self.actions = {"p": self.demarer_partie,
                        "o": self.choisir_options,
                        "s": self.voir_score,
                        }
        self.afficher_menu_initial()
        #self.mouvement_docteur()

    def afficher_menu_initial(self):
        reponse = self.vue.afficher_menu_initial()
        if reponse in self.actions.keys():
            self.actions[reponse]()
        else :
            print("RATÉ")

    def demarer_partie(self):
        self.modele.demarer_partie()
        self.vue.afficher_partie(self.modele.partie_courante)

    def choisir_options(self):
        reponse = self.vue.afficher_menu_option()
        self.modele.changer_option(largeur = reponse)
        self.afficher_menu_initial()

    def voir_score(self):
        print("Score")

if __name__ == '__main__':
    c = Controleur()
