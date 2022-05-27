CYBERPOUNK-2069					NAMES : Jane Caron,  Matis Gaetjens, Gabriel Tremblay, Antonin Lenoir

----SPRINT 1-----
MARCHAND
- Le marchand permet d'acheter des potions avec des gemmes, qui font effet immédiatement en augmentant une certaine statistique du joueuer.
- Il est situé au milieu de la map (position fixe).
- Le prix d'une potion augmente chaque fois qu'on en achète une. 

TUTORIEL
Liste des quêtes du tutoriel ;
- Ramasser des ressources
- Construire un bâtiment
- Spawn un chien et le faire combattre
- Accumuler x bitcoins
- Trouver un marchand et lui acheter un item
- Trouver 1 gem sur un cadavre

----SPRINT 2-----
EVENTS
2 types d'event ;
- Un coffre apparait aléatoirement sur la map (donne des gems).
- Un npc apparait sur la map. On peut lui donner des ressources contre des gems. 
 -->Un de ces deux events arrive à chaque 10 minutes et il faut entrer dans leur zone de vérification pour compléter l'event.

TROUPES ENNEMIS
- *Ce ne sont pas encore des troupes (1 seul ennemi par troupe), à modifier dans un avenir "proche"*
- Ont l'aspect de monstres verdâtres
- Se déplacent comme les daims.
- Attaquent les ouvriers si ceux-ci entrent de leur champ de vision, et peuvent les tuer.
- À la mort d'une troupe ennemis, on récolte des gemmes sur le cadavre, plutôt que de la nourriture.
- L'image utilisée lors de l'état de mort sera changé dans le prochain sprint.

----SPRINT 3-----
BOSS
- Ajout d'un boss avec un point d'apparition fixe, dès l'ouverture du jeu
- Possède une zone d'attaque délimitée par un cercle rouge (lorsqu'un ouvrier la pénètre, le boss l'attaque)
- Pour l'instant le boss attaque une cible à la fois

IMAGES
- Modification des images de bâtiment
- Modification des images des projectiles et des troupes ennemis
- Modification des images des ouvriers et des soldats
- Modification des images des baies et des daims
- Modification du boss avec un gif 
- Modification du marchand avec un gif
- Modification de l'ambiance du jeu

AUTRES AJOUTS
- Barre de vie fonctionnelle pour tout être vivant de la partie

----SPRINT 4-----
BUG FIXING :
- Possible d'attaquer le boss après avoir changer son image par un gif
- Si un ouvrier est interrompu en court de construction, la construction du bâtiment est annulée
- Si plusieurs ouvriers sont sélectionnés lorsqu'on veut construire, un seul ira construire
- Les menus de construction et de marchand disparaissent aux bons moments et n'apparaissent plus les 2 en même temps
- Récolte de cadavre possible en cliquant (même après interruption)
- Barres de vie et de bouclier bien fonctionnelles
- Déplacements et chasse des unités

AJOUTS ET MODIFICATIONS SUPPLÉMENTAIRES :
- Liste des unités que l'on peut utiliser dans le jeu : Ouvrier, Balliste (drone), Druide, Soldat.
- Toutes les unités peuvent attaquer, se faire attaquer et se déplacer
- Ajout de coûts pour créer une unité (si on n'a plus de ressource et aucune unité, 1 ouvrier peut être créer gratuitement)
- Intégration des stats de bouclier et d'attaque pour tout vivant de la partie (une meilleure unité attaque plus fort et coute plus chère à produire)
- Il n'est pas possible qu'un joueur apparaisse dans la zone du boss
- Les troupes ennemis apparaissent graduellement au cours de la partie (+1 chaque 30 secondes, avec un max de 20 troupes ennemis sur la map)
- Message de fin de partie lorsqu'on tue le boss (non complétée malheureusement)


-----Tout ce qu'il faut savoir pour jouer-----

Pour commencer, vous pouvez cliquer sur le batiment mère pour avoir un ouvrier (ils coûtent 10 cryptos chaque). Il vous 
sert à construire vos batiments pour creer toutes les autres unités et récolter des ressources. Pour construire les batiments vous devez cliquer sur
l'ouvrier et choisir le batiment que vous voulez faire. Une fois le batiment construit, vous pouvez cliquer sur ce batiment
pour faire apparaitre l'unité associée à ce batiment. On a aussi implémenté des quêtes que vous pouvez faire sous forme de tutoriel, elles vous aident
à apprendre à jouer (pour voir si vous avez fini une quête, vous devez fermer et réouvrir le fichier de quêtes avec le 
bouton en haut à droite dans le HUD). Pour la première quête, vous devez avoir 300 batteries au total
et pour les obtenir vous devez tuer les petits robots passifs de couleur blanche, noire et rouge. Pour la deuxième vous devez 
seulement construire un batiment comme expliquer précédemment. Pour la troisième, vous devez faire apparaitre un drone. Pour se faire, 
vous devez construire le dernier batiment que vous voyez (un drone coûte 50 cryptos). Pour la quatrième, vous devez aller ramasser 100 
bitcoins (20 par ressource présente sur la map). Pour la cinquième, vous devez tuer un ennemi (il ressemble à des soldats tout en noir tenant une arme). 
Une fois la cible tuée, vous devez ramener les gems au batiment mère. Pour la dernière, vous devez trouver le marchand (c'est un batiment écrit "SHOP" dessus) 
et en cliquant dessus vous allez pouvoir lui acheter des potions qui ont plusieurs effets. Une fois toutes ces quêtes fini vous aurez compris l'essentiel
du jeu. Vous pourrez essayer de vaincre le boss pour finir le jeu (fin de partie non complétée malheureusement).
