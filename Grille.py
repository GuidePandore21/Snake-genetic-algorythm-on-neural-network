import numpy as np
class Grille:
    def __init__(self, height, width):
        """Constructeur de la classe

        Args:
            height (int): hauteur de la fenêtre pygame en px (multiple de 10)
            width (int): largeur de la fenêtre pygame en px (multiple de 10)
        """
        matrice = np.zeros((width // 10, height // 10), dtype=int)   
        
