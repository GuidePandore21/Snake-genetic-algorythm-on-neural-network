import pygame
import random
import copy
from AlgorithmeGenetique import *
from snakeFonctions import *

# -------------------- VARIABLES GLOBALES SNAKE -------------------- #

DISTANCE_SF = 0

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

DIS_WIDTH = 300
DIS_HEIGHT = 250
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))

CLOCK = pygame.time.Clock()

SNAKE_BLOCK = 10
SNAKE_SPEED = 10

X = DIS_WIDTH / 2
Y = DIS_HEIGHT / 2
FOOD_X = 0
FOOD_Y = 0

INPUTS = [X, Y, FOOD_X, FOOD_Y, DISTANCE_SF]
OUTPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]

POPULATION = initGeneration(INPUTS, OUTPUTS)

BEST_INDIVIDU = Network([])
BEST_INDIVIDU.fitness = 0

print("NB ELITE : ", int(NB_INDIVIDU * ELITE))
print("NB ELITE_RATIO_RANG : ", int(NB_INDIVIDU * ELITE * ELITE_RATIO_RANG))
print("NB ELITE_RATIO_ADAPTATION : ", int(NB_INDIVIDU * ELITE * ELITE_RATIO_ADAPTATION))
print("NB ELITE_RATIO_UNIFORME : ", int(NB_INDIVIDU * ELITE * ELITE_RATIO_UNIFORME))
print("NB NB_REPRODUCTION_BON_PAS_BON : ", int(NB_INDIVIDU * NB_REPRODUCTION_BON_PAS_BON))

nouveauxIndividu = (
    int(NB_INDIVIDU * ELITE * ELITE_RATIO_RANG) + 
    int(NB_INDIVIDU * ELITE * ELITE_RATIO_ADAPTATION) + 
    int(NB_INDIVIDU * ELITE * ELITE_RATIO_UNIFORME) + 
    int(NB_INDIVIDU * NB_REPRODUCTION_BON_PAS_BON)
    )

print("NB INDIVIDU_ALEATOIRE : ", NB_INDIVIDU - nouveauxIndividu)
print("TAUX MUTATIONS : ", MUTATION * 100, "%")

# ------------------- PYGAME ------------------- #

pygame.init()

pygame.display.set_caption('Snake')

FONT_STYLE = pygame.font.SysFont(None, 50)

# ------------------- FONCTIONS ------------------- #

def drawSnake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(DIS, GREEN, [x[0], x[1], snake_block, snake_block])
        
