class Poisson:
    def __init__(self, tps_gestation, abscisse, ordonnee):
        self.tps_gestation = tps_gestation
        self.abscisse = abscisse
        self.ordonnee = ordonnee

    #on affecte les nouvelles coordonnées au poisson
    def deplacer(self, x, y):
        self.abscisse = x
        self.ordonnee = y
        self.tps_gestation -= 1
        #return self.reproduire()
        

    #on vérifie s'il y a un poisson donné est voisin de requin
    #et si oui on retourne True afin de pouvoir requin.manger() dans Mer
    #et supprimé le poisson mangé de la grille
    # def est_voisin(self) -> bool:
    #     cotes = [[0,1],[-1,0],[0,-1],[1,0]]
    #     liste_voisin = []
        
    #     for xy in cotes:

    #         nx = self.abscisse + xy[0]
    #         ny = self.ordonnee + xy[1]

    #         if x == self.abscisse + xy[0] and y == self.ordonnee + xy[1]:
    #             return True
    #     return False
    

    #retourne le poisson et on utilise les coordonnées de l'objet poisson dans Mer pour 
    #ajouter un poisson dans les coordonnées précédente du poisson après l'avoir déplacé
    def reproduire(self):
        if self.tps_gestation < 0:
            self.tps_gestation = 5
            return self.abscisse, self.ordonnee 
        return None   
