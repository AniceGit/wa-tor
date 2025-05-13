from models import mer
print("salut de main")
#mer.testKNN()
mer.test()


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