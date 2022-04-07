
import random


class SkillCheck:
    def __init__(self,joueur, opposant=None):
        self.joueur = joueur
        self.opposant = opposant
        self.domination_check = 50  # savoir si on joueur domine l'autre ou pas
        self.resultat_event = None
        self.gagnant_versus = None
        self.skill_check()


    def skill_check(self):
        if self.opposant is None:
            self.skill_check_evenement()
        else:
            self.skill_check_versus()

    def skill_check_evenement(self):
        bonus_joueur = self.joueur.bonus.get(self.activite)
        nbr = random.randint(1, 100)
        if 1 <= nbr <= bonus_joueur:
            self.resultat_event = True
        else :
            self.resultat_event = False


    def skill_check_versus(self):
        bonus_joueur = self.joueur.bonus.get(self.activite)
        bonus_opposant = self.joueur.bonus.get(self.activite)

        if abs(bonus_joueur - bonus_opposant) <= self.domination_check:
            if bonus_joueur > bonus_opposant:
                self.gagnant_versus = self.joueur
            else:
                self.gagnant_versus = self.opposant

        nbr_joueur = random.randrange(bonus_joueur, 100)
        nbr_opposant = random.randrange(bonus_opposant, 100)
        if nbr_joueur < nbr_opposant:
            self.gagnant_versus = self.joueur
        elif nbr_joueur > nbr_opposant:
            self.gagnant_versus = self.opposant
        else:
            self.skill_check_versus()
