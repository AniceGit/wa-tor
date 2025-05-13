from typing import List, Union, Tuple
import random
import os
import time
import pygame
from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille


class Mer:
    def __init__(self, grille):
        self.grille: Grille = grille
        self.liste_poissons: List[Poisson] = []

    # Fonction d'ajout d'un poisson à la grille
    def ajout_poisson(self, un_poisson: Poisson):
        abscisse = un_poisson.abscisse % self.grille.longueur
        ordonnee = un_poisson.ordonnee % self.grille.largeur

        self.grille.tableau[abscisse][ordonnee] = un_poisson

    # Fonction d'ajout de poissons aléatoirement à l'intilisation
    def ajout_poissons_liste(
        self, nb_poissons: int, nb_requins: int
    ) -> List[Union[Poisson, Requin]]:
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

    # FOnction principale de déplacement des poissons dans la mer et la grille
    def deplacer_tous(self):
        liste_nouveaux_nes = []
        for poisson in self.liste_poissons:
            if poisson.est_vivant:
                abscisse = poisson.abscisse
                ordonnee = poisson.ordonnee
                voisins, coordonnees_voisins = self.grille.voisins(
                    poisson.abscisse, poisson.ordonnee
                )

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

                                poisson.deplacer(
                                    coordonnees_voisins[index][0],
                                    coordonnees_voisins[index][1],
                                )
                                poisson.a_bouge = True

                                if poisson.energie < 0:
                                    poisson.est_vivant = False
                                    self.grille.tableau[poisson.abscisse][
                                        poisson.ordonnee
                                    ] = None

                    if poisson.a_bouge:
                        if poisson.a_accouche:
                            self.ajout_poisson(nouveau_ne)
                        else:
                            self.grille.tableau[abscisse][ordonnee] = None

                    if poisson.est_vivant:
                        self.ajout_poisson(poisson)
                else:

                    for index, case in enumerate(voisins):
                        if case == None:
                            if poisson.reproduire():
                                nouveau_ne = Poisson(abscisse, ordonnee)
                                liste_nouveaux_nes.append(nouveau_ne)
                                poisson.a_accouche = True

                            poisson.deplacer(
                                coordonnees_voisins[index][0],
                                coordonnees_voisins[index][1],
                            )

                    if poisson.a_accouche:
                        self.ajout_poisson(nouveau_ne)
                    else:
                        self.grille.tableau[abscisse][ordonnee] = None

                    self.ajout_poisson(poisson)

            poisson.a_accouche = False
            poisson.a_bouge = False
            poisson.a_mange = False

        # On ajoute les nouveaux nés à la liste de poissons
        self.liste_poissons.extend(liste_nouveaux_nes)

        # On supprime les poissons morts
        for poisson in self.liste_poissons:
            if not poisson.est_vivant:
                self.liste_poissons.remove(poisson)

    # Comptage statistique sur console
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
            poissons_str = "\033[93m🐟 Poissons : {}\033[0m".format(
                nb_poissons
            )  # jaune
            requins_str = "\033[91m🦈 Requins : {}\033[0m".format(nb_requins)  # rouge
        elif nb_requins > nb_poissons:
            poissons_str = "\033[91m🐟 Poissons : {}\033[0m".format(
                nb_poissons
            )  # rouge
            requins_str = "\033[93m🦈 Requins : {}\033[0m".format(nb_requins)  # jaune
        else:
            poissons_str = "\033[93m🐟 Poissons : {}\033[0m".format(
                nb_poissons
            )  # égalité : les deux jaunes
            requins_str = "\033[93m🦈 Requins : {}\033[0m".format(nb_requins)

        print(f"{poissons_str}   {requins_str}\n")

    # Comptage statistique sur pygame
    def compter_etats_pygame(self) -> Tuple[int, int]:
        nb_poissons = 0
        nb_requins = 0
        for ligne in self.grille.tableau:
            for case in ligne:
                if isinstance(case, Requin):
                    nb_requins += 1
                elif isinstance(case, Poisson):
                    nb_poissons += 1

        return nb_poissons, nb_requins

    def __str__(self):
        largeur_case = 2
        nb_colonnes = len(self.grille.tableau[0])
        bordure_longueur = nb_colonnes * largeur_case
        sortie = "╔" + "═" * bordure_longueur + "╗\n"
        for ligne in self.grille.tableau:
            sortie += "║"
            for case in ligne:
                if case is None:
                    sortie += "\033[44m🌊\033[0m"
                elif isinstance(case, Requin):
                    sortie += "\033[41m🦈\033[0m"
                elif isinstance(case, Poisson):
                    sortie += "\033[42m🐟\033[0m"
            sortie += "║\n"
        sortie += "╚" + "═" * bordure_longueur + "╝"
        return sortie

    def __repr__(self):
        return str(self)


