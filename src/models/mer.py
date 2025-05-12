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
        for poisson in self.liste_poissons:
            if poisson.est_vivant:
                abscisse = poisson.abscisse
                ordonnee = poisson.ordonnee
                voisins, coordonnees_voisins = self.grille.voisins(poisson.abscisse,poisson.ordonnee)

                if isinstance(poisson, Requin):
                    
                    for index, case in enumerate(voisins):
                        if case and not isinstance(case, Requin):
                            poisson.manger()

                            if poisson.reproduire():
                                nouveau_ne = Requin(abscisse, ordonnee)
                                liste_nouveaux_nes.append(nouveau_ne)
                                poisson.a_accouche = True

                            poisson.deplacer(case.abscisse, case.ordonnee)
                            case.est_vivant = False
                            poisson.a_mange = True 
                            poisson.a_bouge = True

                    if not poisson.a_mange:
                        for index, case in enumerate(voisins):
                            if case == None:
                                if poisson.reproduire():
                                    nouveau_ne = Requin(abscisse, ordonnee)
                                    liste_nouveaux_nes.append(nouveau_ne)
                                    poisson.a_accouche = True

                                poisson.deplacer(coordonnees_voisins[index][0], coordonnees_voisins[index][1])
                                poisson.a_bouge = True

                                if poisson.energie < 0:
                                    poisson.est_vivant = False
                                    self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None

                    if poisson.a_bouge:
                        if poisson.a_accouche:
                            self.ajout_poisson(nouveau_ne)
                        else:
                            self.grille.tableau[abscisse][ordonnee] = None
                            
                    if poisson.est_vivant:
                        self.ajout_poisson(poisson)
                else:

                    for index, case in enumerate(voisins):
                        if case == None :
                            if poisson.reproduire():
                                nouveau_ne = Poisson(abscisse, ordonnee)
                                liste_nouveaux_nes.append(nouveau_ne)
                                poisson.a_accouche = True

                            poisson.deplacer(coordonnees_voisins[index][0], coordonnees_voisins[index][1])


                    if poisson.a_accouche:
                        self.ajout_poisson(nouveau_ne)
                    else:    
                        self.grille.tableau[abscisse][ordonnee] = None

                    self.ajout_poisson(poisson)
                
            poisson.a_accouche = False
            poisson.a_bouge = False
            poisson.a_mange = False
        
        #On ajoute les nouveaux nés à la liste de poissons
        self.liste_poissons.extend(liste_nouveaux_nes)

        #On supprime les poissons morts
        for poisson in self.liste_poissons:
            if not poisson.est_vivant:
                self.liste_poissons.remove(poisson)

        
                

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






    # def KNN_requin(self, requin: Requin) -> List[Tuple[float, Poisson]]:
    #     liste_distances: List[Tuple[float, Poisson]] = []
    #     for poisson in self.liste_poissons:
    #         if not isinstance(poisson, Requin):
    #             liste_distances.append(self.distance(requin.abscisse-poisson.abscisse, requin.ordonnee-poisson.ordonnee), poisson)
    #     return sorted(liste_distances)


    def KNN_requin(self, requin: Requin, k: int = 1) -> List[Tuple[float, Poisson]]:
        def distance(x: int, y: int) -> float:
            return sqrt(x**2 + y**2)

        liste_distances: List[Tuple[float, Poisson]] = []
        for poisson in self.liste_poissons:
            if not isinstance(poisson, Requin):
                dist = distance(
                    requin.abscisse - poisson.abscisse,
                    requin.ordonnee - poisson.ordonnee
                )
                liste_distances.append((dist, poisson))

        # Trie la liste selon la distance et retourne les k plus proches
        # Ici k=1
        return sorted(liste_distances, key=lambda x: x[0])[0]


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
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur,largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_liste(100,40)
    
    print(ma_mer)
    
    print("*****************")
    for _ in range(200):
        ma_mer.deplacer_tous()
        print(ma_mer)

if __name__ == "__main__":
    print("Salut de mer")
    testKNN()


                



if __name__ == "__main__":
    print("Salut de mer")
    l = testKNN()
    if l:
        print(l)
        print("TOTO")
        print(l[0])

