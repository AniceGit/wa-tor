from models.poisson import Poisson

class Requin(Poisson):

    def __init__(self,abscisse, ordonnee, energie):
        super().__init__(abscisse, ordonnee)
        self.energie_initiale = 5
        self.energie = self.energie_initiale

    def manger(self):
        self.energie += self.energie_initiale

    def deplacer(self, x, y):
        super().deplacer(x, y)
        self.energie -= 1

                
