==============================
||       VIKING RTS         ||
==============================

CHANGELOG:

Mar 28, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Changed window for crafting
- Ajout de la stèle et de la fonction de ses points
- Implémentation complète des fonctionnalités de la ferme

Mar 21, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Nettoyage de code
- Changement de l'incrementation des points/sec
- Changement du principe de la rune dans la stèle
- Ajout de fichiers d'images
- Ajout de la classe Ferme
- Ajout d'une section point pour le joueur

Mar 19, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Ajuster ramassage pour être beaucoup plus lent (1 ressource/s) 

Mar 11, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Changement du spawn de la Stèle
- Ajout de fonctions permettant d'arrêter la partie lorsque le nombre de point Max est atteint
- Changer la logique pour la stèle et les runes et implementer
- Ajouter les éléments graphiques de la Stèle

Mar 8, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Ajuster l'ouvrier pour qu'il cherche des nouvelles ressources plus près de lui
  et aggrandi progressivement son radius de recherche 
- Ajouter nouveau graphique pour la forge

Mar 7, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Ajuster cout de production des batiment
- Redid the crafting UI
- Damage, movement, health, and gathering speed all implemented to be changed by forge
- Crafting now updates existing persos

Mar 6, 2022
¯¯¯¯¯¯¯¯¯¯¯¯
- Ajout de la classe Stele
- Nettoyé le code (enlevé code inutilisé) 
- Ajouter les différents types d'arbres avec des graphiques temporaires
- Implémentation de biomes
- Added functionality to upgrading shoes
- Clique droit et clique gauche sur la caserne pour crée differents persos
- Conversion roche >> metal par fournaise implémenté
- Changed crafting to use new model
- Vue utilise maintenant les ressources dans maison
- Ajuster et simplifier les ressources du HUD
- Simplification des ressources dans l'interface
- Changer les ressources dans maison

==========================================================================================================================================================
 \  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /
  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><
 /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
==========================================================================================================================================================

GUIDE DE JEU:

CONCEPT DE BASE									
									
Les joueurs incarnent des clans de vikings transportés sur des terres inconnus. Chaque clan (joueur) est assigné une rune qu'il doit défendre tout en s'emparant des runes des autres joueurs. Plus un joueur possède de runes sur sa stèle, plus il accumule rapidement la faveur d'Odin. Le joueur gagnant sera celui qui atteint le cap de faveur en premier ou le dernier qui reste dans le match.									
									
									
LES RÈGLES									
									
BUT PRINCIPAL									
Obtenir les points maximum de faveur en premier. Le joueur nécessite 1500 points pour gagner, qu'il accumule à un rythme de 1 point par rune, par seconde. Ainsi donc, un joueur avec une seule rune atteindra le cap de 1500 après 25 minutes de jeu, alors qu'un joueur avec 2 runes l'atteindra en 12.5 minutes, ainsi de suite.									
Afin de capturer la rune d'un adversaire, le joueur doit avoir au moins un guerrier de sélectionné et faire un clic de droit sur la stèle runique de cet adversaire. Après 10 secondes, le guerrier le plus près de la pierre "recoit" la rune et le joueur doit ramener ce guerrier près de sa propre pierre afin que la rune s'y rajoute. Si le guerrier qui porte la rune meurt, la rune retourne automatiquement au joueur auquel elle fut dérobé.									
									
MECHANIQUE SECONDAIRE									
La création d'armes, armures et outils à l'aide de la forge joue un rôle important dans la partie. Le joueur pourra utiliser les ressources qu'il trouve pour augmenter la qualité des outils de ses ouvriers pour qu'il récoltent plus rapidement, ou encore en augmentant la qualité des armes de ses guerriers afin qu'ils infligent plus de dégâts. Le joueur qui accédera à ces équipements de haute qualité en premier aura un avantage considérable sur ses adversaires.									
Il n'y a théoriquement pas de limites au nombre d'améliorations possibles sauf pour les chaussures, qui sont limités à 5 améliorations et donc au double de la vitesse de base. Les améliorations coutent un nombre de plus en plus grand de lingots à chaque niveau; les joueurs devront donc priorisé quels augmentations qu'ils veulent dans une partie car elle ne dure pas assez longtemps pour permettre d'avoir tous les augmentations.									
									
									
LES BIOMES									
LES PLAINES									
Chaque coin de la carte se démarque par une plaine découverte, des terres vertes et à plat parfaites pour la construction d'un village. Les joueurs commencent chacun dans un coin avec une Maison Longue et assez de nourriture pour deux ouvriers. Ils doivent s'installer à leur aise dans ce coin parsemé de sources de nourriture et quelques maigres arbres, avec des forêts noires à proximité.									
									
