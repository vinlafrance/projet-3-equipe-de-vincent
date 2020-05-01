# -*- coding: utf-8 -*-
"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.

Examples:

    `> python3 main.py --help`

        usage: main.py [-h] [-l] idul

        Jeu Quoridor - phase 1

        positional arguments:
        idul          IDUL du joueur.

        optional arguments:
        -h, --help    show this help message and exit
        -l, --lister  Lister les identifiants de vos 20 dernières parties.

    `> python3 main.py josmi42`

        Légende: 1=josmi42, 2=robot
           -----------------------------------
        9 | .   .   .   .   2   .   .   .   . |
          |                                   |
        8 | .   .   .   .   .   .   .   .   . |
          |                                   |
        7 | .   .   .   .   .   .   .   .   . |
          |                                   |
        6 | .   .   .   .   .   .   .   .   . |
          |                                   |
        5 | .   .   .   .   .   .   .   .   . |
          |                                   |
        4 | .   .   .   .   .   .   .   .   . |
          |                                   |
        3 | .   .   .   .   .   .   .   .   . |
          |                                   |
        2 | .   .   .   .   .   .   .   .   . |
          |                                   |
        1 | .   .   .   .   1   .   .   .   . |
        --|-----------------------------------
          | 1   2   3   4   5   6   7   8   9

        Type de coup disponible :
        - D : Déplacement
        - MH: Mur Horizontal
        - MV: Mur Vertical

        Choisissez votre type de coup (D, MH ou MV) : D
        Définissez la colonne de votre coup : 5
        Définissez la ligne de votre coup : 2
"""

from api import lister_parties, initialiser_partie, jouer_coup
from quoridor import afficher_damier_ascii, analyser_commande


if __name__ == "__main__":
    ARGS = analyser_commande()
    if ARGS.lister:
        print(lister_parties(ARGS.idul))
    else:
        PARTIE = initialiser_partie(ARGS.idul)
        afficher_damier_ascii(PARTIE[1])
        while True:
            print('''Type de coup disponible :
- D : Déplacement
- MH: Mur Horizontal
- MV: Mur Vertical\n''')
            ID_PARTIE = PARTIE[0]
            TYPE_COUP = input('Choisissez votre type de coup (D, MH ou MV) : ')
            PX = input('Définissez la colonne de votre coup : ')
            PY = input('Définissez la ligne de votre coup : ')
            try:
                DAMIER = jouer_coup(ID_PARTIE, TYPE_COUP, (PX, PY))
                afficher_damier_ascii(DAMIER)
            except RuntimeError as err:
                print(err)
                CHOIX = input("Voulez-vous continuer à jouer, oui ou non? ")
                if CHOIX.lower() == 'non':
                    break
            except StopIteration as err:
                print(f'Le grand gagnant est le joueur {err} !\n')
                break
