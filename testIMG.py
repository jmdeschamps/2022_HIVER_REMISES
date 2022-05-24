
from tkinter import *
from PIL import Image, ImageDraw

root=Tk()
canevas=Canvas(root,width=600,height=400,bg="pink")
canevas.pack()
monimg=""

def creer_image():
    global monimg
    color_1 = (255, 100, 255, 0)  # le parametre '0' indique une pleine transparence
    color_2 = (255, 0, 255)
    im = Image.new('RGBA', (150,150),color_1)
    draw = ImageDraw.Draw(im)
    center=75
    i=10
    draw.ellipse((center - i, center - i, center + i, center + i), width=2, outline=color_2)
    i=20
    color_2 = (100, 235, 235)
    draw.ellipse((center - i, center - i, center + i, center + i), width=4, outline=color_2)
    i=40
    color_2 = (100, 205, 205)
    draw.ellipse((center - i, center - i, center + i, center + i), width=6, outline=color_2)
    images=[im]
    im.save('toto5.png')
    monimg=PhotoImage(file="toto5.png")
    montre_image()

def montre_image():
    canevas.create_image(100,100,image=monimg)
    canevas.create_image(300,100,image=monimg)
    canevas.create_image(100,300,image=monimg)


if __name__ == '__main__':
    creer_image()
    root.mainloop()