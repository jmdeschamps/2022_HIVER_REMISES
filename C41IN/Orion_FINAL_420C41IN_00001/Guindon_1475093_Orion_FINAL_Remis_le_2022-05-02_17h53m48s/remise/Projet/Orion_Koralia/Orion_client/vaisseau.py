import random
from Id import *
from helper import Helper as hlp
from skillcheck import *


class Vaisseau():
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.espace_cargo = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.type_bonus = "vitesse_explorateur"
        self.cible = 0
        self.rayon = 50
        self.type_cible = None
        self.angle_cible = 0
        self.occupe = False
        self.arriver = {"SystemeSolaire": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte
                        }
        self.ang = 0
        self.planetes_trouver = []

        self.log = []
        self.artefact =""


    # Pour le A.I
    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.systemes)
            self.acquerir_cible(cible, "SystemeSolaire")

    def acquerir_cible(self, cible, type_cible):
        if not self.occupe:
            self.type_cible = type_cible
            self.cible = cible
            self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
            self.occupe = True

    def avancer(self):
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            vitesse = self.vitesse + self.parent.bonus[self.type_bonus]
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, vitesse, self.x, self.y)

            if hlp.calcDistance(self.x, self.y, x, y) <= vitesse:
                type_obj = type(self.cible).__name__
                cible = self.arriver[type_obj]()
                self.occupe = False
                return cible

    def arriver_etoile(self):

        if self.cible.id != self.parent.systeme_mere.id:
            info = [[ self.cible.id[3:]]
                                ,[self.cible.ressources["artefact"]],[""]]
            if self.parent.bonus["log_instant"]:

             self.parent.log.append(info)

            else:
                self.log.append(info)

        self.prendre_artefact()

       # self.parent.parent.parent.uptade_log_vue()
        cible = self.cible
        return ["SystemeSolaire", cible]


    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]

    def prendre_artefact(self):
        if self.cible.ressources["artefact"] != "":
            self.artefact = self.cible.ressources["artefact"]
            self.cible.ressources["artefact"] = ""

class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 0.5
        self.type_bonus = "vitesse_cargo"
        self.cible = 0
        self.ang = 0
        self.livraison_en_cours = False
        self.cargo = {
            "nourriture": 0,
            "or": 0,
            "fer": 0,
            "cuivre": 0,
            "titanite": 0,
            "uranium": 0,
            "hydrogene": 0,
            "azote": 0,
            "xenon": 0,
        }
        self.artefact = ""

    def arriver_etoile(self):
        tab = []
        for key in self.cargo.keys():
            if self.cargo[key]!= 0:
                qte = self.cargo[key]
                tab.append(str(key+" "+str(qte) ))


        info = [[self.cible.id],[ " et j'ai récupéré"],[tab]]
        if self.parent.bonus["log_instant"]:
            self.parent.log.append(info)
        else:
            self.log.append(info)

        cible = self.cible
        if cible is self.parent.systeme_mere:
            self.vider_cargo()
        elif cible in self.parent.systemes_controlees:
            self.check_cargo()
        return ["SystemeSolaire", cible]

    def check_cargo(self):
        estVide = True
        for key in self.cargo.keys():
            if self.cargo[key] != 0:
                estVide = False
        if estVide:
            self.remplir_cargo()
        else:
            self.vider_cargo()

    def remplir_cargo(self):
        for key in self.cargo.keys():
            self.cargo[key] = self.cible.ressources[key]
            self.cible.ressources[key] = 0
        if self.cible.ressources["artefact"] != "":
            self.artefact = self.cible.ressources["artefact"]
            self.cible.ressources["artefact"] = ""

    def vider_cargo(self):
        for key in self.cargo.keys():
            self.cible.ressources[key] += self.cargo[key]
            self.cargo[key] = 0
        if self.artefact != "":
            self.parent.ajouter_artefact(self.artefact)
            self.artefact = ""


class Combat(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
        self.type_bonus = "vitesse_guerre"
        self.cible = 0
        self.ang = 0

    # Conquête
    def arriver_etoile(self):
        resultat_event = False
        if self.cible is not self.parent.systeme_mere:
            conquete = SkillCheck(self.parent, "conquete", None, self.cible)
            if conquete.resultat_event:
                info = [  [self.cible.id], [" et j'ai reussie à conquérir"],[""]]
                if self.parent.bonus["log_instant"]:
                    self.parent.log.append(info)
                else:
                    self.log.append(info)
            else:
                info = [[self.cible.id], ["et j'ai échouer à conquérir"],[""]]
                if self.parent.bonus["log_instant"]:
                    self.parent.log.append(info)
                else:
                    self.log.append(info)

            resultat_event = conquete.resultat_event
        cible = self.cible

        if self.parent.bonus["abilite_conquete_enemie"] is False and self.cible.proprietaire != "":
            resultat_event = False

        return ["SystemeSolaire", cible, resultat_event]
