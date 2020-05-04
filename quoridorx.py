"""Module pour encapsuler la classe QuoridorX, qui fait un affichage graphique.
"""
import turtle as t
from quoridor import Quoridor

class QuoridorX(Quoridor):
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)
        self.window = t.Screen()
        self.window.setup(width=700, height=500)
        self.crayon = t.Turtle()
        self.afficher()

    def afficher(self):
        res = super().__str__().split('\n')[:-1]
        style = ('Courier', 20)
        for ligne, contenu in enumerate(res):
            self.crayon.penup()
            self.crayon.goto(-325,200 - ligne * 20)
            self.crayon.pendown()
            self.crayon.write(contenu, font=style, align='left')
        self.crayon.hideturtle()