# Fonction principale pour le jeu
def gameLoop():
    # -------------------- VARIABLES GLOBALES -------------------- #
    global X
    global Y
    global FOOD_X
    global FOOD_Y
    global DISTANCE_SF
    global INPUTS
    global BEST_INDIVIDU
    global SNAKE_SPEED
    
    gameOver = False
    gameClose = False

    # Position initiale du serpent
    X = DIS_WIDTH / 2
    Y = DIS_HEIGHT / 2

    # Initialisation du serpent
    snakeList = []
    lenSnake = 1

    # Positionnement initial de la pomme
    compteurPomme = 0
    listePomme = generationPommeApprentissage(DIS_WIDTH, DIS_HEIGHT)
    
    FOOD_X = listePomme[compteurPomme][0]
    FOOD_Y = listePomme[compteurPomme][1]
    
    # FOOD_X = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    # FOOD_Y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    
    DISTANCE_SF = abs(FOOD_X - X) + abs(FOOD_Y - Y)
    
    INDIVIDU = POPULATION[COMPTEUR_INDIVIDU - 1]
    INDIVIDU.layers[0].neurones[2].inputData = FOOD_X
    INDIVIDU.layers[0].neurones[3].inputData = FOOD_Y
    INDIVIDU.fitness = 0
    
    #-------------------- DEBUG --------------------#
    compteurFreeze = 0
    compteurBoucleDeplacement = 0
    listeDeplacement = [[0, 0]]
    lifeTime = 0

    while not gameOver:

        while gameClose == True:
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
        # INDIVIDU.printOutputNetwork()
        
        x1_change = 0
        y1_change = 0
        
        if deplacement == "LEFT":
            x1_change = -SNAKE_BLOCK
            y1_change = 0
        elif deplacement == "RIGHT":
            x1_change = SNAKE_BLOCK
            y1_change = 0
        elif deplacement == "UP":
            y1_change = -SNAKE_BLOCK
            x1_change = 0
        elif deplacement == "DOWN":
            y1_change = SNAKE_BLOCK
            x1_change = 0

        # Vérification des limites de l'écran
        if X >= DIS_WIDTH or X < 0 or Y >= DIS_HEIGHT or Y < 0:
            gameClose = True
        
        if X == X + x1_change and Y == Y + y1_change:
            compteurFreeze += 1
            if compteurFreeze == 10:
                compteurFreeze = 0
                INDIVIDU.fitness = -100
                gameClose = True
        
        X += x1_change
        Y += y1_change
                
        # augmenter fitness de 1 si il se prapproche de la pomme
        if DISTANCE_SF > abs(FOOD_X - X) + abs(FOOD_Y - Y) and not gameClose:
            INDIVIDU.fitness += 1
        
        if DISTANCE_SF < abs(FOOD_X - X) + abs(FOOD_Y - Y) and not gameClose:
            INDIVIDU.fitness -= 1
        
        DISTANCE_SF = abs(FOOD_X - X) + abs(FOOD_Y - Y)
        
        DIS.fill(BLACK)
        
        pygame.draw.rect(DIS, RED, [FOOD_X, FOOD_Y, SNAKE_BLOCK, SNAKE_BLOCK])
        snakeHead = []
        snakeHead.append(X)
        snakeHead.append(Y)
        snakeList.append(snakeHead)
        
        # -------------------- DETECTION BOUCLE DANS LE DEPLACEMENT -------------------- #
        
        if len(listeDeplacement) >= 2 and snakeHead in listeDeplacement:
            compteurBoucleDeplacement += 1
            if compteurBoucleDeplacement == 10:
                compteurBoucleDeplacement = 0
                INDIVIDU.fitness = -100
                gameClose = True
        
        listeDeplacement.append(snakeHead)        
        
        # -------------------- DEPLACEMENTS SNAKE -------------------- #
        INDIVIDU.deplacement(X, Y, DISTANCE_SF)
        
        if len(listeDeplacement) > 3:
            del listeDeplacement[0]
            
        if len(snakeList) > lenSnake:
            del snakeList[0]

        for x in snakeList[:-1]:
            if x == snakeHead:
                INDIVIDU.fitness = -100
                gameClose = True

        drawSnake(SNAKE_BLOCK, snakeList)

        pygame.display.update()

        # Gestion de la collision avec la pomme
        if X == FOOD_X and Y == FOOD_Y:
            compteurPomme += 1
            lenSnake += 1
            INDIVIDU.mangerPomme(FOOD_X, FOOD_Y, 100)
            
            if compteurPomme > len(listePomme):
                INDIVIDU.fitness += 1000000
                gameClose = True
            else:
                FOOD_X = listePomme[compteurPomme][0]
                FOOD_Y = listePomme[compteurPomme][1]

        CLOCK.tick(SNAKE_SPEED)
        
        lifeTime += 1
        INDIVIDU.fitness += lifeTime // 10
    

# ------------------- SNAKE ------------------- #

moyenneFitnessGeneration = []
maxFitnessGeneration = []
while COMPTEUR_GENERATION <= NB_GENERATION:
    while COMPTEUR_INDIVIDU <= NB_INDIVIDU:
        gameLoop()
        COMPTEUR_INDIVIDU += 1
    moyenneFitnessGeneration.append(moyenneFitnessPopulation(POPULATION))
    maxFitnessGeneration.append(maxFitnessPopulation(POPULATION))
    POPULATION = nouvelleGeneration(POPULATION, INPUTS, OUTPUTS)
    COMPTEUR_INDIVIDU = 1
    COMPTEUR_GENERATION += 1
    
afficherMoyenneFitnessGenerations(moyenneFitnessGeneration)
afficherMaxFitnessGenerations(maxFitnessGeneration)

print("Meilleur Score :", BEST_INDIVIDU.fitness - 1)
# BEST_INDIVIDU.drawNeuroneNetwork()

pygame.quit()
quit()
