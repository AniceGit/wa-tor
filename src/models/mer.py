from src.models.poisson import Poisson
from src.models.requin import Requin
from src.models.grille import Grille

class Mer:
    def __init__(self):
        self.mer = [[None for _ in range(50)] for _ in range(30)]

    def ajout_poisson(self, mon_poisson):
        x = mon_poisson.x_coordinate
        y = mon_poisson.y_coordinate
        if 0 <= x < len(self.mer) and 0 <= y < len(self.mer[0]):
            if self.mer[x][y] is None:
                self.mer[x][y] = mon_poisson
            else:
                print(f"Case ({x},{y}) déjà occupée.")
        else:
            print(f"Coordonnées ({x},{y}) hors limites.")

    def print_mer(self):
        """fonction pour imprimer la mer, avec une variable en fonction de si la case est vide ou occupée.
        """
        for row in self.mer:
            for cell in row:
                if cell is None:
                    print('\033[44m🌊\033[0m', end='')  # océan bleu
                elif isinstance(cell, Poisson):
                    print('\033[43m🐟\033[0m', end='')  # poisson jaune
                elif isinstance(cell, Requin):
                    print('\033[41m🦈\033[0m', end='')  # requin rouge
                else:
                    print(f'{cell} ', end='')  # debug
            print()  
