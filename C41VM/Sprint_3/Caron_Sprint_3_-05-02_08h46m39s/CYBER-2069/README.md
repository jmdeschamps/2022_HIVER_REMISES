# CYBERPOUNK-2069
RTS

----SPRINT 1-----

Ressources :
- nourriture = batterie
- roche = ferraille
- bois = bois
- daim = araignée (possible drop de batterie)
- aurus = bitcoin
- baies = tas de ferraille (possible drop de batterie)
- gem (nouvelle ressource pour upgrades)
- le HUD de droite affiche les bonus actuels appliqués aux stat du joueur (s'incrémente à l'achat de potions chez le marchand)

Marchand :
- Le marchand permet d'acheter des potions avec des gemmes, qui font effet immédiatement en augmentant une certaine statistique du joueuer.
- Il est situé au milieu de la map (position fixe).
- Le prix d'une potion augmente chaque fois qu'on en achète une. 

Tutoriel :
- ramasser des ressources
- construire un bâtiment
- spawn un chien et le faire combattre
- accumuler x bitcoins
- trouver un marchand et lui acheter un item
- trouver 1 gem sur un cadavre


----SPRINT 2-----

Events :
2 types d'event
- Un coffre apparait aléatoirement sur la map (donne des gems).
- Un npc apparait sur la map. On peut lui donner des ressources contre des gems.
-->Un de ces deux events arrive à chaque 10 minutes et il faut entrer dans leur zone de vérification pour compléter l'event.

Troupes ennemis :
- *Ce ne sont pas encore des troupes (1 seul ennemi par troupe), à modifier dans un avenir "proche"*
- Ont l'aspect de monstres verdâtres
- Se déplacent comme les daims.
- Attaquent les ouvriers si ceux-ci entrent de leur champ de vision, et peuvent les tuer.
- À la mort d'une troupe ennemis, on récolte des gemmes sur le cadavre, plutôt que de la nourriture.
- L'image utilisée lors de l'état de mort sera changé dans le prochain sprint.


----SPRINT 3-----

Boss :
- Ajout d'un boss avec un point d'apparition fixe, dès l'ouverture du jeu
- Possède une zone d'attaque délimitée par un cercle  rouge (lorsqu'un ouvrier la pénètre, le boss l'attaque)
- Pour l'instant le boss attaque une cible à la fois

Images :
- Modification des images de bâtiment
- Modification des images des projectiles et des troupes ennemis
- Modification des images des ouvriers et des soldats
- Modification des images des baies et des daims

Autres ajouts : 
- Barre de vie fonctionnelle pour tout être vivant de la partie 
