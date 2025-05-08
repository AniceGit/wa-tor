from models.poisson import Poisson
from models.requin import Requin

class Grille:
    def __init__(self,largeur,longueur):
        self.tableau = [[None for _ in range(largeur)] for _ in range(longueur)]
        self.largeur = largeur
        self.longueur = longueur
    
    def __str__(self):

        sortie = ''
        for ligne in self.grille:
            for case in ligne:
                if case is None:
                    sortie += '\033[44m🌊\033[0m'
                elif isinstance(case, Requin):
                    sortie += '\033[41m🦈\033[0m'
                elif isinstance(case, Poisson):
                    sortie += '\033[43m🐟\033[0m'
            sortie += "\n"
        return sortie

    def repr(self):
        return str(self)
    
    def voisins(self, abscisse, ordonnee):
        directions = [(-1, 0), (1, 0), (0,-1), (0, 1),(-1,-1),(-1, 1),(1, 1),(1, -1)]
        coordonnee_voisins = []
        for dx, dy in directions:
            nx, ny = (abscisse + dx) % self.largeur, (ordonnee + dy) % self.longueur
            coordonnee_voisins.append((nx, ny))
        return list(map(lambda t: self.tableau[t[0]][t[1]], coordonnee_voisins))
