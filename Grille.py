import numpy as np
class Grille:
    def __init__(self, height, width):
        """Constructeur de la classe

        Args:
            height (int): hauteur de la fenêtre pygame en px (multiple de 10)
            width (int): largeur de la fenêtre pygame en px (multiple de 10)
        """
        self.matrice = np.zeros((width // 10, height // 10), dtype=int) 
        
    def changerValeurCase(self, x, y, valeur):
        """Change remplace la valeur de la case à la position x, y de la matrice par la valeur en paramètre

        Args:
            x (int): position en x dans la matrice
            y (int): position en y dans la matrice
            valeur (int): valeur dont va hériter la case, prends une de ces valeurs [-1, 0, 1, 2]
        """
        self.matrice[x, y] = valeur  
    
    def updateGrille(self, snakeList, foodPosition):
        """Mets à jour la grille en replassant le Snake, ça tête et la pomme

        Args:
            snakeList ([[int, int]]): position de toutes les cases occupées par le serpent
            foodPosition ([int, int]): position occupé par la pomme
        """
        self.matrice.fill(0)
        for segment in snakeList[:-1]:
            self.changerValeurCase(segment[0], segment[1], 1)
        head = snakeList[-1]
        self.changerValeurCase(head[0], head[1], 2)
        self.changerValeurCase(foodPosition[0], foodPosition[1], -1)
