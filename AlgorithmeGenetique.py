import random 
import matplotlib.pyplot as plt
from configAlgorithmeGenetique import *
from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone

# -------------------- OUTILS -------------------- #

def triRapide(liste):
    """tri une liste et la retourne

    Args:
        liste (Network): liste de Network

    Returns:
        liste (Network): liste de Network triée
    """
    if len(liste) <= 1:
        return liste
    else:
        pivot = liste[0].fitness
        infAPivot = [objet for objet in liste[1:] if objet.fitness <= pivot]
        supAPivot = [objet for objet in liste[1:] if objet.fitness > pivot]
        return triRapide(infAPivot) + [liste[0]] + triRapide(supAPivot)