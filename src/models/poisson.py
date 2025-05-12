class Poisson:
    def __init__(self, abscisse, ordonnee,tps_gestation_initial=8):
        self.tps_gestation_initial = tps_gestation_initial
        self.tps_gestation = self.tps_gestation_initial
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.est_vivant = True
        self.a_bouge = False
        self.a_mange = False
        self.a_accouche = False

    #on affecte les nouvelles coordonnées au poisson
    def deplacer(self, x, y):
        self.abscisse = x
        self.ordonnee = y
        self.tps_gestation -= 1
        
    #retourne le poisson et on utilise les coordonnées de l'objet poisson dans Mer pour 
    #ajouter un poisson dans les coordonnées précédente du poisson après l'avoir déplacé
    def reproduire(self):
        if self.tps_gestation < 0:
            self.tps_gestation = self.tps_gestation_initial
            return self.abscisse, self.ordonnee 
        return None   
