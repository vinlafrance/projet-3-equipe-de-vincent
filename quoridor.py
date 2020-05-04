"""Module pour encapsuler les classes Quoridor et QuoridorError.
"""
import random
import networkx as nx


class QuoridorError(Exception):
    """Classe pour toutes les erreurs en rapport avec les règles du jeu."""


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Attributes:
        etat (dict): état du jeu tenu à jour.
        graphe (DiGraph): graphique networkx démontrant les coups possibles.
        j1 (str): nom du joueur 1.
        j1MursRestants (int): nombre de murs restants du joueur 1.
        j1Pos (tuple): coordonnées x et y du joueur 1.
        j2 (str): nom du joueur 2.
        j2MursRestants (int): nombre de murs restants du joueur 2.
        j2Pos (tuple): coordonnées x et y du joueur 2.
        mursHorizontaux (list): énumération des coordonnées x et y des murs horizontaux.
        mursVerticaux (list): énumération des coordonnées x et y des murs verticaux.

    Examples:
        >>> q.Quoridor()
    """
    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Args:
            joueurs (list): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle.
            murs (dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu.

        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """
        nbmurs = 0
        try:
            iter(joueurs)
        except TypeError:
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")
        if not len(joueurs) == 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux.")
        self.j1, self.j1mursrestants, self.j1pos = joueurs[0], 10, tuple((5, 1))
        self.j2, self.j2mursrestants, self.j2pos = joueurs[1], 10, tuple((5, 9))
        self.murshorizontaux, self.mursverticaux = [], []
        if murs:
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
            for indice, mur in enumerate(murs['horizontaux']):
                if not 1 <= mur[0] <= 8 or not 2 <= mur[1] <= 9:
                    raise QuoridorError("La position d'un mur est invalide.")
                for indice2, mur2 in enumerate(murs['horizontaux']):
                    if indice == indice2:
                        continue
                    if (mur2[0], mur2[1]) == (mur[0], mur[1]) or (mur2[0] + 1, mur2[1]) == (mur[0], mur[1]):
                        raise QuoridorError("La position d'un mur est invalide.")
                nbmurs += 1
            for indice, mur in enumerate(murs['verticaux']):
                if not 2 <= mur[0] <= 9 or not 1 <= mur[1] <= 8:
                    raise QuoridorError("La position d'un mur est invalide.")
                for indice2, mur2 in enumerate(murs['verticaux']):
                    if indice == indice2:
                        continue
                    if (mur2[0], mur2[1]) == (mur[0], mur[1]) or (mur2[0], mur2[1] + 1) == (mur[0], mur[1]):
                        raise QuoridorError("La position d'un mur est invalide.")
                nbmurs += 1
            self.murshorizontaux, self.mursverticaux = murs['horizontaux'], murs['verticaux']
        if isinstance(joueurs[0], dict):
            if joueurs[0]['murs'] > 10 or joueurs[0]['murs'] < 0:
                raise QuoridorError('''Le nombre de murs qu'un joueur peut
                                    placer est plus grand que 10, ou négatif.''')
            if not 1 <= joueurs[0]['pos'][0] <= 9 or not 1 <= joueurs[0]['pos'][1] <= 9:
                raise QuoridorError("La position d'un joueur est invalide.")
            self.j1, self.j1mursrestants = joueurs[0]['nom'], joueurs[0]['murs']
            self.j1pos = tuple(joueurs[0]['pos'])
        if isinstance(joueurs[1], dict):
            if joueurs[1]['murs'] > 10 or joueurs[1]['murs'] < 0:
                raise QuoridorError('''Le nombre de murs qu'un joueur peut placer est plus grand que
                                    10, ou négatif.''')
            if not 1 <= joueurs[1]['pos'][0] <= 9 or not 1 <= joueurs[1]['pos'][1] <= 9:
                raise QuoridorError("La position d'un joueur est invalide.")
            self.j2, self.j2mursrestants = joueurs[1]['nom'], joueurs[1]['murs']
            self.j2pos = tuple(joueurs[1]['pos'])
        nbmurs += self.j1mursrestants + self.j2mursrestants
        if not nbmurs == 20:
            raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20.")
        self.etat = self.état_partie()
        self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                        self.etat['murs']['horizontaux'],
                                        self.etat['murs']['verticaux'])

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        res = []
        ligne = 9
        for i in range(20, 0, -1):
            if i == 20:
                res.append(f'Légende: 1={self.j1}, 2={self.j2}'
                           + '\n   ' + 35 * '-' + '\n')
                continue
            if i == 2:
                res.append('--|' + 35 * '-' + '\n  | 1   2   3   4   5   6   7   8   9\n')
                break
            if i % 2 == 0:
                res.append(list('  |' + 35 * ' ' + '|\n'))
                continue
            res.append(list(f'{ligne} | .   .   .   .   .   .   .   .   . |\n'))
            ligne = ligne - 1
            continue
        for indice_ligne in range(18):
            if indice_ligne == 0:
                continue
            for x, y in self.murshorizontaux:
                if str(y) in res[indice_ligne]:
                    for z in range(7):
                        res[indice_ligne + 1][3 + 4 * (x - 1) + z] = '-'
            for x, y in self.mursverticaux:
                if str(y) in res[indice_ligne]:
                    for z in range(3):
                        res[indice_ligne - z][2 + 4 * (x - 1)] = '|'
            if str(self.j1pos[1]) in res[indice_ligne]:
                res[indice_ligne][4 + 4 * (self.j1pos[0] - 1)] = f'{1}'
            if str(self.j2pos[1]) in res[indice_ligne]:
                res[indice_ligne][4 + 4 * (self.j2pos[0] - 1)] = f'{2}'
        for k in range(18):
            res[k] = ''.join(res[k])
        return ''.join(res)

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (tuple): Le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        if joueur == 1:
            if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
                raise QuoridorError("La position est invalide (en dehors du damier).")
            if not position in self.graphe.successors(self.j1pos):
                raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
            self.j1pos = position
        elif joueur == 2:
            if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
                raise QuoridorError("La position est invalide (en dehors du damier).")
            if not position in self.graphe.successors(self.j2pos):
                raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
            self.j2pos = position
        else:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        self.etat = self.état_partie()
        self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                        self.etat['murs']['horizontaux'],
                                        self.etat['murs']['verticaux'])

    def état_partie(self):
        """Produire l'état actuel de la partie.

        Returns:
            dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.

        Examples:

            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ],
                'murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }

            où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
            au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
            associée à sa position sur le damier. Une position est représentée par un tuple
            de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

            Les murs actuellement placés sur le damier sont énumérés dans deux listes de
            positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
            est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
            situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
            mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        etat = {}
        etat['joueurs'] = [{'nom' : self.j1, 'murs' : self.j1mursrestants, 'pos' : self.j1pos},
                           {'nom' : self.j2, 'murs' : self.j2mursrestants, 'pos' : self.j2pos}]
        etat['murs'] = {}
        etat['murs']['horizontaux'] = self.murshorizontaux
        etat['murs']['verticaux'] = self.mursverticaux
        return etat

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.

        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        choix = random.randrange(0, 3)
        j1chemin = nx.shortest_path(self.graphe, self.j1pos, 'B1')
        j2chemin = nx.shortest_path(self.graphe, self.j2pos, 'B2')
        test = 0
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")
        if joueur == 1:
            if self.j1mursrestants == 0:
                choix = 2
            if choix == 0:
                for possible in j2chemin[:-1]:
                    try:
                        self.placer_mur(joueur, possible, 'horizontal')
                        typemove = 'MH'
                        position = possible
                        test = 1
                        break
                    except QuoridorError as err:
                        if str(err) == "Le mur enferme complètement un joueur.":
                            self.murshorizontaux.pop()
                            self.j1mursrestants += 1
                        continue
                if test == 0:
                    self.etat = self.état_partie()
                    self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                                    self.etat['murs']['horizontaux'],
                                                    self.etat['murs']['verticaux'])
                    self.déplacer_jeton(joueur, j1chemin[1])
                    typemove = 'D'
                    position = j1chemin[1]
            elif choix == 1:
                for possible in j2chemin[:-1]:
                    try:
                        self.placer_mur(joueur, possible, 'vertical')
                        typemove = 'MV'
                        position = possible
                        test = 1
                        break
                    except QuoridorError as err:
                        if str(err) == "Le mur enferme complètement un joueur.":
                            self.mursverticaux.pop()
                            self.j1mursrestants += 1
                        continue
                if test == 0:
                    self.etat = self.état_partie()
                    self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                                    self.etat['murs']['horizontaux'],
                                                    self.etat['murs']['verticaux'])
                    self.déplacer_jeton(joueur, j1chemin[1])
                    typemove = 'D'
                    position = j1chemin[1]
            else:
                self.déplacer_jeton(joueur, j1chemin[1])
                typemove = 'D'
                position = j1chemin[1]
        elif joueur == 2:
            if self.j2mursrestants == 0:
                choix = 2
            if choix == 0:
                for possible in j1chemin[:-1]:
                    try:
                        self.placer_mur(joueur, possible, 'horizontal')
                        typemove = 'MH'
                        position = possible
                        test = 1
                        break
                    except QuoridorError as err:
                        if str(err) == "Le mur enferme complètement un joueur.":
                            self.murshorizontaux.pop()
                            self.j2mursrestants += 1
                        continue
                if test == 0:
                    self.etat = self.état_partie()
                    self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                                    self.etat['murs']['horizontaux'],
                                                    self.etat['murs']['verticaux'])
                    self.déplacer_jeton(joueur, j2chemin[1])
                    typemove = 'D'
                    position = j2chemin[1]
            elif choix == 1:
                for possible in j1chemin[:-1]:
                    try:
                        self.placer_mur(joueur, possible, 'vertical')
                        typemove = 'MV'
                        position = possible
                        test = 1
                        break
                    except QuoridorError as err:
                        if str(err) == "Le mur enferme complètement un joueur.":
                            self.mursverticaux.pop()
                            self.j2mursrestants += 1
                        continue
                if test == 0:
                    self.etat = self.état_partie()
                    self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                                    self.etat['murs']['horizontaux'],
                                                    self.etat['murs']['verticaux'])
                    self.déplacer_jeton(joueur, j2chemin[1])
                    typemove = 'D'
                    position = j2chemin[1]
            else:
                self.déplacer_jeton(joueur, j2chemin[1])
                typemove = 'D'
                position = j2chemin[1]
        else:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        return (typemove, position)

    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.j1pos[1] == 9:
            return self.j1
        if self.j2pos[1] == 1:
            return self.j2
        return False

    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (tuple): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
            QuoridorError: Le choix d'orientation est invalide.
            QuoridorError: Le mur enferme complètement un joueur.
        """
        for x, y in self.murshorizontaux:
            if orientation == 'horizontal':
                if (position[0], position[1]) == (x + 1, y) or (position[0], position[1]) == (x - 1, y) or position == (x, y):
                    raise QuoridorError("Un mur occupe déjà cette position.")
            if orientation == 'vertical':
                if (position[0], position[1]) == (x + 1, y - 1):
                    raise QuoridorError("Un mur occupe déjà cette position.")
        for x, y in self.mursverticaux:
            if orientation == 'vertical':
                if (position[0], position[1]) == (x, y + 1) or (position[0], position[1]) == (x, y - 1) or position == (x, y):
                    raise QuoridorError("Un mur occupe déjà cette position.")
            if orientation == 'horizontal':
                if (position[0], position[1]) == (x - 1, y + 1):
                    raise QuoridorError("Un mur occupe déjà cette position.")
        if joueur == 1:
            if self.j1mursrestants == 0:
                raise QuoridorError("Le joueur a déjà placé tous ses murs.")
            if orientation == 'horizontal':
                if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
                    raise QuoridorError("La position est invalide pour cette orientation.")
                self.murshorizontaux.append(position)
            elif orientation == 'vertical':
                if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                    raise QuoridorError("La position est invalide pour cette orientation.")
                self.mursverticaux.append(position)
            else:
                raise QuoridorError("Le choix d'orientation est invalide.")
            self.j1mursrestants -= 1
        elif joueur == 2:
            if self.j2mursrestants == 0:
                raise QuoridorError("Le joueur a déjà placé tous ses murs.")
            if orientation == 'horizontal':
                if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
                    raise QuoridorError("La position est invalide pour cette orientation.")
                self.murshorizontaux.append(position)
            elif orientation == 'vertical':
                if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                    raise QuoridorError("La position est invalide pour cette orientation.")
                self.mursverticaux.append(position)
            else:
                raise QuoridorError("Le choix d'orientation est invalide.")
            self.j2mursrestants -= 1
        else:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        self.etat = self.état_partie()
        self.graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                        self.etat['murs']['horizontaux'],
                                        self.etat['murs']['verticaux'])
        for pos, objectif in [(self.j1pos, 'B1'), (self.j2pos, 'B2')]:
            if not nx.has_path(self.graphe, pos, objectif):
                raise QuoridorError("Le mur enferme complètement un joueur.")


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.

    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.

    Args:
        joueurs (list): une liste des positions (x,y) des joueurs.
        murs_horizontaux (list): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (list): une liste des positions (x,y) des murs verticaux.

    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
