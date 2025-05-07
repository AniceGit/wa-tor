class Poisson:
    def __init__(self, tps_gestation, abscisse, ordonnee):
        self.tps_gestation = tps_gestation
        self.abscisse = abscisse
        self.ordonnee = ordonnee

    def deplacer(self, x, y):
        self.abscisse = x
        self.ordonnee = y
    

    def reproduire(self):
        if self.tps_gestation <= 0:
            self.tps_gestation = 5
            return self 
        return None   