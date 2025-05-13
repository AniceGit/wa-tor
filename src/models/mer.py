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
        liste_nouveaux_nes = []

        for poisson in list(self.liste_poissons):  # Copie de la liste pour éviter modification en cours d'itération
            if not poisson.est_vivant:
                continue

            abscisse = poisson.abscisse
            ordonnee = poisson.ordonnee
            voisins, coord_voisins = self.grille.voisins(abscisse, ordonnee)

            if isinstance(poisson, Requin):
                # KNN pour trouver un poisson cible
                try:
                    _, cible = self.KNN_requin(poisson)
                except Exception:
                    cible = None

                if cible:
                    # Direction vers le poisson cible
                    dx = (cible.abscisse - abscisse)
                    dy = (cible.ordonnee - ordonnee)
                    dx = (1 if dx > 0 else -1 if dx < 0 else 0)
                    dy = (1 if dy > 0 else -1 if dy < 0 else 0)

                    # Mouvement prioritaire horizontal
                    nouveau_x, nouveau_y = abscisse + dx, ordonnee
                    if dx != 0 and self.grille.tableau[nouveau_x][nouveau_y] is None:
                        pass
                    elif dy != 0 and self.grille.tableau[abscisse][ordonnee + dy] is None:
                        nouveau_x, nouveau_y = abscisse, ordonnee + dy
                    else:
                        nouveau_x, nouveau_y = abscisse, ordonnee  # Pas de déplacement possible

                    # Vérifie si on atteint la cible
                    if (nouveau_x, nouveau_y) == (cible.abscisse, cible.ordonnee):
                        cible.est_vivant = False
                        poisson.manger()
                        poisson.a_mange = True

                    # Reproduction
                    if poisson.reproduire():
                        nouveau_ne = Requin(abscisse, ordonnee)
                        liste_nouveaux_nes.append(nouveau_ne)
                        poisson.a_accouche = True

                    # Déplacement et perte d’énergie
                    poisson.deplacer(nouveau_x, nouveau_y)
                    poisson.energie -= 1
                    poisson.a_bouge = True

                    # Vérifie l’énergie après déplacement
                    if poisson.energie < 0:
                        poisson.est_vivant = False
                        self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None

                # Nettoyage ancien emplacement
                if poisson.a_bouge:
                    self.grille.tableau[abscisse][ordonnee] = None
                if poisson.a_accouche:
                    self.ajout_poisson(nouveau_ne)
                if poisson.est_vivant:
                    self.ajout_poisson(poisson)

            else:  # Poisson simple
                for i, case in enumerate(voisins):
                    if case is None:
                        nouveau_x, nouveau_y = coord_voisins[i]

                        if poisson.reproduire():
                            nouveau_ne = Poisson(abscisse, ordonnee)
                            liste_nouveaux_nes.append(nouveau_ne)
                            poisson.a_accouche = True

                        poisson.deplacer(nouveau_x, nouveau_y)
                        self.grille.tableau[abscisse][ordonnee] = None
                        break  # Un seul déplacement

                if poisson.a_accouche:
                    self.ajout_poisson(nouveau_ne)
                self.ajout_poisson(poisson)

            # Réinitialisation des états
            poisson.a_accouche = False
            poisson.a_bouge = False
            poisson.a_mange = False

        # Ajout des nouveaux nés
        self.liste_poissons.extend(liste_nouveaux_nes)

        # Suppression des morts
        self.liste_poissons = [p for p in self.liste_poissons if p.est_vivant]

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
        

        liste_distances: List[Tuple[float, Poisson]] = []
        for poisson in self.liste_poissons:
            if not isinstance(poisson, Requin) and poisson.est_vivant:
                dist = distance_manhattan(requin.abscisse, requin.ordonnee, poisson.abscisse, poisson.ordonnee, self.grille.longueur, self.grille.hauteur)
                liste_distances.append((dist, poisson))

        # Trie la liste selon la distance et retourne les k plus proches
        # Ici k=1
        return sorted(liste_distances, key=lambda x: x[0])[0]


def distance_manhattan(x: int, y: int, x_cible: int, y_cible: int, largeur: int, hauteur: int) -> int:
    dx = min(abs(x - x_cible), largeur - abs(x - x_cible))
    dy = min(abs(y - y_cible), hauteur - abs(y - y_cible))
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
    for _ in range(50):
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