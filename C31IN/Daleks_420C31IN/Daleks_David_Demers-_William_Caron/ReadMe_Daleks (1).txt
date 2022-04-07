Équipe: William Caron - 1569047 et David Demers - 1942878
Date : 31 janvier 2022

Le but du jeu Dalek est de déplacer un docteur (illustré par la lettre D majuscule) sur une surface de jeu de 6
cases de hauteur et de 8 cases de largeur sans se faire tuer par les daleks (illustré par la lettre X majuscule).

Une fois le jeu lancé, l'utilisateur possède un menu avec trois choix à faire. Soit de lancer la partie, soit de lancer 
le menu option ou soit d'afficher la liste des scores.

Si l'option lancée par le menu d'option est choisie, on demande à l'utilisateur de choisir une nouvelle largeur pour la
surface de jeu et ensuite une nouvelle hauteur aussi pour la surface de jeu.

Si l'option afficher la liste des scores est choisi, comme celle-ci na pas été complète au complet, 
elle retourne le score lorsque l'utilisateur perd.

Si l'option lancer la partie a été choisi, le jeu se lance et une surface de jeu est affiché a l'écran.
Lors du lancement de la partie le docteur est placé au centre de la surface de jeu et 5 daleks sont placé 
de façon aléatoire sur la surface de jeu.

L'utilisateur se fait donc demander s'il veut utiliser le zappeur qui permet d'éliminer tous les daleks se trouvant
autour du docteur. S'il dit non, un menu option pour le déplacement est affiché.
Il suffit que l'utilisateur écrive un mouvement représenté par GH,H,DH,G,C,D,GB,B,DB qui représente toutes les options 
qui le docteur peut se déplacer. Comme la fonction téléportation n'a pas été réalisée, celle-ci n'est pas offerte
comme déplacement possible. Une fois un déplacement réalisé le docteur se déplace et les daleks le suivent en 
allant vers la position la plus proche du docteur.

Si deux daleks entrent en contact ou sont zappés, ceux-ci sont remplacés par une 
ferraille (illustré par la lettre W majuscule). Par la suite, si un dalek se déplace vers une ferraille, il est 
détruit lui aussi laissant la ferraille. Dans le cas ou l'utilisateur demande de se déplacer vers une ferraille le
docteur restera sur la même position est les daleks pourront avancé.

Une fois que le docteur se fait tué, on affiche le score et que la partie est terminée et on réaffiche le menu option.

Si le docteur, réussis a tué tous les daleks dans le niveau, le prochain niveau est lancé en 
ajoutant 5 daleks supplémentaires, en enlevant toutes les ferrailles et le zapper est réinitialisé.Tout en gardant
la même position du docteur.

Lors de la réalisation du projet certain bug ont été rencontré et son toujours présent dans le jeu.
Premièrement, si le joueur tente de sortir de la zone de surface de jeu.
Deuxièmement, il peut arriver que lors de la collision de plusieurs dalek sur une ferraille, un certain dalek ne soit pas 
supprimé. 

De plus, le système de difficulté n'a pas été intégré dans le menu "Options"

Il est arrivé aussi qu'on perçoive un certain bug, mais que la source ne soit pas connue.





