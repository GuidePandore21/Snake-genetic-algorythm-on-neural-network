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

CHECKLOOP_MAX_SIZE = 15
MAX_MOVES_WITHOUT_FOOD = 20

# -------------------- Bonus -------------------- #

BONUS_POMME = 100
BONUS_RAPPROCHEMENT_POMME = 5
BONUS_SURVIE = 0.5

# -------------------- Pénalités -------------------- #

PENALITE_TAILLE = 0.001
PENALITE_COLLISION = -120
PENALITE_SORTIE = -120
PENALITE_LOOP = -300
PENALITE_IDIOT = -500
PENALITE_IMPASSE = -150
PENALITE_INNACTION = -50
PENALITE_ELOIGNEMENT_POMME = -1
