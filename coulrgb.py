from tkinter import *

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.img=PhotoImage(file="toto1.png")
        self.cane=Canvas(self.root,width=500,height=400,bg="green")
        self.cane.pack()
        self.cane.create_image(100,100,anchor="center",image=self.img)

class Modele():
    def __init__(self,parent):
        self.parent=parent

class Controleur():
    def __init__(self):
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()

if __name__=="__main__":
    c=Controleur()