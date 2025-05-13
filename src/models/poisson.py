class Poisson:
    """
    Classe représentant un poisson dans la simulation Wa-Tor.
    Un poisson peut se déplacer et se reproduire.
    """
    
    def __init__(self, abscisse, ordonnee, tps_gestation_initial=8):
        """
        Initialise un nouveau poisson.
        
        Args:
            abscisse: Position x initiale du poisson
            ordonnee: Position y initiale du poisson
            tps_gestation_initial: Temps nécessaire avant de pouvoir se reproduire
        """
        self.tps_gestation_initial = tps_gestation_initial
        self.tps_gestation = self.tps_gestation_initial
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.est_vivant = True
        self.a_bouge = False
        self.a_accouche = False
    
    def deplacer(self, x, y):
        """
        Déplace le poisson vers de nouvelles coordonnées.
        Réduit également le temps de gestation restant.
        
        Args:
            x: Nouvelle position x
            y: Nouvelle position y
        """
        self.abscisse = x
        self.ordonnee = y
        self.tps_gestation -= 1
        self.a_bouge = True
    
    def reproduire(self):
        """
        Vérifie si le poisson peut se reproduire.
        Si oui, réinitialise le temps de gestation.
        
        Returns:
            bool: True si le poisson peut se reproduire, False sinon
        """
        if self.tps_gestation <= 0:
            self.tps_gestation = self.tps_gestation_initial
            return True
        return False

