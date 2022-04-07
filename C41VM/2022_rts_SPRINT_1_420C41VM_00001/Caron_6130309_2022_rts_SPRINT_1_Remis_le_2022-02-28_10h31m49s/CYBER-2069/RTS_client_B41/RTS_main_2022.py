## -*- Encoding: UTF-8 -*-

import urllib.request
import urllib.parse
import urllib.error
import json 
import random
import pickle
from helper import Helper
from RTS_divers import *
from RTS_vue import *
from RTS_modele import *
import time
import threading
"""
Application client RTS, base sur le modele approximatif d'Age of Empire I

module principal (main), essentiellement le controleur, dans l'architecture M-V-C
"""

class Controleur():
    def __init__(self):
        self.civilisation="1"
        # indique si on 'cree' la partie, c'est alors nous qui pourront Demarre la pertie
        self.egoserveur=0 
        # le no de cadre pour assurer la syncronisation avec les autres participants
        # cette variable est gerer par la boucle de jeu (bouclersurjeu)
        self.cadrejeu=0    
        # la liste de mes actions a envoyer au serveur, rempli par les actions du joueur AFFECTANT le jeu                 
        self.actionsrequises=[] 
        
        # cette variable INDENTIFIE les joueurs dans le jeu IMPORTANT            
        # createur automatique d'un nom de joueur, pour faciliter les tests (pas besoin d'inscrire un chaque fois)
        # NOTE la fonction ne garantie pas l'unicite des noms - probleme en cas de conflit - non traite pour l'instant
        self.monnom=self.generer_nom()
        # la variable donnant acces au jeu pour le controleur, cree lorsque la partie est initialise (initialiserpartie)
        self.modele=None
        # liste des noms de joueurs pour le lobby
        self.joueurs=[]
        # requis pour sortir de cette boucle et passer au lobby du jeu
        self.prochainsplash=None
        # indicateur que le jeu se poursuive - sinon on attend qu'un autre joeur nous rattrape
        self.onjoue=1
        # delai en ms de la boucle de jeu
        self.maindelai=50
        # frequence des appel au serveur, evite de passer son temps a communiquer avec le serveur
        self.moduloappeler_serveur=5
        
        # adresses du URL du serveur de jeu, adresse 127.0.0.1 est pour des tests avec un serveur local... utile pour tester
        #self.urlserveur = "http://jmdeschamps.pythonanywhere.com"
        self.urlserveur = "http://127.0.0.1:8000"

        # creation de la l'objet vue pour l'affichage et les controles du jeu

        testdispo = self.tester_etat_serveur()
        print(testdispo)
        self.vue=Vue(self,self.urlserveur,self.monnom,testdispo[0])
        # requiert l'affichage initiale du splash screen (fenetre initiale de l'application)
        #####self.vue.changercadre("splash")
        # lancement de la communication avec les serveur
        #self.boucler_sur_splash()
        # demarrage de la boucle evenementielle du logiciel
        # cette boucle gere les evenements (souris, click, clavier)
        self.vue.root.mainloop()

    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut (jeu disponible, pas de joueur)
    # indique le resultat dans le splash
    def reset_partie(self):
        leurl=self.urlserveur+"/reset_jeu"
        reptext = self.appeler_serveur(leurl, 0)

        self.vue.update_splash(reptext[0][0])
        return reptext
        
    # methode pour connaitre l'etat du serveur au lancement de l'application seulement
    # dispo=on peur creer une partie
    # attente=on peut se connecter a la partie
    # courante= la partie est en cours, on ne peut plus se connecter
    def tester_etat_serveur(self):
        leurl=self.urlserveur+"/tester_jeu"

        repdecode = self.appeler_serveur(leurl, None)[0]

        print(repdecode)
        if "dispo" in repdecode:
            return ["dispo",repdecode]
        elif "attente" in repdecode:
            return ["attente",repdecode]
        elif "courante" in repdecode:
            return ["courante",repdecode]
        else:
            return "impossible"
    
    # a partir du splash, permet de creer une partie (lance le lobby pour permettre a d'autres joueurs de se connecter)
    # l'argument valciv n'est pas utilise pour l'INSTANT, elle sert de recette pour envoyer des parameters lors de la demande de creation d'une partie
    # on pourrait ainsi deja fournir des options de jeu
    def creer_partie(self,nom,urljeu):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash=None
        if nom:
            self.monnom=nom
        url = self.urlserveur+"/creer_partie"
        params = {"nom": self.monnom}
        reptext=self.appeler_serveur(url,params)
        self.egoserveur=1
        self.vue.root.title("je suis "+self.monnom)
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()
            
    # permettre a un joueur de s'inscrire a une partie creer (mais non lancer...)
    # transporter alors dans le lobby, en attente du lancement de la partie
    # le joueur peut aussi choisir une option 
    def inscrire_joueur(self,nom,urljeu):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash=None
        if nom:
            self.monnom=nom
        url = self.urlserveur+"/inscrire_joueur"
        params = {"nom": self.monnom}
        reptext=self.appeler_serveur(url,params)
        self.vue.root.title("je suis "+self.monnom)
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()
    
    # e partir du lobby, le createur de la partie peut lancer la partie
    # fournissant des options (ici nbrIA) uniquement accessible au createur
    # lors que le createur voit tous ses joueurs esperes insrit il peut (seul d'ailleurs) lancer la partie
    # cette methode ne fait que changer l'etat de la partie sur le serveur pour le mettre a courant
    # lorsque chaque joueur recevra cet etat la partie sera initialiser et demarrer localement pour chacun
    def lancer_partie(self):
        ## au lancement le champ 'champnbtIA' du lobby est lu...
        url = self.urlserveur+"/lancer_partie"
        params = {"nom": self.monnom}
        reptext=self.appeler_serveur(url,params)
        
    # methode de demarrage local de la boucle de jeu (partie demarre ainsi)
    def initialiser_partie(self,mondict):
        # on recoit les divers parametres d'initialisation du serveur
        initaleatoire=mondict[1][0][0]
        #ment, decommenter un ligne et commenter l'autre
        # mais pour tester c'est bien de toujours avoir la meme suite de random
        # random ALEATOIRE fourni par le serveur
        #random.seed(int(initaleatoire))
        # random FIXE pour test
        random.seed(12473)
        
        # on recoit la derniere liste des joueurs pour la partie
        listejoueurs=[]
        for i in self.joueurs:
            listejoueurs.append(i[0])
        
        # le  nombre d'IA desires est envoye au modele
        #nbrIA=mondict[2][0][0]
        # on cree le modele (la partie)
        self.modele=Partie(self,listejoueurs)
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele=self.modele
        # on met la vue a jour avec les infos de partie 
        self.vue.initialiser_avec_modele()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.changer_cadre("jeu")
        self.vue.centrer_maison()

        self.boucler_sur_jeu()  # on lance la boucle de jeu

    ##########   BOUCLES: SPLASH, LOBBY ET JEU    #################

    # boucle de comunication intiale avec le serveur pour creer ou s'inscrire a la partie
    def boucler_sur_splash(self):
        url = self.urlserveur+"/tester_jeu"
        params = {"nom": self.monnom }
        mondict=self.appeler_serveur(url,params)
        print(self.monnom,mondict)
        if mondict:
            self.vue.update_splash(mondict[0])
        self.prochainsplash=self.vue.root.after(50,self.boucler_sur_splash)
    
    # on boucle sur le lobby en attendant l'inscription de tous les joueurs attendus
    def boucler_sur_lobby(self):
        url = self.urlserveur+"/boucler_sur_lobby"
        params = {"nom": self.monnom }
        mondict=self.appeler_serveur(url,params)
        # si l'etat est courant, c'est que la partie vient d'etre lancer
        if "courante" in mondict[0]:
            self.initialiser_partie(mondict)
        else:
            self.joueurs=mondict
            self.vue.update_lobby(mondict)
            self.vue.root.after(50,self.boucler_sur_lobby)
         
    def boucler_sur_jeu(self):
        # increment du compteur de boucle de jeu
        self.cadrejeu+=1
        # test pour communiquer avec le serveur periodiquement
        if self.cadrejeu%self.moduloappeler_serveur==0:
            if self.actionsrequises:
                actions=self.actionsrequises
            else:
                actions=None
            self.actionsrequises=[]
            url = self.urlserveur+"/boucler_sur_jeu"
            params = {"nom": self.monnom,
                      "cadrejeu":self.cadrejeu,
                      "actionsrequises":actions}

            try:
                mondict=self.appeler_serveur(url,params)
                #verifie pour requete d'attente d'un joueur plus lent
                if "ATTENTION" in mondict:
                    print("SAUTEEEEE")
                    self.onjoue=0
                #sinon on ajoute l'action
                else:
                    self.modele.ajouter_actions_a_faire(mondict)

            except urllib.error.URLError as e:
                print("ERREUR ",self.cadrejeu,e)
                self.onjoue=0

        if self.onjoue:
            # envoyer les messages au modele et a la vue de faire leur job
            self.modele.jouer_prochain_coup(self.cadrejeu)
            self.vue.afficher_jeu()
        else:
            self.cadrejeu -= 1
            self.onjoue = 1

        self.vue.root.after(self.maindelai,
                            self.boucler_sur_jeu)  # appel ulterieur de la meme fonction jusqu'a l'arret de la partie

    ##############   FONCTIONS pour serveur #################
    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut
    def reset_partie(self):
        leurl = self.urlserveur + "/reset_jeu"
        reptext = self.appeler_serveur(leurl, 0)
        self.vue.update_splash(reptext[0][0])
        return reptext

    #   retour de l'etat du serveur
    def tester_etat_serveur(self):
        leurl = self.urlserveur + "/tester_jeu"
        repdecode = self.appeler_serveur(leurl, None)[0]
        if "dispo" in repdecode:  # on peut creer une partie
            return ["dispo", repdecode]
        elif "attente" in repdecode:  # on peut s'inscrire a la partie
            return ["attente", repdecode]
        elif "courante" in repdecode:  # la partie est en cours
            return ["courante", repdecode]
        else:
            return "impossible"

    # fonction d'appel normalisee d'appel pendant le jeu
    def appeler_serveur(self, url, params):
        self.onjoue=1
        # appel ulterieur de la meme fonction jusqu'a l'arret de la partie
        self.vue.root.after(self.maindelai,self.boucler_sur_jeu)

    # generateur de nouveau nom,
    # peut generer UN NOM EXISTANT mais c'est rare, NON GERER PAR LE SERVEUR
    def generer_nom(self):
        monnom="CYBER_"+str(random.randrange(100,1000)) # CHANGEMENT ANTO
        return monnom

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appeler_serveur(self,url,params):
        if params:
            query_string = urllib.parse.urlencode( params )
            data = query_string.encode( "ascii" )
        else:
            data=None
        rep=urllib.request.urlopen( url , data, timeout=None) # pour probleme de connection A SUIVRE
        reptext=rep.read()
        rep=reptext.decode('utf-8')
        rep=json.loads(rep)
        return rep
    
    def abandonner(self):
        action=[self.monnom,"abandonner",[self.monnom+": J'ABANDONNE !"]]
        self.actionsrequises=action
        self.vue.root.after(500,self.vue.root.destroy)
    ###############################################################################
    ### Placez vos fonctions


    def afficher_marchand(self):
        self.vue.afficher_marchand()

    def afficher_batiment(self,nom,batiment):
        self.vue.afficher_batiment(nom,batiment)
        
    def afficher_bio(self,bio):
        self.vue.afficher_bio(bio)


    def installer_batiment(self, nomjoueur,batiment):
        x1, y1, x2, y2 = self.vue.afficher_batiment(nomjoueur,batiment)
        return [x1, y1, x2, y2]

    def trouver_valeurs(self):
        vals=self.modele.trouver_valeurs()
        return vals
if __name__ == '__main__':
    print("Bienvenue au RTS")
    c=Controleur()
    #print("FIN DE PROGRAMME")
