from typing import List, Union, Tuple
from math import sqrt

import random
from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille

class Mer:
    def __init__(self, grille):
        self.grille: Grille = grille
        self.liste_poissons:List[Poisson] = []

    def ajout_poisson(self, un_poisson:Poisson):
        abscisse = un_poisson.abscisse % self.grille.longueur
        ordonnee = un_poisson.ordonnee % self.grille.largeur

        self.grille.tableau[abscisse][ordonnee] = un_poisson

    def ajout_poissons_liste(self, nb_poissons: int, nb_requins: int) -> List[Union[Poisson, Requin]]:
        liste_poissons: List[Union[Poisson, Requin]] = []
        total = nb_poissons + nb_requins
        largeur = self.grille.largeur
        longueur = self.grille.longueur

        cases_disponibles = [(x, y) for x in range(longueur) for y in range(largeur)]
        random.shuffle(cases_disponibles)
        cases_choisies = cases_disponibles[:total]

        for i in range(nb_poissons):
            x, y = cases_choisies[i]
            poisson = Poisson(x, y)
            self.grille.tableau[x][y] = poisson
            liste_poissons.append(poisson)

        for i in range(nb_poissons, total):
            x, y = cases_choisies[i]
            requin = Requin(x, y)
            self.grille.tableau[x][y] = requin
            liste_poissons.append(requin)

        self.liste_poissons = liste_poissons
        return liste_poissons

    
    
    def deplacer_tous(self):
        """
        Déplace tous les poissons et requins dans la grille.
        Gère les interactions entre les organismes (déplacement, reproduction, alimentation).
        Les organismes morts sont retirés à la fin du cycle.
        """
        liste_nouveaux_nes = []

        for poisson in list(self.liste_poissons):  # Utilise une copie pour éviter les problèmes de modification pendant l'itération
            if not poisson.est_vivant:
                continue

            abscisse = poisson.abscisse
            ordonnee = poisson.ordonnee
            voisins, coord_voisins = self.grille.voisins(abscisse, ordonnee)

            if isinstance(poisson, Requin):
                # Trouve un poisson cible avec KNN
                cible = None
                try:
                    proches_poissons = [(dist, p) for dist, p in self.KNN_requin(poisson, k=1) 
                                    if not isinstance(p, Requin) and p.est_vivant]
                    if proches_poissons:
                        _, cible = proches_poissons[0]
                except Exception as e:
                    print(f"Erreur dans KNN: {e}")
                    cible = None

                # Logique de déplacement pour le requin
                if cible:
                    # Calcule la direction vers la cible en tenant compte du monde toroïdal
                    dx = (cible.abscisse - abscisse + self.grille.longueur//2) % self.grille.longueur - self.grille.longueur//2
                    dy = (cible.ordonnee - ordonnee + self.grille.largeur//2) % self.grille.largeur - self.grille.largeur//2
                    
                    # Normalise pour obtenir la direction (-1, 0, ou 1)
                    dx = (1 if dx > 0 else -1 if dx < 0 else 0)
                    dy = (1 if dy > 0 else -1 if dy < 0 else 0)

                    # Essaie de se déplacer horizontalement d'abord
                    nouveau_x = (abscisse + dx) % self.grille.longueur
                    nouveau_y = ordonnee
                    moved = False

                    if dx != 0 and self.grille.est_libre(nouveau_x, nouveau_y):
                        moved = True  # Déplacement horizontal possible
                    elif dy != 0:
                        # Essaie le déplacement vertical si horizontal impossible
                        tmp_x = abscisse
                        tmp_y = (ordonnee + dy) % self.grille.largeur
                        if self.grille.est_libre(tmp_x, tmp_y):
                            nouveau_x, nouveau_y = tmp_x, tmp_y
                            moved = True
                    
                    # Vérifie si on peut manger le poisson cible
                    target_position = ((abscisse + dx) % self.grille.longueur, 
                                    (ordonnee + dy) % self.grille.largeur)
                    
                    if (target_position[0], target_position[1]) == (cible.abscisse, cible.ordonnee):
                        # Le requin mange le poisson
                        cible.est_vivant = False
                        self.grille.tableau[cible.abscisse][cible.ordonnee] = None
                        poisson.manger()
                        nouveau_x, nouveau_y = cible.abscisse, cible.ordonnee
                        moved = True
                    
                    # Déplace le requin si possible
                    if moved:
                        # Efface l'ancienne position
                        self.grille.tableau[abscisse][ordonnee] = None
                        # Met à jour la position du requin
                        poisson.deplacer(nouveau_x, nouveau_y)
                        # Met à jour la grille avec le requin à la nouvelle position
                        self.grille.tableau[nouveau_x][nouveau_y] = poisson
                else:
                    # Aucun poisson cible trouvé, se déplace aléatoirement si possible
                    free_spaces = [(i, pos) for i, (pos, content) in enumerate(zip(coord_voisins, voisins)) if content is None]
                    if free_spaces:
                        idx, (nouveau_x, nouveau_y) = random.choice(free_spaces)
                        # Efface l'ancienne position
                        self.grille.tableau[abscisse][ordonnee] = None
                        # Met à jour la position du requin
                        poisson.deplacer(nouveau_x, nouveau_y)
                        # Met à jour la grille avec le requin à la nouvelle position
                        self.grille.tableau[nouveau_x][nouveau_y] = poisson

                # Gère la reproduction du requin
                peut_reproduire = poisson.reproduire()
                if peut_reproduire:  # Si la reproduction est possible
                    nouveau_ne = Requin(abscisse, ordonnee)
                    liste_nouveaux_nes.append(nouveau_ne)
                    self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                    poisson.a_accouche = True

                # Vérifie si le requin meurt de faim
                if poisson.energie <= 0:
                    poisson.est_vivant = False
                    self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None

            else:  # Déplacement d'un poisson normal
                # Trouve les cellules voisines vides
                free_spaces = [(i, pos) for i, (pos, content) in enumerate(zip(coord_voisins, voisins)) if content is None]
                
                if free_spaces:
                    # Choisit une cellule vide aléatoire
                    idx, (nouveau_x, nouveau_y) = random.choice(free_spaces)
                    
                    # Gère la reproduction du poisson
                    peut_reproduire = poisson.reproduire()
                    if peut_reproduire:  # Si la reproduction est possible
                        nouveau_ne = Poisson(abscisse, ordonnee)
                        liste_nouveaux_nes.append(nouveau_ne)
                        self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                        poisson.a_accouche = True
                    else:
                        # Si pas de reproduction, efface l'ancienne cellule
                        self.grille.tableau[abscisse][ordonnee] = None
                    
                    # Déplace le poisson
                    poisson.deplacer(nouveau_x, nouveau_y)
                    self.grille.tableau[nouveau_x][nouveau_y] = poisson

        # Ajoute les nouveau-nés à la liste
        self.liste_poissons.extend(liste_nouveaux_nes)

        # Retire les organismes morts
        self.liste_poissons = [p for p in self.liste_poissons if p.est_vivant]

        # Réinitialise les états pour le prochain tour
        for p in self.liste_poissons:
            p.a_bouge = False
            p.a_accouche = False
            if isinstance(p, Requin):
                p.a_mange = False









    def __str__(self):
        sortie = ""
        for ligne in self.grille.tableau:
            for case in ligne:
                if case is None:
                    sortie += '\033[44m🌊\033[0m'
                elif isinstance(case, Requin):
                    sortie += '\033[41m🦈\033[0m'
                elif isinstance(case, Poisson):
                    sortie += '\033[42m🐟\033[0m'
            sortie += "\n"
        return sortie 

    def __repr__(self):
        return str(self)


    def KNN_requin(self, requin: Requin, k: int = 1) -> List[Tuple[float, Poisson]]:
        """
        Trouve les k poissons les plus proches du requin en utilisant la distance de Manhattan.
        Prend en compte la nature toroïdale du monde (bords connectés).
        
        Args:
            requin: Le requin qui cherche une proie
            k: Nombre de plus proches voisins à renvoyer (par défaut 1)
            
        Returns:
            Liste de tuples (distance, poisson) triés par distance croissante
        """
        liste_distances = []
        
        for poisson in self.liste_poissons:
            # Ne considère que les poissons vivants (pas les requins)
            if not isinstance(poisson, Requin) and poisson.est_vivant:
                # Calcule la distance de Manhattan en tenant compte du monde toroïdal
                dist = self.distance_manhattan(
                    requin.abscisse, requin.ordonnee, 
                    poisson.abscisse, poisson.ordonnee
                )
                liste_distances.append((dist, poisson))
        
        # Trie par distance et renvoie les k plus proches poissons
        liste_distances.sort(key=lambda x: x[0])
        
        # Renvoie soit le nombre demandé de voisins, soit tous si moins existent
        return liste_distances[:k] if liste_distances else []

    def distance_manhattan(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        Calcule la distance de Manhattan sur un monde toroïdal.
        Prend le chemin le plus court (en contournant les bords si nécessaire).
        
        Args:
            x1, y1: Coordonnées du premier point
            x2, y2: Coordonnées du deuxième point
            
        Returns:
            La distance de Manhattan minimale entre les deux points
        """
        # Calcule la distance en x en tenant compte du monde circulaire
        dx = min(
            abs(x2 - x1), 
            self.grille.longueur - abs(x2 - x1)
        )
        
        # Calcule la distance en y en tenant compte du monde circulaire
        dy = min(
            abs(y2 - y1), 
            self.grille.largeur - abs(y2 - y1)
        )
        
        return dx + dy




def testKNN():
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)

    # Ajoute 100 poissons et 1 requin
    ma_mer.ajout_poissons_liste(100, 1)

    for poisson in ma_mer.liste_poissons:
        if isinstance(poisson, Requin):
            plus_proche = ma_mer.KNN_requin(poisson, k=1)
            print(f"Le poisson le  plus proches de {poisson} est :")
            print(f"  - {plus_proche[1]}, il est à une distance de {plus_proche[0]:.2f}")
            print(f"  - ses coordonnées sont : {plus_proche[1].abscisse} {plus_proche[1].ordonnee}")

def test():
    longueur = 40
    largeur = 25
    ma_grille = Grille(longueur,largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_liste(100,5)
    
    print(ma_mer)
    
    print("*****************")
    for _ in range(100):
        ma_mer.deplacer_tous()
        print(ma_mer)

if __name__ == "__main__":
    test()
#     print("Salut de mer")
#     testKNN()


                



# if __name__ == "__main__":
#     print("Salut de mer")
#     l = testKNN()
#     if l:
#         print(l)
#         print("TOTO")
#         print(l[0])