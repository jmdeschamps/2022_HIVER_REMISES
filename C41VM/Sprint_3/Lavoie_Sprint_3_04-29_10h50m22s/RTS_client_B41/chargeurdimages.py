## - Encoding: UTF-8 -*-
# changer pour changeurdimages

# Refactoriser pour lire le contenu de dossier

from tkinter import PhotoImage
# toutes les images devraient �tre ins�r�es ici

import os, os.path


def chargerimages2():
    images = {
        'siteX': PhotoImage(file='images/divers/siteX.png'),
        'javelotGH': PhotoImage(file='images/divers/javelotGH.png'),
        'javelotGB': PhotoImage(file='images/divers/javelotGB.png'),
        'javelotDH': PhotoImage(file='images/divers/javelotDH.png'),
        'javelotDB': PhotoImage(file='images/divers/javelotDB.png'),

        'plaine': PhotoImage(file='images/terrain/plaine.png'),
        'arbre': PhotoImage(file='images/terrain/arbre.png'),
        'roche': PhotoImage(file='images/terrain/roche.png'),
        'eau': PhotoImage(file='images/terrain/eau.png'),

        'V_ouvrier': PhotoImage(file='images/vert/V_ouvrier.png'),
        'V_soldat': PhotoImage(file='images/vert/V_soldat.png'),
        'V_Village': PhotoImage(file='images/vert/V_village.png'),
        'V_Caserne': PhotoImage(file='images/vert/V_caserne.png'),
        'V_Ferme': PhotoImage(file='images/vert/V_ferme.png'),
        'V_Mine': PhotoImage(file='images/vert/V_mine.png'),
        'V_Scierie': PhotoImage(file='images/vert/V_scierie.png'),
        'V_Pecherie': PhotoImage(file='images/vert/V_pecherie.png'),
        'V_Tour': PhotoImage(file='images/vert/V_tour.png'),

        'V_ouvrier_attack0': PhotoImage(file='images/vert/V_ouvrier_attack0.png'),
        'V_ouvrier_attack1': PhotoImage(file='images/vert/V_ouvrier_attack1.png'),
        'V_ouvrier_attack2': PhotoImage(file='images/vert/V_ouvrier_attack2.png'),

        'V_soldat_attack0': PhotoImage(file='images/vert/V_soldat_attack0.png'),
        'V_soldat_attack1': PhotoImage(file='images/vert/V_soldat_attack1.png'),
        'V_soldat_attack2': PhotoImage(file='images/vert/V_soldat_attack2.png'),

        'J_ouvrier': PhotoImage(file='images/jaune/J_ouvrier.png'),
        'J_soldat': PhotoImage(file='images/jaune/J_soldat.png'),
        'J_Village': PhotoImage(file='images/jaune/J_village.png'),
        'J_Caserne': PhotoImage(file='images/jaune/J_caserne.png'),
        'J_Ferme': PhotoImage(file='images/jaune/J_ferme.png'),
        'J_Mine': PhotoImage(file='images/jaune/J_mine.png'),
        'J_Scierie': PhotoImage(file='images/jaune/J_scierie.png'),
        'J_Pecherie': PhotoImage(file='images/jaune/J_pecherie.png'),
        'J_Tour': PhotoImage(file='images/jaune/J_tour.png'),

        'J_ouvrier_attack0': PhotoImage(file='images/jaune/J_ouvrier_attack0.png'),
        'J_ouvrier_attack1': PhotoImage(file='images/jaune/J_ouvrier_attack1.png'),
        'J_ouvrier_attack2': PhotoImage(file='images/jaune/J_ouvrier_attack2.png'),

        'J_soldat_attack0': PhotoImage(file='images/jaune/J_soldat_attack0.png'),
        'J_soldat_attack1': PhotoImage(file='images/jaune/J_soldat_attack1.png'),
        'J_soldat_attack2': PhotoImage(file='images/jaune/J_soldat_attack2.png'),

        'B_ouvrier': PhotoImage(file='images/bleu/B_ouvrier.png'),
        'B_soldat': PhotoImage(file='images/bleu/B_soldat.png'),
        'B_Village': PhotoImage(file='images/bleu/B_village.png'),
        'B_Caserne': PhotoImage(file='images/bleu/B_caserne.png'),
        'B_Ferme': PhotoImage(file='images/bleu/B_ferme.png'),
        'B_Mine': PhotoImage(file='images/bleu/B_mine.png'),
        'B_Scierie': PhotoImage(file='images/bleu/B_scierie.png'),
        'B_Pecherie': PhotoImage(file='images/bleu/B_pecherie.png'),
        'B_Tour': PhotoImage(file='images/bleu/B_tour.png'),

        'B_ouvrier_attack0': PhotoImage(file='images/bleu/B_ouvrier_attack0.png'),
        'B_ouvrier_attack1': PhotoImage(file='images/bleu/B_ouvrier_attack1.png'),
        'B_ouvrier_attack2': PhotoImage(file='images/bleu/B_ouvrier_attack2.png'),

        'B_soldat_attack0': PhotoImage(file='images/bleu/B_soldat_attack0.png'),
        'B_soldat_attack1': PhotoImage(file='images/bleu/B_soldat_attack1.png'),
        'B_soldat_attack2': PhotoImage(file='images/bleu/B_soldat_attack2.png'),

        'R_ouvrier': PhotoImage(file='images/rouge/R_ouvrier.png'),
        'R_soldat': PhotoImage(file='images/rouge/R_soldat.png'),
        'R_Village': PhotoImage(file='images/rouge/R_village.png'),
        'R_Caserne': PhotoImage(file='images/rouge/R_caserne.png'),
        'R_Ferme': PhotoImage(file='images/rouge/R_ferme.png'),
        'R_Mine': PhotoImage(file='images/rouge/R_mine.png'),
        'R_Scierie': PhotoImage(file='images/rouge/R_scierie.png'),
        'R_Pecherie': PhotoImage(file='images/rouge/R_pecherie.png'),
        'R_Tour': PhotoImage(file='images/rouge/R_tour.png'),

        'R_ouvrier_attack0': PhotoImage(file='images/rouge/R_ouvrier_attack0.png'),
        'R_ouvrier_attack1': PhotoImage(file='images/rouge/R_ouvrier_attack1.png'),
        'R_ouvrier_attack2': PhotoImage(file='images/rouge/R_ouvrier_attack2.png'),

        'R_soldat_attack0': PhotoImage(file='images/rouge/R_soldat_attack0.png'),
        'R_soldat_attack1': PhotoImage(file='images/rouge/R_soldat_attack1.png'),
        'R_soldat_attack2': PhotoImage(file='images/rouge/R_soldat_attack2.png'),

        'O_ouvrier': PhotoImage(file='images/orange/O_ouvrier.png'),
        'O_soldat': PhotoImage(file='images/orange/O_soldat.png'),
        'O_Village': PhotoImage(file='images/orange/O_village.png'),
        'O_Caserne': PhotoImage(file='images/orange/O_caserne.png'),
        'O_Ferme': PhotoImage(file='images/orange/O_ferme.png'),
        'O_Mine': PhotoImage(file='images/orange/O_mine.png'),
        'O_Scierie': PhotoImage(file='images/orange/O_scierie.png'),
        'O_Pecherie': PhotoImage(file='images/orange/O_pecherie.png'),
        'O_Tour': PhotoImage(file='images/orange/O_tour.png'),

        'o_ouvrier_attack0': PhotoImage(file='images/orange/o_ouvrier_attack0.png'),
        'o_ouvrier_attack1': PhotoImage(file='images/orange/o_ouvrier_attack1.png'),
        'o_ouvrier_attack2': PhotoImage(file='images/orange/o_ouvrier_attack2.png'),

        'O_soldat_attack0': PhotoImage(file='images/orange/O_soldat_attack0.png'),
        'O_soldat_attack1': PhotoImage(file='images/orange/O_soldat_attack1.png'),
        'O_soldat_attack2': PhotoImage(file='images/orange/O_soldat_attack2.png'),
    }
    return images


images = {}


def chargerimages(chemin=None):
    if chemin == None:
        chemin = os.getcwd()
        chemin = chemin + "\\images"
    for i in os.listdir(chemin):
        che = chemin + "\\" + i
        if os.path.isdir(che):
            chargerimages(che)
        else:
            nom, ext = os.path.splitext(os.path.basename(i))
            if ".png" == ext:
                images[nom] = PhotoImage(file=che)  # .replace("\\","/")
    return images


def chargergifs():
    gifs = {}
    lesgifs = ["poissons.gif", "marche.gif"]
    for nom in lesgifs:
        listeimages = []
        testverite = 1
        noindex = 0
        while testverite:
            try:
                img = PhotoImage(file='./images/GIFS/' + nom, format="gif -index " + str(noindex))
                listeimages.append(img)
                noindex += 1
            except Exception:
                gifs[nom[:-4]] = listeimages
                testverite = 0
    return gifs


if __name__ == '__main__':
    images = chargerimages()

    for i in images.keys():
        print(i, images[i])