LES FORÊTS NOIRES									
Source abondante d'arbres de toutes sortes, c'est ici que les joueurs trouveront tout le bois dont ils auront de besoin, la ressource la plus fréquement utilisé pour construire les bâtiments. Les forêts noires se situent à proximités des plaines de départ, vers le centre de la carte.									
									
LES PRAIRIES									
Le biome final au centre de la carte est la source principale de pierre du jeu. Plusieurs rochers énormes s'y trouvent. Étant le biome qui contient la ressource la plus convoitée du jeu mais étant aussi le biome le plus petit, c'est presque garantie que les joueurrs s'y rencontreront et s'affronteront.									
									
									
LES RESSOURCES									
NOURRITURE									
La nourriture est la seule ressource que le joueur possède au début de la partie, en quantité suffisante pour crée 2 ouvriers. Le joueur devra ensuite partir à la recherche de nourriture par lui-même. Plusieurs choix s'offrent à lui:									
									
>	Des daims se promènent librement dans les plaines. Ils méandrent lentement et s'arrêtent fréquement pour brouter. Ils ne fuieront pas les entités du joueur mais se sauveront lorsqu'ils sont attaqués et prendront quelques secondes avant de se calmer et brouter à nouveau.								
>	Plusieurs petites sources végétales existent aussi dans les plaines et les forêts noires tel que des champignons, framboises et bleuets. De nouveaux champignons et arbustres sont générés régulièrement durant la partie.								
>	Les fermes seront la source la plus stable de nourriture pour les joueurs. Contrairement aux sources naturelles de nourriture, les joueurs doivent construire une ferme et y assigner un ouvrier; la ferme produira indéfiniment 100 de nourriture par 50 de bois.								
									
	SOURCE		BIOME		QUANTITÉ DE NOURRITURE						
	framboises	plaines			10						
	champignon	plaines, forets		15						
	bleuets		forets			20						
	daims		partout			50						
	fermes		---			100						
									
BOIS									
Le bois est utilisé en abondance pour construire initialement les bâtisses du joueur, puis devient une ressource taxée régulièrement pour le maintient des fermes et le fonctionnement des fonderies. Les plaines du début contiendront quelques hêtres qui donnent une quantité modeste de bois, mais la vaste majorité des arbres qui donnent le plus grand rendement de bois se situeront, pertinement, dans les forêts noires.									
									
	SOURCE		BIOME	QUANTITÉ DE BOIS						
	Hêtre		plaines		10						
	Bouleau		plaines		15						
	Pin		forets		40						
	Sapin		forets		35						
									
PIERRE									
Une ressource qui sera utilisé initialement pour construire les bâtiments avancés du jeu, la pierre sera aussi grandement convoité car elle peut être convertie en lingots de métal. La pierre se trouve seulement au centre de la carte, en abondance mais aussi dans une zone très restreinte.									
									
	SOURCE		QUANTITÉ DE PIERRE							
	Caillous		100							
	Pierre			200							
	Rocher			300							
									
MÉTAL									
Étant la seule ressource qui n'apparait pas du tout de facon naturelle, les lingots de métal seront sans doute aussi la ressource la plus convoitée. Les lingots sont essentiel au forgeron pour augmenter les capacités des entités des joueurs et sera donc vital tout au long d'un match.									
									
		RESSOURCES REQUISES		TEMPS					
		BOIS	PIERRE						
	1 lingot =	5	10	10 sec					
									
									
LES BÂTIMENTS									
									
LA MAISON LONGUE			100 BOIS					HP 200	DEF 1
Bâtiment de base des vikings qui sert aussi de maison. C'est ici que les ouvriers reviennent par défaut pour déposer leur butin. C'est aussi ici que sont créés les ouvriers en tant que tel. Un joueur peut détenir jusqu'à 10 ouvriers.									
									
LA FONDERIE			50 BOIS, 25 PIERRE					HP 100	DEF 3
Ici, le joueur pourra convertir la pierre qu'il trouve en métal, à un ratio de 10 pierres pour 1 lingot. La fonte elle-même se fait sur un délai de 5 secondes et le joueur peut faire de la fabrication en file d'attente jusqu'à 20 lingots. Ces lingots sont utilisés pour forger des outils, armes et armures, c'est-à-dire les matériaux requis pour l'amélioration des entités du joueur.									
									
