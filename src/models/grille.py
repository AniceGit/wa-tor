from typing import List, Tuple, Union
from models.poisson import Poisson
from models.requin import Requin
from models.rocher import Rocher

class Grille:
    def __init__(self,largeur,longueur):
        self.tableau = [[None for _ in range(largeur)] for _ in range(longueur)]
        self.largeur = largeur
        self.longueur = longueur
    
    
    def voisins(self, abscisse, ordonnee)->Tuple[List[Union[Poisson, Requin, Rocher, None]], List[Tuple[int, int]]]:
        directions = [(-1, 0), (1, 0), (0,-1), (0, 1)]
        coordonnee_voisins = []
        for dx, dy in directions:
            nx, ny = (abscisse + dx) % self.longueur, (ordonnee + dy) % self.largeur
            coordonnee_voisins.append((nx, ny))

        return (list(map(lambda t: self.tableau[t[0]][t[1]] , coordonnee_voisins)), coordonnee_voisins)

    def est_libre(self, x: int, y: int) -> bool:
        """
        Retourne vrai si la case de coordonnées(x modulo longueur, y modulo largeur ) est à None
        On utilise des modulos pour éviter les problèmes de débordement du tableau             
        """

        x = x % self.longueur
        y = y % self.largeur
        return self.tableau[x][y] is None