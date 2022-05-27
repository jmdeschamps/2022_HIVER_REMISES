# Plague RTS

### AUTEURS: 
- Frédéric Châteauneuf
- Lemar Andar
- Christophe Descary Auclair 
- Bile Esli Jerem Koffi

### DESCRIPTION: 
Un tout nouveau RTS avec un thême artistique jamais vu qui est sûre de vous époustoufler!
Ce jeu ce passe dans le systeme immunitaire d'un humain.
Kidnappé par un scientifique, ce dernier est injecté avec des super virus intelligents, 
ils observent les virus pour voir lequel gagne. 
Ils doivent contaminer la plus grosse partie du corps pour être le virus dominant qui sera capable de contrôler son hôte pour ensuite aller conquérir le monde!!!
Ce jeu se limite à quatre joueur 
Jeu de RTS inspiré du gameplay des Zergs de Starcraft

### CONTROLES: 
- Clique-droit de la souris pour faire apparaitre les ouvriers et pour attaquer les autres NPCs
- Clique-gauche apres avoir choisit une cellule merepour le faire apparaitre sur le territoire qui proliférera le terrioire
- Shift-LeftClick pour selectionner plusieurs troupeau de travailleur pour ensuite leur faire faire une tache 
- Ctrl-MiddleClick pour attaquer les joueurs

### CAMERA
- Mousewheel pour bouger la camera de haut en bas
- Ctrl-Mousewheel pour bouger la camera de droite a gauche
- Ctrl-MouseMotion pour bouger en liberté

### VERSION 0.4 
- Les images qui n'était pas utilisé ont été éliminé
- Les batiments ennemis peuvent etre détruits
- Les batiments morts ont une image quand ils sont mis décommission
- Le code inutile a été enlevé
- Les joueurs ennemi peuvent s'entretuer 
- Le lag quand on joue singleplayer a été éliminé
- Les barres de vie marchent maintenant
- Les ouvriers vont maintenant à la cellule la plus proche
- Les victory screen on été essayé d'être mis


### VERSION 0.3:
- Toutes les entitées sont mis dans leur place spécifié sur la map
- Toutes les entitées ont leur propres couleurs sur la mini-map
- Les joueurs sont aléatoirement mis dans un des quatre coin du jeu
- Les territoires des différents joueurs sont definis par leur couleurs
- Les terriroires sont maintenant fonctionnels à plusieurs joueurs
- Les bâtiments peuvent seulement être construit par les ouvriers
- Les bâtiments on leurs propres fonctions
  - Les watchtowers donnent plus de terrioires que les autres bâtiments
  - Les barracks font spawn les autres sortes de bibites
  - Les turrets font rien pour l'instant (ils vont être utiles plus tard)
- Les NPCs détectent les joueurs et se figent
- La majorité des assets sont présent
- L'interface du splash a été revamped avec le nom de notre jeu
- Ajout de la fonctionalité de mouvement de la caméra en liberté (avec CTRL+MouseMotion)


### VERSION 0.2:
- Les assets des NPCs et des joueurs sont mis a jours pour rentrer dans le theme du jeu
- L'interface du Skill Tree existe (rien dedans pour l'instant)
- Les NPCs existent (ne font rien pour l'instant)
- Les joueurs peuvent faire du PVP
- L'ajout de la fonction "supply"
- Les arbres, les marais et le reste des objets on été mis en commentaire
- Les joueurs peuvent seulement construire des cellules dans son territoire
- Le minimap affiche son territoire


### VERSION 0.1: 
- Revision de l'engin d'actions
- La fonction de territoire existe et peut s'agrandir
- L'ajout de beacon (Objet qui spawn aléatoirement qui agrandit le territoire --> ceci vas etre ajouter plus tard)
- Les joueurs peut maintenant attaquer sans avoir donner la commande si les ennemis sont trop proche d'eux pendant leur mouvement en cours
- Les joueurs se deplacent en formation et ne s'entassent plus un par dessus l'autre
- Renommage des fonctions avec "_"
- Serveur compense pour les distance de cadre de jeu entre les joueurs, dit ATTENTION, le client décremente son cadrejeu et saute les jouer_prochain_coup
- La densité et la répartition des ressources est amélioré, moins dense, moins carré, par plus grande distrbution de petites surfaces qui se rejoignent pour former des régions polygonales
