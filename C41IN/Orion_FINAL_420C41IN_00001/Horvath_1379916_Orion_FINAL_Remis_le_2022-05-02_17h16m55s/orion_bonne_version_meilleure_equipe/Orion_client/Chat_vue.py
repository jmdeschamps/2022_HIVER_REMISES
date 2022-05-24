from Orion_vue import *
from Chat import *


class Chat_vue(Toplevel):
    def __init__(self, parent,controleur):
        self.parent = parent
        self.controleur = controleur


    def ouvrir_chat(self):
        self.chat_root = Toplevel(self.parent.root)
        self.chat_root.title("Chat")
        self.message_frame = Frame(self.chat_root)
        self.message = StringVar()
        self.scrollbar = Scrollbar(self.message_frame)
        self.liste_message = Listbox(self.message_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.input_message = Entry(self.chat_root, textvariable=self.message)
        self.btn_envoyer = Button(self.chat_root, text="Envoye", command=self.envoye_message_vue)
        self.btn_destinataires = []

        self.liste_message.pack(side=LEFT, fill=BOTH)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.message_frame.pack()
        self.input_message.bind("<Return>, envoye_message_vue")
        self.input_message.pack()
        self.btn_envoyer.pack()


    def envoye_message_vue(self):
        for message in self.parent.modele.chat.liste_messages_envoyes:
            if message.origine_msg == self.parent.mon_nom:
                destination_msg = message.destination_msg
                texte_message = self.message.get()
                Label(self.parent.creer_cadre_outils.label_chat,
                      text=destination_msg + ":").pack()
                Label(self.message_frame, text=texte_message).pack()
                action = [self.parent.mon_nom, "envoyer_message",
                          [destination_msg, texte_message]]
                self.controleur.actionsrequises.append(action)
                self.input_message.delete(0, END)

    def recevoir_message_vue(self):
        for message in self.parent.modele.chat.liste_messages_recues:
            if message.destination_msg == self.parent.mon_nom:
                origine_msg = message.origine_msg
                texte_message = message.texte_message
                Label(self.message_frame, text=origine_msg + ":").pack()
                Label(self.message_frame, text=texte_message).pack()
                action = [self.parent.mon_nom, "recevoir_message",
                          [origine_msg, texte_message]]
                self.controleur.actionsrequises.append(action)
