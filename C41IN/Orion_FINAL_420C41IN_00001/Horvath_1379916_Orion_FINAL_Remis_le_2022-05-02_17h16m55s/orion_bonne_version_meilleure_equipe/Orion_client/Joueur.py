from Batiment import *
from Ressource import *
from Vaisseau import *
from helper import Helper as hlp
from Annonce import *


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
        self.technologies = []
        self.capsules_ouvertes = {}
        self.moral = 50
        self.militaire = 0
        self.diplomatie = 0
        self.science = 200
        self.credits = 0
        self.nourriture = Nourriture(10)
        self.limite_nourriture = 500
        self.energie = Energie(30)
        self.eau = Eau(350)
        self.fer = Fer(200)
        self.titanium = Titanium(200)
        self.cuivre = Cuivre(200)
        self.exclu = False
        self.compteur = 0
        self.isIa = False

        self.generation_passive = {
            "moral": 5,
            "science": 5,
            "diplomatie": 10,
            "nourriture": 10,
            "eau": 5,
            "energie": 5,
            "fer": 5,
            "titanium": 5,
            "cuivre": 5
        }

        self.cout_passif = {
            "nourriture": 2,
            "eau": 2
        }

        self.niveaux = {
            "Cargo": 1,
            "Scout": 1,
            "Destroyer": 1,
            "Colonisateur": 1,
            "Spacefighter": 1,
            "Raffinerie": 1,
            "Ferme": 1,
            "Usine": 1,
            "Laboratoire": 1,
            "SatDefensif": 1,
            "SatVision": 1
        }

        self.ressources_possession = {
            Fer.nom: self.fer,
            Titanium.nom: self.titanium,
            Cuivre.nom: self.cuivre
        }

        self.flotte = {
            "Vaisseau": {},
            "Cargo": {},
            "Scout": {},
            "Destroyer": {},
            "Colonisateur": {},
            "Spacefighter": {}
       }

        self.satel = {"SAT Defensif": {},
                      "SAT Vision": {},
                      "SAT Kamikaze": {}}

        self.batiment = {"Raffinerie": {},
                         "Ferme": {},
                         "Laboratoire": {},
                         "Usine": {}}

        self.merveille = {"Merveille": {}}

        self.figure = {"Figure": {}}

        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte,
                        "creersatellite": self.creersatellite,
                        "acquerir_tech": self.acquerir_tech,
                        "creerbatiment": self.creerbatiment,
                        "creerfigure": self.creerfigure,
                        "creermerveille": self.creermerveille,
                        "ajouter_echange": self.ajouter_echange,
                        "retirer_echange": self.retirer_echange,
                        "accepter_echange": self.accepter_echange,
                        "proposer_alliance":self.proposer_alliance,
                        "accepter_alliance":self.accepter_alliance,
                        "rompre_alliance":self.rompre_alliance,
                        "refuser_alliance":self.refuser_alliance,
                        "ajouter_annonce":self.ajouter_annonce
                        }

        self.alliances = []
        self.demandes_alliances =[]

        self.demande_envoye = 0
        self.demande_recu = 0

        self.message_envoye = 0
        self.message_recu = 0
        self.annonce = None

    def proposer_alliance(self,param):
        self.parent.joueurs[param[1]].demandes_alliances.append(param[0])
        texte = param[0] + " vous propose une alliance"
        action = [param[0], "ajouter_annonce", [texte, param[1]]]
        self.parent.parent.actionsrequises.append(action)

    def refuser_alliance(self,param):
        texte=param[0]+" a refusé votre demande"
        action = [param[0], "ajouter_annonce", [texte, param[1]]]
        self.parent.parent.actionsrequises.append(action)
        self.parent.joueurs[param[0]].demandes_alliances.remove(param[1])

    def ajouter_annonce(self,param):
        self.parent.joueurs[param[1]].annonce = Annonce(param[0])

    def accepter_alliance(self,param):
        self.parent.joueurs[param[1]].alliances.append(param[0])
        self.parent.joueurs[param[0]].demandes_alliances.remove(param[1])
        self.parent.joueurs[param[0]].alliances.append(param[1])
        texte = param[0] + " a accepté votre demande d'alliance"
        action = [param[0], "ajouter_annonce", [texte, param[1]]]
        self.parent.parent.actionsrequises.append(action)

    def rompre_alliance(self,param):
        texte = param[0] + " a rompu son alliance avec vous"
        action = [param[0], "ajouter_annonce", [texte, param[1]]]
        self.parent.parent.actionsrequises.append(action)
        self.parent.joueurs[param[1]].alliances.remove(param[0])
        self.parent.joueurs[param[0]].alliances.remove(param[1])

    def tuer_satellite(self,satellite):
        if isinstance(satellite,SatKamikaze):
            self.satel["SAT Kamikaze"].pop(satellite.id)
        elif isinstance(satellite,SatKamikaze):
            self.satel["SAT Vision"].pop(satellite.id)
        elif isinstance(satellite,SatDefensif):
            self.satel["SAT Defensif"].pop(satellite.id)

    def tuer_vaisseau(self,vaisseau):
        try:
            if isinstance(vaisseau, Cargo):
                self.flotte["Cargo"].pop(vaisseau.id)
            elif isinstance(vaisseau, Scout):
                self.flotte["Scout"].pop(vaisseau.id)
            elif isinstance(vaisseau, Destroyer):
                self.flotte["Destroyer"].pop(vaisseau.id)
            elif isinstance(vaisseau, Colonisateur):
                self.flotte["Colonisateur"].pop(vaisseau.id)
            elif isinstance(vaisseau, Spacefighter):
                self.flotte["Spacefighter"].pop(vaisseau.id)
            try:
                if isinstance(vaisseau, Vaisseau):
                    self.flotte["Vaisseau"].pop(vaisseau.id)
            except:
                pass
        except:
            pass

    def acquerir_tech(self, param):
        self.parent.technologies[param[0]].acquerir(self)

    def accepter_echange(self,param):
        self.parent.marche.accepter_offre(self.nom, param)
        self.parent.parent.vue.marche_vue.marche_root.destroy()
        self.parent.parent.vue.marche_vue.ouvrir_marche()

    def retirer_echange(self,param):
        self.parent.marche.retirer_echange(self.nom, param)
        self.parent.parent.vue.marche_vue.marche_root.destroy()
        self.parent.parent.vue.marche_vue.ouvrir_marche()
        

    def ajouter_echange(self,param):
        self.parent.marche.ajouter_echange(self.nom,param)
        self.parent.parent.vue.marche_vue.marche_root.destroy()
        self.parent.parent.vue.marche_vue.ouvrir_marche()

    def entretien_civ(self):
        capacite_metaux = 9999
        # pour la version livrée:
        # capacite_metaux = 0
        # for etoile in self.etoiles_controlees:
        #     for batiment in etoile.batiment:
        #         if isinstance(batiment, Raffinerie):
        #             capacite_metaux += batiment.capacite
        for batiment in self.batiment.items():
            if batiment[0] == "Raffinerie":
                for b_id, b_object in batiment[1].items():
                    capacite_metaux += b_object.capacite
            if batiment[0] == "Ferme":
                for b_id, b_object in batiment[1].items():
                    self.generation_passive["nourriture"] += b_object.generation
                    self.generation_passive["eau"] += b_object.generation
            if batiment[0] == "Laboratoire":
                for b_id, b_object in batiment[1].items():
                    print(self.generation_passive["science"])
                    self.generation_passive["science"] += b_object.gen_science
                    print(self.generation_passive["science"])


        self.moral = hlp.clamp(self.moral + self.generation_passive["moral"], 0, 100)
        self.science = hlp.clamp(self.science + self.generation_passive["science"], 0, 9999)
        self.diplomatie = hlp.clamp(self.science + self.generation_passive["diplomatie"], 0, 9999)
        self.nourriture.quantite = hlp.clamp(self.nourriture.quantite + self.generation_passive["nourriture"], 0, 9999)
        self.eau.quantite = hlp.clamp(self.eau.quantite + self.generation_passive["eau"], 0, 9999)
        self.energie.quantite = hlp.clamp(self.energie.quantite + self.generation_passive["energie"], 0, 9999)
        self.fer.quantite = hlp.clamp(self.fer.quantite + self.generation_passive["fer"], 0, capacite_metaux)
        self.titanium.quantite = hlp.clamp(self.titanium.quantite + self.generation_passive["titanium"], 0, capacite_metaux)
        self.cuivre.quantite = hlp.clamp(self.cuivre.quantite + self.generation_passive["cuivre"], 0, capacite_metaux)

        self.nourriture.quantite = hlp.clamp(self.nourriture.quantite - self.cout_passif["nourriture"], 0, 9999)
        self.eau.quantite = hlp.clamp(self.eau.quantite - self.cout_passif["eau"], 0, 9999)

        if self.nourriture == 0:
            self.moral = hlp.clamp(self.moral - self.parent.penalite_moral, 0, 100)

        if self.moral == 0:
            self.exclu = True
            self.annonce = Annonce(self, "Vous avez perdu!")

    # ---- ACTIONS COMMENCENT ICI -----
    # cette méthode est appelé à chaque X frames de la mainloop
    # afin de forcer le Joueur à développer une économie dans « le vert »
    # le coût d'entretien est affecté par la population des planètes possédés,
    # le nombre d'infrastructures, la taille de la flotte de la civilisation, etc...

    def creervaisseau(self, params):
        type_vaisseau = params[0]

        for i in self.etoiles_controlees:
            try:
                if i.id == params[1]:
                    if i.possede_usine:
                        if type_vaisseau == "Cargo":
                            v = Cargo(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
                        elif type_vaisseau == "Colonisateur":
                            v = Colonisateur(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
                        elif type_vaisseau == "Scout":
                            v = Scout(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
                        elif type_vaisseau == "Destroyer":
                            v = Destroyer(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
                        elif type_vaisseau == "Spacefighter":
                            v = Spacefighter(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)
                    else:
                        self.annonce = Annonce("L'étoile ne possède pas d'usine")
            except:
                pass

            if self.isIa:
                v = Vaisseau(self, self.nom, self.etoile_mere.x + 10, self.etoile_mere.y)

            self.flotte[type_vaisseau][v.id] = v

            if self.nom == self.parent.parent.mon_nom:
                self.parent.parent.lister_objet(type_vaisseau, v.id)
            return v

    def creersatellite(self, params):

        self.compteur = 0
        for i,j in self.satel.items():
            for _ in j.items():
                self.compteur += 1

        if self.compteur < self.etoile_mere.max_satellite:
            type_satellite = params[0]
            if type_satellite == "SAT Defensif":
                s = SatDefensif(self, self.nom, self.etoile_mere)
            elif type_satellite == "SAT Vision":
                s = SatVision(self, self.nom, self.etoile_mere)
            elif type_satellite == "SAT Kamikaze":
                s = SatKamikaze(self, self.nom, self.etoile_mere)

            if s.verification_creation():
                self.satel[type_satellite][s.id] = s
                return s

    def creerbatiment(self, params):

        self.compteur = 0

        for i in self.etoiles_controlees:
            if i.id == params[1]:
                for m, n in i.batiment.items():
                    for _ in n.items():
                        self.compteur += 1

                if self.compteur < i.max_batiment:
                    type_batiment = params[0]
                    if type_batiment == "Raffinerie":
                        p = Raffinerie(self, self.nom, i)
                    elif type_batiment == "Ferme":
                        p = Ferme(self, self.nom, i)
                    elif type_batiment == "Laboratoire":
                        p = Laboratoire(self, self.nom, i)
                    elif type_batiment == "Usine":
                        p = Usine(self, self.nom, i)

                    if p.verification_creation():
                        self.batiment[type_batiment][p.id] = p
                        i.batiment[type_batiment][p.id] = p
                        return p
    def creerfigure(self, params):

        self.compteur = 0
        for i,j in self.figure.items():
            for _ in j.items():
                self.compteur += 1

        if self.compteur < self.etoile_mere.max_figure_importance:
            type_figure = params[0]
            if type_figure == "Figure":
                s = FigureImportance(self, self.nom, self.etoile_mere)

            if s.verification_creation():
                self.figure[type_figure][s.id] = s
                return s

    def creermerveille(self, params):

        self.compteur = 0

        for i in self.etoiles_controlees:
            if i.id == params[1]:

                for m,n in i.merveille.items():
                    for _ in n.items():
                        self.compteur += 1

                if self.compteur < i.max_merveille:

                    type_merveille = params[0]
                    if type_merveille == "Merveille":
                        s = Merveille(self, self.nom, i)
                    self.merveille[type_merveille][s.id] = s

                    if s.verification_creation():
                        self.merveille[type_merveille][s.id] = s
                        i.merveille[type_merveille][s.id] = s
                        return s

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
            elif type_cible == "Flotte":
                for joueur in self.parent.joueurs.values():
                    if joueur.nom == self.nom:
                        continue
                    else:
                        for type_flotte in joueur.flotte.keys():
                            for id_flotte in joueur.flotte.get(type_flotte).keys():
                                if id_flotte == iddesti:
                                    cible = joueur.flotte.get(type_flotte).get(id_flotte)
                                    ori.acquerir_cible(cible, type_cible)

    def verif_alliance_possible(self):
        alliance = self.amis.relation
        if alliance > 0.4:
            self.amis.proposer_alliance(1)
        return alliance

    # ---- PAS DES ACTIONS -----

    def jouer_prochain_coup(self):
        self.avancer_flotte()
        self.avancer_satellite()

    # le paramètre chercher_nouveau est réservé au AI. Si arg > 0, cherche nouvelle Étoile
    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            try:
                for j in self.flotte[i]:
                    j = self.flotte[i][j]
                    rep = j.jouer_prochain_coup(chercher_nouveau)
                    if rep:
                        if rep[0] == "Etoile":  # voir jouer_prochain_coup de vaisseau
                            # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                            #       quand on l'attribue aux etoiles_controlees
                            #       et que ce passe-t-il si l'etoile a un proprietaire ???
                            if rep[1] not in self.etoiles_controlees:
                                self.etoiles_controlees.append(rep[1])
                            if rep[1] == self.etoile_mere:
                                for capsule in j.capsules:
                                    capsule.ouvrir_capsule(self)
                            self.parent.parent.afficher_etoile(self.nom, rep[1])
                        elif rep[0] == "PorteVers":
                            pass
            except:
                print("Un vaisseau n'est pas retrouvé car a été éliminé au même moment (fast patch)")  # RuntimeError

    def avancer_satellite(self):
        try :
            for i in self.satel:
                for j in self.satel[i]:
                    j = self.satel[i][j]
                    if isinstance(j, SatDefensif):
                        j.deplacerSatellite()
                        j.verification_range_vaisseau()
                    elif isinstance(j, SatVision):
                        j.deplacerSatellite()
                    elif isinstance(j, SatKamikaze):
                        if j.deplacement_sur_planete:
                            j.deplacerSatellite()
                            j.verification_range_kamikaze()
                        else:
                            j.suivre_vaisseau()
        except: pass

    def nouvelle_annonce(self, message):
        self.annonce = Annonce(self, message)


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoile_mere, couleur):
        Joueur.__init__(self, parent, nom, etoile_mere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20
        self.commencer = 0
        self.IASAT = []
        self.isIa = True

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoiles_controlees.append(rep[1])
        self.avancer_flotte(1)

        if self.commencer == 0:
            self.IASAT.append(self.creersatellite(["SAT Defensif"]))
            self.commencer += 1
        self.avancer_satellite()

        if self.cooldown == 0:

            v = self.creervaisseau(["Vaisseau"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")

            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1
