"""Module pour encapsuler la classe QuoridorX, qui fait un affichage graphique.
"""
import turtle
from quoridor import Quoridor

print('test')

fen = turtle.Screen()
fen.title("Ma fenêtre de tortues!")
fen.setup(width=800, height=600)
alex = turtle.Turtle()

alex.forward(50) # avancer de 50 pixels
alex.left(90)    # tourner de 90° en sens anti-horaire
alex.forward(30) # avancer de 30 pixels
input("Press any key to exit ...")

class QuoridorX(Quoridor):
    pass