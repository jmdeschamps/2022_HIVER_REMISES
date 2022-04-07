William Caron - 1569047 
Date : 7 février 2022

Le but du jeu du carré rouge est de déplacer un carré rouge sur une interface de jeu représenté d'un carré blanc
et d'éviter de toucher la surface du carré noir, le tout sans se faire toucher par les sentinelles (illustrées par des rectangles bleues).

La partie est lancée, lorsque l'utilisateur fait un clique gauche sur le carré rouge tout en gardant le maintien du clique gauche cela 
nous permet de déplacer le carré qui suit la trajectoire de la souris.

L'utilisateur a donc pour objectif de survivre le plus longtemps que possible et un minuteur situé 
au-dessus de la surface de jeu permet de voir son temps effectué.

Les sentinelles se déplacent avec une vitesse constante et lorsqu'ils touche l'extrémité de la surface de jeu noire, ils rebondissent.
Chaque sentinelle possède une taille différente comme demandé dans le mandat.
Pour effectuer un déplacement il suffit de donner une vitesse en x et en y. Pour ensuite les faires rebondir il suffit de changer leurs 
vitesse soit par une valeur positive ou négative.
Pour vérifier la collision entre le carré rouge et les sentinelles, il suffit de comparer les demi tailles du carré rouge et des sentinelles pour 
voir s'il y une superposition entre les deux.

Une fois que le carré se fait toucher soit par une sentinelle soit par la surface de jeu noire, on affiche le score en temps de la partie dans la console
et le jeu est replacé de sorte que l'utilisateur peut relancer la partie en cliquant dessus a nouveau.

Le jeu possède certains bugs connus comme que les sentinelles ne rebondissent pas clairement sur les coins, ils semblent sortir de la zone de jeu.

Certaines demandes du mandat n'ont pas pu être réalisées comme la demande d'ajout de plusieurs difficultés qui aurait donc fait changer la vitesse
en fonction du choix effectué. Dans l'ensemble par contre le jeu est fonctionnel et fonctionne assez bien.


