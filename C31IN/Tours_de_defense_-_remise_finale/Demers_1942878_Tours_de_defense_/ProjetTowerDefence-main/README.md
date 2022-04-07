# VOID
Équipe: Parisien, Pierre Olivier ; Horvath, Samuel ; Demers, David ; Caron, Jean-Christophe
Date : 2022-02-21

But du jeu :

le but du jeu est de defendre un portail situé a l'extrémité droite de la carte, contre des vagues successives
d'ennemis qui suivent un chemin tracé. Ils sont représentés par des points noirs. Pour y parvenir, nous avons des tours
qui tirent des projectiles sur les ennemis, selon leur rayon respectif. Ces tours ont un coût et le joueur commence avec
assez d'argent pour en installer quelques unes. Si les ennemis penètrent dans le portail, le joueur perd une vie. Le joueur
possède 3 vies. Pour commencer la partie, il faut appuyer sur le bouton en haut à gauche de l'écran. Si le joueur n'a plus
de vie, la partie se termine. Si une tour détruit un ennemi, il gagne une certaine somme d'argent et un certain nombre de
points. Pour acheter une tour, il suffit de faire un clique gauche sur un terrain vaccant. On ne permet pas de construire 
une tour sur le chemin. Nous avons programmé un niveau qui comporte 10 vagues. La première commence avec 10 monstres et 
augmente en difficulté en incrementant la vitesse des monstres et la vie des monstres.



Suite du projet :


pour l'instant, il n'y a pas de bugs rencontrés, toutefois, nous n'avons pas eu le temps de faire des améliorations,
de creer différentes tours, différents ennemis, un affichage de vague, des boss.

De plus, il faudrait régler la difficulté, les vitesses de tir, les vitesses de déplacement des monstres, le nombre 
d'ennemis par vague, pour rendre le jeu plus difficile. 


Update sprint 2:
Notre visuel a grandement été amélioré c'était notre premier mandat pour satisfaire le client. Nous avons ajouté des gifs 
pour représenter les monstres et le Boss. On peut maintenant améliorer les tours en les sélectionnant et en cliquant sur le
bouton "améliorer la tour" en haut a gauche. De plus, nous avons 5 types de tour : les tours de glace qui ralentissent
l'ennemi,les tours sniper qui on un rayon d'attaque et des dégats élevés, les tours poison qui empoisonnent indéfiniment l'ennemi, les
tours mitraillettes qui ont une cadence de tir élevé et les tours bombes qui attaquent avec un boulet qui explose tous les 
monstres dans le rayon du projectile. Nous pouvons améliorer le niveau des tours à deux reprises. Ceux-ci en retour peuvent 
augmenter les dégats des projectiles,  augmenter le rayon et la cadense.

L'ajout des tours a causé une restructuration du code, car nous avons dû changer la liste de tours pour un dictionnaire de 
tour. Ainsi que l'ajout des tags dynamiques et des id pour pouvoir sélectionner une tour déja créée et l'améliorer.

Le menu a subi une mise a jour visuelle,c'est à dire que le client peut maintenant sélectionner la tour qu'il souhaite construire.
Il y a des petits icônes représentant les tours pour aider le client dans son choix. Notre client nous a aussi mentionné 
qu'un bouton pause est essentiel et nous l'avons ajouté la journée même.


le jeu possède un menu initial et un menu de fin de partie avec des images.
Il y a aussi un bouton qui permet d'afficher les scores des précédents utilisateurs.






