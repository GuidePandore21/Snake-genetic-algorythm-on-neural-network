import random
import numpy as np
import copy
from configSnake import *
from AlgorithmeGenetique import *
from snakeFonctions import *
from Grille import Grille

# -------------------- VARIABLES GLOBALES SNAKE -------------------- #

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

def generateFoodPosition():
    """Génère une position aléatoire pour la pomme qui n'est pas sur le corps du serpent."""
    zeroPositions = np.argwhere(GRILLE.matrice == 0)
    
    if zeroPositions.size == 0:
        return None

    random_index = np.random.choice(len(zeroPositions))
    
    return tuple(zeroPositions[random_index])

def gameLoop():
    global BEST_INDIVIDU, SNAKE_SPEED

    gameOver = False
    gameClose = False

    # Position initiale du serpent
    snakeList = [[DIS_WIDTH // (2 * SNAKE_BLOCK), DIS_HEIGHT // (2 * SNAKE_BLOCK)]]
    lenSnake = 1

    # Positionnement initial de la pomme
    foodPosition = generateFoodPosition()
    print("POMME :", foodPosition)

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
                    INDIVIDU.fitness = PENALITE_ERREUR

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

        print("Snake : ", (headX, headY), "Food : ", foodPosition)
        
        if 0 <= headX < DIS_WIDTH // SNAKE_BLOCK and 0 <= headY < DIS_HEIGHT // SNAKE_BLOCK:
            # Vérification de la collision avec le corps du serpent
            if [headX, headY] in snakeList:
                INDIVIDU.fitness += PENALITE_COLLISION
                gameClose = True

            # Mettre à jour la position du serpent
            snakeList.append([headX, headY])
            if len(snakeList) > lenSnake:
                del snakeList[0]

            # Gestion de la collision avec la pomme
            if (headX, headY) == foodPosition:
                lenSnake += 1
                INDIVIDU.fitness += BONUS_POMME
                foodPosition = [random.randint(0, DIS_WIDTH // SNAKE_BLOCK - 1), random.randint(0, DIS_HEIGHT // SNAKE_BLOCK - 1)]
            
            # Mettre à jour la grille
            GRILLE.updateGrille(snakeList, foodPosition)

            DIS.fill(BLACK)
            pygame.draw.rect(DIS, RED, [foodPosition[0] * SNAKE_BLOCK, foodPosition[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])
            drawSnake(snakeList)
            pygame.display.update()

            CLOCK.tick(SNAKE_SPEED)
            INDIVIDU.fitness += BONUS_SURVIE
        else:
            INDIVIDU.fitness += PENALITE_SORTIE  # Penalité pour sortie de l'écran
            gameClose = True

# ------------------- SNAKE ------------------- #
print("toto2")
while COMPTEUR_GENERATION <= NB_GENERATION:
    while COMPTEUR_INDIVIDU <= NB_INDIVIDU:
        gameLoop()
        COMPTEUR_INDIVIDU += 1
    POPULATION = nouvelleGeneration(POPULATION, INPUTS, OUTPUTS)
    COMPTEUR_INDIVIDU = 1
    COMPTEUR_GENERATION += 1

pygame.quit()
quit()
