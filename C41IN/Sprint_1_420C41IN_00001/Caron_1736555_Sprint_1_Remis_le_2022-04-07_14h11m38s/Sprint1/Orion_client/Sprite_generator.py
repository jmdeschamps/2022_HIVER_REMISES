from PIL import Image

class Picture:
 def __init__(self, couleur_primaire, couleur_secondaire):
    self.image = Image.new('RGB',(16, 16))
    self.longueur = 16
    self.hauteur = 16
    self.couleur_primaire = couleur_primaire
    self.couleur_secondaire = couleur_secondaire
    self.contour_vaisseau = 110 # gris
    self.blanc = 255 # blanc
    self.lumiere_vaisseau = [252, 4, 4] # rouge


 def creer_etoile(self):

     # i = y j = x sur un tableau cartésien
     # faire un paramètre couleur qui prends 3 int puis ensuite on passe
    for i in range(self.longueur):
        for j in range(self.hauteur):
            if j == 0 or j == 15:
                if 11 > i > 4:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
            elif j == 1:
                if 5 > i > 2 or 10 < i < 13:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 4 < i < 11:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 2:
                if i == 2 or i == 13:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 2 < i < 13:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 3:
                if  i == 1 or  i == 14:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 1 < i < 14:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 4:
                if  i == 1 or  i == 14:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 1 < i < 14:
                    if i == 4 or i == 5:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 5:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    if 8 < i < 12:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 6:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 7:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    if 4 < i < 9:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 8:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 9:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    if 11 < i < 14:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 10:
                if  i == 0 or  i == 15:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    if 2 < i < 8:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 11:
                if  i == 1 or  i == 14:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 1 < i < 14:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 12:
                if  i == 1 or  i == 14:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 15:
                    if 6 < i < 11:
                        self.image.putpixel((i,j),(self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 13:
                if  i == 2 or  i == 13:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 2 < i < 13:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 14:
                if 2 < i < 5 or  10 < i < 13:
                    self.image.putpixel((i, j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 4 < i < 11:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            else:
                self.image.putpixel((i, j), (0, 0, 0)) # couleur noir

    self.image.save("test.png")

 def creer_vaisseau(self):

     # i = y j = x sur un tableau cartésien
     # faire un paramètre couleur qui prends 3 int puis ensuite on passe
    for i in range(self.longueur):
        for j in range(self.hauteur):
            if j == 0:
                if 5 < i < 10:
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau)) # Gris la couleur autour des vaisseaux
            elif j == 1:
                if 13 < i or i < 2:
                    self.image.putpixel((i, j),(self.lumiere_vaisseau[0], self.lumiere_vaisseau[1], self.lumiere_vaisseau[2])) # rouge lumière du vaisseaux
                elif i == 2 or i == 13:
                    self.image.putpixel((i,j),(self.blanc, self.blanc, self.blanc)) # blanc lumière du vaisseaux
                elif i == 5 or i == 10:
                    self.image.putpixel((i,j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau)) # Gris la couleur autour des vaisseaux
                elif 5 < i < 10:
                    if i == 8:
                        self.image.putpixel((i,j), (221, 235, 247))
                    else:
                        self.image.putpixel((i,j), (189, 215, 238))
            elif j == 2:
                if i < 3 or i > 12:
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
                elif i == 5 or i == 10:
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
                elif 5 < i < 10:
                    if i == 7:
                        self.image.putpixel((i,j), (221, 235, 247))
                    else:
                        self.image.putpixel((i,j), (189, 215, 238))
            elif j == 3:
                if  i == 4 or i == 11:
                    self.image.putpixel((i, j), (0, 0 , 0))
                elif 0 < i < 3 or 12 < i < 15:
                    self.image.putpixel((i,j),(self.couleur_primaire[0],self.couleur_primaire[1],self.couleur_primaire[2]))
                elif 5 < i < 10:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j), (189, 215, 238))
                else :
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 4 or j == 5:
                if  i == 4 or i == 11:
                    self.image.putpixel((i, j), (0, 0 , 0))
                elif 0 < i < 3 or 12 < i < 15:
                    if i == 1 or i == 14:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_primaire[0],self.couleur_primaire[1],self.couleur_primaire[2]))
                elif 5 < i < 10:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                else :
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 6:
                if  i == 4 or i == 11:
                    self.image.putpixel((i, j), (0, 0 , 0))
                elif 0 < i < 3 or 12 < i < 15:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                elif 5 < i < 10:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                else :
                    self.image.putpixel((i, j), (self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 7:
                if i == 3 or i == 12:
                    self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 3 or 12 < i < 15:
                    self.image.putpixel((i,j), (self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                elif 5 < i < 10:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                else:
                    self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 8:
                if i == 4 or i == 11:
                    self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                elif 0 < i < 4 or 11 < i < 15:
                    self.image.putpixel((i,j), (self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                elif 5 < i < 10:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
                else:
                    self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 9:
                if i == 1 or i == 14:
                   self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
                elif 1 < i < 14:
                    if i == 6 or i == 9:
                        self.image.putpixel((i,j), (self.couleur_primaire[0], self.couleur_primaire[1], self.couleur_primaire[2]))
                    else:
                        self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 10:
                if i == 2 or i == 13:
                   self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
                elif 2 < i < 13:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 11:
                if  2 < i < 6 or 9 < i < 13:
                    self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
                elif 5 < i < 10:
                    self.image.putpixel((i,j),(self.couleur_secondaire[0],self.couleur_secondaire[1],self.couleur_secondaire[2]))
            elif j == 12:
                if 3 < i < 12:
                    if i == 5:
                        self.image.putpixel((i,j),(252, 150, 4)) # orange
                    elif i == 10:
                        self.image.putpixel((i,j), (252, 194, 4)) # jaune
                    else:
                        self.image.putpixel((i,j),(self.contour_vaisseau, self.contour_vaisseau, self.contour_vaisseau))
            elif j == 13:
             if 3 < i < 12:
                    if 5 < i < 11:
                        self.image.putpixel((i,j),(252, 194, 4)) # jaune
                    else:
                        self.image.putpixel((i,j), (252, 150, 4)) # orange
            elif j == 14:
               if 3 < i < 12:
                    if i == 5 or i == 8 or i == 10:
                        self.image.putpixel((i,j),(252, 194, 4)) # jaune
                    else:
                        self.image.putpixel((i,j), (252, 150, 4)) # orange
            elif j == 15:
                if i == 5 or i == 8 or i == 10:
                    self.image.putpixel((i,j), (252, 150, 4)) # orange
            else:
                self.image.putpixel((i, j), (0, 0, 0)) # couleur noir

    self.image.save("vaisseau_test.png")
def main():
    secondaire = [0, 176, 80]
    primaire = [5, 135, 64]
    picture = Picture(primaire, secondaire)
    picture_vaisseau = Picture(primaire, secondaire)
    picture_vaisseau.creer_vaisseau()
    picture.creer_etoile()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 main()