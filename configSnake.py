import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

DIS_WIDTH = 300
DIS_HEIGHT = 250

DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
CLOCK = pygame.time.Clock()

SNAKE_BLOCK = 10
SNAKE_SPEED = 10