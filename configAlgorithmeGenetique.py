# -------------------- VARIABLES GLOBALES ALGORITHME GENETIQUE -------------------- #
import sys

ELITE = 0.6
ELITE_RATIO_RANG = 0.3
ELITE_RATIO_ADAPTATION = 0.3
ELITE_RATIO_UNIFORME = 1 - ELITE_RATIO_RANG - ELITE_RATIO_ADAPTATION
NB_REPRODUCTION_BON_PAS_BON = 0.1
MUTATION = 0.05

INDIVIDU = None
NB_INDIVIDU = 100
COMPTEUR_INDIVIDU = 1
NB_GENERATION = 100
COMPTEUR_GENERATION = 1

NB_MAX_NEURONES_PAR_LAYER = 50
NB_MAX_LAYER_PAR_NETWORK = 100

sys.setrecursionlimit(NB_INDIVIDU)