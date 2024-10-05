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
    
def choisirDansListeSansRemise(liste):
    """retourne au minimum un élément de la liste placé en paramètre avec un tirage sans remise

    Args:
        liste (Neurone): liste de Neurone

    Returns:
        Neurone: retourne une liste de Neurone
    """
    if len(liste) == 0:
        nbLiens = 0
    elif len(liste) == 1:
        nbLiens = 1
    else:
        nbLiens = random.randint(1, len(liste))
    tirage = random.sample(liste, nbLiens)
    return tirage

def choisirDansListeSansRemiseNombre(liste, nombre):
    """retourne au minimum un élément de la liste placé en paramètre avec un tirage sans remise

    Args:
        liste (Neurone): liste de Neurone
        nombre (int): nombre de fois que l'on fait le tirage

    Returns:
        Neurone: retourne une liste de Neurone
    """
    tirage = random.sample(liste, nombre)
    return tirage