from random import randint
import matplotlib.pyplot as plt

def generationPommeApprentissage(DIS_WIDTH, DIS_HEIGHT):
    """génère un chemin de pomme pour l'apprentissage

    Args:
        DIS_WIDTH (int): largeur de la fenêtre de jeu
        DIS_HEIGHT (int): longueur de la fenêtre de jeu

    Returns:
        [[int, int]]: liste des coordonnées des pommes
    """
    pommes = []
    # Haut : round(DIS_HEIGHT / 10 * i / 10) * 10
    # Bas : round((DIS_HEIGHT / 10 * i + (DIS_HEIGHT / 2 + DIS_HEIGHT / 10)) / 10) * 10
    # Gauche : round(DIS_WIDTH / 10 * i / 10) * 10
    # Droite : round((DIS_WIDTH / 10 * i + (DIS_WIDTH / 2 + DIS_WIDTH / 10)) / 10) * 10
    
    # Haut
    for i in range(4, 0, -1):
        pommes.append([round(DIS_WIDTH / 2 / 10) * 10, round(DIS_HEIGHT / 10 * i / 10) * 10])
    
    # Gauche
    for i in range(4, 0, -1):
        pommes.append([round(DIS_WIDTH / 10 * i / 10) * 10, round(DIS_HEIGHT / 10 / 10) * 10])
       
    # Bas 
    for i in range(1, 5):
        pommes.append([round(DIS_WIDTH / 10 / 10) * 10, round((DIS_HEIGHT / 10 * i + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Droite
    for i in range(1, 5):
        pommes.append([round((DIS_WIDTH / 10 * i + (DIS_WIDTH / 10)) / 10) * 10, round((DIS_HEIGHT / 10 * 4 + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Bas 
    for i in range(5, 9):
        pommes.append([round((DIS_WIDTH / 10 * 4 + (DIS_WIDTH / 10)) / 10) * 10, round((DIS_HEIGHT / 10 * i + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Droite
    for i in range(5, 9):
        pommes.append([round((DIS_WIDTH / 10 * i + (DIS_WIDTH / 10)) / 10) * 10, round((DIS_HEIGHT / 10 * 8 + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Haut
    for i in range(8, 4, -1):
        pommes.append([round((DIS_WIDTH / 10 * 8 + (DIS_WIDTH / 10)) / 10) * 10, round(DIS_HEIGHT / 10 * i / 10) * 10])
    
    # Gauche
    for i in range(8, 0, -1):
        pommes.append([round(DIS_WIDTH / 10 * i / 10) * 10, round(DIS_HEIGHT / 10 * 5 / 10) * 10])
    
    # Bas 
    for i in range(5, 9):
        pommes.append([round(DIS_WIDTH / 10 / 10) * 10, round((DIS_HEIGHT / 10 * i + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Droite
    for i in range(1, 5):
        pommes.append([round((DIS_WIDTH / 10 * i + (DIS_WIDTH / 10)) / 10) * 10, round((DIS_HEIGHT / 10 * 8 + (DIS_HEIGHT / 10)) / 10) * 10])
        
    # Haut
    for i in range(8, 4, -1):
        pommes.append([round((DIS_WIDTH / 10 * 4 + (DIS_WIDTH / 10)) / 10) * 10, round(DIS_HEIGHT / 10 * i / 10) * 10])
    
    # Droite
    for i in range(5, 9):
        pommes.append([round((DIS_WIDTH / 10 * i + (DIS_WIDTH / 10)) / 10) * 10, round((DIS_HEIGHT / 10 * 4 + (DIS_HEIGHT / 10)) / 10) * 10])
    
    # Haut
    for i in range(4, 0, -1):
        pommes.append([round((DIS_WIDTH / 10 * 8 + (DIS_WIDTH / 10)) / 10) * 10, round(DIS_HEIGHT / 10 * i / 10) * 10])
    
    # Gauche
    for i in range(8, 4, -1):
        pommes.append([round(DIS_WIDTH / 10 * i / 10) * 10, round(DIS_HEIGHT / 10 * 1 / 10) * 10])
    
    # Bas 
    for i in range(1, 5):
        pommes.append([round(DIS_WIDTH / 10 * 5 / 10) * 10, round((DIS_HEIGHT / 10 * i + (DIS_HEIGHT / 10)) / 10) * 10])
        
        pommes.append([DIS_WIDTH - 10, round(DIS_HEIGHT / 4 * 3 / 10) * 10])
    
    pommes.append([round(DIS_WIDTH / 4 * 3 / 10) * 10, DIS_HEIGHT - 10])
    pommes.append([round(DIS_WIDTH / 2 / 10) * 10, DIS_HEIGHT - 10])
    pommes.append([round(DIS_WIDTH / 4 / 10) * 10, DIS_HEIGHT - 10])
    
    pommes.append([0, round(DIS_HEIGHT / 4 * 3 / 10) * 10])
    pommes.append([0, round(DIS_HEIGHT / 2 / 10) * 10])
    pommes.append([0, round(DIS_HEIGHT / 4 / 10) * 10])
    
    
    pommes.append([round(DIS_WIDTH / 4 / 10) * 10, 0])
    pommes.append([round(DIS_WIDTH / 2 / 10) * 10, 0])
    pommes.append([round(DIS_WIDTH / 4 * 3 / 10) * 10, 0])
    
    pommes.append([DIS_WIDTH - 10, round(DIS_HEIGHT / 4 / 10) * 10])
    pommes.append([DIS_WIDTH - 10, round(DIS_HEIGHT / 2 / 10) * 10])
    
    y = DIS_HEIGHT - 10
    while y >= 0:
        pommes.append([DIS_WIDTH - 20, y])
        pommes.append([0, y])
        if y - 10 >= 0:
            pommes.append([0, y - 10])
            pommes.append([DIS_WIDTH - 20, y - 10])
        y -= 20
    
    for i in range(10):
        randomX = randint(0, DIS_WIDTH - 6)
        randomY = randint(0, DIS_HEIGHT - 6)
        pommes.append([round(randomX / 10) * 10, round(randomY / 10) * 10])
        
    return pommes

def afficherPommes(pommes, DIS_WIDTH, DIS_HEIGHT):
    """Affiche un graphe de visualization de l'emplacement des pommes

    Args:
        [[int, int]]: liste des coordonnées des pommes
        DIS_WIDTH (int): largeur de la fenêtre de jeu
        DIS_HEIGHT (int): longueur de la fenêtre de jeu
    """
    x = [] 
    y = []  
    for pomme in pommes:
        x.append(pomme[0])
        y.append(pomme[1])

    plt.scatter(x, y, c="red")

    plt.xlim(0, DIS_WIDTH) 
    plt.ylim(0, DIS_HEIGHT) 

    plt.gca().invert_yaxis()

    plt.title('Coordonnées Pommes Apprentissage')
    plt.xlabel('Axe X')
    plt.ylabel('Axe Y')

    plt.show()
    
# pommes = generationPommeApprentissage(600, 500)
# afficherPommes(pommes, 600, 500)