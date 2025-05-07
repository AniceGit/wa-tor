from src.models.poisson import Poisson
from src.models.requin import Requin

class Grille:
    def init(self,largeur,longueur):
        self.grille = [[None for _ in range(largeur)] for _ in range(longueur)]
        self.largeur = largeur
        self.longueur = longueur

    def str(self):
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