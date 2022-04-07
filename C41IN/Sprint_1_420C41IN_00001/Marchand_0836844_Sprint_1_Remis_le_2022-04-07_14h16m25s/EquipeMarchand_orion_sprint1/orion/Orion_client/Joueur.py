from Id import *
from Ressource import *
from Vaisseau import *


class Joueur:
    def __init__(self, parent, nom, etoile_mere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoile_mere = etoile_mere
        self.etoile_mere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.etoiles_controlees = [
            etoile_mere
        ]
        self.capsules_ouvertes = {}
        self.moral = 50
        self.militaire = 0
        self.diplomatie = 0
        self.science = 0
        self.nourriture = Nourriture(10)
        self.energie = Energie(25)
        self.eau = Eau(50)
        self.fer = Fer(15)
        self.titanium = Titanium(0)
        self.cuivre = Cuivre(5)
        self.credits = 0
        self.flotte = {"Vaisseau": {},
                       "Cargo": {},
                       "Scout": {},
                       "Destroyer": {},
                       "Colonisateur": {},
                       "Spacefighter": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte}

    def entretien_civ(self):
        pass

    # ---- ACTIONS COMMENCENT ICI -----

    # cette méthode est appelé à chaque X frames de la mainloop
    # afin de forcer le Joueur à développer une économie dans « le vert »
    # le coût d'entretien est affecté par la population des planètes possédés,
    # le nombre d'infrastructures, la taille de la flotte de la civilisation, etc...

    def creervaisseau(self, params):
        type_vaisseau = params[0]
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
        elif type_vaisseau == "Colonisateur":
            v = Colonisateur(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
        elif type_vaisseau == "Scout":
            v = Scout(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
        elif type_vaisseau == "Destroyer":
            v = Destroyer(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
        else:
            v = Vaisseau(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(type_vaisseau, v.id)
        return v

    def ciblerflotte(self, params):
        idori, iddesti, type_cible = params
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        # Vérifier l'existence d'objets associés à leur id
        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return
            elif type_cible == "Porte_de_ver":
                cible = None
                for j in self.parent.trou_de_vers:
                    if j.porte_a.id == iddesti:
                        cible = j.porte_a
                    elif j.porte_b.id == iddesti:
                        cible = j.porte_b
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return

    # ---- PAS DES ACTIONS -----

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    # le paramètre chercher_nouveau est réservé au AI. Si arg > 0, cherche nouvelle Étoile
    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile": # voir jouer_prochain_coup de vaisseau
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoiles_controlees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        if rep[1] not in self.etoiles_controlees:
                            self.etoiles_controlees.append(rep[1])
                        if rep[1] == self.etoile_mere:
                            for capsule in j.capsules:
                                capsule.ouvrir_capsule(self)
                        self.parent.parent.afficher_etoile(self.nom, rep[1])
                    elif rep[0] == "Porte_de_ver":
                        pass

# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoile_mere, couleur):
        Joueur.__init__(self, parent, nom, etoile_mere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoiles_controlees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Vaisseau"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1
