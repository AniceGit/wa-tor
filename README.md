# Wator - Simulation de vie marine

Wator est une simulation simple de vie marine inspirée du modèle Wator.  
Le but est de modéliser l’interaction entre des poissons, des requins, et des obstacles immobiles (rochers) dans un environnement en grille.

---

## 📁 Structure du projet
```
Wa-tor/
├── assets/ # Ressources graphiques (sprites, polices)
├── src/
│ ├── main.py # Point d’entrée principal du programme
│ ├── models/ # Classes des entités du jeu
│ │ ├── poisson.py # Classe Poisson
│ │ ├── requin.py # Classe Requin (hérite de Poisson)
│ │ ├── rocher.py # Classe Rocher
│ │ └── mer.py # Logique principale de la simulation
└── README.md # Ce fichier
└── requirements.txt
└── .gitignore
└── LICENCE
```

---

## 🐟 Description des classes principales

### Poisson
- Représente un poisson qui peut se déplacer, vieillir, et se reproduire après un certain temps de gestation.
- **Attributs clés :**
  - Position dans la grille (`abscisse`, `ordonnee`)
  - Temps de gestation pour reproduction
  - Vieillissement
  - Statuts (`est_vivant`, `a_bouge`, `a_mange`, etc.)

### Requin
- Hérite de `Poisson`, avec des comportements supplémentaires :
  - Énergie qui diminue lors des déplacements et augmente en mangeant un poisson
  - Temps de gestation plus long
  - Durée de vie plus longue

### Rocher
- Obstacle immobile dans la grille.  
- Ne bouge pas, ne meurt pas, ne se reproduit pas.

---

## ⚙️ Fonctionnement global

- La simulation se déroule dans une grille où poissons, requins et rochers cohabitent.
- Chaque entité possède des règles de déplacement et d’interaction (reproduction, chasse, vieillissement).
- Les requins chassent les poissons pour regagner de l’énergie.
- Les poissons se déplacent et se reproduisent après un certain temps.
- Les rochers bloquent le déplacement.

---

## ▶️ Lancement du programme

Pour lancer la simulation avec interface graphique (Pygame), exécute :

python src/main.py

Le programme démarre la simulation via la fonction `mer.start_pygame()` (dans le module `mer`).

## 🎨 Ressources

Les sprites et polices utilisés pour l’interface sont dans le dossier `assets/`.

## 🔧 Extension et personnalisation

- Modifier les paramètres de gestation, d’énergie, ou d’âge dans les classes **Poisson** et **Requin** pour expérimenter différents comportements.
- Possibilité d’ajouter d’autres entités ou obstacles.
- Le moteur graphique **Pygame** peut être étendu pour afficher plus d’informations ou améliorer les animations.

## ⚙️ Installation rapide & dépendances

pip install -r requirements.txt

## 🎬 Résultat Pygame attendu

![alt text](animiertes-gif-von-online-umwandeln-de.gif)

## 🖥️ Résultat Console attendu

![alt text](<Capture d’écran du 2025-05-15 16-37-36.png>)

## 🚀 Fonctionnalités à venir

- Ajout d’autres types d’entités marines (ex : kraken, baleines)
- Amélioration de l’interface graphique (animations plus fluides)
- Interaction en temps réel
- Implémentation de statistiques plus approfondies en temps réel sur la population

## 🤝 Contribution

Les contributions sont les bienvenues !  
Merci de forker le repo et proposer des pull requests pour toute amélioration.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE]pour plus de détails.

## 📬 Contact

Pour toute question ou suggestion :  
**Email :** anice.guiren@gmail.com  |  labonne.remi@gmail.com
**GitHub :** [AniceGit](https://github.com/AniceGit/wa-tor)

*Projet développé dans un cadre d’apprentissage sur la simulation et la programmation orientée objet.*

