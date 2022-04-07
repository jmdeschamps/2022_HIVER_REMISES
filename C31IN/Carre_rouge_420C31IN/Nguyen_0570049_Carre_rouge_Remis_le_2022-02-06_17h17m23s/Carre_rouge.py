from tkinter import *
import time

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.modele=self.parent.modele
        self.root=Tk()
        self.root.title("Carre Rouge, alpha_0.1")
        self.cadres=self.creer_interface()

    def creer_interface(self):
        # cadre HUD affichant la duree
        self.cadre_info=Frame(self.root, bg="lightgreen")
        self.var_duree=StringVar()
        label_duree=Label(self.cadre_info,text="0",textvariable=self.var_duree)
        label_duree.pack()

        # Frame 1
        self.frame1 = Frame(self.root, bg="black", width=550, height=550)
        self.frame1.pack()

        # Frame 2
        self.frame2 = Frame(self.frame1, bg="white", width=450, height=450)
        self.frame2.pack(pady=50, padx=50)

        # le canevas de jeu
        self.canevas = Canvas(self.frame2, width=self.modele.largeur, height=self.modele.hauteur, bg="white")
        self.canevas.tag_bind("pion","<Button>",self.debuter_partie)
        # visualiser
        self.cadre_info.pack(expand=1,fill=X)
        self.canevas.pack()


        self.afficher_partie()

    def debuter_partie(self,evt):
        self.canevas.tag_unbind("pion","<Button>")
        self.canevas.bind("<B1-Motion>",self.recibler_pion)
        self.canevas.bind("<ButtonRelease>",self.fin_de_partie)
        self.parent.debuter_partie()

    def arreter_jeu(self,evt):
        self.parent.partie_en_cours=0
        self.canevas.tag_bind("pion","<Button>",self.debuter_partie)
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

    def recibler_pion(self,evt):
        x=evt.x
        y=evt.y
        self.parent.recibler_pion(x,y)

    def afficher_partie(self):
        self.canevas.delete(ALL)
        x=self.modele.pion.x
        y=self.modele.pion.y
        d=self.modele.pion.demitaille
        self.canevas.create_rectangle(x-d,y-d,x+d,y+d,
        fill="red",tags=("pion",))

        x=self.modele.poteau1.x
        y=self.modele.poteau1.y
        d=self.modele.poteau1.demitaille
        self.canevas.create_rectangle(x-30,y-30,x+30,y+30,
        fill="blue",tags=("poteau_1",))

        x=self.modele.poteau2.x 
        y=self.modele.poteau2.y 
        d=self.modele.poteau2.demitaille
        self.canevas.create_rectangle(x-30,y-25,x+30,y+25,
        fill="blue",tags=("poteau_2",))
        
        x=self.modele.poteau3.x 
        y=self.modele.poteau3.y
        d=self.modele.poteau3.demitaille
        self.canevas.create_rectangle(x-15,y-30,x+15,y+30,
        fill="blue",tags=("poteau_3",))

        x=self.modele.poteau4.x 
        y=self.modele.poteau4.y
        d=self.modele.poteau4.demitaille
        self.canevas.create_rectangle(x-50,y-10,x+50,y+10,
        fill="blue",tags=("poteau_4",))     
                   
        if self.modele.pion.vivant == 0:
            self.var_duree.set(str(round(self.modele.duree,2)))

    def deplacer_poteau(self):
        self.parent.deplacer_poteau()

    def fin_de_partie(self, evt):
        self.cadre_info.destroy()
        self.canevas.delete(ALL)
        self.parent.partie_en_cours=0
        self.canevas.unbind("<B1-Motion>")
        self.canevas.unbind("<ButtonRelease>")

        self.frame_final = Canvas(
            self.canevas, bg="darkblue", width=400, height=400)
        self.frame_final.pack()
        self.frame_final.create_text(200, 200, text=('{:.2f}'.format(self.modele.duree)) + " sec",
                           fill="yellow", font=('Helvetica 15 bold'))

        self.boutton_initialiser = Button(self.canevas, text ="Reinitialiser", command =  self.parent.reinitialiser_partie()).pack()

class Modele():
    def __init__(self,parent):
        self.parent=parent
        self.largeur=450
        self.hauteur=450
        self.debut=None
        self.duree=0
        self.duree_final = 0
        self.pion=Pion(self)
        
        self.poteau1=Poteau(self, 100, 100)
        self.poteau2=Poteau(self, 300, 85)
        self.poteau3=Poteau(self, 85, 350)
        self.poteau4=Poteau(self, 355, 340)
        self.liste_poteau = [self.poteau1, self.poteau2, self.poteau3, self.poteau4]

    def recibler_pion(self,x,y):
        if self.pion.vivant == 0:
            self.pion.recibler(x,y)

    def jouer_tour(self):
        self.duree=time.time()-self.debut

    def deplacer_poteau(self):
        for i in self.liste_poteau:
            i.deplacer()

    def duree_jeu_final(self):
        if self.pion.vivant == 1:
            self.duree_final = self.duree
            return self.duree_final

