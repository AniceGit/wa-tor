class Poisson:
    def __init__(self, tps_gestation, abscisse, ordonnee):
        self.tps_gestation = tps_gestation
        self.abscisse = abscisse
        self.ordonnee = ordonnee

    #on affecte les nouvelles coordonnées au poisson
    def deplacer(self, x, y):
        self.abscisse = x
        self.ordonnee = y
    

    #retourne le poisson et on utilise les coordonnées de l'objet poisson dans Mer pour 
    #ajouter un poisson dans les coordonnées précédente du poisson après l'avoir déplacé
    def reproduire(self):
        if self.tps_gestation <= 0:
            self.tps_gestation = 5
            return self 
        return None   
