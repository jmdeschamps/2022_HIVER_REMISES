PROJET TOWER DEFENCE
============

Auteurs: Manil Boudjemai, Maxence Guindon, Nicolas Charbonneau, Pierre Long Nguyen
Date de remise: 21 FEVRIER, 2022
Titre: TOWER DEFENCE EXTREME ACTION
Language de programmation: Python


INTRODUCTION
============

Dans le jeu TOWER DÉFENCE, l'objectif est de survivre à travers de multiples de vagues d'ennemies en les éléminant avec des tours placées STATÉGIQUEMENT sur la plateforme de jeu avant que les vagues n'atteignent la base du joueur.

PARTICULARITÉS ET DEROULEMENT DU JEU
=====================

Le jeu débute avec un menu de présentation. Une fois la partie initialisée, de multiples vagues vont être lancées en séquence à vitesses déterminées. Le joueur peut placer des tour ayant des types d'attaques différents pour essayer de détruire le plus d'ennemies possible avant qu'ils atteingnent la base du joueur. Si le joueur n'a plus de point de vie, le jeu met fin à la partie et le score est affiché.    


INSTRUCTIONS D'UTILISATIONS
===========================

LE PANNEAU DE COMMANDE
---------------------------
Pour commencer la partie, il faut cliquer le bouton (BRING IT ON!!!). L'affichage du panneau de commande va offrir différentes options au joueur.
 - Le 1er frame va afficher les scores, les pièces d'or et l'expérience du joueur pour la partie courante.
   - Score: Indique le score total de la partie à des fins de palmarès des meilleurs joueurs.
   - Pièce d'or: La monnaie d'échange pour l'achats des différents tours du jeu.
   - Expérience: La monnaie d'échange pour l'aquisition des différentes habiletés du joueur (En développement)
 - Le 2e frame va afficher les différentes tours disponibles.
 - Le 3e frame va afficher les informations interactives relatives aux cliques de la souris. 
 - Le 4e frame inférieur va afficher 4 boutons de commande.
   - Bouton Vitesse: Permet 3 choix de vitesse de jeu (1x, 2x, 4x) (en développement).
   - Bouton Pause: Permet de mettre en pause le jeu (en développement).
   - Bouton Commencer: Permet d'initialiser les vagues. Une fois une vague lancée, le nombre de vie du joueur va s'afficher sur le bouton jusqu'à ce que la prochaine vague soit prête à être lancée.
   - Bouton Quitter: Permet de quitter le jeu.

LES TOURS
---------------------------
Le joueur utilise diverses tours pour protéger sa forteresse.

Ces tours ont la capacité d'éliminer les Creeps ou d'affecter leur progression de déplacement vers la forteresse.
De par son pouvoir d'achat, le joueur a le choix d'utiliser parmi 4 tours.
Chacune des 4 tours a un prix qui varie selon son efficacité et l'impact sur les Creeps.
Chacune des 4 tours, attaque le Creep lorsqu'il est dans sa portée.
Sauf pour la Tour de Glace, chacune des tours accessibles au joueur projète des missiles par intervalle de temps fixe.


Tour Feu
--------
Projète des missiles à tête chercheuse et cible des Creeps.
Les projectiles feu sont projetés tant qu'il y a des Creeps dans le rayon d'attaque de la tour.
Le dégât des projectiles feu est le plus élevé parmis les tours.
C'est une tour très efficace pour éliminer les Creeps aussi rapidement que possible.

Tour Poison
-----------
Cible un Creep et l'empoisonne; soit le ralenti dans sa progression - la vitesse du Creep est diminiuée. Un dégât minimum est infligé au creep.

Tour Glace
----------
Cible un Creep et l'immobilise. Tant que la cible demeure immobilisée, cette tour n'est plus apte d'attaquer un autre Creep.


Tour Mitraille
--------------
Projète plusieurs missiles à la fois en ciblant plusieurs Creeps.

LES CREEPS 
---------------------------
Il y a cing différentes sortes de creeps inclus dans le jeu. 
Quatre d'entre-eux sont des creeps de vague régulière.
Ils apparaissent selon le progrès dans le niveau, du moins fort au plus fort.
À la fin du niveau, un boss est introduit. Il s'agit du dernier creep implémenté.
Celui-ci possède un nombre de points de vie largement supérieur à celui des autres creeps.
Lorsqu'un creep franchit le sentier, il occasionne un certain dégât au joueur selon la difficulté du creep (1,2,3,4). 
Le boss est celui qui fait le plus de dégât s'il n'est pas tué à temps (50).
Les creeps se déplacent selon une vitesse qui est propre au genre de creep. Cependant, pour l'instant, nous leur avons mis la même vitesse.


BUGS
=========================================
- Lorsque le creep ciblé par la tour de glace meurt, celle-ci ne prend pas de nouvelle cible.
- Une erreur de bitmap est lancée lorsqu'on est rendu à la vague 8 et nous force à quitter le programme.
  Nous pensons qu'il s'agit d'une erreur lancée du fait que nous ouvrons constamment les images des objets à chaque affichage.

CARACTÉRISTIQUES ET AMÉLIORATIONS À AJOUTER POUR LE 2E SPRINT
===========================================

 - Bouton de réinitialisation du jeu à ajouter
 - interface d'inscription du joueur.
 - Interface de palmares des joueurs.
 - Amélioration des images des tours.
 - Implémentation d'un nouveau niveau.
 - Ajouter les fonctionalités des boutons vitesse et pause.

CARACTÉRISTIQUES ET AMÉLIORATIONS SUGGÉRÉES
===========================================

- Avoir une base de donnée pour enregistrer plusieurs joueurs.
- Faire des cartes collaboratives ou pvp.
- Équilibrer la tour de feu car celle-ci est trop forte comparativement aux autres tours.
- Ajuster les points de vie des creeps selon les dégâts des tours
- Pour l'instant notre nombre de vie est à 5 pour nous permettre de faire des tests. Dans la version finale du jeu, le joueur aura 100 points à défendre.