class Poteau():
    def __init__(self,parent, x, y):
        self.parent=parent
        self.x=x
        self.y=y
        self.demitaille=30
        self.ciblex = None
        self.cibley = None
        self.vitesse = 5
        self.reverse_x = False
        self.reverse_y = False
        # augmentation de la vitesse
        self.acceleration = 0.001

    def deplacer(self):
        if self.parent.pion.vivant == 0:
            if (self.x > 400):
                self.reverse_x = True
            elif (self.x < 50):
                self.reverse_x = False

            if (self.reverse_x == False):
                self.vitesse += self.acceleration
                self.x += self.vitesse
            elif (self.reverse_x == True):
                self.x -= self.vitesse


            if (self.y > 400):
                self.reverse_y = True
            elif (self.y < 50):
                self.reverse_y = False

            if (self.reverse_y == False):
                self.vitesse += self.acceleration
                self.y += self.vitesse

            elif (self.reverse_y == True):
                self.y -= self.vitesse

class Pion():
    def __init__(self,parent):
        self.parent=parent
        self.x=self.parent.largeur/2
        self.y=self.parent.largeur/2
        self.demitaille=20
        self.vivant = 0

    def recibler(self,x,y):
        if self.vivant <3:
            self.x=x
            self.y=y
            self.tester_collision()
        else: 
            pass

    def tester_collision(self):
        x1=self.x-self.demitaille
        y1=self.y-self.demitaille
        x2=self.x+self.demitaille
        y2=self.y+self.demitaille
 
        pot1=self.parent.poteau1
        potx11=pot1.x-pot1.demitaille
        poty11=pot1.y-pot1.demitaille
        potx21=pot1.x+pot1.demitaille
        poty21=pot1.y+pot1.demitaille

        if (x2>potx11 and x1<potx21) and (y2>poty11 and y1<poty21):
            # print("collision avec poteau 1",self.parent.duree)
            self.vivant += 1
            return   

        pot2=self.parent.poteau2
        potx12=pot2.x-pot2.demitaille
        poty12=pot2.y-pot2.demitaille
        potx22=pot2.x+pot2.demitaille
        poty22=pot2.y+pot2.demitaille

        if (x2>potx12 and x1<potx22) and (y2>poty12 and y1<poty22):
            # print("collision avec poteau 2",self.parent.duree)
            self.vivant += 1
            return

        pot3=self.parent.poteau3
        potx13=pot3.x-pot3.demitaille
        poty13=pot3.y-pot3.demitaille
        potx23=pot3.x+pot3.demitaille
        poty23=pot3.y+pot3.demitaille

        if (x2>potx13 and x1<potx23) and (y2>poty13 and y1<poty23):
            # print("collision avec poteau 3",self.parent.duree)
            self.vivant += 1
            return
            
        pot4 = self.parent.poteau4
        potx14=pot4.x-pot4.demitaille
        poty14=pot4.y-pot4.demitaille
        potx24=pot4.x+pot4.demitaille
        poty24=pot4.y+pot4.demitaille

        if (x2 > potx14 and x1 < potx24) and (y2 > poty14 and y1 < poty24):
            # print("collision avec poteau 4",self.parent.duree)  
            self.vivant += 1
            return

        if (x2 < 50 or x1 > 400) or (y2 < 50 or y1 > 400):
            # print("collision avec mur",self.parent.duree) 
            self.vivant += 1
            return
        return 
           

class Controleur():
    def __init__(self):
        self.partie_en_cours=0
        self.modele=Modele(self)
        self.vue=Vue(self)
        if self.modele.pion.vivant < 5:
            self.vue.root.mainloop()

    def recibler_pion(self,x,y):
        self.modele.recibler_pion(x,y)

    def debuter_partie(self):
        self.modele.debut=time.time()
        self.partie_en_cours=1
        self.jouer_partie()

    def jouer_partie(self):
        if self.partie_en_cours:
            self.modele.jouer_tour()
            self.vue.afficher_partie()
            self.modele.deplacer_poteau()
            if self.modele.pion.vivant == 0:
                self.vue.root.after(40,self.jouer_partie)
            elif self.modele.pion.vivant > 1 and self.modele.pion.vivant < 3:
                self.vue.fin_de_partie(self)

    def reinitialiser_partie(self):
        # self.
        self.modele.debut=time.time()
        self.partie_en_cours=1
        self.jouer_partie()


        
if __name__ == '__main__':
    c=Controleur()
    print("L'application se termine")

