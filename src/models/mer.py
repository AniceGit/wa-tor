#region Import
from typing import List, Union, Tuple
import random
import os
import time
import pygame
import math
from models.poisson import Poisson
from models.requin import Requin
from models.grille import Grille
from models.rocher import Rocher


class Mer:
    def __init__(self, grille):
        self.grille: Grille = grille
        self.liste_poissons: List[Poisson] = []
#region Ajouts poissons
    # Fonction d'ajout d'un poisson à la grille
    def ajout_poisson(self, un_poisson: Poisson):
        abscisse = un_poisson.abscisse % self.grille.longueur
        ordonnee = un_poisson.ordonnee % self.grille.largeur

        self.grille.tableau[abscisse][ordonnee] = un_poisson

    # Fonction d'ajout de poissons aléatoirement à l'intilisation
    def ajout_poissons_liste(
        self, nb_poissons: int, nb_requins: int, nb_rochers:int = 300
    ) -> List[Union[Poisson, Requin, Rocher]]:
        liste_poissons: List[Union[Poisson, Requin, Rocher]] = []
        total = nb_poissons + nb_requins + nb_rochers
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

        for i in range(nb_poissons,nb_requins+nb_poissons):
            x, y = cases_choisies[i]
            requin = Requin(x, y)
            self.grille.tableau[x][y] = requin
            liste_poissons.append(requin)

        for i in range(nb_requins+nb_poissons, nb_rochers+nb_requins+nb_poissons):
            x, y = cases_choisies[i]
            rocher = Rocher(x, y)
            self.grille.tableau[x][y] = rocher
            liste_poissons.append(rocher)

        self.liste_poissons = liste_poissons

        print(len(self.liste_poissons))
        print(sum(1 for r in self.liste_poissons if isinstance(r, Rocher)))
        return liste_poissons

#region deplacer tous basique
    # # FOnction principale de déplacement des poissons dans la mer et la grille
    # def deplacer_tous(self):
    #     liste_nouveaux_nes = []
    #     for poisson in self.liste_poissons:
    #         if poisson.est_vivant:
    #             abscisse = poisson.abscisse
    #             ordonnee = poisson.ordonnee
    #             voisins, coordonnees_voisins = self.grille.voisins(
    #                 poisson.abscisse, poisson.ordonnee
    #             )

    #             if isinstance(poisson, Requin):

    #                 for index, case in enumerate(voisins):
    #                     if case and not isinstance(case, Requin):
    #                         poisson.manger()

    #                         if poisson.reproduire():
    #                             nouveau_ne = Requin(abscisse, ordonnee)
    #                             liste_nouveaux_nes.append(nouveau_ne)
    #                             poisson.a_accouche = True

    #                         poisson.deplacer(case.abscisse, case.ordonnee)
    #                         case.est_vivant = False
    #                         poisson.a_mange = True
    #                         poisson.a_bouge = True

    #                 if not poisson.a_mange:
    #                     for index, case in enumerate(voisins):
    #                         if case == None:
    #                             if poisson.reproduire():
    #                                 nouveau_ne = Requin(abscisse, ordonnee)
    #                                 liste_nouveaux_nes.append(nouveau_ne)
    #                                 poisson.a_accouche = True

    #                             poisson.deplacer(
    #                                 coordonnees_voisins[index][0],
    #                                 coordonnees_voisins[index][1],
    #                             )
    #                             poisson.a_bouge = True

    #                             if poisson.energie < 0:
    #                                 poisson.est_vivant = False
    #                                 self.grille.tableau[poisson.abscisse][
    #                                     poisson.ordonnee
    #                                 ] = None

    #                 if poisson.a_bouge:
    #                     if poisson.a_accouche:
    #                         self.ajout_poisson(nouveau_ne)
    #                     else:
    #                         self.grille.tableau[abscisse][ordonnee] = None

    #                 if poisson.est_vivant:
    #                     self.ajout_poisson(poisson)
    #             else:

    #                 for index, case in enumerate(voisins):
    #                     if case == None:
    #                         if poisson.reproduire():
    #                             nouveau_ne = Poisson(abscisse, ordonnee)
    #                             liste_nouveaux_nes.append(nouveau_ne)
    #                             poisson.a_accouche = True

    #                         poisson.deplacer(
    #                             coordonnees_voisins[index][0],
    #                             coordonnees_voisins[index][1],
    #                         )

    #                 if poisson.a_accouche:
    #                     self.ajout_poisson(nouveau_ne)
    #                 else:
    #                     self.grille.tableau[abscisse][ordonnee] = None

    #                 self.ajout_poisson(poisson)

    #         poisson.a_accouche = False
    #         poisson.a_bouge = False
    #         poisson.a_mange = False

    #     # On ajoute les nouveaux nés à la liste de poissons
    #     self.liste_poissons.extend(liste_nouveaux_nes)

    #     # On supprime les poissons morts
    #     for poisson in self.liste_poissons:
    #         if not poisson.est_vivant:
    #             self.liste_poissons.remove(poisson)

