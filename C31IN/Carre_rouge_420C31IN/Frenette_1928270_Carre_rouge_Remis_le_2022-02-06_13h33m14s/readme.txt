Jeu du Carré Rouge
Par Korallia Frenette

Jeu vidéo programmé en Python 3.9, utilisant TK 0.3.1
Copie du jeux:  http://www.kabubble.com/ga_red_square.htm

-- Opération et Objectif du jeu

Le but du jeu est de survivre le plus longtemp possible sans
que le carré rouge touche la bordure noire ou
les sentinelles (rectangles bleus)

Pour démarrer le jeu, cliquer sur le carré rouge et gardez
le bouton de la sourir pesé.

Les sentinelles commenceront à bouger, en rebondissant lorsqu'elles
frappent un mur extérieur.

Un compte du nombre de temps écoulé est affiché en haut de l'écran.

La partie se termine lorsque:
    - Le carré rouge touche à la bordure noire
    - Le carré rouge touche à une sentinelle (ou qu'une sentinelle touche au carrée rouge)
    - Le bouton de la souris est relachée

-- Bugs

Si la taille de la fenêtre est changée, l'affichage n'est plus optimal.

Une fois la partie terminée, une nouvelle partie démarre sans avoir relaché le bouton.
Dans ce cas, les sentinelles ne bougent pas mais le temps avance, et la détection
de collision n'est pas fonctionelle.

Lors de la fin de la partie, le temps final n'est pas affiché séparement du temps
actuel, rendant difficile de savoir son temps réel.








