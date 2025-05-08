from models.poisson import Poisson

class Requin(Poisson):

    def __init__(self, tps_gestation, abscisse, ordonnee, energie):
        super().__init__(tps_gestation, abscisse, ordonnee)
        self.energie = energie

    #on vérifie s'il y a un poisson donné est voisin de requin
    #et si oui on retourne True afin de pouvoir requin.manger() dans Mer
    #et supprimé le poisson mangé de la grille
    def est_voisin(self, x, y) -> bool:
        cotes = [[0,1],[-1,0],[0,-1],[1,0]]
        for xy in cotes:
            if x == self.abscisse + xy[0] and y == self.ordonnee + xy[1]:
                return True
        return False
    
    def manger(self):
        self.energie += 5

                