#region deplacer tous knn
    def deplacer_tous_knn(self):
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
                                        if not isinstance(p, Requin) and not isinstance(p, Rocher) and p.est_vivant]
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

                    # Vérifie si le requin meurt de faim ou de vieillesse
                    if poisson.energie <= 0 or poisson.age==0:
                        poisson.est_vivant = False
                        self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None

                elif isinstance(poisson, Poisson):  # Déplacement d'un poisson normal
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

                    # Vérifie si le poisson meurt de vieillesse
                    if poisson.age==0:
                        poisson.est_vivant = False
                        self.grille.tableau[poisson.abscisse][poisson.ordonnee] = None
                else :
                    self.grille.tableau[abscisse][ordonnee] = poisson

        
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

        print(len(self.liste_poissons))
        print(sum(1 for r in self.liste_poissons if isinstance(r, Rocher)))


#region knn requin
    def KNN_requin(self, requin: Requin, k: int = 1, champ_de_vision: int = 2) -> List[Tuple[float, Poisson]]:
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
                if dist > champ_de_vision:
                    continue
                else :
                    liste_distances.append((dist, poisson))
        
        # Trie par distance et renvoie les k plus proches poissons
        liste_distances.sort(key=lambda x: x[0])
        
        # Renvoie soit le nombre demandé de voisins, soit tous si moins existent
        return liste_distances[:k] if liste_distances else []

#region distance manhattan
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

#region statistiques console
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

#region statistiques pygame
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

#region str et repr
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


#region start console
# -------------------------START CONSOLE----------------------------
def start(iterations=300, intervalle=0.2):
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_liste(100,100)
    for tour in range(iterations):
        os.system("cls" if os.name == "nt" else "clear")
        # print("\033[H\033[J", end="")
        print(f"🌍 Simulation Wa-Tor — Tour {tour + 1}\n")
        ma_mer.compter_etats()
        print(ma_mer)
        ma_mer.deplacer_tous()
        time.sleep(intervalle)



# -------------------------START PYGAME----------------------------
#region effet retro
def ajouter_scanlines(ecran):
    # Créer des lignes horizontales toutes les 4 pixels, sur toute la hauteur de l’écran
    hauteur_pixels = ecran.get_height()
    for i in range(0, hauteur_pixels, 4):
        pygame.draw.line(ecran, (0, 0, 0), (0, i), (ecran.get_width(), i), 1)

def ajouter_effet_crt(ecran):
    """Ajoute un effet CRT rétro avec scanlines et grain."""
    largeur, hauteur = ecran.get_size()

    # Création d'une surface temporaire semi-transparente
    effet_surface = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)

    # Scanlines (lignes sombres toutes les 4 lignes)
    for y in range(0, hauteur, 4):
        pygame.draw.line(effet_surface, (0, 0, 0, 50), (0, y), (largeur, y), 1)

    # Grain (bruit léger aléatoire)
    for _ in range(1000):  # nombre de "grains", à ajuster
        x = random.randint(0, largeur - 1)
        y = random.randint(0, hauteur - 1)
        alpha = random.randint(10, 40)
        gris = random.randint(100, 200)
        effet_surface.set_at((x, y), (gris, gris, gris, alpha))

    # Superpose le tout sur l'écran
    ecran.blit(effet_surface, (0, 0))




