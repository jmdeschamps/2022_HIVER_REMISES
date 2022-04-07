class Sentier1:
    def __init__(self):
        # Coordonnées de départ
        self.depart_x = 830
        self.depart_y = 0
        # Coordonnées d'arrivée
        self.arrivee_x = 0
        self.arrivee_y = 425
        # Coordonnées des étapes du sentier
        self.chemin = [[830, 0], [830, 175], [700, 175], [700, 80], [190, 80], [190, 315], [305, 315], [305, 210],
                       [405, 210], [405, 315], [495, 315], [495, 210], [595, 210], [595, 430], [710, 430],
                       [710, 285], [830, 285], [830, 515], [470, 515], [470, 425], [0, 425]]
        # Image de la carte
        self.image = "images/Maps/ocean_road.png"
        # Couleur d'arrière-plan
        self.couleurBG = "#cec37e"
