import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

DIS_WIDTH = 300
DIS_HEIGHT = 300

DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
CLOCK = pygame.time.Clock()

SNAKE_BLOCK = 50
SNAKE_SPEED = 0

# -------------------- Bonus -------------------- #

BONUS_POMME = 50
BONUS_RAPPROCHEMENT_POMME = 5
BONUS_SURVIE = 1

# -------------------- Penalités -------------------- #

PENALITE_TAILLE = 0.01

PENALITE_ERREUR = -10
PENALITE_COLLISION = -10
PENALITE_SORTIE = 0
PENALITE_ELOIGNEMENT_POMME = -5
