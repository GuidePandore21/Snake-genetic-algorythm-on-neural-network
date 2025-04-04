import random
import numpy as np
import pandas as pd

from configSnake import *
from AlgorithmeGenetique import *
from Grille import Grille
from SaveAndLoadSnake import *

# -------------------- VARIABLES GLOBALES SNAKE -------------------- #

GRILLE = Grille(DIS_HEIGHT // SNAKE_BLOCK, DIS_WIDTH // SNAKE_BLOCK)
# INPUTS = GRILLE.matrice.flatten().tolist()
INPUTS = [0 for _ in range(18)]
OUTPUTS = ["UP", "DOWN", "LEFT", "RIGHT"]

POPULATION = initGeneration(INPUTS, OUTPUTS)
# POPULATION = [copy.deepcopy(loadNetwork("1_348.48.json")) for i in range(NB_INDIVIDU)]

    
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
        color = GREEN
        # color = GREEN if i < len(snakeList) - 1 else WHITE  # Tête en blanc, corps en vert
        pygame.draw.rect(DIS, color, [segment[0] * SNAKE_BLOCK, segment[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])

def fitnessPenaliteTailleSnake(individu):
    nbNeurones = 0
    nbConnexions = 0
    
    for layer in individu.layers:
        if layer.label != "InputLayer":
            for neurone in layer.neurones:
                nbNeurones += 1
                for input in neurone.inputs:
                    nbConnexions += 1
    
    return  -PENALITE_TAILLE * (nbNeurones + nbConnexions)
    

def generateFoodPosition():
    """Génère une position aléatoire pour la pomme qui n'est pas sur le corps du serpent."""
    zeroPositions = np.argwhere(GRILLE.matrice == 0)
    
    if zeroPositions.size == 0:
        return None

    random_index = np.random.choice(len(zeroPositions))
    
    return tuple(zeroPositions[random_index])

def generateFoodPositionTemplate():
    coordinates = []
    
    foodPosition = [DIS_WIDTH // SNAKE_BLOCK // 2, DIS_HEIGHT // SNAKE_BLOCK // 2]
    
    for i in range(DIS_WIDTH // SNAKE_BLOCK // 2 - 1, -1, -1):
        coordinates.append((i, foodPosition[1]))
    
    for j in range(1, DIS_HEIGHT // SNAKE_BLOCK // 2 + 1):
        if j % 2 == 1:
            for i in range(DIS_WIDTH // SNAKE_BLOCK - 1):
                coordinates.append((i, foodPosition[1] - j))
        else:
            for i in range(DIS_WIDTH // SNAKE_BLOCK - 2, -1, -1):
                coordinates.append((i, foodPosition[1] - j))
    
    for j in range(0, DIS_HEIGHT // SNAKE_BLOCK):
        coordinates.append((DIS_WIDTH // SNAKE_BLOCK - 1, j))
    
    for j in range(DIS_HEIGHT // SNAKE_BLOCK - 1, DIS_HEIGHT // SNAKE_BLOCK // 2 , -1):
        if j % 2 == 1:
            for i in range(DIS_WIDTH // SNAKE_BLOCK - 2, -1, -1):
                coordinates.append((i, j))
        else:
            for i in range(DIS_WIDTH // SNAKE_BLOCK - 1):
                coordinates.append((i, j))
    
    for i in range(DIS_WIDTH // SNAKE_BLOCK - 2, DIS_WIDTH // SNAKE_BLOCK // 2 - 1, -1):
        coordinates.append((i, foodPosition[1]))

    return coordinates

def getDirectionalInputs(snakeList, foodPosition, grille):
    headX, headY = snakeList[-1]
    maxY, maxX = grille.shape

    directions = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0)
    }

    vision = []

    for dx, dy in directions.values():
        distance = 1
        foundBody = 0
        foundFood = 0
        x, y = headX + dx, headY + dy

        while 0 <= x < maxX and 0 <= y < maxY:
            if grille[y][x] == -1 and not foundBody:
                foundBody = 1
            if grille[y][x] == 1 and not foundFood:
                foundFood = 1
            x += dx
            y += dy
            distance += 1

        distanceMur = 1 / distance
        vision.extend([distanceMur, foundBody, foundFood])

    # Direction actuelle du serpent (one-hot)
    if len(snakeList) >= 2:
        dx = snakeList[-1][0] - snakeList[-2][0]
        dy = snakeList[-1][1] - snakeList[-2][1]
        directionOneHot = {
            (0, -1): [1, 0, 0, 0],  # UP
            (0, 1): [0, 1, 0, 0],   # DOWN
            (-1, 0): [0, 0, 1, 0],  # LEFT
            (1, 0): [0, 0, 0, 1],   # RIGHT
        }.get((dx, dy), [0, 0, 0, 0])
    else:
        directionOneHot = [0, 0, 0, 0]

    # Position relative à la pomme
    foodX, foodY = foodPosition
    positionRelativePommeX = (foodX - headX) / maxX
    positionRelativePommeY = (foodY - headY) / maxY

    return vision + directionOneHot + [positionRelativePommeX, positionRelativePommeY]

all_counts = []
all_fitnesses = []
all_generation = []

def gameLoop():
    global BEST_INDIVIDU, SNAKE_SPEED, CHECKLOOP, CHECKLOOPPOSITION, all_counts, all_fitnesses, all_generation

    gameOver = False
    gameClose = False

    # Position initiale du serpent
    snakeList = [[DIS_WIDTH // SNAKE_BLOCK // 2, DIS_HEIGHT // SNAKE_BLOCK // 2]]
    lenSnake = 1

    # Positionnement initial de la pomme
    foodPosition = generateFoodPosition()
    
    # listeFoodPosition = generateFoodPositionTemplate()
    # compteurPomme = 0
    # foodPosition = listeFoodPosition[compteurPomme]

    # Mettre à jour la grille
    GRILLE.updateGrille(snakeList, foodPosition)
    CHECKLOOPPOSITION.append(GRILLE.matrice.flatten().tolist())
    previousDistance = GRILLE.distanceManhattan(snakeList[-1], foodPosition)

    INDIVIDU = POPULATION[COMPTEUR_INDIVIDU - 1]
    # INDIVIDU.fitness = 0
    INDIVIDU.fitness = fitnessPenaliteTailleSnake(INDIVIDU)
    
    # INPUTS = GRILLE.matrice.flatten().tolist()
    INPUTS = getDirectionalInputs(snakeList, foodPosition, GRILLE.matrice)
    INDIVIDU.miseAJourInputValue(INPUTS)

    while not gameOver:
        
        while gameClose: 
            print("GENERATION :", COMPTEUR_GENERATION, " INDIVIDU :", COMPTEUR_INDIVIDU, "SCORE :", INDIVIDU.fitness - 1)
            # saveNetwork(INDIVIDU, f"Save_Network/{COMPTEUR_GENERATION}" + "/" + str(COMPTEUR_INDIVIDU) + "_" + str(INDIVIDU.fitness) + ".json")
            saveNetwork(INDIVIDU, f"oldGen/{COMPTEUR_INDIVIDU}.json")
            
            if INDIVIDU.fitness > BEST_INDIVIDU.fitness:
                BEST_INDIVIDU = copy.deepcopy(INDIVIDU)
            CHECKLOOPPOSITION = []
            gameOver = True
            gameClose = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameClose = True
                    INDIVIDU.fitness = PENALITE_ERREUR
        
        # Mettre à jour la grille
        GRILLE.updateGrille(snakeList, foodPosition)
        # INPUTS = GRILLE.matrice.flatten().tolist()
        INPUTS = getDirectionalInputs(snakeList, foodPosition, GRILLE.matrice)
        INDIVIDU.miseAJourInputValue(INPUTS)
        
        # print(INPUTS)
        deplacement = INDIVIDU.outputNetwork()
        # print(deplacement)

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
                # print("penalité collision avec lui même")

            # Mettre à jour la position du serpent
            snakeList.append([headX, headY])
            if len(snakeList) > lenSnake:
                del snakeList[0]

            currentDistance = GRILLE.distanceManhattan([headX, headY], foodPosition)

            # Gestion de la collision avec la pomme
            if (headX, headY) == foodPosition:
                lenSnake += 1
                INDIVIDU.fitness += BONUS_POMME
                CHECKLOOP = 0
                foodPosition = [random.randint(0, DIS_WIDTH // SNAKE_BLOCK - 1), random.randint(0, DIS_HEIGHT // SNAKE_BLOCK - 1)]
                # compteurPomme += 1
                # foodPosition = listeFoodPosition[compteurPomme]
            else :
                if currentDistance < previousDistance:
                    INDIVIDU.fitness += BONUS_RAPPROCHEMENT_POMME
                else:
                    INDIVIDU.fitness += PENALITE_ELOIGNEMENT_POMME
            previousDistance = currentDistance

            # Mettre à jour la grille
            GRILLE.updateGrille(snakeList, foodPosition)
            
            # print(CHECKLOOPPOSITION)
            
            if GRILLE.matrice.flatten().tolist() in CHECKLOOPPOSITION:
                INDIVIDU.fitness += PENALITE_ERREUR
                CHECKLOOPPOSITION = []
                gameClose = True
                # print("penalité boucle infinie")
                
            CHECKLOOPPOSITION.append(GRILLE.matrice.flatten().tolist())
            if len(CHECKLOOPPOSITION) > 4:
                CHECKLOOPPOSITION.pop(0)

            DIS.fill(BLACK)
            pygame.draw.rect(DIS, RED, [foodPosition[0] * SNAKE_BLOCK, foodPosition[1] * SNAKE_BLOCK, SNAKE_BLOCK, SNAKE_BLOCK])
            drawSnake(snakeList)
            pygame.display.update()

            CLOCK.tick(SNAKE_SPEED)
            INDIVIDU.fitness += BONUS_SURVIE
        else:
            INDIVIDU.fitness += PENALITE_SORTIE # Penalité pour sortie de l'écran
            # print("penalité sortie de l'écran")
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
    print(f"----------------- Data pour Generation {COMPTEUR_GENERATION} -------------------------------")

# ------------------- SNAKE ------------------- #
while COMPTEUR_GENERATION <= NB_GENERATION:
    print("GENERATION :", COMPTEUR_GENERATION)
    os.makedirs(f"Save_Network/{COMPTEUR_GENERATION}", exist_ok=True)
    
    folder = "oldGen"
    suppressionContenuDossier(folder)
    
    while COMPTEUR_INDIVIDU <= NB_INDIVIDU:
        gameLoop()
        COMPTEUR_INDIVIDU += 1
    
       
    populationSelectionne = chargerTousLesFichiersDUnDossier(folder)

    saveData(COMPTEUR_GENERATION)

    all_counts = []
    all_fitnesses = []
    all_generation = []

    if POPULATION != []:
        supprimerProprementPopulation(POPULATION)
                
    POPULATION = nouvelleGeneration(populationSelectionne, INPUTS, OUTPUTS)
    
    if populationSelectionne != []:
        supprimerProprementPopulation(populationSelectionne)
        
    gc.collect()
      
    # POPULATION = nouvelleGeneration(POPULATION, INPUTS, OUTPUTS)   
    COMPTEUR_INDIVIDU = 1
    COMPTEUR_GENERATION += 1

saveNetwork(BEST_INDIVIDU, "Le_Soat_" + str(BEST_INDIVIDU.fitness) + ".json")


pygame.quit()
quit()
