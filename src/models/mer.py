from typing import List
from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille
#from src.models.poisson import Poisson
#from src.models.requin import Requin
#from src.models.grille import Grille

class Mer:
    def __init__(self, grille):
        self.grille: Grille = grille
        self.liste_poissons:List[Poisson] = []

    def ajout_poisson(self, un_poisson):
        abscisse = un_poisson.abscisse % self.grille.largeur
        ordonnee = un_poisson.ordonnee % self.grille.longueur
        if self.grille.tableau[abscisse][ordonnee] is None:
            self.grille.tableau[abscisse][ordonnee] = un_poisson
            self.liste_poissons.append(un_poisson)
        else:
            print(f"Case ({abscisse},{ordonnee}) déjà occupée.")

    def deplacer_tous(self):
        for poisson in self.liste_poissons:
            if poisson:
                print(f"poisson en actuel : {poisson}")
                a_accouche = False
                if isinstance(poisson, Requin):
                    abscisse = poisson.abscisse
                    ordonnee = poisson.ordonnee
                    voisins, coordonnees_voisins = self.grille.voisins(poisson.abscisse,poisson.ordonnee)
                    a_mange = False
                    a_bouge = False
                    
                    for index, case in enumerate(voisins):
                        if case and not isinstance(case, Requin):
                            #print(f"case : {case}")
                            poisson.manger()
                            if poisson.reproduire():
                                nouveau_ne = Requin(5, abscisse, ordonnee, 5)
                                a_accouche = True
                            poisson.deplacer(case.abscisse, case.ordonnee)
                            print("HEEEEEYYYYYY", [p for p in self.liste_poissons])
                            self.liste_poissons.remove(case)
                            a_mange = True
                            a_bouge = True

                    if not a_mange:
                        for case in voisins:
                            if case == None:
                                #print(f"cas du none, poisson : {poisson} case : {case} ")
                                if poisson.reproduire():
                                    nouveau_ne = Requin(5, abscisse, ordonnee)
                                    
                                    a_accouche = True
                                poisson.deplacer(coordonnees_voisins[index][0], coordonnees_voisins[index][1])
                                a_bouge = True
                    if a_bouge:
                        #print(f"A bougé poisson : {poisson}case 2{case}")
                        if a_accouche:
                            #self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                            self.grille.tableau[abscisse][ordonnee] = None
                            self.liste_poissons.append(nouveau_ne)
                            self.ajout_poisson(nouveau_ne)
                            
                        else:
                            self.grille.tableau[abscisse][ordonnee] = None


                        self.grille.tableau[poisson.abscisse][poisson.ordonnee] = poisson
                else:
                    abscisse = poisson.abscisse
                    ordonnee = poisson.ordonnee
                    if self.grille.tableau[poisson.abscisse][poisson.ordonnee +1] == None:
                        if poisson.reproduire():
                            nouveau_ne = Poisson(5, abscisse, ordonnee)
                            a_accouche = True

                        poisson.deplacer(abscisse, poisson.ordonnee +1)
                        
                    elif self.grille.tableau[poisson.abscisse][poisson.ordonnee -1] == None:
                        if poisson.reproduire():
                            nouveau_ne = Poisson(5, abscisse, ordonnee)
                            a_accouche = True

                        poisson.deplacer(abscisse, poisson.ordonnee -1)
                    elif self.grille.tableau[poisson.abscisse +1][poisson.ordonnee] == None:
                        if poisson.reproduire():
                            nouveau_ne = Poisson(5, abscisse, ordonnee)
                            a_accouche = True

                        poisson.deplacer(poisson.abscisse +1 , ordonnee)
                    elif self.grille.tableau[poisson.abscisse -1][poisson.ordonnee] == None:
                        if poisson.reproduire():
                            nouveau_ne = Poisson(5, abscisse, ordonnee)
                            a_accouche = True

                        poisson.deplacer(poisson.abscisse -1, ordonnee)
                    if a_accouche:
                        #self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                        self.grille.tableau[abscisse][ordonnee] = None
                        self.liste_poissons.append(nouveau_ne)
                        self.ajout_poisson(nouveau_ne)
                    else:    
                        self.grille.tableau[abscisse][ordonnee] = None
                    self.grille.tableau[poisson.abscisse][poisson.ordonnee] = poisson
                

                



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

    



def test():
    ma_grille = Grille(10,5)
    ma_mer = Mer(ma_grille)
    dico_p1 = {'tps_gestation' : -1, 'abscisse' : 1, 'ordonnee' : 2}
    dico_r1 = {'tps_gestation' : -1, 'abscisse' : 2 , 'ordonnee' : 2, 'energie' : 10}
    dico_p2 = {'tps_gestation' : 5, 'abscisse' : 3, 'ordonnee' : 2}
    p1 = Poisson(**dico_p1)
    p2 = Poisson(**dico_p2)
    r1 = Requin(**dico_r1)
    ma_mer.ajout_poisson(p1)
    ma_mer.ajout_poisson(r1)
    ma_mer.ajout_poisson(p2)
    
    print(ma_mer)

    v1 = ma_grille.voisins(1, 2)
    v2 = ma_grille.voisins(2, 2)

    print("*****************")

    ma_mer.deplacer_tous()

    print(ma_mer)


if __name__ == "__main__":
    test()

