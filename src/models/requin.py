from typing import List, Tuple, Union
from models.poisson import Poisson

class Requin(Poisson):
    """
    Représente un requin dans la simulation, héritant du comportement d'un Poisson.

    Le requin possède de l'énergie qu'il perd en se déplaçant et qu'il regagne en mangeant.

    Attributs supplémentaires
    -------------------------
    energie_initiale : int
        Quantité d'énergie de départ du requin.
    energie : int
        Énergie actuelle du requin, diminue avec les déplacements et augmente en mangeant.
    """

    def __init__(self, abscisse: int, ordonnee: int, tps_gestation: int = 8):
        """
        Initialise un requin avec sa position, son temps de gestation et son énergie.

        Paramètres
        ----------
        abscisse : int
            Coordonnée verticale (ligne) initiale du requin.
        ordonnee : int
            Coordonnée horizontale (colonne) initiale du requin.
        tps_gestation : int, optionnel
            Temps de gestation avant reproduction (par défaut 8).
        """
        super().__init__(abscisse, ordonnee, tps_gestation)
        self.energie_initiale = 6
        self.energie = self.energie_initiale
        self.age = 30

    def manger(self) -> None:
        """
        Augmente l'énergie du requin lorsqu'il mange un poisson.
        """
        self.energie += 4  # Gain d'énergie en mangeant un poisson

    def deplacer(self, x: int, y: int) -> None:
        """
        Déplace le requin vers une nouvelle position, tout en réduisant son énergie.

        Paramètres
        ----------
        x : int
            Nouvelle abscisse (ligne).
        y : int
            Nouvelle ordonnée (colonne).
        """
        super().deplacer(x, y)
        self.energie -= 1  # Perte d'énergie en se déplaçant
