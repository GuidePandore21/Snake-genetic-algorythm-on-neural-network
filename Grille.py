import numpy as np
class Grille:
    def __init__(self, height, width):
        matrice = np.zeros((height // 10, width // 10), dtype=int)
        
