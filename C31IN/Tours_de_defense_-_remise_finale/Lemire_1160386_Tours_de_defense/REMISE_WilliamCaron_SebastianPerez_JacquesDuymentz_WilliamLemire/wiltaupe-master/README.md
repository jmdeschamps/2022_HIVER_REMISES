Nom du programme: EQ4_TKTD.py

Auteurs: William C., Jacques D., William L., Sebastian P. 

Date: 07-03-2022

Version 2.0

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ DESCRIPTION ♦
*Ceci est la deuxième version du jeu SYSTEM DEFENSE: VIRUS EDITION.* 

Votre système est envahis par des virus et vous devez le défendre, vague après vague, en utilisant des tours de défense anti-virus. Si trop d'ennemis se rendent à votre CPU, votre système se déteriore peu à peu. 
Si son état se rend à 0, toutes vos données seront perdues. 

Vous êtes la dernière ligne de défense. 

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ FONCTIONNEMENT ♦
En appuyant sur le bouton *DÉBUTER PARTIE* la première vague d'ennemis commence l'envahissement de votre système. 

Pour acheter une tour, pesez le bouton de la tour que vous voulez construire et cliquez ensuite autour du bus (sentier) pour la placer. 

Les vagues deviendront de plus en plus difficiles, puisqu'elles seront de plus en plus populeuses, et que les ennemis plus faibles (Oranges) deviendront moins nombreux, alors que les plus forts (Jaunes et Rouges) augmenteront en nombre. 
Plus le temps avance, plus les virus deviennent résistants.

Le dernier ennemi de chaque vague est un Trojan, qui est beaucoup plus puissant que les virus réguliers.

Chaque ennemi détruit octroie des points, qui vous offrent la possibilité de garder votre nom en mémoire pour la postérité, dans le highscore.

En détruisant des ennemis, vous gagnez de l'argent qui vous permettera d'acheter de nouvelles tours anti-virus. 

Chaque vague détruite vous donnera des points de sagesse, qui permettent d'améliorer vos tours. 

Le bouton SCAN fait un scan du système et endommage tous les virus qui y sont actuellement. Chaque scan coûte 1000৳. Un nouveau scan est octroyé à la fin de chaque niveau. 

Le bouton MINE place un petit dispositif anti-virus qui endommage un virus qui croise son chemin. Chaque mine anti-virus coûte 100৳.

Le bouton AMÉLIORER RANGE augmente la portée de tir de la tour sélectionnée: 300௹.

Le bouton AMÉLIORER DÉGATS augmente le dommage causé par la tour sélectionnée: 300௹.

Le bouton AMÉLIORER SPÉCIAL améliore le type de tir de la tour améliorée (500௹):
  - Une tour Verte augmentera sa cadence de tir;
  - Une tour Mauve augmentera le nombre de ses projectils;
  - Une tour Blanche rebondira plus de fois.

Les virus se déplacent à une vitesse aléatoire, rendant le jeu imprévisible.

Si un niveau est complété sans qu'aucun ennemi se rende au CPU, un bonus est octroyé.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ BUGS CONNUS ♦
  
  1. Classe projectils_rebond: quand le projectile  est rendu au dernier creep à l'écran, et qU'il n'a pas terminé sa trajectoire, il attend, immobile, jusqu'au prochain creep         qui rentrera à l'écran.
  2. Classe projectils_shotgun: des projectiles, une fois rendus sur le bord de l'écran, s'y amoncèlent au lieu de disparaître.
 

