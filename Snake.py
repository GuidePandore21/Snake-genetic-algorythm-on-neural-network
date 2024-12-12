import random
import numpy as np
import copy

import pandas as pd

from configSnake import *
from AlgorithmeGenetique import *
from snakeFonctions import *
from Grille import Grille
from SaveAndLoadSnake import *

# -------------------- VARIABLES GLOBALES SNAKE -------------------- #

GRILLE = Grille(DIS_HEIGHT, DIS_WIDTH)
INPUTS = GRILLE.matrice.flatten().tolist()
OUTPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]

POPULATION = initGeneration(INPUTS, OUTPUTS)
BEST_INDIVIDU = Network([])
BEST_INDIVIDU.fitness = 0

CHECKLOOP = 0
CHECKLOOPPOSITION = []

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


all_counts = []
all_fitnesses = []
all_generation = []

def gameLoop():
    global BEST_INDIVIDU, SNAKE_SPEED, CHECKLOOP, CHECKLOOPPOSITION, all_counts, all_fitnesses, all_generation

    gameOver = False
    gameClose = False

    # Position initiale du serpent
    snakeList = [[DIS_WIDTH // (2 * SNAKE_BLOCK), DIS_HEIGHT // (2 * SNAKE_BLOCK)]]
    lenSnake = 1

    # Positionnement initial de la pomme
    foodPosition = generateFoodPosition()

    # Mettre à jour la grille
    GRILLE.updateGrille(snakeList, foodPosition)
    CHECKLOOPPOSITION.append(GRILLE.matrice.flatten().tolist())

    INDIVIDU = POPULATION[COMPTEUR_INDIVIDU - 1]
    INDIVIDU.fitness = 0

    while not gameOver:
        while gameClose:
            print("GENERATION :", COMPTEUR_GENERATION, " INDIVIDU :", COMPTEUR_INDIVIDU, "SCORE :", INDIVIDU.fitness - 1)
            all_counts.append(COMPTEUR_INDIVIDU)
            all_fitnesses.append(INDIVIDU.fitness - 1)
            all_generation.append(COMPTEUR_GENERATION)

            if INDIVIDU.fitness > BEST_INDIVIDU.fitness:
                BEST_INDIVIDU = copy.deepcopy(INDIVIDU)
            
            if INDIVIDU.fitness - 1 not in [-100, 11, 13, 14, 111, 113, 114]:
                saveNetwork(INDIVIDU, f"Save_Network/Generation_{COMPTEUR_GENERATION}_Individu_{COMPTEUR_INDIVIDU}_Score_{INDIVIDU.fitness}.txt")
                
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
                CHECKLOOP = 0
                foodPosition = [random.randint(0, DIS_WIDTH // SNAKE_BLOCK - 1), random.randint(0, DIS_HEIGHT // SNAKE_BLOCK - 1)]

            # Mettre à jour la grille
            GRILLE.updateGrille(snakeList, foodPosition)
            
            # print(CHECKLOOPPOSITION)
            
            if GRILLE.matrice.flatten().tolist() in CHECKLOOPPOSITION:
                INDIVIDU.fitness = PENALITE_ERREUR
                CHECKLOOPPOSITION = []
                gameClose = True
                
            CHECKLOOPPOSITION.append(GRILLE.matrice.flatten().tolist())
            if len(CHECKLOOPPOSITION) > 4:
                CHECKLOOPPOSITION.pop(0)
                
            INPUTS = GRILLE.matrice.flatten().tolist()
            INDIVIDU.miseAJourInputValue(INPUTS)

            DIS.fill(BLACK)
            pygame.draw.rect(DIS, RED, [foodPosition[0] * SNAKE_BLOCK, foodPosition[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])
            drawSnake(snakeList)
            pygame.display.update()

            CLOCK.tick(SNAKE_SPEED)
            INDIVIDU.fitness += BONUS_SURVIE
        else:
            INDIVIDU.fitness += PENALITE_SORTIE # Penalité pour sortie de l'écran
            gameClose = True

# ------------------- Save Data ------------------- #
def saveData(COMPTEUR_GENERATION):
    global all_counts, all_fitnesses, all_generation
    final_data = pd.DataFrame({
        "Generation" : all_generation,
        "Individu": all_counts,
        "Score": all_fitnesses,
    })

    final_data.to_csv(f"Save_Data/Generation_{COMPTEUR_GENERATION}.csv", index=False)
    print(f"----------------- Data pour Generation {COMPTEUR_GENERATION}-------------------------------")

# ------------------- SNAKE ------------------- #
while COMPTEUR_GENERATION <= NB_GENERATION:
    print("GENERATION :", COMPTEUR_GENERATION)

    while COMPTEUR_INDIVIDU <= NB_INDIVIDU:
        gameLoop()
        COMPTEUR_INDIVIDU += 1

    print(saveData(COMPTEUR_GENERATION))

    all_counts = []
    all_fitnesses = []
    all_generation = []

    POPULATION = nouvelleGeneration(POPULATION, INPUTS, OUTPUTS)
    COMPTEUR_INDIVIDU = 1
    COMPTEUR_GENERATION += 1


pygame.quit()
quit()
