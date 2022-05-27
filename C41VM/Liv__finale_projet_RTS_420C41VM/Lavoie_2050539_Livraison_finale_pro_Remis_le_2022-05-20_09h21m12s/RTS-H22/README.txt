# RTS Battle for Westnoth

Membres de l'équipe:
	Fabien Juteau-Desjardins
	Patrice Gallant
	Raphaël Lavoie
	Roberto Nightingale Castillo

## ChangeLog
### Sprint 1 
 

- les daims ont été enlevés
- les baies ont été enlevés
- tous les joueurs ont une ZdC (zone de contrôle)
  - les nouveaux batiments peuve seulement être construis dans la ZdC du joueur
  - quand un nouveaux batiment est construit il agrandi la ZdC du joueur dans un carre autour du batiment
- tous les couts sont maintenant en or
- les ferme generent de l'or (les fermes utilise l'image de l'abrie pout l'instant)
- le jeu fonctione maintenant sur un systeme de grille
- la couleur des cases indique leur type
  - les case blanches sont des plaines
  - les case bleux sont de l'eau
  - les case vertes sont des arbres
  - les case rouges sont des batiments
- les case qui ne sont pas ocuper par des batiments on leur coordenées d'écrite par dessus (utile pour le debugage)
- les case qui sont occupées par des batiments on la premiere lettre du type de batiment d'écrite par dessus
- les ouvriers vont beaucoup plus vite (utile pour les test)

### Sprint 2

- Créer des soldats coûte 50 ors et un ouvrier coûte 20 ors
- Ajoutée une fonction de pathfinding pour les persos (un peu funky)
- Ajoutée des scieries, pecheries et mines qui doivent êtres construits près de leurs ressources correspondantes pour générer de l'or
  - Pour l'instant, chaque batiment génère 1 or/sec pour chaque ressource appropriée dans sa zône de controle
- Ajouté des tours qui tirent automatiquement des flèches sur les unités ennemies à proximité (3 carrés)
- Seulement les soldats peuvent attaquer avec une fonction d'aggressivité
  - Les soldats attaquent automatiquement les unités ennemies à proximité (3 carrés)
  - Les batiments peuvent aussi êtres attaqués et sa zone de contrôle est perdu lors de sa destruction
- Code séparé en plus de fichiers afin d'aider la navigation.

### Sprint 3

- Retirer le pathfinding (causait des ralentissements et ne fonctionnait pas vraiment)
- Ajouter les conditions de victoire (être le dernier joueur avec une zone de contrôle)
  - Ajouter un écran de victoire/défaite
- Ajuster la priorité d'aggro des soldats
- Les batiments ont maintenant une barre de vie
  - Les ouvriers peuvent maintenant réparer les batiments (clique droit sur un batiment avec un ouvrier sélectionner)
- Amélioration du multi-select (shift n'est plus nécessaire et aucune unité n'est oublié)
- Sélectionner une unité différente change l'unité active au lieu de l'ajouter à la liste de persos sélectionnés
- Intégration des graphiques pour la version final
- Balance changes
- HOMING ARROWS!
- Autres bugs divers ont été réglés

### Sprint 4
- Embellissement du menu principal ainsi que l'écran de fin de jeu
- Ajouté un texte montrant le coût d'une unitée lors d'un hover sur le bâtiment
- Plusieurs ouvriers peuvent construire en même temps pour accélérer la construction
- Ajouté des raccourcis clavier pour sélectionner un bâtiment à construire
- Tentative non conclusive d'ajouter de la musique (idée abandonnée)
- Balance changes
- Bug fixes

# Instructions: 
- Installer l'interpreteur 3.9 de python sur votre IDE si ce n'est pas déjà fait.
- Demarrez le fichier ../RTS_serveur_B41/start_server.py avec ctrl+shit+F10
- Demarrez le fichier ../RTS_client_B41/RTS_main_2022.py avec ctrl+shit+F10
- Appuyez sur le bouton gauche de la souris pour intérragir avec le village
  - Lorsqu'un ouvrier apparaitra, appuyez dessus avec le bouton gauche de la souris.
  - Selectionnez un batiment avec le bouton gauche de la souris.
  - Selectionnez un emplacement SUR VOTRE ZONE DE CONTRÔLE avec le bouton droit de la souris.
  * Certains bâtiments doivent être construits sur leur ressource correspondante:
        Mine - Roche
        Pêcherie - Eau
        Scierie - Arbres
        Village, Caserne, Ferme - N'importe où
  * Les bâtiments d'exploitation (Mine, Pêcherie, Scierie) génére un montant d'or par seconde
    selon la quantité de ressources dans sa zone de contrôle
    (une Mine entourée de 5 roches produit plus d'or qu'une Mine entourée de 2 roches).
    Une Ferme génére un montant d'or fixe mais peut être construit n'importe où.
- Un clic gauche sur une unité CHANGE l'unité active, pour sélectionner plusieurs unités, glisser la souris en maintenant le clic gauche
- La Caserne génére des soldats.
- Vous gagnez la partie lorsque vous êtes le dernier à posséder une zone de contrôle.

