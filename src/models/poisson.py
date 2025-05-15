from typing import Tuple, Union

class Poisson:
    """
    Représente un poisson dans une simulation de vie marine.

    Attributs
    ----------
    abscisse : int
        Position verticale actuelle du poisson dans la grille.
    ordonnee : int
        Position horizontale actuelle du poisson dans la grille.
    tps_gestation_initial : int
        Temps nécessaire avant de pouvoir se reproduire à nouveau.
    tps_gestation : int
        Temps restant avant que le poisson puisse se reproduire.
    est_vivant : bool
        Indique si le poisson est encore en vie.
    a_bouge : bool
        Indique si le poisson s'est déjà déplacé pendant le tour actuel.
    a_mange : bool
        Indique si le poisson a mangé pendant le tour actuel.
    a_accouche : bool
        Indique si le poisson s'est reproduit pendant le tour actuel.
    age : int
        Âge restant du poisson avant sa mort naturelle.
    """

    def __init__(self, abscisse: int, ordonnee: int, tps_gestation_initial: int = 4):
        """
        Initialise un poisson avec sa position et son temps de gestation.

        Paramètres
        ----------
        abscisse : int
            Coordonnée verticale (ligne) de départ du poisson.
        ordonnee : int
            Coordonnée horizontale (colonne) de départ du poisson.
        tps_gestation_initial : int, optionnel
            Temps de gestation initial (par défaut à 4).
        """
        self.tps_gestation_initial = tps_gestation_initial
        self.tps_gestation = self.tps_gestation_initial
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.est_vivant = True
        self.a_bouge = False
        self.a_mange = False
        self.a_accouche = False
        self.age = 20

    def deplacer(self, x: int, y: int) -> None:
        """
        Déplace le poisson vers de nouvelles coordonnées et met à jour son état.

        Réduit aussi le temps de gestation et l'âge du poisson.

        Paramètres
        ----------
        x : int
            Nouvelle abscisse (ligne).
        y : int
            Nouvelle ordonnée (colonne).
        """
        self.abscisse = x
        self.ordonnee = y
        self.tps_gestation -= 1
        self.age -= 1

    def reproduire(self) -> Union[Tuple[int, int], None]:
        """
        Tente de reproduire le poisson si son temps de gestation est écoulé.

        Retourne les coordonnées du poisson pour créer une nouvelle instance si la reproduction est possible.
        Réinitialise le temps de gestation après reproduction.

        Retourne
        -------
        Union[Tuple[int, int], None]
            Un tuple contenant les coordonnées actuelles du poisson si reproduction,
            ou None si le poisson n'est pas prêt à se reproduire.
        """
        if self.tps_gestation < 0:
            self.tps_gestation = self.tps_gestation_initial
            return self.abscisse, self.ordonnee 
        return None

