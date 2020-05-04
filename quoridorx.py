"""Module pour encapsuler la classe QuoridorX, qui fait un affichage graphique.
"""
import turtle as t
from quoridor import Quoridor

class QuoridorX(Quoridor):
    """Class servant à jouer au jeu dans une fenêtre graphique.

    Args:
        Quoridor (class): Classe qui encapsule le jeu Quoridor.
    """
    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe QuoridorX.

        Initialise une partie de Quoridor en mode graphique avec les joueurs et
        les murs spécifiés, en s'assurant de faire une copie profonde de tout ce
        qui a besoin d'être copié.

        Args:
            joueurs (list): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle.
            murs (dict, optional): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu.
        """
        super().__init__(joueurs, murs)
        self.window = t.Screen()
        self.window.setup(width=700, height=500)
        self.crayon = t.Turtle()
        self.afficher()

    def afficher(self):
        """Affiche l'état de la partie dans une fenêtre graphique.
        """
        res = super().__str__().split('\n')[:-1]
        style = ('Courier', 20)
        for ligne, contenu in enumerate(res):
            self.crayon.penup()
            self.crayon.goto(-325,200 - ligne * 20)
            self.crayon.pendown()
            self.crayon.write(contenu, font=style, align='left')
        self.crayon.hideturtle()