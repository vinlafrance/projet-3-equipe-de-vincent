# -*- coding: utf-8 -*-
"""Module d'API du jeu Quoridor

Ce module permet d'interagir avec le serveur
afin de pouvoir jouer contre un adversaire robotisé.

Attributes:
    URL (str): Début de l'url du serveur de jeu.

Functions:
    * initialiser_partie - Retourne un tuple constitué de l'identifiant
                           de la partie et de l'état initial du jeu
    * jouer_coup - Retourne un dictionnaire représentant l'état actuel du jeu
"""
import requests

URL = "https://python.gel.ulaval.ca/quoridor/api"

def initialiser_partie(idul):
    """Initialiser une nouvelle partie.

    Initialise une partie en effectuant une requête à l'URL cible
    /quoridor/api/initialiser/

    Cette requête est de type POST.

    Elle s'attend en entrée à recevoir une seule donnée nommée idul,
    toujours sous la forme d'une chaîne de caractères. Elle retourne
    en JSON un dictionnaire contenant les clés suivantes:

        id: l'identifiant de la nouvelle partie;
        état: l'état initial du jeu sous la forme d'un dictionnaire;
        message (optionnel): un message en cas d'erreur.

    Args:
        idul (str): Identifiant du joueur.

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie et de l'état initial du jeu.

    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.

    Examples:
        >>> idul = 'josmi42'
        >>> partie = initialiser_partie(idul)
        >>> print(partie)
        ('c1493454-1f7f-446f-9c61-bd7a9d66c92d', { 'joueurs': ... })
    """
    rep = requests.post(f'{URL}/initialiser/', data={'idul': idul})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep:
            raise RuntimeError(rep['message'])
    else:
        raise RuntimeError(f"le POST sur {URL} a produit le code d'erreur {rep.status_code}.")
    return (rep['id'], rep['état'])


def jouer_coup(id_partie, type_coup, position):
    """Jouer votre coup dans une partie en cours

    Joue un coup en effectuant une requête à l'URL cible
    /quoridor/api/jouer/

    Cette requête est de type POST.

    Elle s'attend à recevoir en entrée trois (3) paramètres associés au POST:

        id: l'identifiant de la partie;
        type: le type de coup du joueur
              'D' pour déplacer le jeton,
              'MH' pour placer un mur horizontal,
              'MV' pour placer un mur vertical;
        pos: la position (x, y) du coup.

    Elle retourne en JSON un dictionnaire contenant les clés suivantes:

        état: l'état actuel du jeu;
        message (optionnel): un message en cas d'erreur;
        gagnant (optionnel): le nom du joueur gagnant si la partie est terminée.

    Args:
        id_partie (str): Identifiant de la partie.
        type_coup (str): Type de coup du joueur :
                            'D' pour déplacer le jeton,
                            'MH' pour placer un mur horizontal,
                            'MV' pour placer un mur vertical;
        position (tuple): La position (x, y) du coup.

    Returns:
        dict: Uniquement le dictionnaire représentant l'état actuel du jeu,
            après avoir décodé le JSON de sa réponse.

    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.
        StopIteration: Erreur levée lorsqu'il y a présence d'un gagnant
            dans la réponse du serveur.

    Examples:
        >>> id_partie = 'c1493454-1f7f-446f-9c61-bd7a9d66c92d'
        >>> type_coup = 'D'
        >>> position = (3, 5)
        >>> partie = jouer_coup(id_partie, type_coup, position)
        >>> print(partie)
        { 'joueurs': ..., 'murs': ... }
    """
    rep = requests.post(f'{URL}/jouer/', data={'id': id_partie, 'type': type_coup, 'pos': position})
    if rep.status_code == 200:
        rep = rep.json()
        if 'gagnant' in rep:
            raise StopIteration(rep['gagnant'])
        if 'message' in rep:
            raise RuntimeError(rep['message'])
    else:
        raise RuntimeError(f"le POST sur {URL} a produit le code d'erreur {rep.status_code}.")
    return rep['état']
