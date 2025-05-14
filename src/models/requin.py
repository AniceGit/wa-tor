from typing import List, Tuple, Union
from models.poisson import Poisson
class Requin(Poisson):
    def __init__(self, abscisse, ordonnee, tps_gestation=8):
        super().__init__(abscisse, ordonnee, tps_gestation)
        self.energie_initiale = 6
        self.energie = self.energie_initiale
        self.age = 30
        
    def manger(self):
        self.energie += 4  # Gain d'énergie en mangeant un poisson
        
    def deplacer(self, x, y):
        super().deplacer(x, y)
        self.energie -= 1  # Perte d'énergie en se déplaçant