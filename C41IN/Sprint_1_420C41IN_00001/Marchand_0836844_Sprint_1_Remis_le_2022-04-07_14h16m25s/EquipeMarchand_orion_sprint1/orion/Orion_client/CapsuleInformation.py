from CorpsCeleste import *
import Joueur
import Technologie


class CapsuleInformation:
    def __init__(self, vaisseau, contenu):
        self.vaisseau = vaisseau
        self.contenu = contenu
        self.cle = ""
        pass

    def ouvrir_capsule(self, joueur):
        if isinstance(self.contenu, CorpsCeleste):
            self.cle = self.contenu.id
        elif isinstance(self.contenu, Technologie):
            pass
        elif isinstance(self.contenu, Joueur.Joueur):
            pass
        joueur.capsules_ouvertes[str(self.cle)]=self.contenu
        self.vaisseau.capsules.remove(self)





