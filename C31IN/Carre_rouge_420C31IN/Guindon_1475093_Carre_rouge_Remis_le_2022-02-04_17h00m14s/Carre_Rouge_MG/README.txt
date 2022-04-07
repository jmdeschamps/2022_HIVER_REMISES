*****************************************************
	    JEU RED SQUARE V1.0.2
		   READ ME
*****************************************************
		 2022-02-03
*****************************************************
	   Auteur : Maxence Guindon
*****************************************************

1ère partie : décrire le jeu

Bienvenu au jeu du Red Square. Appuyer simplement sur
le carré rouge pour démarrer une partie. Attention, les
sentinelles vont se mettre en marche dès que la partie
démarre. S’il vous touche ou que vous accrochez les
bandes noires, vous perdez la partie. Vous y verrez votre
score en temps. Appuyez sur la boite en bleu pour relancer
le jeu. Sélectionner votre Red Square et vous êtes repartis.

2e partie : décrire les bogues et autres éléments à améliorer

Attention, il s’agit encore d’une version alpha, donc il
y a plusieurs bogues dans le jeu. Tout d’abord, une variable
evt n’est pas définie, mais sans cette erreur, la fonction
qui permet au score de s’afficher ne se lance pas (du moins
les éléments graphiques ne se lancent pas).
De plus, il est possible que vous relanciez une partie trop
rapidement une fois que vous aurez perdu. Il n’y a aucun
timer qui limite le temps avant que le clic sur le rectangle
bleu relance une partie, si vous êtes trop pris par le jeu,
cela risque d’arriver.

Il est également possible que lorsque vous appuyez sur le
rectangle bleu pour relancer une partie, que le score change
simplement pour 0.

3e partie : chose à ajouter

Pour la prochaine version, il reste à faire en sorte que
les scores puissent être sauvegardés sur un fichier externe
et que celui-ci puisse être accessible pour aller lire
chacun des scores que le joueur a eus. Finalement, il reste
aussi à peaufiner le menu pour le rendre plus convivial et
efficace pour le joueur.



