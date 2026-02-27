# Runner Game (Pygame)

Un jeu endless runner développé en Python avec Pygame.
Le joueur doit éviter des obstacles tout en survivant le plus longtemps possible.
Le projet est basé sur un tutoriel YouTube, avec des fonctionnalités supplémentaires ajoutées pour approfondir la compréhension de la gestion des sprites, des collisions et du temps en Pygame.

Tutoriel suivi :
https://www.youtube.com/watch?v=AY9MnQ4x3zk

![Gameplay]

<p align="center">
  <img src=gameplay.gif" width="600">
</p>

# Sommaire

- Fonctionnalités

- Installation

- Usage

# Fonctionnalités
## Base du tutoriel

- Système de saut avec gravité.

- Apparition automatique d’obstacles (snail / fly).

- Score basé sur le temps de survie.

## Améliorations personnelles

- Système de tir : le joueur peut lancer des projectiles vers la droite.

- Cooldown de tir : limitation de la fréquence des tirs via pygame.time.get_ticks().

- Collision projectile / obstacle avec suppression automatique via pygame.sprite.groupcollide.

- Score augmenté par kill en plus du score basé sur le temps.

- Ajout d’un visuel pour les projectiles.

# Installation
## 1. Cloner le dépôt
```
# Clone le dépôt
git clone https://github.com/ton-utilisateur/runner-game.git

# Accède au répertoire
cd runner-game
## 2. Installer les dépendances
pip install pygame
```
# Usage

Pour lancer le jeu :
```
python main.py
```
## Contrôles

- Espace → Sauter

- Clic gauche → Tirer

- Fermer la fenêtre → Quitter le jeu

Note : Assurez-vous que le dossier graphics/ et les assets sont bien présents dans le répertoire du projet.