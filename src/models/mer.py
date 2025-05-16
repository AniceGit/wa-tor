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
    """
    Classe représentant un environnement marin dans une grille torique.
    Gère les entités vivantes : poissons, requins et rochers, ainsi que leur logique de déplacement, reproduction,
    alimentation et extinction.

    Attributs :
        grille (Grille): La grille représentant l'environnement.
        historique_poissons (List[int]): Historique du nombre de poissons à chaque tour.
        historique_requins (List[int]): Historique du nombre de requins à chaque tour.
        liste_poissons (List[Poisson]): Liste des poissons vivants.
        liste_requins (List[Requin]): Liste des requins vivants.
        liste_rochers (List[Rocher]): Liste des rochers placés dans la mer.
        min_poisson (int): Nombre minimal de poissons observé.
        max_poisson (int): Nombre maximal de poissons observé.
        min_requin (int): Nombre minimal de requins observé.
        max_requin (int): Nombre maximal de requins observé.
    """
    def __init__(self, grille):
        self.grille: Grille = grille
        self.historique_poissons = []
        self.historique_requins = []
        self.liste_poissons: List[Poisson] = []
        self.liste_requins: List[Requin] = []
        self.liste_rochers: List[Rocher] = []
        self.liste_creatures: List[Poisson, Requin] = []
        # self.min_poisson = self.grille.largeur * self.grille.longueur
        # self.max_poisson = -1

        # self.min_requin = self.grille.largeur * self.grille.longueur
        # self.max_requin = -1
        self.min_poisson = grille.largeur * grille.longueur
        self.max_poisson = -1
        self.min_requin = grille.largeur * grille.longueur
        self.max_requin = -1