#region afficher stats pygame
def afficher_stats_pygame(poissons, requins, ecran, tour):
    # Définir une police et une taille
    font_path = "assets/press-start-2p/PressStart2P.ttf"
    font = pygame.font.Font(font_path, 18)
    color_text_black = (0, 0, 0)
    color_text_vert = (144, 238, 144)
    color_text_rouge = (255, 100, 100)

    """Affiche les statistiques de la simulation."""
    texte_poissons = f"Poissons: {poissons}"
    texte_requins = f"Requins: {requins}"
    texte_tour = f"TOUR: {tour}"

    # Couleur text dynamique
    if poissons > requins:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_vert)
        texte_requins_surface = font.render(texte_requins, True, color_text_rouge)
    elif requins > poissons:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_rouge)
        texte_requins_surface = font.render(texte_requins, True, color_text_vert)
    else:
        texte_poissons_surface = font.render(texte_poissons, True, color_text_black)
        texte_requins_surface = font.render(texte_requins, True, color_text_black)
    
    texte_tour_surface = font.render(texte_tour, True, color_text_black)

    # Barckgound des stats
    color_background = (0, 119, 190)
    stats_surface = pygame.Surface((ecran.get_width() // 4, 80))  # taille brackground
    stats_surface.fill(color_background)  # couleur fond
    stats_surface.set_alpha(180)  # modif opacité

    # Affiche le texte à des positions spécifiques sur l'écran
    ecran.blit(stats_surface, (0, 0))
    ecran.blit(texte_poissons_surface, (10, 10))
    ecran.blit(texte_requins_surface, (10, 50))
    ecran.blit(texte_tour_surface, (10, 90))

#region start pygame
def start_pygame(iterations=2000, intervalle=0.8):
    # pygame setup
    pygame.init()
    longueur = 80
    largeur = 40
    cell_taille = 20
    ecran = pygame.display.set_mode((longueur * cell_taille, largeur * cell_taille))
    pygame.display.set_caption("Simulation Wa-Tor")

    # initialisation de la mer
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)
    ma_mer.ajout_poissons_liste(400, 200)


    clock = pygame.time.Clock()
    running = True
    tour = 0

    # On charge les images et on les redimensionne
    img_eau = pygame.image.load("assets/eau.png")
    img_eau = pygame.transform.scale(img_eau, (cell_taille, cell_taille))

    img_poisson = pygame.image.load("assets/poisson-clown.png")
    img_poisson = pygame.transform.scale(img_poisson, (cell_taille, cell_taille))

    img_requin = pygame.image.load("assets/requin-cool.png")
    img_requin = pygame.transform.scale(img_requin, (cell_taille, cell_taille))

    img_rocher = pygame.image.load("assets/rocher-pointu.png")
    img_rocher = pygame.transform.scale(img_rocher, (cell_taille, cell_taille))

    while running and tour < iterations:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        ecran.fill("#b3d8f4")

        # RENDER YOUR GAME HERE
        for i in range(longueur):
            for j in range(largeur):
                ecran.blit(img_eau, (i * cell_taille, j * cell_taille))
                case = ma_grille.tableau[j][i]
                if isinstance(case, Requin):
                    ecran.blit(img_requin, (i * cell_taille, j * cell_taille))
                elif isinstance(case, Poisson):
                    ecran.blit(img_poisson, (i * cell_taille, j * cell_taille))
                elif isinstance(case, Rocher):
                    ecran.blit(img_rocher, (i * cell_taille, j * cell_taille))

        # Calcul des statistiques et affichage
        nb_poisson, nb_requin = ma_mer.compter_etats_pygame()
        afficher_stats_pygame(nb_poisson, nb_requin, ecran, tour)

        # Style retro
        #ajouter_scanlines(ecran)
        ajouter_effet_crt(ecran)



        # On déplace les poissons et requins
        ma_mer.deplacer_tous_knn()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(10)  # limits FPS to 10
        tour += 1

        #Stopper boucle quand une population s'eteint
        if nb_poisson == 0 or nb_requin == 0 :
            if nb_poisson == 0 :
                perdant = f"Poissons"
                img = pygame.image.load("assets/poisson-clown.png")
                img = pygame.transform.scale(img, (cell_taille*10, cell_taille*10))
            else:
                perdant = f"Requins"
                img = pygame.image.load("assets/requin-cool.png")
                img = pygame.transform.scale(img, (cell_taille*10, cell_taille*10))
            ecran.fill((0, 0, 0))  # écran fond noir

            # Affiche un message à l'écran
            img_dino = pygame.image.load("assets/dino_squelette.png")
            img_dino = pygame.transform.scale(img_dino, (cell_taille*10, cell_taille*10))

            font_path = "assets/press-start-2p/PressStart2P.ttf"
            font = pygame.font.Font(font_path, 18)
            message = f"Extinction des {perdant}! (Tours : {tour})"
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(ecran.get_width() // 2, ecran.get_height() // 2))
            img_rect_perdant = img.get_rect(center=(ecran.get_width() // 1.5, text_rect.bottom + img.get_height() // 2 + 10))
            img_rect_dino = img_dino.get_rect(center=(ecran.get_width() // 2.5, text_rect.bottom + img_dino.get_height() // 2 + 10))
            ecran.blit(text, text_rect)
            ecran.blit(img, img_rect_perdant)
            ecran.blit(img_dino, img_rect_dino)
            pygame.display.flip()
            ajouter_effet_crt(ecran)
            # Maintient l'écran quelques secondes
            pygame.time.wait(3000)
            running = False


    pygame.quit()


if __name__ == "__main__":
    start()
