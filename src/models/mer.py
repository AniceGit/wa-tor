from poisson import Poisson
from requin import Requin
from grille import Grille

class Mer:
    def init(self, grille):
        self.grille = grille

    def ajout_poisson(self, abscisse, ordonnee, un_poisson):
        abscisse = un_poisson.abscisse % self.grille.largueur
        ordonnee = un_poisson.ordonnee % self.grille.longueur
        if self.grille[abscisse][ordonnee] is None:
            self.grille[abscisse][ordonnee] = un_poisson
        else:
                print(f"Case ({abscisse},{ordonnee}) déjà occupée.")