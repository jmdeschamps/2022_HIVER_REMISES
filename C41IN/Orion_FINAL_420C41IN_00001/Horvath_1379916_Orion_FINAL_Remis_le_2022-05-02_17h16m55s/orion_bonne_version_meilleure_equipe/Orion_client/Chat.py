from tkinter import *

class Chat():
    def __init__(self, parent):
        self.parent = parent
        self.liste_messages_envoyes = []
        self.liste_messages_recues = []

    def envoyer_message(self, nom_joueur, param):
        destination_msg, texte_message = param
        obj = Message(nom_joueur, destination_msg, texte_message)
        self.liste_messages_envoyes.append(obj)
        pass

    def recevoir_message(self, nom_joueur, param):
        origine_msg, texte_message = param
        obj = Message(nom_joueur, origine_msg, texte_message)
        self.liste_messages_recues.append(obj)
        pass


class Message:
    def __init__(self, origine_msg, destination_msg, texte_message):
        self.origine_msg = origine_msg
        self.destination_msg = destination_msg
        self.texte_message = texte_message
