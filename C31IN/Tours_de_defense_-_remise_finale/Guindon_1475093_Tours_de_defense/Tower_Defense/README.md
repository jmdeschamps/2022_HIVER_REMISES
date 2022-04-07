PROJET TOWER DEFENCE
============

Auteurs: Manil Boudjemai, Maxence Guindon, Nicolas Charbonneau, Pierre Long Nguyen
Date de remise: 07 Mars, 2022
Titre: TOWER DEFENCE EXTREME ACTION
Language de programmation: Python


INTRODUCTION
============

Dans le jeu TOWER DÉFENCE, l'objectif est de survivre à travers de multiples de vagues d'ennemies en les éléminant avec des tours placées STATÉGIQUEMENT sur la plateforme de jeu avant que les vagues n'atteignent la base du joueur.

PARTICULARITÉS ET DEROULEMENT DU JEU
=====================

Le jeu débute avec un menu de présentation. Une fois la partie initialisée, de multiples vagues vont être lancées en séquence à vitesses déterminées. Le joueur peut placer des tour ayant des types d'attaques différents pour essayer de détruire le plus d'ennemies possible avant qu'ils atteignent la base du joueur. Si le joueur n'a plus de point de vie, le jeu met fin à la partie et le score est affiché.    


INSTRUCTIONS D'UTILISATIONS
===========================

LE PANNEAU DE COMMANDE
---------------------------
Pour commencer la partie, il faut cliquer le bouton (BRING IT ON!!!). L'ajout d'un nom de joueur est facultatif. Sans quoi, il sera identifié comme 'Joueur inconnu' et il ne pourra pas accumulé d'expérience. L'affichage du panneau de commande va offrir différentes options au joueur.

 - Le 1er frame va afficher la vie, les scores, les pièces d'or, et le niveau du joueur pour la partie courante.
   - Vie : indique le nombre de vies qu'il reste au joueur avant de mourir.
   - Score: Indique le score total de la partie à des fins de palmarès des meilleurs joueurs.
   - Pièce d'or: La monnaie d'échange pour l'achats des différents tours du jeu.
   - Niveau du joueur: L'expérience pour l'activation des différentes tours du jeu
 - Le 2e frame va afficher les différentes tours disponibles.
 - Le 3e frame va afficher les informations interactives relatives aux cliques de la souris.
   - Contient entre autre le bouton Amélioration et Vendre lorsqu'on clique sur une Tour.
 - Le 4e frame inférieur va afficher 4 boutons de commande.
   - Bouton Vitesse: Permet le choix de vitesse de jeu (1x, 2x).
   - Bouton Pause/Commencer: Permet de mettre en pause le jeu. Lorsque le jeu est en pause, le remettre en marche. Une fois une vague terminée, le bouton permet d'initialiser la prochaine vague.
   - Bouton Réinitialiser: Relance la partir avec les paramètres initiaux. 
   - Bouton Quitter: Permet de quitter le jeu.

LES TOURS
---------------------------
Le joueur utilise diverses tours pour protéger sa forteresse.

Ces tours ont la capacité d'éliminer les Creeps ou d'affecter leur progression de déplacement vers la forteresse.
De par son pouvoir d'achat, le joueur a le choix parmi 4 tours.
Chacune des 4 tours a un prix qui varie selon son efficacité et l'impact sur les Creeps.
Chacune des 4 tours attaque le Creep lorsqu'il est dans sa portée et selon un intervalle de temps qui lui est propre.
Chacune des tours possède une amélioration. 
Il suffit de cliquer sur la tour désirée, puis, dans le centre de commandes, il faut cliquer sur le bouton améliorer.
L'amélioration possède un coût qui lui est propre et ce moment sera déduit du portefeuille du joueur.
Chacune des tours peut être vendu, de la même façon que pour l'améliorer et ce, pour 80% de sa valeur initiale.
Les améliorations et l'accès au tour sont conditionnels au niveau du joueur.

Tour Feu
--------
Projète des missiles à tête chercheuse et cible des Creeps.
Les projectiles feu sont projetés tant qu'il y a des Creeps dans le rayon d'attaque de la tour.
Le dégât des projectiles feu est le plus élevé parmi les tours.
C'est une tour très efficace pour éliminer un Creep en particulier.

Amélioration : double les dégats de la tour
Coût : 100 $
Amélioration accessible à partir du niveau 3

Tour Poison
-----------
Cible un Creep et l'empoisonne; soit le ralenti dans sa progression - la vitesse du Creep est diminuée. Un dégât minimum est infligé au Creep.

Amélioration : occasionne du dégât au fil du temps lorsque le creep est empoisonné.
Coût : 180 $
Amélioration accessible à partir du niveau 2

Tour Glace
----------
Cible les Creep et l'immobilise. Tant que la cible demeure immobilisée, cette tour n'est plus apte d'attaquer un autre Creep.

Accessible à partir du niveau 2

Amélioration : augmente le temps pendant lequel le Creep est gelé
Coût : 150 $
Amélioration accessible à partir du niveau 2

Tour Mitraille
--------------
Projète plusieurs missiles à la fois en ciblant plusieurs Creeps.

Accessible à partir du niveau 6

Amélioration : double la vitesse d'attaque et augmente sa portée
Coût : 400 $
Amélioration accessible à partir du niveau 8


LES CREEPS 
---------------------------
Il y a cinq différentes sortes de creeps inclus dans le jeu. 
Quatre d'entre-eux sont des creeps de vague régulière.
Ils apparaissent selon le progrès dans le niveau, du moins fort au plus fort.
À la fin du niveau, un boss est introduit. Il s'agit du dernier creep implémenté.
Celui-ci possède un nombre de points de vie largement supérieur à celui des autres creeps.
Lorsqu'un creep franchit le sentier, il occasionne un certain dégât au joueur selon la difficulté du creep (1,2,3,4). 
Si le Boss franchit le sentier, le joueur perd la partie automatiquement.
Les creeps se déplacent selon une vitesse qui est propre au genre de creep.
Plus qu'on est rendu loin dans le jeu, plus la vie des creeps augmente afin de complexifié le jeu.

BUGS
=========================================
Aucun bug majeur décelé dans cette version.

CARACTÉRISTIQUES ET AMÉLIORATIONS SUGGÉRÉES
===========================================

- implémentation du "drag n' drop" d'une tour depuis le menu de contrôle sur le terrain de jeu
- Faire des cartes collaboratives ou pvp.
- Affichage du rayon d'attaque d'une tour située sur le terrain de jeu
- Création de la tour bateau.
- Création des objets pièges déposable sur le chemin des creeps.




