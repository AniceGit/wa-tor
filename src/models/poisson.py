import random
from grille import Grille

class Poisson:
    def __init__(self, tps_gestation, abscisse, ordonnee):
        self.tps_gestation = tps_gestation
        self.abscisse = abscisse
        self.ordonnee = ordonnee


    # def move(self, sea:Sea):
    #     # dx = random.choice([-1, 0, 1])
    #     # dy = random.choice([-1, 0, 1])
    #     dx = random.randint(-1, 1)
    #     dy = random.randint(-1, 1)

    #     new_x = self.abscisse + dx
    #     new_y = self.ordonnee + dy

    #     if 0 <= new_x < len(sea.sea[0]) and 0 <= new_y < len(sea.sea):
    #         if sea.sea[new_x][new_y] is None:
    #             sea.sea[self.abscisse][self.ordonnee] = None

    #             self.abscisse = new_x
    #             self.ordonnee = new_y

    #             sea.sea[new_x][new_y] = self

        def prend_voisin(self):
            directions = [(-1, 0), (1, 0), (0,-1), (0, 1),(-1,-1),(-1, 1),(1, 1),(1, -1)]
            coordonnees_voisins = []
            for dx, dy in directions:
                vx, vy = (self.abscisse + dx) % self.sea.width, (self.y_coordinate + dy) % self.mer.length
                coordonnees_voisins.append((vx, vy))
            return list(map(lambda t: self.sea.sea[t[0]][t[1]],coordonnees_voisins))

    def deplacer(self, abscisse, ordonnee):
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        
    # def reproduire(self, sea:Sea):
    #     age = self.age
    #     tps_gestation = self.tps_gestation

    #     if age%tps_gestation == 0 :
    #         sea.add_fish()