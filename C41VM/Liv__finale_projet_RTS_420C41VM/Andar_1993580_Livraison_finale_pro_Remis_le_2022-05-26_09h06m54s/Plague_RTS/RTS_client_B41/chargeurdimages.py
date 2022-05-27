## - Encoding: UTF-8 -*-
# changer pour changeurdimages

# Refactoriser pour lire le contenu de dossier

from tkinter import PhotoImage
# toutes les images devraient �tre ins�r�es ici

import os, os.path


def chargerimages2():
    images = {
        # logo splash
        'logo': PhotoImage(file='images/misc/logo.png'),
        'win': PhotoImage(file='images/misc/win.png'),
        'lose': PhotoImage(file='images/misc/lost.png'),

        # organes
        'coeur': PhotoImage(file='images/organe/coeur.png'),
        'cerveau': PhotoImage(file='images/organe/cerveau.png'),
        'poumon': PhotoImage(file='images/organe/poumon.png'),
        'reins': PhotoImage(file='images/organe/reins.png'),
        'intestins': PhotoImage(file='images/organe/intestin.png'),
        'foie': PhotoImage(file='images/organe/foie.png'),
        'estomac': PhotoImage(file='images/organe/estomac.png'),
        'oeil': PhotoImage(file='images/organe/oeil.png'),

        # ennemi
        'npc': PhotoImage(file="images/ennemi/npc.png"),
        'globulerougeMORT': PhotoImage(file='images/ennemi/globulerougeMORT.png'),
        'globulerouge': PhotoImage(file='images/ennemi/globulerouge.png'),

        # batiments morts
        'watchtowerMORT': PhotoImage(file='images/batimentsMORT/watchtowerMORT.png'),
        'barracksMORT': PhotoImage(file='images/batimentsMORT/barracksMORT.png'),
        'turretsMORT': PhotoImage(file='images/batimentsMORT/turretsMORT.png'),
        'maisonMORT': PhotoImage(file='images/batimentsMORT/maisonMORT.png'),

        # cellules blanches
        "monocyte": PhotoImage(file='images/cellblanc/monocyte.png'),
        'neutrophil': PhotoImage(file='images/cellblanc/neutrophil.png'),
        'lymphocyte': PhotoImage(file='images/cellblanc/lymphocyte.png'),

        # misc
        'seringue': PhotoImage(file='images/misc/seringe.png'),
        'dna': PhotoImage(file='images/misc/dna.png'),
        'beacon': PhotoImage(file='images/misc/beacon.png'),
        'morve': PhotoImage(file='images/misc/test.png'),
        'siteX': PhotoImage(file='images/misc/siteX.png'),

        # equipe verte
        # batiments
        'V_icon_watchtower': PhotoImage(file='images/vert/V_icon_watchtower.png'),
        'V_watchtower': PhotoImage(file='images/vert/V_watchtower.png'),
        'V_barracks': PhotoImage(file='images/vert/V_barracks.png'),
        'V_turrets': PhotoImage(file='images/vert/V_turrets.png'),
        'V_ballista': PhotoImage(file='images/vert/V_ballista.png'),
        'V_maison': PhotoImage(file='images/vert/V_maison.png'),
        'V_ouvrier': PhotoImage(file='images/vert/V_ouvrier.png'),
        'V_soldat': PhotoImage(file='images/vert/V_soldat.png'),
        'V_druide': PhotoImage(file='images/vert/V_druide.png'),

        # equipe bleu
        # batiments
        'B_icon_watchtower': PhotoImage(file='images/bleu/B_icon_watchtower.png'),
        'B_watchtower': PhotoImage(file='images/bleu/B_watchtower.png'),
        'B_barracks': PhotoImage(file='images/bleu/B_barracks.png'),
        'B_turrets': PhotoImage(file='images/bleu/B_turrets.png'),
        'B_ballista': PhotoImage(file='images/bleu/B_ballista.png'),
        'B_maison': PhotoImage(file='images/bleu/B_maison.png'),
        'B_ouvrier': PhotoImage(file='images/bleu/B_ouvrier.png'),
        'B_soldat': PhotoImage(file='images/bleu/B_soldat.png'),
        'B_druide': PhotoImage(file='images/bleu/B_druide.png'),

        # equipe rouge
        # batiments
        'R_icon_watchtower': PhotoImage(file='images/rouge/R_icon_watchtower.png'),
        'R_watchtower': PhotoImage(file='images/rouge/R_watchtower.png'),
        'R_barracks': PhotoImage(file='images/rouge/R_barracks.png'),
        'R_turrets': PhotoImage(file='images/rouge/R_turrets.png'),
        'R_ballista': PhotoImage(file='images/rouge/R_ballista.png'),
        'R_maison': PhotoImage(file='images/rouge/R_maison.png'),
        'R_ouvrier': PhotoImage(file='images/rouge/R_ouvrier.png'),
        'R_soldat': PhotoImage(file='images/rouge/R_soldat.png'),
        'R_druide': PhotoImage(file='images/rouge/R_druide.png'),

        # equipe jaune
        # batiments
        'J_icon_watchtower': PhotoImage(file='images/jaune/J_icon_watchtower.png'),
        'J_watchtower': PhotoImage(file='images/jaune/J_watchtower.png'),
        'J_barracks': PhotoImage(file='images/jaune/J_barracks.png'),
        'J_turrets': PhotoImage(file='images/jaune/J_turrets.png'),
        'J_ballista': PhotoImage(file='images/jaune/J_ballista.png'),
        'J_maison': PhotoImage(file='images/jaune/J_maison.png'),
        'J_ouvrier': PhotoImage(file='images/jaune/J_ouvrier.png'),
        'J_soldat': PhotoImage(file='images/jaune/J_soldat.png'),
        'J_druide': PhotoImage(file='images/jaune/J_druide.png'),
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

# asdsadsad
