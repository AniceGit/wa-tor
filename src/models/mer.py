from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille
#from src.models.poisson import Poisson
#from src.models.requin import Requin
#from src.models.grille import Grille

class Mer:
    def __init__(self, grille):
        self.grille = grille

    def ajout_poisson(self, abscisse, ordonnee, un_poisson):
        abscisse = un_poisson.abscisse % self.grille.largeur
        ordonnee = un_poisson.ordonnee % self.grille.longueur
        if self.grille.tableau[abscisse][ordonnee] is None:
            self.grille.tableau[abscisse][ordonnee] = un_poisson
        else:
                print(f"Case ({abscisse},{ordonnee}) déjà occupée.")

def test():
    ma_grille = Grille(10,5)
    ma_mer = Mer(ma_grille)
    dico_p1 = {'tps_gestation' : 3, 'abscisse' : 1, 'ordonnee' : 1}
    dico_r1 = {'tps_gestation' : 5, 'abscisse' : 2 , 'ordonnee' : 2, 'energie' : 10}
    p1 = Poisson(**dico_p1)
    r1 = Requin(**dico_r1)
    ma_mer.ajout_poisson(1, 1, p1)
    ma_mer.ajout_poisson(2, 2, r1)
    print(ma_mer)   

if __name__ == "__main__":
    test()