#region Ajouts poissons
    # Fonction d'ajout d'un poisson à la grille
    def ajout_poisson(self, un_poisson: Poisson):
        """
        Ajoute un poisson à la grille à sa position donnée (modulo la taille de la grille).

        Args:
            un_poisson (Poisson): L'instance du poisson à ajouter.
        """
        abscisse = un_poisson.abscisse % self.grille.longueur
        ordonnee = un_poisson.ordonnee % self.grille.largeur

        self.grille.tableau[abscisse][ordonnee] = un_poisson

    # Fonction d'ajout de poissons aléatoirement à l'intilisation
    def ajout_poissons_requin_rochers_dans_liste(
        self, nb_poissons: int, nb_requins: int, nb_rochers:int = 300):
        """
        Ajoute un nombre spécifié de poissons, requins et rochers à des positions aléatoires sur la grille.

        Args:
            nb_poissons (int): Nombre de poissons à générer.
            nb_requins (int): Nombre de requins à générer.
            nb_rochers (int, optional): Nombre de rochers à générer (par défaut 300).
        """
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
            self.liste_poissons.append(poisson)

        for i in range(nb_poissons, nb_poissons + nb_requins):
            x, y = cases_choisies[i]
            requin = Requin(x, y)
            self.grille.tableau[x][y] = requin
            self.liste_requins.append(requin)

        for i in range(nb_poissons + nb_requins, nb_poissons + nb_requins + nb_rochers):
            x, y = cases_choisies[i]
            rocher = Rocher(x, y)
            self.grille.tableau[x][y] = rocher
            self.liste_rochers.append(rocher)




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
    def deplacer_tous(self):
        """
        Déplace toutes les créatures (poissons et requins) en fonction de leur logique respective :
        - Les requins poursuivent les poissons dans leur champ de vision (KNN).
        - Les poissons fuient les requins ou se déplacent aléatoirement.
        - Les entités peuvent se reproduire ou mourir (faim ou prédation).
        Met à jour les listes d'entités, la grille et les statistiques.
        """
        liste_nouveaux_nes_poissons = []
        liste_nouveaux_nes_requins = []
        liste_creatures = []
        liste_creatures.extend(self.liste_poissons)
        liste_creatures.extend(self.liste_requins)
        random.shuffle(liste_creatures)

        for creature in liste_creatures[:]:   # copie pour éviter itération sur liste modifiée
            if not creature.est_vivant:
                continue

            x, y = creature.abscisse, creature.ordonnee
            voisins, coords = self.grille.voisins(x, y)

            # --- REQUIN : poursuit et mange ---
            if isinstance(creature, Requin):
                # Trouver poisson cible
                cible = None
                try:
                    knn = self.KNN_requin(creature, k=1)  # [(dist, poisson)]
                    if knn:
                        _, cible = knn[0]
                except Exception:
                    pass

                a_bouge = False
                # Si cible, tenter de s'en approcher
                if cible:
                    dx = ((cible.abscisse - x + self.grille.longueur//2)
                        % self.grille.longueur) - self.grille.longueur//2
                    dy = ((cible.ordonnee - y + self.grille.largeur//2)
                        % self.grille.largeur) - self.grille.largeur//2
                    dx = 1 if dx>0 else -1 if dx<0 else 0
                    dy = 1 if dy>0 else -1 if dy<0 else 0

                    # On vérifie d'abord si on peut manger une cible adjacente (non diagonale)
                    if (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1):
                        nx, ny = (x+dx) % self.grille.longueur, (y+dy) % self.grille.largeur
                        if (nx, ny) == (cible.abscisse, cible.ordonnee):
                            cible.est_vivant = False
                            self.grille.tableau[cible.abscisse][cible.ordonnee] = None
                            creature.manger()
                            nx, ny = cible.abscisse, cible.ordonnee
                            a_bouge = True
                    else:
                        # priorité horizontale
                        nx, ny = (x+dx) % self.grille.longueur, y
                        if dx != 0 and self.grille.est_libre(nx, ny):
                            a_bouge = True
                        elif dy != 0:
                            tx, ty = x, (y+dy) % self.grille.largeur
                            if self.grille.est_libre(tx, ty):
                                nx, ny = tx, ty
                                a_bouge = True

                else:
                    # pas de poisson dans le champ, va sur un voisin libre au hasard
                    libre = [(pos, coord) for pos, coord in zip(voisins, coords) if pos is None]
                    if libre:
                        _, (nx, ny) = random.choice(libre)
                        a_bouge = True

                # mise à jour si déplacement ou faim
                if a_bouge:
                    self.grille.tableau[x][y] = None
                    creature.deplacer(nx, ny)
                    self.grille.tableau[nx][ny] = creature
                    creature.energie -= 1
                else:
                    # même sans bouger, on perd de l'énergie
                    creature.energie -= 1

                # reproduction
                nouveau_ne = creature.reproduire()
                if nouveau_ne:
                    bx, by = x, y
                    coordonnee_parent = Requin(bx, by)
                    liste_nouveaux_nes_requins.append(coordonnee_parent)
                    self.grille.tableau[bx][by] = coordonnee_parent

                # mort de faim
                if creature.energie <= 0:
                    creature.est_vivant = False
                    self.grille.tableau[creature.abscisse][creature.ordonnee] = None

            # --- POISSON : fuit le requin le plus proche ---
            else:
                # Trouver requin le plus proche
                requin_menacant = None
                try:
                    knn = self.KNN_poisson(creature, k=1)
                    if knn:
                        _, requin_menacant = knn[0]
                except Exception:
                    pass

                # Toutes les cases libres voisines
                libre = [(coord) for (coord, cont) in zip(coords, voisins) if cont is None]
                if libre:
                    # Si un requin menace, on choisit la case qui maximise la distance à ce requin
                    if requin_menacant:
                        # calcule la distance de chaque candidat à menacer
                        meilleures_distance_de_fuite = -1
                        meilleur_coordonnee = None
                        for nx, ny in libre:
                            d = self.distance_manhattan(nx, ny,
                                                        requin_menacant.abscisse, requin_menacant.ordonnee)
                            if d > meilleures_distance_de_fuite:
                                meilleures_distance_de_fuite, meilleur_coordonnee = d, (nx, ny)
                        nx, ny = meilleur_coordonnee
                    else:
                        # sinon choix aléatoire
                        nx, ny = random.choice(libre)

                    # déplacement
                    self.grille.tableau[x][y] = None
                    creature.deplacer(nx, ny)
                    self.grille.tableau[nx][ny] = creature

                # reproduction
                nouveau_ne = creature.reproduire()
                if nouveau_ne:
                    bx, by = x, y
                    coordonnee_parent = Poisson(bx, by)
                    liste_nouveaux_nes_poissons.append(coordonnee_parent)
                    self.grille.tableau[bx][by] = coordonnee_parent

        # Mise à jour des listes principales (suppression des morts)
        self.liste_poissons = [p for p in self.liste_poissons if p.est_vivant]
        self.liste_requins = [r for r in self.liste_requins if r.est_vivant]

        # Ajout des nouveaux-nés
        self.liste_poissons.extend(liste_nouveaux_nes_poissons)
        self.liste_requins.extend(liste_nouveaux_nes_requins)

        # Mise à jour de l'historique
        nb_poissons = len(self.liste_poissons)
        nb_requins = len(self.liste_requins)
        self.historique_poissons.append(nb_poissons)
        self.historique_requins.append(nb_requins)

        if nb_poissons < self.min_poisson:
            self.min_poisson = nb_poissons
        if nb_poissons > self.max_poisson:
            self.max_poisson = nb_poissons

        if nb_requins < self.min_requin:
            self.min_requin = nb_requins
        if nb_requins > self.max_requin:
            self.max_requin = nb_requins



#region knn requin
    def KNN_requin(self, requin: Requin, k: int = 1, champ_de_vision: int = 3) -> List[Tuple[float, Poisson]]:
        """
        Recherche les k poissons les plus proches d'un requin dans un rayon défini.

        Args:
            requin (Requin): Le requin observant son environnement.
            k (int): Nombre de voisins les plus proches à retourner.
            champ_de_vision (int): Distance maximale de vision.

        Returns:
            List[Tuple[float, Poisson]]: Liste des tuples (distance, poisson).
        """
        liste_distances = []

        for poisson in self.liste_poissons:  # Chercher parmi les poissons
            if poisson.est_vivant:
                dist = self.distance_manhattan(
                    requin.abscisse, requin.ordonnee,
                    poisson.abscisse, poisson.ordonnee
                )
                if dist <= champ_de_vision:
                    liste_distances.append((dist, poisson))

        liste_distances.sort(key=lambda x: x[0])
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

#region knn poisson
    def KNN_poisson(self, poisson: Poisson, k: int = 1, champ_de_vision: int = 3) -> List[Tuple[float, Requin]]:
        """
        Recherche les k requins les plus proches d’un poisson dans un rayon défini.

        Args:
            poisson (Poisson): Le poisson observant son environnement.
            k (int): Nombre de voisins les plus proches à retourner.
            champ_de_vision (int): Distance maximale de vision.

        Returns:
            List[Tuple[float, Requin]]: Liste des tuples (distance, requin).
        """
        liste_distances = []

        for requin in self.liste_requins:  # Chercher parmi les requins, pas les poissons
            if requin.est_vivant:
                dist = self.distance_manhattan(
                    requin.abscisse, requin.ordonnee,
                    poisson.abscisse, poisson.ordonnee
                )
                if dist <= champ_de_vision:
                    liste_distances.append((dist, requin))

        liste_distances.sort(key=lambda x: x[0])
        return liste_distances[:k] if liste_distances else []

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
        """
        Compte le nombre de poissons et de requins pour affichage dans l’interface Pygame.

        Returns:
            Tuple[int, int]: Nombre de poissons et nombre de requins.
        """
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
        """
        Retourne une représentation textuelle de la grille avec des emojis,
        en couleurs selon le type de créature.

        Returns:
            str: Représentation ASCII de l’état de la mer.
        """
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
                elif isinstance(case, Rocher):
                    sortie += "\033[44m🪨\033[0m"
            sortie += "║\n"
        sortie += "╚" + "═" * bordure_longueur + "╝"
        return sortie

    def __repr__(self):
        """
        Fournit une représentation officielle de la mer.

        Returns:
            str: Représentation ASCII de la mer.
        """
        return str(self)


#region start console
# -------------------------START CONSOLE----------------------------
def start(iterations=300, intervalle=0.2):
    """
    Lance la simulation de l'écosystème Wa-Tor en mode console.

    Arguments:
        iterations (int): Le nombre de tours à simuler. Par défaut, 300 tours.
        intervalle (float): Le temps d'attente entre chaque tour en secondes. Par défaut, 0.2 secondes.
    """
    longueur = 80
    largeur = 25
    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)

    ma_mer.ajout_poissons_requin_rochers_dans_liste(100,100)
    for tour in range(iterations):
        os.system("cls" if os.name == "nt" else "clear")
        # print("\033[H\033[J", end="")
        print(f"🌍 Simulation Wa-Tor — Tour {tour + 1}\n")
        ma_mer.compter_etats()
        print(ma_mer)
        ma_mer.deplacer_tous()
        time.sleep(intervalle)

# -------------------------START PYGAME----------------------------
def ajouter_scanlines(ecran):
    """
    Ajoute des lignes horizontales (scanlines) à l'écran pour un effet rétro.

    Arguments:
        ecran (pygame.Surface): La surface sur laquelle dessiner les lignes.
    """
    # Créer des lignes horizontales toutes les 4 pixels, sur toute la hauteur de l’écran
    hauteur_pixels = ecran.get_height()
    for i in range(0, hauteur_pixels, 4):
        pygame.draw.line(ecran, (0, 0, 0), (0, i), (ecran.get_width(), i), 1)

def ajouter_effet_crt(ecran):
    """
    Applique un effet CRT rétro avec des scanlines et du bruit (grain) à l'écran.

    Arguments:
        ecran (pygame.Surface): La surface sur laquelle appliquer l'effet.
    """
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
def afficher_stats_pygame(mer:Mer, poissons, requins, rochers, ecran, tour):
    """
    Affiche les statistiques de la simulation sur l'écran dans un style rétro.

    Arguments:
        mer (Mer): L'instance de la mer qui contient les informations de l'écosystème.
        poissons (int): Le nombre de poissons dans la simulation.
        requins (int): Le nombre de requins dans la simulation.
        rochers (int): Le nombre de rochers dans la simulation.
        ecran (pygame.Surface): La surface sur laquelle afficher les statistiques.
        tour (int): Le numéro du tour actuel de la simulation.
    """
    # Définir une police et une taille
    font_path = "assets/press-start-2p/PressStart2P.ttf"
    font = pygame.font.Font(font_path, 12)
    color_text_black = (0, 0, 0)
    color_text_brown = (48, 48, 48)
    color_text_vert = (144, 238, 144)
    color_text_rouge = (255, 93, 34)
    color_text_vert_fluo = (0,255,26)
    color_text_bleu_marine = (0,0,128)

    """Affiche les statistiques de la simulation."""
    texte_poissons = f"Poissons: {poissons}"
    texte_requins = f"Requins: {requins}"
    texte_rochers = f"Rochers: {rochers}"
    texte_tour = f"TOUR: {tour}"

    text_poissons_max = f"Poissons max: {mer.max_poisson}"
    text_poissons_min = f"Poissons min: {mer.min_poisson}"
    text_requins_max = f"Requins max: {mer.max_requin}"
    text_requins_min = f"Requins min: {mer.min_requin}"

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
    texte_rochers_surface = font.render(texte_rochers, True, color_text_brown)
    texte_poissons_max_surface = font.render(text_poissons_max, True, color_text_vert_fluo)
    text_poissons_min_surface = font.render(text_poissons_min, True, color_text_vert_fluo)
    text_requins_max_surface = font.render(text_requins_max, True, color_text_bleu_marine)
    text_requins_min_surface = font.render(text_requins_min, True, color_text_bleu_marine)

    # Barckgound des stats chiffres
    color_background = (0, 119, 190)
    stats_surface = pygame.Surface((ecran.get_width() // 3.7 , 160))  #80# taille brackground
    stats_surface.fill(color_background)  # couleur fond
    stats_surface.set_alpha(230)  # modif opacité

    # Affiche le texte à des positions spécifiques sur l'écran
    ecran.blit(stats_surface, (0, 0))
    ecran.blit(texte_poissons_surface, (10, 10))
    ecran.blit(texte_requins_surface, (10, 50))
    ecran.blit(texte_rochers_surface, (10, 90))
    ecran.blit(texte_tour_surface, (10, 130))

    ecran.blit(texte_poissons_max_surface, (stats_surface.get_width()/2, 10))
    ecran.blit(text_poissons_min_surface, (stats_surface.get_width()/2, 50))
    ecran.blit(text_requins_max_surface, (stats_surface.get_width()/2, 90))
    ecran.blit(text_requins_min_surface, (stats_surface.get_width()/2, 130))

    ######
    #AFFICHAGE DU GRAPH À DROITE DE L'ECRAN
    color_background_graph = (0, 119, 190)
    stats_surface_graph = pygame.Surface((ecran.get_width() // 4.5 , 200))  #80# taille brackground
    stats_surface_graph.fill(color_background_graph)  # couleur fond
    stats_surface_graph.set_alpha(230)  # modif opacité

    afficher_graphiques(stats_surface_graph, mer.historique_poissons, mer.historique_requins)
    ecran.blit(stats_surface_graph, (ecran.get_width() - ecran.get_width() // 4.5 ,0))  # x et y = position du graphe
    ######

# Affichage du graphique pygame
def afficher_graphiques(surface, historique_poissons, historique_requins, largeur=300, hauteur=200):
    """
    Affiche les graphiques de l'évolution des populations de poissons et de requins.

    Arguments:
        surface (pygame.Surface): La surface sur laquelle afficher les graphiques.
        historique_poissons (list): Liste des populations de poissons à chaque tour.
        historique_requins (list): Liste des populations de requins à chaque tour.
        largeur (int): La largeur du graphique. Par défaut, 300 pixels.
        hauteur (int): La hauteur du graphique. Par défaut, 200 pixels.
    """
    if len(historique_poissons) < 2:
        return

    max_val = max(max(historique_poissons), max(historique_requins), 1)

    for i in range(1, len(historique_poissons)):
        x1 = (i - 1) * largeur // len(historique_poissons)
        x2 = i * largeur // len(historique_poissons)

        y1_p = hauteur - (historique_poissons[i - 1] * hauteur // max_val)
        y2_p = hauteur - (historique_poissons[i] * hauteur // max_val)

        y1_r = hauteur - (historique_requins[i - 1] * hauteur // max_val)
        y2_r = hauteur - (historique_requins[i] * hauteur // max_val)

        pygame.draw.line(surface, (0,255,26), (x1, y1_p), (x2, y2_p), 2)  # Poissons en vert
        pygame.draw.line(surface, (0,0,128), (x1, y1_r), (x2, y2_r), 2)  # Requins en bleu

#R
#region fenetre principale
# import pygame
# from mer import Mer
# from grille import Grille
# from poisson import Poisson
# from requin import Requin
# from rocher import Rocher
# from utils import afficher_stats_pygame, ajouter_effet_crt
h0 = 200
def creer_fenetre(largeur, hauteur, h=h0):

    pygame.init()
    fenetre_principale = pygame.display.set_mode((largeur, hauteur))
    ecran = pygame.Surface((largeur, hauteur - h))
    surface_exterieure = pygame.Surface((largeur, h))
    return fenetre_principale, ecran, surface_exterieure

def remplir_surface_exterieure(surface, label_texte, font, image_bouton_eau, image_bouton_poisson, image_bouton_requin, image_bouton_rocher, n):
    surface.fill((30, 30, 30))  # fond sombre pour distinguer
    texte_surface = font.render(label_texte, True, (255, 255, 255))
    surface.blit(texte_surface, (10, 10))

    # Affiche les boutons sur la surface extérieure
    surface.blit(image_bouton_eau, (30, 30))
    surface.blit(image_bouton_poisson, (30, 30 + n))
    surface.blit(image_bouton_requin, (30 + n, 30 + n))
    surface.blit(image_bouton_rocher, (30 + n, 30))

    # Optionnel : cadre blanc autour des boutons sélectionnés
    pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(30, 30, n, n), 1)
    pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(30, 30 + n, n, n), 1)
    pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(30 + n, 30, n, n), 1)
    pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(30 + n, 30 + n, n, n), 1)

    return {
        'eau': pygame.Rect(30, 30, n, n),
        'poisson': pygame.Rect(30, 30 + n, n, n),
        'rocher': pygame.Rect(30 + n, 30, n, n),
        'requin': pygame.Rect(30 + n, 30 + n, n, n)
    }

def start_pygame(iterations=2000, intervalle=0.8, h=h0):
    pygame.init()

    longueur = 80
    largeur = 40
    cell_taille = 20
    f_principale, ecran, s_exterieure = creer_fenetre(longueur * cell_taille, largeur * cell_taille + h)

    pygame.display.set_caption("Simulation Wa-Tor")

    ma_grille = Grille(longueur, largeur)
    ma_mer = Mer(ma_grille)
    ma_mer.ajout_poissons_requin_rochers_dans_liste(1000, 200)

    clock = pygame.time.Clock()
    running = True
    tour = 0

    # Charger police
    font = pygame.font.Font("assets/press-start-2p/PressStart2P.ttf", 12)

    # Texte initial
    label_texte = "Contrôle Simulation **"

    # Chargement des images
    bouton_eau = pygame.image.load("assets/eau.png").convert_alpha()
    bouton_eau = pygame.transform.scale(bouton_eau, (2*cell_taille, 2*cell_taille))

    bouton_poisson = pygame.image.load("assets/poisson-clown.png")
    bouton_poisson = pygame.transform.scale(bouton_poisson, (2*cell_taille, 2*cell_taille))

    bouton_requin = pygame.image.load("assets/requin-cool.png")
    bouton_requin = pygame.transform.scale(bouton_requin, (2*cell_taille, 2*cell_taille))

    bouton_rocher = pygame.image.load("assets/rocher-pointu.png")
    bouton_rocher = pygame.transform.scale(bouton_rocher, (2*cell_taille, 2*cell_taille))

    img_eau = pygame.image.load("assets/eau.png")
    img_eau = pygame.transform.scale(img_eau, (cell_taille, cell_taille))

    img_poisson = pygame.image.load("assets/poisson-clown.png")
    img_poisson = pygame.transform.scale(img_poisson, (cell_taille, cell_taille))

    img_requin = pygame.image.load("assets/requin-cool.png")
    img_requin = pygame.transform.scale(img_requin, (cell_taille, cell_taille))

    img_rocher = pygame.image.load("assets/rocher-pointu.png")
    img_rocher = pygame.transform.scale(img_rocher, (cell_taille, cell_taille))

    # Élément actuellement sélectionné (eau, poisson, requin, rocher)
    element_selectionne = 'eau'

    # Variable pour stocker la pause
    pause = False

    while running and tour < iterations:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                souris_pos = event.pos  # position du clic

                # Si clic dans la zone des boutons (en haut)
                if souris_pos[1] < h:
                    # Obtenir les rectangles des boutons mis à jour
                    boutons_rects = remplir_surface_exterieure(s_exterieure, label_texte, font,
                                                              bouton_eau, bouton_poisson,
                                                              bouton_requin, bouton_rocher,
                                                              2*cell_taille)

                    # Vérifier quel bouton a été cliqué
                    if boutons_rects['eau'].collidepoint(souris_pos):
                        element_selectionne = 'eau'
                        label_texte = "Eau sélectionnée"
                    elif boutons_rects['poisson'].collidepoint(souris_pos):
                        element_selectionne = 'poisson'
                        label_texte = "Poisson sélectionné"
                    elif boutons_rects['requin'].collidepoint(souris_pos):
                        element_selectionne = 'requin'
                        label_texte = "Requin sélectionné"
                    elif boutons_rects['rocher'].collidepoint(souris_pos):
                        element_selectionne = 'rocher'
                        label_texte = "Rocher sélectionné"
                else:
                    # Clic dans la zone simulation : calcul des coordonnées de la case
                    x_souris, y_souris = souris_pos
                    case_x = x_souris // cell_taille
                    case_y = (y_souris - h) // cell_taille  # - h car ta zone simulation est en dessous des boutons

                    if 0 <= case_x < longueur and 0 <= case_y < largeur:
                        print(f"Case cliquée : ({case_x}, {case_y})")

                        contenu = ma_mer.grille.tableau[case_y][case_x]




                        # Placer l'élément sélectionné
                        if element_selectionne == 'eau':
                            if isinstance(contenu, Requin):
                                contenu.est_vivant = False
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_requins.remove(contenu)
                            if isinstance(contenu, Poisson):
                                contenu.est_vivant = False
                                # if contenu in ma_mer.liste_poissons:
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_poissons.remove(contenu)
                            elif isinstance(contenu, Rocher):
                                ma_mer.liste_rochers.remove(contenu)
                            ma_mer.grille.tableau[case_y][case_x] = None

                        elif element_selectionne == 'poisson':
                            nouveau_poisson = Poisson(case_y, case_x)
                            if contenu == None:
                                ma_mer.liste_poissons.append(nouveau_poisson)
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_poisson
                            if isinstance(contenu, Requin):
                                contenu.est_vivant = False
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_requins.remove(contenu)
                                ma_mer.liste_poissons.append(nouveau_poisson)
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_poisson
                            elif isinstance(contenu, Rocher):
                                ma_mer.liste_rochers.remove(contenu)
                                ma_mer.liste_poissons.append(nouveau_poisson)
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_poisson

                        elif element_selectionne == 'requin':
                            nouveau_requin = Requin(case_y, case_x)
                            if contenu == None:
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_requin
                                ma_mer.liste_requins.append(nouveau_requin)
                            if isinstance(contenu, Poisson) and not isinstance(contenu, Requin):
                                contenu.est_vivant = False
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_poissons.remove(contenu)
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_requin
                                ma_mer.liste_requins.append(nouveau_requin)
                            elif isinstance(contenu, Rocher):
                                ma_mer.liste_rochers.remove(contenu)
                                ma_mer.grille.tableau[case_y][case_x] = nouveau_requin
                                ma_mer.liste_requins.append(nouveau_requin)
                        elif element_selectionne == 'rocher':
                            if isinstance(contenu, Requin):
                                contenu.est_vivant = False
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_requins.remove(contenu)
                            if isinstance(contenu, Poisson):
                                contenu.est_vivant = False
                                # ma_mer.liste_creatures.remove(contenu)
                                # ma_mer.liste_poissons.remove(contenu)
                            nouveau_rocher = Rocher(case_x, case_y)
                            ma_mer.grille.tableau[case_y][case_x] = nouveau_rocher
                            ma_mer.liste_rochers.append(nouveau_rocher)

            # Ajout de la touche pour mettre en pause
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    if pause:
                        label_texte = "Simulation en pause"
                    else:
                        label_texte = "Simulation en cours"

        # Affichage de la grille
        ecran.fill("#b3d8f4")

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

        nb_poisson, nb_requin = ma_mer.compter_etats_pygame()
        nb_rochers = len(ma_mer.liste_rochers)
        afficher_stats_pygame(ma_mer, nb_poisson, nb_requin, nb_rochers, ecran, tour)

        ajouter_effet_crt(ecran)

        # Déplacer les éléments seulement si la simulation n'est pas en pause
        if not pause:
            ma_mer.deplacer_tous()

        # Affiche l'interface dans la surface_exterieure
        boutons_rects = remplir_surface_exterieure(s_exterieure, label_texte, font,
                                                  bouton_eau, bouton_poisson,
                                                  bouton_requin, bouton_rocher,
                                                  2*cell_taille)

        # Dessiner un cadre plus épais autour du bouton sélectionné
        if element_selectionne == 'eau':
            pygame.draw.rect(s_exterieure, (255, 255, 0), boutons_rects['eau'], 3)
        elif element_selectionne == 'poisson':
            pygame.draw.rect(s_exterieure, (255, 255, 0), boutons_rects['poisson'], 3)
        elif element_selectionne == 'requin':
            pygame.draw.rect(s_exterieure, (255, 255, 0), boutons_rects['requin'], 3)
        elif element_selectionne == 'rocher':
            pygame.draw.rect(s_exterieure, (255, 255, 0), boutons_rects['rocher'], 3)

        # Affiche les deux surfaces dans la fenêtre principale
        f_principale.blit(ecran, (0, h))
        f_principale.blit(s_exterieure, (0, 0))

        pygame.display.flip()
        clock.tick(10)

        if not pause:
            tour += 1

        if nb_poisson == 0 or nb_requin == 0:
            if nb_poisson == 0:
                perdant = "Poissons"
                img = pygame.image.load("assets/poisson-clown.png")
            else:
                perdant = "Requins"
                img = pygame.image.load("assets/requin-cool.png")
            img = pygame.transform.scale(img, (cell_taille * 10, cell_taille * 10))
            ecran.fill((0, 0, 0))
            font_path = "assets/press-start-2p/PressStart2P.ttf"
            font = pygame.font.Font(font_path, 18)
            message = f"Extinction des {perdant}! (Tours : {tour})"
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(ecran.get_width() // 2, ecran.get_height() // 2))
            img_rect = img.get_rect(center=(ecran.get_width() // 2, text_rect.bottom + img.get_height() // 2 + 10))
            ecran.blit(text, text_rect)
            ecran.blit(img, img_rect)

            f_principale.blit(ecran, (0, h))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    pygame.quit()

if __name__ == "__main__":
    start_pygame()