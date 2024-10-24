import pygame
import random
import copy
from AlgorithmeGenetique import *
from snakeFonctions import *
from Grille import Grille

# -------------------- VARIABLES GLOBALES SNAKE -------------------- #

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

GRILLE = Grille(DIS_HEIGHT, DIS_WIDTH)
INPUTS = GRILLE.matrice.flatten().tolist()
OUTPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]

POPULATION = initGeneration(INPUTS, OUTPUTS)
BEST_INDIVIDU = Network([])
BEST_INDIVIDU.fitness = 0

# ------------------- PYGAME ------------------- #

pygame.init()
pygame.display.set_caption('Snake')

# ------------------- FONCTIONS ------------------- #

def drawSnake(snakeList):
    """Dessine le serpent sur la grille Pygame"""
    for i, segment in enumerate(snakeList):
        color = GREEN if i < len(snakeList) - 1 else WHITE  # Tête en blanc, corps en vert
        pygame.draw.rect(DIS, color, [segment[0] * SNAKE_BLOCK, segment[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])

def gameLoop():
    global BEST_INDIVIDU, SNAKE_SPEED

    gameOver = False
    gameClose = False

    # Position initiale du serpent
    snakeList = [[DIS_WIDTH // (2 * SNAKE_BLOCK), DIS_HEIGHT // (2 * SNAKE_BLOCK)]]
    lenSnake = 1

    # Positionnement initial de la pomme
    foodPosition = [random.randint(0, DIS_WIDTH // SNAKE_BLOCK - 1), random.randint(0, DIS_HEIGHT // SNAKE_BLOCK - 1)]

    # Mettre à jour la grille
    GRILLE.updateGrille(snakeList, foodPosition)

    INDIVIDU = POPULATION[COMPTEUR_INDIVIDU - 1]
    INDIVIDU.fitness = 0

    while not gameOver:
        while gameClose:
            print("GENERATION :", COMPTEUR_GENERATION, " INDIVIDU :", COMPTEUR_INDIVIDU, "SCORE :", INDIVIDU.fitness - 1)
            if INDIVIDU.fitness > BEST_INDIVIDU.fitness:
                BEST_INDIVIDU = copy.deepcopy(INDIVIDU)
            gameOver = True
            gameClose = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameClose = True
                    INDIVIDU.fitness = -100

        deplacement = INDIVIDU.outputNetwork()

        headX, headY = snakeList[-1]
        if deplacement == "LEFT":
            headX -= 1
        elif deplacement == "RIGHT":
            headX += 1
        elif deplacement == "UP":
            headY -= 1
        elif deplacement == "DOWN":
            headY += 1

        if 0 <= headX < DIS_WIDTH // SNAKE_BLOCK and 0 <= headY < DIS_HEIGHT // SNAKE_BLOCK:
            GRILLE.updateGrille(snakeList, foodPosition)
            # Vérification de la collision avec le corps du serpent
            if [headX, headY] in snakeList:
                INDIVIDU.fitness -= -100
                gameClose = True

            # Mettre à jour la position du serpent
            snakeList.append([headX, headY])
            if len(snakeList) > lenSnake:
                del snakeList[0]

            # Mettre à jour la grille
            GRILLE.updateGrille(snakeList, foodPosition)

            # Gestion de la collision avec la pomme
            if [headX, headY] == foodPosition:
                lenSnake += 1
                INDIVIDU.fitness += 100
                foodPosition = [random.randint(0, DIS_WIDTH // SNAKE_BLOCK - 1), random.randint(0, DIS_HEIGHT // SNAKE_BLOCK - 1)]

            DIS.fill(BLACK)
            pygame.draw.rect(DIS, RED, [foodPosition[0] * SNAKE_BLOCK, foodPosition[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])
            drawSnake(snakeList)
            pygame.display.update()

            CLOCK.tick(SNAKE_SPEED)
            INDIVIDU.fitness += 1  # Augmenter la fitness par la survie
        else:
            INDIVIDU.fitness -= 100  # Penalité pour sortie de l'écran
            gameClose = True

# ------------------- SNAKE ------------------- #

while COMPTEUR_GENERATION <= NB_GENERATION:
    while COMPTEUR_INDIVIDU <= NB_INDIVIDU:
        gameLoop()
        COMPTEUR_INDIVIDU += 1
    POPULATION = nouvelleGeneration(POPULATION, INPUTS, OUTPUTS)
    COMPTEUR_INDIVIDU = 1
    COMPTEUR_GENERATION += 1

pygame.quit()
quit()
