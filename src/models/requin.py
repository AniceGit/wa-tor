from models.poisson import Poisson
class Requin(Poisson):
    """
    Classe représentant un requin dans la simulation Wa-Tor.
    Un requin est un type spécial de poisson qui a besoin de manger
    d'autres poissons pour survivre.
    """
    
    def __init__(self, abscisse, ordonnee, tps_gestation=11):
        """
        Initialise un nouveau requin.
        
        Args:
            abscisse: Position x initiale du requin
            ordonnee: Position y initiale du requin
            tps_gestation: Temps nécessaire avant de pouvoir se reproduire
        """
        super().__init__(abscisse, ordonnee, tps_gestation)
        self.energie_initiale = 8
        self.energie = self.energie_initiale
        self.a_mange = False
    
    def manger(self):
        """
        Le requin mange un poisson et regagne de l'énergie.
        """
        self.energie += self.energie_initiale
        self.a_mange = True
    
    def deplacer(self, x, y):
        """
        Déplace le requin vers de nouvelles coordonnées.
        Le requin perd de l'énergie à chaque déplacement.
        
        Args:
            x: Nouvelle position x
            y: Nouvelle position y
        """
        super().deplacer(x, y)
        self.energie -= 1