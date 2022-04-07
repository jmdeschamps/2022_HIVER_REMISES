Auteur : David Demers
Matricule : 1942878
Date : 2022-02-07


//But du jeu//


le but du jeu est de déplacer le carré rouge en maintenant la souris sur celui-ci, le carré suit alors la souris. lorsqu'on appuie et maintien pour la première fois, 
les sentinelles (des rectangles bleus au nombre de 4 positioné à quatres endroits stratégiques) commencent leur déplacement, la partie commence et un minuteur démarre. 
Les sentinelles se déplacent en diagonal et rebondissent sur les parois d'un grand carré. leur vitesse initiale est variable ce qui empêche les sentinelles d'avoir le 
même schéma de mouvement. il y a collision et fin de partie lorsque le carré rouge entre en contact avec les sentinelles ou sort du carré blanc qui constitue le terrain 
de jeu. Au fil du temps, la vitesse des sentinelles augmente. Lorsqu'il y a fin de partie, les rectangles et le carré sont repositionnés à leur position initiale et le 
minuteur est arrêté. si on réappuie, la partie recommence.


//Problèmes rencontrés//


-Difficulté à trouver la vitesse initiale de départ, il faudrait donc tester pour trouver une vitesse idéale.
-Difficulté à incrémenter la vitesse. idem
-Je n'ai pas eu le temps de faire un menu options, qui permettrait de modifier les positions, les vitesse, les tailles.
-Une fonctionnalité de score n'a pas été fait.

 


