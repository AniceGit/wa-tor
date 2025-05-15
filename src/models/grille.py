from typing import List, Tuple, Union
from models.poisson import Poisson
from models.requin import Requin
from models.rocher import Rocher

class Grille:
    """
    Représente une grille bidimensionnelle contenant des objets de type Requin, Poisson, Rocher, ou None.

    Attributs
    ----------
    tableau : List[List[Union[Requin, Poisson, Rocher, None]]]
        Représentation en 2D de la grille.
    largeur : int
        Nombre de colonnes dans la grille.
    longueur : int
        Nombre de lignes dans la grille.
    """
    def __init__(self, largeur: int, longueur: int):
        """
        Initialise une grille vide de dimensions spécifiées.

        Paramètres
        ----------
        largeur : int
            Largeur (nombre de colonnes) de la grille.
        longueur : int
            Longueur (nombre de lignes) de la grille.
        """
        self.tableau: List[List[Union[Requin, Poisson, Rocher, None]]] = [[None for _ in range(largeur)] for _ in range(longueur)]
        self.largeur = largeur
        self.longueur = longueur
    
    def voisins(self, abscisse: int, ordonnee: int) -> Tuple[List[Union[Poisson, Requin, Rocher, None]], List[Tuple[int, int]]]:
        """
        Retourne les entités voisines et leurs coordonnées autour d'une position donnée.

        Les voisins sont les cellules directement adjacentes (haut, bas, gauche, droite),
        et le tableau est considéré comme torique (les bords sont connectés).

        Paramètres
        ----------
        abscisse : int
            Position verticale (ligne) de la cellule.
        ordonnee : int
            Position horizontale (colonne) de la cellule.

        Retourne
        -------
        Tuple[List[Union[Poisson, Requin, Rocher, None]], List[Tuple[int, int]]]
            Une liste des entités voisines (valeurs dans la grille) et une liste de leurs coordonnées correspondantes.
        """
        directions = [(-1, 0), (1, 0), (0,-1), (0, 1)]
        coordonnee_voisins = []
        for dx, dy in directions:
            nx, ny = (abscisse + dx) % self.longueur, (ordonnee + dy) % self.largeur
            coordonnee_voisins.append((nx, ny))

        return (list(map(lambda t: self.tableau[t[0]][t[1]] , coordonnee_voisins)), coordonnee_voisins)

    def est_libre(self, x: int, y: int) -> bool:
        """
        Vérifie si une cellule de la grille est libre (None), en tenant compte du débordement via modulo.

        Paramètres
        ----------
        x : int
            Coordonnée verticale (ligne).
        y : int
            Coordonnée horizontale (colonne).

        Retourne
        -------
        bool
            True si la cellule est vide (None), False sinon.
        """
        x = x % self.longueur
        y = y % self.largeur
        return self.tableau[x][y] is None
