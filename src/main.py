from src.models.poisson import Poisson
from src.models.requin import Requin
from src.models.grille import Grille
from models.mer2 import Mer

ma_grille = Grille(10,5)
ma_mer = Mer(ma_grille)


dico_p1 = {'tps_gestation' : 3, 'abscisse' : 1, 'ordonnee' : 1}
dico_r1 = {'tps_gestation' : 5, 'abscisse' : 2 , 'ordonnee' : 2, 'energie' : 10}
p1 = Poisson(**dico_p1)
r1 = Requin(**dico_r1)

ma_mer.ajout_poisson(p1)
ma_mer.ajout_poisson(r1)
print(ma_mer)