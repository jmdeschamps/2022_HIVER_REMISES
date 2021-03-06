## - Encoding: UTF-8 -*-
# changer pour changeurdimages

# Refactoriser pour lire le contenu de dossier

from tkinter import PhotoImage
# toutes les images devraient �tre ins�r�es ici

import os, os.path


def chargerimages2():
    images = {
        'siteX': PhotoImage(file='images/divers/siteX.png'),
        'EnConstruction': PhotoImage(file='images/divers/EnConstruction.png'),
        'EnConstruction2': PhotoImage(file='images/divers/EnConstruction2.png'),
        'flecheGH': PhotoImage(file='images/divers/flecheGH.png'),
        'flecheGB': PhotoImage(file='images/divers/flecheGB.png'),
        'flecheDH': PhotoImage(file='images/divers/flecheDH.png'),
        'flecheDB': PhotoImage(file='images/divers/flecheDB.png'),
        'javelotGH': PhotoImage(file='images/divers/javelotGH.png'),
        'javelotGB': PhotoImage(file='images/divers/javelotGB.png'),
        'javelotDH': PhotoImage(file='images/divers/javelotDH.png'),
        'javelotDB': PhotoImage(file='images/divers/javelotDB.png'),
        'cerfD': PhotoImage(file='images/animal/cerfD.png'),
        'cerfD': PhotoImage(file='images/animal/cerfD.png'),
        'cerfG': PhotoImage(file='images/animal/cerfG.png'),
        'cheval': PhotoImage(file='images/animal/cheval.png'),
        'chevalG': PhotoImage(file='images/animal/chevalG.png'),
        'daimMORT': PhotoImage(file='images/animal/DaimMORT.png'),
        'daimDB': PhotoImage(file='images/animal/DaimDB.png'),
        'daimDH': PhotoImage(file='images/animal/DaimDH.png'),
        'daimGB': PhotoImage(file='images/animal/DaimGB.png'),
        'daimGH': PhotoImage(file='images/animal/DaimGH.png'),
        'ours60_db': PhotoImage(file='images/animal/ours60_db.png'),
        'ours60_dh': PhotoImage(file='images/animal/ours60_dh.png'),
        'ours60_gb': PhotoImage(file='images/animal/ours60_gb.png'),
        'ours60_gh': PhotoImage(file='images/animal/ours60_gh.png'),
        'arbre0grand': PhotoImage(file='images/arbre/arbre0grand_pix.png'),
        'arbre0petit': PhotoImage(file='images/arbre/arbre0petit_pix.png'),
        'arbre1grand': PhotoImage(file='images/arbre/arbre1grand_pix.png'),
        'arbre2grand': PhotoImage(file='images/arbre/arbre2grand_pix.png'),
        'arbresapin0grand': PhotoImage(file='images/arbre/arbresapin0grand_pix.png'),
        'arbresapin0petit': PhotoImage(file='images/arbre/arbresapin0petit_pix.png'),
        'baiegrand': PhotoImage(file='images/arbuste/arbustebaiesgrand.png'),
        'baiepetit': PhotoImage(file='images/arbuste/arbustebaiespetit.png'),
        'baievert': PhotoImage(file='images/arbuste/arbustevert.png'),
        'aureusbrillant': PhotoImage(file='images/aureus/aureusbrillant.png'),
        'aureusD_': PhotoImage(file='images/aureus/aureusD_.png'),
        'aureusG': PhotoImage(file='images/aureus/aureusG.png'),
        'aureusrocgrand': PhotoImage(file='images/aureus/aureusrocgrand.png'),
        'aureusrocmoyen': PhotoImage(file='images/aureus/aureusrocmoyen.png'),
        'aureusrocpetit': PhotoImage(file='images/aureus/aureusrocpetit.png'),
        'B_abri': PhotoImage(file='images/bleu/B_abri.png'),
        'B_usineballiste': PhotoImage(file='images/bleu/B_usineballiste.png'),
        'B_ballistaDH': PhotoImage(file='images/bleu/B_ballistaDH.png'),
        'B_ballistaDB': PhotoImage(file='images/bleu/B_ballistaDB.png'),
        'B_ballistaGH': PhotoImage(file='images/bleu/B_ballistaGH.png'),
        'B_ballistaGB': PhotoImage(file='images/bleu/B_ballistaGB.png'),
        'B_archerD': PhotoImage(file='images/bleu/B_archerD.png'),
        'B_archerG': PhotoImage(file='images/bleu/B_archerG.png'),
        'B_caserne': PhotoImage(file='images/bleu/B_caserne.png'),
        'B_chevalierD': PhotoImage(file='images/bleu/B_chevalierD.png'),
        'B_chevalierG': PhotoImage(file='images/bleu/B_chevalierG.png'),
        'B_RogueReaperD': PhotoImage(file='images/bleu/B_RogueReaperD.png'),
        'B_RogueReaperG': PhotoImage(file='images/bleu/B_RogueReaperG.png'),
        'B_maison': PhotoImage(file='images/bleu/B_maison.png'),
        'B_ouvrierD': PhotoImage(file='images/bleu/B_ouvrierD.png'),
        'B_ouvrierG': PhotoImage(file='images/bleu/B_ouvrierG.png'),
        'B_kidReaperD': PhotoImage(file='images/bleu/B_kidReaperD.png'),
        'B_kidReaperG': PhotoImage(file='images/bleu/B_kidReaperG.png'),

        'O_abri': PhotoImage(file='images/orange/O_abri.png'),
        'O_usineballiste': PhotoImage(file='images/orange/O_usineballiste.png'),
        'O_ballistaDH': PhotoImage(file='images/orange/O_ballistaDH.png'),
        'O_ballistaDB': PhotoImage(file='images/orange/O_ballistaDB.png'),
        'O_ballistaGH': PhotoImage(file='images/orange/O_ballistaGH.png'),
        'O_ballistaGB': PhotoImage(file='images/orange/O_ballistaGB.png'),
        'O_archerD': PhotoImage(file='images/orange/O_archerD.png'),
        'O_archerG': PhotoImage(file='images/orange/O_archerG.png'),
        'O_caserne': PhotoImage(file='images/orange/O_caserne.png'),
        'O_chevalierD': PhotoImage(file='images/orange/O_chevalierD.png'),
        'O_chevalierG': PhotoImage(file='images/orange/O_chevalierG.png'),
        'O_RogueReaperD': PhotoImage(file='images/orange/O_RogueReaperD.png'),
        'O_RogueReaperG': PhotoImage(file='images/orange/O_RogueReaperG.png'),
        'O_maison': PhotoImage(file='images/orange/O_maison.png'),
        'O_ouvrierD': PhotoImage(file='images/orange/O_ouvrierD.png'),
        'O_ouvrierG': PhotoImage(file='images/orange/O_ouvrierG.png'),
        'O_kidReaperD': PhotoImage(file='images/orange/O_kidReaperD.png'),
        'O_kidReaperG': PhotoImage(file='images/orange/O_kidReaperG.png'),

        'gazonfond': PhotoImage(file='images/divers/gazonfond.png'),
        'quaiD': PhotoImage(file='images/divers/quaiD.png'),
        'quaiG': PhotoImage(file='images/divers/quaiG.png'),
        'eaugrand': PhotoImage(file='images/eau/eaugrand.png'),
        'eaugrand1': PhotoImage(file='images/eau/eaugrand1.png'),
        'eaugrand2': PhotoImage(file='images/eau/eaugrand2.png'),
        'eaugrand3': PhotoImage(file='images/eau/eaugrand3.png'),
        'culturegrand': PhotoImage(file='images/ferme/culturegrand.png'),
        'culturemoyen': PhotoImage(file='images/ferme/culturemoyen.png'),
        'culturepetit': PhotoImage(file='images/ferme/culturepetit.png'),
        'J_abri': PhotoImage(file='images/jaune/J_abri.png'),
        'J_usineballiste': PhotoImage(file='images/jaune/J_usineballiste.png'),
        'J_ballistaDH': PhotoImage(file='images/jaune/J_ballistaDH.png'),
        'J_ballistaDB': PhotoImage(file='images/jaune/J_ballistaDB.png'),
        'J_ballistaGH': PhotoImage(file='images/jaune/J_ballistaGH.png'),
        'J_ballistaGB': PhotoImage(file='images/jaune/J_ballistaGB.png'),
        'J_archeG': PhotoImage(file='images/jaune/J_archeG.png'),
        'J_archerD': PhotoImage(file='images/jaune/J_archerD.png'),
        'J_caserne': PhotoImage(file='images/jaune/J_caserne.png'),
        'J_chevalierD': PhotoImage(file='images/jaune/J_chevalierD.png'),
        'J_chevalierG': PhotoImage(file='images/jaune/J_chevalierG.png'),
        'J_RogueReaperD': PhotoImage(file='images/jaune/J_RogueReaperD.png'),
        'J_RogueReaperG': PhotoImage(file='images/jaune/J_RogueReaperG.png'),
        'J_maison': PhotoImage(file='images/jaune/J_maison.png'),
        'J_ouvrierD': PhotoImage(file='images/jaune/J_ouvrierD.png'),
        'J_ouvrierG': PhotoImage(file='images/jaune/J_ouvrierG.png'),
        'J_kidReaperD': PhotoImage(file='images/jaune/J_kidReaperD.png'),
        'J_kidReaperG': PhotoImage(file='images/jaune/J_kidReaperG.png'),
        'marais1': PhotoImage(file='images/marais/marais1.png'),
        'marais2': PhotoImage(file='images/marais/marais2.png'),
        'marais3': PhotoImage(file='images/marais/marais3.png'),
        'roches1 grand': PhotoImage(file='images/roche/roches1 grand.png'),
        'roches1petit': PhotoImage(file='images/roche/roches1petit.png'),
        'roches2grand': PhotoImage(file='images/roche/roches2grand.png'),
        'roches2petit': PhotoImage(file='images/roche/roches2petit.png'),
        'roches3grand': PhotoImage(file='images/roche/roches3grand.png'),
        'roches3petit': PhotoImage(file='images/roche/roches3petit.png'),
        'roches4grand': PhotoImage(file='images/roche/roches4grand.png'),
        'roches4petit': PhotoImage(file='images/roche/roches4petit.png'),
        'roches5grand': PhotoImage(file='images/roche/roches5grand.png'),
        'R_abri': PhotoImage(file='images/rouge/R_abri.png'),
        'R_archerD': PhotoImage(file='images/rouge/R_archerD.png'),
        'R_usineballiste': PhotoImage(file='images/rouge/R_usineballiste.png'),
        'R_ballistaDH': PhotoImage(file='images/rouge/R_ballistaDH.png'),
        'R_ballistaDB': PhotoImage(file='images/rouge/R_ballistaDB.png'),
        'R_ballistaGH': PhotoImage(file='images/rouge/R_ballistaGH.png'),
        'R_ballistaGB': PhotoImage(file='images/rouge/R_ballistaGB.png'),
        'R_archerG': PhotoImage(file='images/rouge/R_archerG.png'),
        'R_caserne': PhotoImage(file='images/rouge/R_caserne.png'),
        'R_chevalierD': PhotoImage(file='images/rouge/R_chevalierD.png'),
        'R_chevalierG': PhotoImage(file='images/rouge/R_chevalierG.png'),
        'R_RogueReaperD': PhotoImage(file='images/rouge/R_RogueReaperD.png'),
        'R_RogueReaperG': PhotoImage(file='images/rouge/R_RogueReaperG.png'),
        'R_maison': PhotoImage(file='images/rouge/R_maison.png'),
        'R_ouvrierD': PhotoImage(file='images/rouge/R_ouvrierD.png'),
        'R_ouvrierG': PhotoImage(file='images/rouge/R_ouvrierG.png'),
        'R_kidReaperD': PhotoImage(file='images/rouge/R_kidReaperD.png'),
        'R_kidReaperG': PhotoImage(file='images/rouge/R_kidReaperG.png'),
        'V_abri': PhotoImage(file='images/vert/V_abri.png'),
        'V_usineballiste': PhotoImage(file='images/vert/V_usineballiste.png'),
        'V_ballistaDH': PhotoImage(file='images/vert/V_ballistaDH.png'),
        'V_ballistaDB': PhotoImage(file='images/vert/V_ballistaDB.png'),
        'V_ballistaGH': PhotoImage(file='images/vert/V_ballistaGH.png'),
        'V_ballistaGB': PhotoImage(file='images/vert/V_ballistaGB.png'),
        'V_archerD': PhotoImage(file='images/vert/V_archerD.png'),
        'V_archerG': PhotoImage(file='images/vert/V_archerG.png'),
        'V_caserne': PhotoImage(file='images/vert/V_caserne.png'),
        'V_chevalierD': PhotoImage(file='images/vert/V_chevalierD.png'),
        'V_chevalierG': PhotoImage(file='images/vert/V_chevalierG.png'),
        'V_RogueReaperD': PhotoImage(file='images/vert/V_RogueReaperD.png'),
        'V_RogueReaperG': PhotoImage(file='images/vert/V_RogueReaperG.png'),
        'V_maison': PhotoImage(file='images/vert/V_maison.png'),
        'V_ouvrierD': PhotoImage(file='images/vert/V_ouvrierD.png'),
        'V_ouvrierG': PhotoImage(file='images/vert/V_ouvrierG.png'),
        'V_kidReaperD': PhotoImage(file='images/vert/V_kidReaperD.png'),
        'V_kidReaperG': PhotoImage(file='images/vert/V_kidReaperG.png')}
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
