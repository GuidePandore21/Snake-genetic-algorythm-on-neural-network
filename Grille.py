import numpy as np
class Grille:
    def __init__(self, height, width):
        """Constructeur de la classe

        Args:
            height (int): hauteur de la fenêtre pygame en px (multiple de 10)
            width (int): largeur de la fenêtre pygame en px (multiple de 10)
        """
        matrice = np.zeros((width // 10, height // 10), dtype=int) 
        
    def changerValeurCase(self, x, y, valeur):
        """Change remplace la valeur de la case à la position x, y de la matrice par la valeur en paramètre

        Args:
            x (int): position en x dans la matrice
            y (int): position en y dans la matrice
            valeur (int): valeur dont va hériter la case, prends une de ces valeurs [-1, 0, 1, 2]
        """
        self.matrice[x, y] = valeur  
        
