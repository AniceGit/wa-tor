from typing import List, Union
import random
import os
import time
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

    def compter_etats(self):
        nb_poissons = 0
        nb_requins = 0
        for ligne in self.grille.tableau:
            for case in ligne:
                if isinstance(case, Requin):
                    nb_requins += 1
                elif isinstance(case, Poisson):
                    nb_poissons += 1

        if nb_poissons > nb_requins:
            poissons_str = '\033[93m🐟 Poissons : {}\033[0m'.format(nb_poissons)  # jaune
            requins_str = '\033[91m🦈 Requins : {}\033[0m'.format(nb_requins)     # rouge
        elif nb_requins > nb_poissons:
            poissons_str = '\033[91m🐟 Poissons : {}\033[0m'.format(nb_poissons)  # rouge
            requins_str = '\033[93m🦈 Requins : {}\033[0m'.format(nb_requins)     # jaune
        else:
            poissons_str = '\033[93m🐟 Poissons : {}\033[0m'.format(nb_poissons)  # égalité : les deux jaunes
            requins_str = '\033[93m🦈 Requins : {}\033[0m'.format(nb_requins)

        print(f"{poissons_str}   {requins_str}\n")
        
     
    def __str__(self):
        largeur_case = 2
        nb_colonnes = len(self.grille.tableau[0])
        bordure_longueur = nb_colonnes * largeur_case
        sortie = "╔" + "═" * bordure_longueur + "╗\n"
        for ligne in self.grille.tableau:
            sortie += "║"
            for case in ligne:
                if case is None:
                    sortie += '\033[44m🌊\033[0m'
                elif isinstance(case, Requin):
                    sortie += '\033[41m🦈\033[0m'
                elif isinstance(case, Poisson):
                    sortie += '\033[42m🐟\033[0m'
            sortie += "║\n"
        sortie += "╚" + "═" * bordure_longueur + "╝"
        return sortie


    def __repr__(self):
        return str(self)


def start(iterations = 300, intervalle=0.2):
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur,largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_liste(100,40)
    
    for tour in range(iterations):
        # os.system('cls' if os.name == 'nt' else 'clear') 
        print("\033[H\033[J", end="")
        print(f"🌍 Simulation Wa-Tor — Tour {tour + 1}\n")
        ma_mer.compter_etats()
        print(ma_mer)
        ma_mer.deplacer_tous()
        time.sleep(intervalle)

if __name__ == "__main__":
    start()


