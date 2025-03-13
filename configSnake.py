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
SNAKE_SPEED = 1

# -------------------- Bonus -------------------- #

BONUS_POMME = 100
BONUS_SURVIE = 1

# -------------------- Penalités -------------------- #

PENALITE_ERREUR = -100
PENALITE_COLLISION = -100
PENALITE_SORTIE = 0
