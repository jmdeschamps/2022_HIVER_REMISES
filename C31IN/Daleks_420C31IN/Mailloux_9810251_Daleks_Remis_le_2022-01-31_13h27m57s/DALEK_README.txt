
<==============31 janvier 2022============>
<==================Dalek_v7===============>

Version console du jeu Dalek.  

Au démarage du jeu, les scores sont chargés.

Les options offertes avant d'initialiser une partie sont de pouvoir spécifier les dimensions du 
tableau, afficher les scores (automatiquement sauvegardés dans un fichier high_scores.txt lorsqu'on quitte), quitter sinon démarrer un partie.

Lorsque la partie démarre, les différents niveaux de diffcultés offerts sont 

débutant: le docteur se téléporte à plus d'une case des Daleks
intermédiare: le docteur se téléporte peut-être à côté d'un Dalek
expert: le docteur peut se téléporter sur un Dalek et mourir.

Vous n'avez qu'une seule vie et vous n'avez qu'un seul "zapper" au début du premier niveau.

Un "zapper" vous permet de détruire tous les Daleks qui sont à une case adjacente au docteur.

Si vous n'utilisez pas votre zapper et terminez le niveau, vous le conservez pour le prochain niveau
en plus d'en gagner un autre: cela dit, vous commencez toujours un niveau
avec au moins un zapper.

Dans le jeu vous pouvez vous déplacer d'une seule case dans n'importe qu'elle direction 
et vous ne pouvez pas sortir du tableau. Les Daleks se rapprochent toujours de vous. 
En plus du zapper, vous pouvez détruire les Daleks en faisant en sorte qu'ils se retrouvent
sur la même case, ils se transforment alors en tas de ferraille. Si un Dalek percute 
un tas de ferraille existant, il est détruit. Finalement, le docteur peut se téléporter
à tout moment, mais attention aux contraintes (débutant, intermédiare, expert).
Si la densité de Dalek devient trop élévée, le tableau gagne une colonne et une rangée supplémentaire.

Vous gagnez 5 points par Dalek détruit.

Il y a 5 Daleks de plus par niveau.

Bonne chance!!!

<=========================================>

Bugs et implémentation futures:

	- Décharger le modèle de certaines tâches dédiées à la vue.
	- Peaufiner le graphisme		
	
<=========================================>

Mathieu Mailloux
Jessica Chan