# -------------------------START CONSOLE----------------------------
def start(iterations=300, intervalle=0.2):
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_liste(100, 40)
    for tour in range(iterations):
        os.system("cls" if os.name == "nt" else "clear")
        # print("\033[H\033[J", end="")
        print(f"🌍 Simulation Wa-Tor — Tour {tour + 1}\n")
        ma_mer.compter_etats()
        print(ma_mer)
        ma_mer.deplacer_tous()
        time.sleep(intervalle)


# def ajouter_scanlines(ecran, hauteur):
#     # Créer des lignes horizontales qui simulent les scanlines
#     for i in range(0, hauteur, 4):  # Espace de 4px pour chaque ligne de scanline
#         pygame.draw.line(ecran, (0, 0, 0), (0, i), (ecran.get_width(), i), 1)  # Lignes noires


# -------------------------START PYGAME----------------------------
def afficher_stats_pygame(poissons, requins, ecran):
    # Définir une police et une taille
    font_path = "assets/press-start-2p/PressStart2P.ttf"
    font = pygame.font.Font(font_path, 18)
    color_text_black = (0, 0, 0)
    color_text_vert = (144, 238, 144)
    color_text_rouge = (255, 100, 100)

    """Affiche les statistiques de la simulation."""
    texte_poissons = f"Poissons: {poissons}"
    texte_requins = f"Requins: {requins}"

    # Crée une surface avec le texte
    if poissons > requins:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_vert)
        texte_requins_surface = font.render(texte_requins, True, color_text_rouge)
    elif requins > poissons:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_rouge)
        texte_requins_surface = font.render(texte_requins, True, color_text_vert)
    else:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_black)
        texte_requins_surface = font.render(texte_requins, True, color_text_black)

    # Barckgound des stats
    color_background = (0, 119, 190)
    stats_surface = pygame.Surface((ecran.get_width() // 4, 80))  # taille brackground
    stats_surface.fill(color_background)  # couleur fond
    stats_surface.set_alpha(180)  # modif opacité

    # Affiche le texte à des positions spécifiques sur l'écran
    ecran.blit(stats_surface, (0, 0))
    ecran.blit(texte_poissons_surface, (10, 10))
    ecran.blit(texte_requins_surface, (10, 50))

def start_pygame(iterations=300, intervalle=0.8):
    # pygame setup
    pygame.init()
    longueur = 80
    largeur = 40
    cell_taille = 15
    ecran = pygame.display.set_mode((longueur * cell_taille, largeur * cell_taille))
    pygame.display.set_caption("Simulation Wa-Tor")

    # initialisation de la mer
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)
    ma_mer.ajout_poissons_liste(100, 40)

    print("x : ", len(ma_grille.tableau[0]))

    clock = pygame.time.Clock()
    running = True
    tour = 0

    # On charge les images et on les redimensionne
    img_eau = pygame.image.load("assets/eau.png")
    img_eau = pygame.transform.scale(img_eau, (cell_taille, cell_taille))

    img_poisson = pygame.image.load("assets/poisson.png")
    img_poisson = pygame.transform.scale(img_poisson, (cell_taille, cell_taille))

    img_requin = pygame.image.load("assets/requin.png")
    img_requin = pygame.transform.scale(img_requin, (cell_taille, cell_taille))

    while running and tour < iterations:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        ecran.fill("white")

        # RENDER YOUR GAME HERE
        for i in range(longueur):
            for j in range(largeur):
                ecran.blit(img_eau, (i * cell_taille, j * cell_taille))
                case = ma_grille.tableau[j][i]
                if isinstance(case, Requin):
                    ecran.blit(img_requin, (i * cell_taille, j * cell_taille))
                elif isinstance(case, Poisson):
                    ecran.blit(img_poisson, (i * cell_taille, j * cell_taille))

        # Calcul des statistiques et affichage
        nb_poisson, nb_requin = ma_mer.compter_etats_pygame()
        afficher_stats_pygame(nb_poisson, nb_requin, ecran)

        # Style retro
        # ajouter_scanlines(ecran,largeur)

        # On déplace les poissons et requins
        ma_mer.deplacer_tous()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(10)  # limits FPS to 60
        tour += 1

    pygame.quit()


if __name__ == "__main__":
    start()
