class Rocher:
    """
    Représente un rocher immobile dans la simulation.

    Contrairement aux entités vivantes comme les poissons ou les requins, 
    le rocher ne se déplace pas, ne se reproduit pas et ne change pas d’état.

    Attributs
    ----------
    abscisse : int
        Position verticale (ligne) du rocher dans la grille.
    ordonnee : int
        Position horizontale (colonne) du rocher dans la grille.
    est_vivant : bool
        Attribut utilisé pour uniformiser la logique, bien qu’un rocher soit inerte (toujours True ici).
    type : str
        Chaîne identifiant l’objet comme un rocher (valeur : 'rocher').
    """

    def __init__(self, abscisse: int, ordonnee: int):
        """
        Initialise un rocher à une position donnée dans la grille.

        Paramètres
        ----------
        abscisse : int
            Coordonnée verticale (ligne) du rocher.
        ordonnee : int
            Coordonnée horizontale (colonne) du rocher.
        """
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.est_vivant = True
        self.type = 'rocher'
