from models.poisson import Poisson

class Requin(Poisson):

    def __init__(self,abscisse, ordonnee, tps_gestation =6):
        super().__init__(abscisse, ordonnee,tps_gestation)
        self.energie_initiale = 5
        self.energie = self.energie_initiale
        self.age = 30
        

    def manger(self):
        # self.energie += self.energie_initiale
        self.energie += 4

    def deplacer(self, x, y):
        super().deplacer(x, y)
        self.energie -= 1
        

                
