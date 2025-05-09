from typing import List
from models.poisson import Poisson
from models.requin import Requin

class Grille:
    def __init__(self,largeur,longueur):
        self.tableau = [[None for _ in range(largeur)] for _ in range(longueur)]
        self.largeur = largeur
        self.longueur = longueur
    
    
    def voisins(self, abscisse, ordonnee)->List[Poisson]:
        directions = [(-1, 0), (1, 0), (0,-1), (0, 1)]
        coordonnee_voisins = []
        for dx, dy in directions:
            nx, ny = (abscisse + dx) % self.largeur, (ordonnee + dy) % self.longueur
            coordonnee_voisins.append((nx, ny))

        return (list(map(lambda t: self.tableau[t[0]][t[1]] , coordonnee_voisins)), coordonnee_voisins)
