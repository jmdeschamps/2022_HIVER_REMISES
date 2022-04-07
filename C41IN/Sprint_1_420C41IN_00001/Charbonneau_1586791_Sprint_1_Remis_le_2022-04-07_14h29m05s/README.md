Nom du programme: ORION: Galaxie en Guerre

Auteurs: Carlens Belony, Nicolas Charbonneau, David Demers, Jonathan Frédéric, et William Lemire. 

Date: 07-04-2022

Version ALPHA 

--------------------------------------------------------------------------------------------------------------------------------------------------------------
# ♦ DESCRIPTION ♦

C'est la guerre dans la galaxie d'Orion, déchirée en différentes factions qui luttent pour le contrôle total. En tant que nation interstellaire, vous devrez vous développer en explorant et exploitant les étoiles avoisinantes afin d'augmenter votre puissance. Pour arriver à vos fin, vous pourrez tisser des alliances pour détruire vos ennemis, ou les assujetir. 

La galaxie est composée d'un certain nombre d'étoiles qui ont des ressources finies, que le joueur doit exploiter afin de se développer. Il doit premièrement créer des mines afin d'en extraire les ressources. Elles doivent ensuite être transportées par vaisseau Cargo vers une étoile possédant une usine. Étant donné que les usines sont très coûteuses, vous commencez la partie avec une qui se situe sur l'étoile mère, la première étoile possédée par le joueur. 

Afin de défendre votre système interstellaire, vous pouvez construire des vaisseaux Combattants pour détruire vos ennemis. Tous les vaisseaux peuvent se défendre, mais font moins de dégâts. 

Il y a aussi des vaisseaux d'exploration, ces vaisseaux sont plus rapide que les autres mais font moins de dégats, il peuvent établir un tracé de reconnaissance et prendre possession des étoiles une par une.


--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ FONCTIONNALITÉS DU JEU ♦

## Exploiter
- Le joueur possède un vaisseau de type Cargo qui peut transporter des ressources extraites de la mine vers l'usine la plus près de sa position. Une fois qu'un cargo est pointé vers une étoile pour extraire, son processus d'acheminement de ressources est commencé: il charge son cargo de ressources jusqu'à capacité totale, puis revient automatiquement vers l'usine pour y décharger les ressources extraites, et recommence la boucle jusqu'à contre-indication du joueur.

Les mines possèdent une capacité d'extraction pour les ressources suivantes: or, argent, bronze, et hydrogène. Ces ressources servent à construire les bâtiments. 

Les usines permettent de transformer les ressources extraites en ressources transformées qui peuvent être utilisées pour construire de nouveaux bâtiments et des vaisseaux utilitaires. Pour l'instant, les vaisseaux peuvent être construit gratuitement sur l'etoile mère, cependant, nous voulons modifier cette façon de faire en leur associant un coût et que ce soit les usines qui les construisent. Nous voudrions aussi créer un bâtiment spécifique aux équipements militaires (dont le vaisseau de combat, les tours militaires qui défendent les étoile et les avant-postes qui pourraient permettre d'accroître la communication (dont les rapports) ainsi que de procurer des avantages stratégiques aux vaisseaux.

Les fermes produisent de la nourriture qui est essentiel à la survie de la population. Après un certain nombre de temps, la ferme génère X quantité de nourritures.

Les résidences produisent de la population sur l'étoile. Après un certain nombre de temps, la résidence génère X quantité d'habitants.

## Exterminer
- chaque vaisseau peuvent attaquer les vaisseaux ennemis. Selon leurs caractéristiques, ils possèdent plus ou moins d'attaque/vitesse d'attaque.

## Exploration
- Afin d'explorer la galaxie, le joueur peut créer des vaisseaux de type Explorateur, qui sont plus rapides que les autres et plus économes en carburant. Il faut faire attention lors de l'exploration (ainsi que toute autre activité interstellaire) puisqu'un vaisseau peut manquer de carburant et devenir ainsi inopérable. 

## Expansion
- Le joueur peut conquérir des planètes simplement en se déplaçant jusqu'à elle. Une fois sous le contrôle du joueur, il peut y construire des bâtiments.

## Expérience
- Pour l'instant, il est possible d'améliorer les bâtiments construits, selon un coût associé à un multiple de son niveau.


La fonctionnalité multijoueurs est 100% fonctionnelle.
--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ PROCHAINES ÉTAPES ♦

- Construire tours militaires;
- Construire avant-postes;
- Utilisation de la population pour produire;
- Utilisation d'artefacts pour débloquer des technologies;
- On pourrait ajouter des ressources (ex:eau, autres minéraux);
- Les bâtiments pourraient avoir un coût de production en énergie (pour l'instant hydrogène);
- Lorsqu'on capture une étoile, les bâtiments, les ressources et la population sont transférés au conquérant;
- Trouver une manière de remplir le carburant des vaisseaux.
- conquérir une étoile prend + de temps si elle est possédé par un autre joueur, de plus il faudrait devoir détruire l'avant-poste adverse pour pouvoir prendre possession de celle-ci. 
- implanter rayon de vision.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# ♦ BUGS CONNUS ♦
- le rayon de vision n'est pas encore implanté complètement.
- bug étoile mère adverse visible.
- un bug non décelé arrive parfois lors d'une action envoyé au serveur, erreur : "unhashable list"
