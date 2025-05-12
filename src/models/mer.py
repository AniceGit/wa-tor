from typing import List
from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille

class Mer:
    def __init__(self, grille):
        self.grille: Grille = grille
        self.liste_poissons:List[Poisson] = []

    def ajout_poisson(self, un_poisson:Poisson):
        abscisse = un_poisson.abscisse % self.grille.largeur
        ordonnee = un_poisson.ordonnee % self.grille.longueur

        self.grille.tableau[abscisse][ordonnee] = un_poisson

    def deplacer_tous(self):
        liste_nouveaux_nes = []
        for poisson in self.liste_poissons:
            print(poisson.est_vivant)
            if poisson.est_vivant:
                print(f"poisson en actuel : {poisson}")

                abscisse = poisson.abscisse
                ordonnee = poisson.ordonnee
                voisins, coordonnees_voisins = self.grille.voisins(poisson.abscisse,poisson.ordonnee)
                #print("voisins :", [v for v in voisins])

                if isinstance(poisson, Requin):
                    
                    for index, case in enumerate(voisins):
                        if case and not isinstance(case, Requin):
                            poisson.manger()

                            if poisson.reproduire():
                                nouveau_ne = Requin(5, abscisse, ordonnee, 5)
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
                                    nouveau_ne = Requin(5, abscisse, ordonnee)
                                    liste_nouveaux_nes.append(nouveau_ne)
                                    poisson.a_accouche = True

                                poisson.deplacer(coordonnees_voisins[index][0], coordonnees_voisins[index][1])
                                poisson.a_bouge = True

                                if poisson.energie < 0:
                                    poisson.est_vivant = False
                                    self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None

                    if poisson.a_bouge:
                        if poisson.a_accouche:
                            #self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                            self.ajout_poisson(nouveau_ne)
                        else:
                            self.grille.tableau[abscisse][ordonnee] = None
                            
                    if poisson.est_vivant:
                        #self.grille.tableau[poisson.abscisse][poisson.ordonnee] = poisson
                        self.ajout_poisson(poisson)
                else:

                    for index, case in enumerate(voisins):
                        if case == None :
                            if poisson.reproduire():
                                nouveau_ne = Poisson(5, abscisse, ordonnee)
                                liste_nouveaux_nes(nouveau_ne)
                                poisson.a_accouche = True
                            print("premier voisin vide du thon : ", coordonnees_voisins[index][0]," ",coordonnees_voisins[index][1])
                            poisson.deplacer(coordonnees_voisins[index][0], coordonnees_voisins[index][1])


                    if poisson.a_accouche:
                        #self.grille.tableau[abscisse][ordonnee] = nouveau_ne
                        self.ajout_poisson(nouveau_ne)
                    else:    
                        self.grille.tableau[abscisse][ordonnee] = None

                    #self.grille.tableau[poisson.abscisse][poisson.ordonnee] = poisson
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

        #On ajoute les poissons à la grille (Update de grille)
        # for poisson in self.liste_poissons :
        #     self.ajout_poisson(poisson)

        
                

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
    dico_p1 = {'abscisse' : 1, 'ordonnee' : 2}
    dico_p2 = {'abscisse' : 3, 'ordonnee' : 2}
    dico_r1 = {'abscisse' : 2 , 'ordonnee' : 2, 'energie' : 10}
    p1 = Poisson(**dico_p1)
    p2 = Poisson(**dico_p2)
    r1 = Requin(**dico_r1)
    ma_mer.ajout_poisson(p1)
    ma_mer.ajout_poisson(r1)
    ma_mer.ajout_poisson(p2)
    ma_mer.liste_poissons = [p1,p2,r1]
    
    print(ma_mer)

    v1 = ma_grille.voisins(1, 2)
    v2 = ma_grille.voisins(2, 2)
    print(p1.abscisse, " ", p1.ordonnee)
    print("*****************")

    ma_mer.deplacer_tous()
    print(p1.abscisse, " ", p1.ordonnee)
    print(ma_mer)


if __name__ == "__main__":
    test()

