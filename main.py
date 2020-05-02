# -*- coding: utf-8 -*-
"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.

Functions:
    * analyser_commande - Retourne la liste des parties reçues du serveur

Examples:

    `> python3 main.py --help`

        usage: main.py [-h] [-a] [-x] idul

        Jeu Quoridor - phase 3

        positional arguments:
          idul               IDUL du joueur.

        optional arguments:
          -h, --help         show this help message and exit
          -a, --automatique  Activer le mode automatique.
          -x, --graphique    Activer le mode graphique.
"""
import argparse
from api import initialiser_partie, jouer_coup
from quoridor import Quoridor
from quoridorx import QuoridorX

def analyser_commande():
    """Génère un analyseur de ligne de commande

    En utilisant le module argparse, génère un analyseur de ligne de commande.

    L'analyseur offre (1) argument positionnel:
        idul: IDUL du joueur.

    Ainsi que les (3) arguments optionnels:
        help: show this help message and exit
        automatique: Activer le mode automatique.
        graphique: Activer le mode graphique.

    Returns:
        Namespace:  Retourne un objet de type Namespace possédant
                    les clefs «idul», «automatique» et «graphique».
    """
    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase 3")
    parser.add_argument('idul', help='IDUL du joueur.')
    parser.add_argument('-a', '--automatique', action='store_true', dest='automatique',
                        help='Activer le mode automatique.')
    parser.add_argument('-x', '--graphique', action='store_true', dest='graphique',
                        help='Activer le mode graphique.')
    return parser.parse_args()

if __name__ == "__main__":
    ARGS = analyser_commande()
    if ARGS.automatique and ARGS.graphique:
        print('automatique et graphique')
    elif ARGS.automatique:
        print('automatique')
    elif ARGS.graphique:
        print('graphique')
    else:
        print('manuel')
        PARTIE = initialiser_partie(ARGS.idul)
        ID_PARTIE = PARTIE[0]
        q = Quoridor(PARTIE[1]['joueurs'], PARTIE[1]['murs'])
        print(q)
        while True:
            print('''Type de coup disponible :
- D : Déplacement
- MH: Mur Horizontal
- MV: Mur Vertical\n''')
            TYPE_COUP = input('Choisissez votre type de coup (D, MH ou MV) : ')
            PX = input('Définissez la colonne de votre coup : ')
            PY = input('Définissez la ligne de votre coup : ')
            try:
                DAMIER = jouer_coup(ID_PARTIE, TYPE_COUP, (PX, PY))
                q = Quoridor(DAMIER['joueurs'], DAMIER['murs'])
                print(q)
            except RuntimeError as err:
                print(err)
                CHOIX = input("Voulez-vous continuer à jouer, oui ou non? ")
                if CHOIX.lower() == 'non':
                    break
            except StopIteration as err:
                print(f'Le grand gagnant est le joueur {err} !\n')
                break
