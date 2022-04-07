*****************************************************
	           JEU DES DALEKS V1.0.0
		              READ ME
*****************************************************
		            2022-01-27
****************************************************
## AUTEURS

Maxence Guindon
Pierre-Olivier Parisien


## INTRODUCTION

Notre présent mandat était de reproduire le jeu des 
Daleks de Isaac Sukin. 
Il s'agit d'un damier de 8 par 6 sur lequel un
docteur, représenté par la lettre D, est pourchassé
par 5 Daleks, qu l'on désigne par la lettre W.

Il est possible de modifier la largeur du damier avec
la fonction choisir_options du menu.

Une nouvelle partie peut être lancée en appuyant sur
la lettre p. Vous devez échapper le plus longtemps
possible au Daleks (généralement 2 tours, sur le
damier actuel).

À chaque mouvement du docteur, les Daleks vont se
rapprocher de lui d'une case.


## OUTILS

Afin de faire apparaître les Daleks à des positions 
aléatoires au début de chaque niveau, Nous importont
la librairie "random".


## BOGUES CONNUS

Faites attention, si vous tentez de passer plus loin
que la derniere ligne du bas ou de droite du damier, 
le jeu va planter et le programme arrêtera subitement
de s'exécuter.


## FONCTIONNALITÉS À VENIR

Dans la version subséquente, nous ferons en sorte que
lorsque le docteur se fait manger, la partie se 
termine. De plus, nous devons veiller à ce que, 
lorsque les Daleks entrent mutuellement en collision, 
ils se transforment en tas de ferrailles immobiles. Un
tas de férailles peut également tuer un Daleks lorqu'il 
y a une rencontre entre les deux.

Il nous restera aussi à ajouter au Docteur la 
possibilité d'obtenir des pouvoirs, comme l'utilisation 
du Zapper, qui fera exploser les Daleks qui sont à une 
case de distance de celui-ci. Également, nous voulons 
que le Docteur puisse se téléporter à une position aléatoire
au cours d'une partie.

Actuellement, les boutons du power-up sont présents, 
mais ils ne sont pas fonctionnels.

Finalement, nous ferons en sorte qu'il soit possible
d'afficher les scores du jeu, de les sauvegarder ainsi que 
de permettre au joueur de recommencer une partie en cliquant 
sur "r".




