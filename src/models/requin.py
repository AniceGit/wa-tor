from src.models.poisson import Poisson

class Requin(Poisson):
        def __init__(self, tps_gestation, abscisse, ordonnee, energie):
            super().__init__(tps_gestation, abscisse, ordonnee)
            self.energie = energie
        def manger():
            pass