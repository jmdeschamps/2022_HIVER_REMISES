Jean-Christophe Caron, Karl Marchand, Koralia Frenette et Sebastian Perez
#Receuille des fonctions et abréviations utilisées dans le projet

#Abréviations
###nbr -> Nombres
###num -> Numero
###qte -> quantité
###nat -> naturel
###art -> artificiel
###res -> ressources
###met -> métaux
###def -> defense
###g -> gauche
###btn -> bouton




Dans la vue
self.gold -> or (or est un mot réservé)
Coupable : Maxence

#Fonctions

##construire()
        Description: Construis un bâtiment dans un système solaire. Peut être étoffé pour gérer les types de mines et de gaz. 
        Fichier: Orion_client/systeme_solaire.py
        Parent: SystemeSolaire
        Paramètres: catégorie de bâtiment (voir dictionnaie du Système Solaire)
        Retourne: rien
        Coupable: Karl


##production()
        Description: Appel la fonction production de chaque bâtiment dans son dictionnaire si le système a un propriétaire.
        Fichier: Orion_client/systeme_solaire.py
        Parent: SystemeSolaire
        Paramètres: aucun
        Retourne: rien mais met son inventaire à jour selon le retour des bâtiments
        Coupable: Karl


##production()
       Description: Produit les ressource de ce bâtiment s'il a l'énergie nécessaire. 
                        Pour ce faire, il va chercher le bonus du joueur propriétaire s'il 
                        en a, le bonus de moral de la planète et son taux de production de base. 
                        Il fait cette opération pour chaque ressource dans son propre tableau de 
                        ressource. Les bâtiments produisant de la progression auront un 
                        fonctionnement différent (feront progresser des production/recherches).
       Fichier: Orion_client/systeme_solaire.py
       Parent: Infrastructure
       Paramètres: aucun
       Retourne: un tableau de production composé de tableaux [Type, quantité]
       Coupable: Karl 


##consommation()
        Description: Le bâtiment calcul son cout de consommation en energie en utilisant les 
                        malus du joueur et sa consommation de base.
       Fichier: Orion_client/systeme_solaire.py
       Parent: Infrastructure
       Paramètres: aucun
       Retourne: une montant de consommation
       Coupable: Karl

##afficher_ressources()
        Description: Va chercher les ressources du joueurs pour les affichers sur l'interfaces
       Fichier: Orion_client/Orion_vue.py
       Parent: vue
       Paramètres: aucun
       Retourne: retourne la quantité des ressources du joueurs
       Coupables: Maxence et Sebastian

##creation_menu_lateral_g()
        Description : Création du cadre ayant les boutons pour affichers différentes tables d'information
        Fichier: Orion_client/Orion_vue.py
        Parent : Vue
        Paramètres : aucun
        Retourne : retourne la quantité des ressources du joueurs
        Coupables: Maxence et Sebastian

##conquete()
        Description : l'action d'aller vers une cible de l'attaquer
        Fichier: Orion_client/Orion_modele.py
        Parent : Modele
        Paramètres : tableau de données reçu par le serveur (voir la fonction conquete dans le fichier Orion_client)
        Retourne : rien
        Coupables: Jean-Christophe Caron

##skill_check()
        Description : equivalent d'un brassage de dé en dungeon and dragons
        Fichier: Orion_client/skillcheck.py
        Parent : SkillCheck
        Paramètres : rien
        Retourne : le joueur gagnant
        Coupables: Jean-Christophe Caron