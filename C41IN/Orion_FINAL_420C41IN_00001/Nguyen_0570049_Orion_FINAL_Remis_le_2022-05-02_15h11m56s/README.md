PROJET Orion
============

Auteurs: Jessica Chan, Mathieu Mailloux, Pierre-Olivier Parisien, Jacques Duymentz, Pierre Long Nguyen
Date de remise: 2 Mai, 2022
Titre: Orion
Language de programmation: Python


INTRODUCTION
============

Orion se veut un jeu de conquête et de développement dans lequel le joueur doit assurer une saine gestion de ses ressources afin de pouvoir prendre possession du plus de planètes possible avant que les autres joueurs ne le fassent OU générer une quantité exorbitante de nourriture (1 000 000) afin de gagner la partie.

INSTRUCTIONS D'UTILISATIONS
===========================

En cliquant sur la planète mère, le joueur verra 3 boutons afin de créer un explorateur, un cargo ou un chasseur.
En cliquant sur un vaisseau créé, le joueur peut ensuite cliquer sur une planète qu'il n'a pas conquise pour y amener le vaisseau. Afin d'obtenir l'information quant aux ressources que le joueur pourra exploiter, le vaisseau devra revenir à la planète mère lorsqu'il aura fini de visiter (et de prendre possession) d'une ou pluieurs planètes. Lorsque le vaisseau sera revenu, il sera possible de cliquer sur les différentes planètes conquises afin d'avoir l'information. 

Lorsqu'une planète est sélectionnée, un menu des bâtiments est disponible: coût et quantité déjà construite, selon 3 niveaux.

## Vaisseau :   
- Cargo (Vaisseau avec capacité de minage/collecte de ressources sur les planètes conquises)
- Explorateur (Vaisseau avec vitesse de déplacement élevée, rayon de vision élevé et un faible coût de carburant)
- Chasseur (Vaisseau avec capacité de combat)

## Batiment : 
- Alimentation (Augmentation constante de nourriture sur le temps selon le niv.)
>  +2 Alimentation / niv 1
> 
> +10 Alimentation / niv 2
> 
> +40 Alimentation / niv 3
- Science (débloquer des capacités des chasseurs et explorateur selon le niv.) 
> +1 niveau de Science = +1% vitesse et 15% HP (chasseur)
> +1 niveau de Science = +2% vitesse et 5% HP (explorateur)
> 
> Niveau de Science (2) = +100 rayon de vision et +50 rayon attaque (chasseur)
> 
> Niveau de Science (3) = +100 rayon de vision et +50 rayon attaque (chasseur)
> 
> 3 x Niveau de Science (3) = +200 rayon de vision et +50 rayon attaque (chasseur)
  
- Industrie (la vitesse de minage selon le niveau)
> +1 vitesse de minage, +0.1 vitesse de deplacement, +10 Hp / niv 1
>
> +2 vitesse de minage, +100 capacité maximun du cargo / niv 2
> 
> +5 vitesse de minage, +500 capacité maximun du cargo, +200 hp / niv 3

- Habitation (Augmentation de la population disponible)
> +100 population / niv 

## Condition de victoire
- Lorsqu'un joueur atteint 50 planètes conquises
- Lorsqu'un joueur atteint 1 000 000 stocks de nourriture 

Une fois l'une des conditions de victoire atteint, un message annoncant le joueur gagnant est affiché et le jeu est arrêté.

BUGS
====

- Lors de l'étape de minage d'un cargo, si le joueur sélectionne une autre planète, la cible de minage actuelle change: ex. le cargo sera à la planète x et ce sera alors les ressources de la planète y qui seront récoltées.
- Glitch graphiques pour certains mouvements de vaisseaux avec le cadre rouge de selection qui se multiplie lorsque le vaisseau se déplace.
- Les missiles que le joueur lance ne seront pas observables sur la partie d'un autre joueur, de la même manière, les dommages sont seulement traités en local. 
- Le menu de droite ne s'affiche pas toujours bien lorsqu'on est pas dans le mode plein écran.
- Les images des vaisseaux mises à jour ne sont pas utilisées, car celles des ennemies s'affichent avec un clignotement rapide et partiellement d'une mauvaise couleur lorsque l'on joue en multijoueur.

CARACTÉRISTIQUES SPÉCIAUX DU JEUX
===========================================
- Chaques planètes possèdent des ressources minables alloués à chaque joueur. Un joueur, pennant contrôle d'une planète enemie, peux miner la planète conquise comme une planète nouvellement conquise.
- Les vaisseaux sont capables de faire des allés-retours.



CARACTÉRISTIQUES ET AMÉLIORATIONS SUGGÉRÉES
===========================================

- Les ruines et les artefacts comme bonus récupérables dans l'espace.
- Le coût de construction des bâtiments augmente exponentiellement selon le niveau. 
- Implémentation d'une fonction de combat manuelle, différente du mode automatique-défensif : combat offensif (cliquer sur un chasseur et ensuite cliquer sur la cible pour qu'il la traque).
- Augmentation de la force de frappe des missiles en fonction des bâtiments construits (évolution de la science).
- Possibilité de communiquer via un pseudo-chat (messages pré-formatés et choix de réponses).
- Ajouter plus de bonus pour le batiment habitation
- Créer une section affichant des informations sur chaque action du joueur
- Créer cadre de victoire