LE HALL DE CHASSE			50 BOIS					HP 100	DEF 4
Ici, les vikings redoutables s'entraînent et s'exercent dans l'art de combat. Le joueur peut ici créer des guerriers, hommes féroces qui attaquent avec leurs haches et seront la force offensive principale du joueur, ainsi que les archers, militants émérites capable d'atteindre des cibles lointaines avec précision mais qui se déplacent plus lentement.									
									
LES FERMES DE BAIES			50 BOIS					HP 50	DEF 1
Comme le nom l'indique, il s'agit d'un "bâtiment" qui produit de la nourriture. Tant qu'un ouvrier y reste, il pourra y récolter de la nourriture. Si elle s'épuise, l'ouvrier la renouvelera automatiquement pour un autre 50 bois si disponible.									
									
LA FORGE			50 BOIS, 20 PIERRE, 10 LINGOT					HP 100	DEF 3
C'est par l'entremise de cette bâtisse que le joueur pourra entreprendre l'amélioration de l'équipement pour ses entités. Les améliorations sont divisés en 4 catégories. Il y a premièrement l'équipement de chausse qui augmente la vitesse de marche de tous les entités, les outils qui augmentent la vitesse de récolte de matériaux des ouviers, puis les armes et armures qui augmentent la force et défense des guerriers et archers, respectivement. 									
									
LES AMÉLIORATIONS DE LA FORGE									
									
CATÉGORIE	COÛT								
		Upgrade 1	Upgrade 2	Upgrade 3	Upgrade 4	Upgrade 5	Upgrade 6	Upgrade 7	Upgrade 8	
> Chaussures	1 lingot	2 lingots	4 lingots	6 lingots	10 lingots	---		---		---	
   mouvement	+ 1		+ 1		+ 1		+ 1		+ 1		---		---		---	
> Outils	1 lingot	2 lingots	5 lingots	5 lingots	8 lingots	10 lingots	10 lingots	12 lingots	
   nb items/s	+ 0.4		+ 0.4		+ 0.4		+ 0.4		+ 0.4		+ 0.4		+ 0.4		+ 0.4	
> Armes		2 lingots	3 lingots	4 lingots	5 lingots	6 lingots	10 lingots	14 lingots	18 lingots	
   force	+ 1		+ 1		+ 1		+ 1		+ 1		+ 1		+ 1		+ 1	
> Armures	2 lingots	3 lingots	4 lingots	5 lingots	6 lingots	10 lingots	14 lingots	18 lingots	
   défense	+ 1		+ 1		+ 1		+ 1		+ 1		+ 1		+ 1		+ 1	
									
									
LES ENTITÉS DU JOUEUR									
									
L'OUVRIER			50 NOURRITURE					FORCE 2	HP 40	DEF 0
(Description à venir)									
									
LE GUERRIER			100 NOURRITURE, 10 BOIS				FORCE 7	HP 50	DEF 3
(Description à venir)									
									
L'ARCHER			150 NOURRITURE, 15 BOIS				FORCE 10	HP 30	DEF 1
(Description à venir)

==========================================================================================================================================================
 \  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /
  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><  ><
 /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
==========================================================================================================================================================

MANIPULATIONS DANS L'AIRE DE JEU:

Clic Gauche: sur le terrain:	déselectionne tout

Clic Gauche: sur les persos:	sélectionne le perso,
	affiche un bar jaune, 
	affiche les commandes associées
			
Clic Gauche: sur une ressource si des ouvriers selectionnes:	
	commande d'aller ramasser cette ressource
	NOTE: les ressources disopnibles sont
	arbres -> bois
	roches -> roche
	ferme, arbustes, champignons, daims  -> nourriture
	_________________________________________________________
	| Lorsque la ressource est épuisée, l'ouvrier cherche	|
	| une ressource identique près de lui d'abord, puis	|
	| progressivement plus loin jusqu'à un maximum		|
	¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

Clic roulette: sur le terrain, si perso selectionné
	dirige le perso à cet endroit
			
Majuscule-Clic Gauche,glisse,relâche:
	sur le terrain:	selectionne le groupe
	de vos persos à l'intérieur

CREATION DE BATIMENT (si perso choisi)
Clic Gauche: Le bouton passe au vert (actif)
et
Clic Droit: sur le terrain, construit le batiment choisi
	à cet endroit
	ATTENTION - aucun test est effectué pour
	permettre ou non de le positionner

FORGE
Clic Droit: Affiche le menus d'améliorations
et
Clic Gauche sur item du menu: Améliore la valeur voulu