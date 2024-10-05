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

def trouverElementsNonConnexes(elementsPresent, elementsCible):
    """retourne la liste des éléments non connexes entre ces deux listes

    Args:
        elementsPresent (all): liste élément présent
        elementsCible (all): liste élément à analyser

    Returns:
        all: liste des éléments non connexes
    """
    res = []
    for elementCible in elementsCible:
        if elementCible not in elementsPresent:
            res.append(elementCible)
    return res

def renameLayerNetworkDecalage(network, index):
    """renome tout les Layer à partir de l'index car insertion d'un précédent Layer

    Args:
        network (Network): Network dans lequel le renomage se fait
        index (int): index à partir du quel il faut renomer (index d'insertion du Layer)
    """
    compteurLayeur = 0
    for layer in network.layers:
        if compteurLayeur >= index and compteurLayeur < len(network.layers) - 1:
            layer.label = "HiddenLayer" + str(compteurLayeur + 1)
            compteurNeurone = 0
            for neurone in layer.neurones:
                neurone.label = layer.label + "Neurone" + str(compteurNeurone + 1)
                compteurNeurone += 1
        compteurLayeur += 1

def insererNouveauLayer(network, index , layer):
    """insert un nouveau Layer dans le Network au bonne endroit dans la liste

    Args:
        network (Network): Network dans lequel l'insertion se fait
        index (int): index d'insertion du Layer
        layer (Layer): Layer qu'il faut insérer
    """
    network.layers.insert(index, layer)

def remplacerConnexion(layerSuivant, layerCible):
    """créer des nouvelles connexion qui remplace les précédentes entre deux Layer

    Args:
        layerSuivant (Layer): Layer N + 1 par rapport à la cible
        layerCible (Layer): Layer où vont les connexions
    """
    for neurone in layerSuivant.neurones:
        temp = neuroneGenerator("trash", layerCible)
        neurone.inputs = temp.inputs

def chooseRandomLayer(network):
    """choisit de manière aléatoire un Layer dans le Network (inputLayer non inclus)

    Args:
        network (Network): Network dans lequel on choisit le Layer

    Returns:
        Layer: Layer choisit de manière aléatoire
        int: indexLayer
    """
    randomLayer = random.randint(1, len(network.layers) - 1)
    for layerIndex in range(len(network.layers)):
        if randomLayer == layerIndex:
            return network.layers[layerIndex], layerIndex
        
def chooseRandomAllLayer(network):
    """choisit de manière aléatoire un Layer dans le Network

    Args:
        network (Network): Network dans lequel on choisit le Layer

    Returns:
        Layer: Layer choisit de manière aléatoire
        int: indexLayer
    """
    randomLayer = random.randint(0, len(network.layers) - 1)
    for layerIndex in range(len(network.layers)):
        if randomLayer == layerIndex:
            return network.layers[layerIndex], layerIndex

def chooseRandomHiddenLayer(network):
    """choisit de manière aléatoire un hidden Layer dans le Network

    Args:
        network (Network): Network dans lequel on choisit le Layer

    Returns:
        Layer: hidden Layer choisit de manière aléatoire
        int: index Layer
    """
    randomLayer = random.randint(1, len(network.layers) - 2)
    for layerIndex in range(len(network.layers)):
        if randomLayer == layerIndex:
            return network.layers[layerIndex], layerIndex

def chooseRandomNeurone(layer):
    """choisit de manière aléatoire un Neurone dans un Layer

    Args:
        layer (Layer): Layer dans lequel on choisit le Neurone

    Returns:
        Neurone: Neurone choisit de manière aléatoire
        int: index Neurone
    """
    try:
        randomNeurone = random.randint(0, len(layer.neurones) - 1)
    except Exception as e:
        print("Impossible de choisir un Neurone")
        return -1
    for neuroneIndex in range(len(layer.neurones)):
        if randomNeurone == neuroneIndex:
            return layer.neurones[neuroneIndex], neuroneIndex

def chooseRandomConnexion(neurone):
    """choisit de manière aléatoire l'index d'une connexion dans un Neurone

    Args:
        neurone (Neurone): Neurone dans lequel on choisit la connexion

    Returns:
        int: index
    """
    try:
        randomConnexion = random.randint(0, len(neurone.inputs) - 1)
    except Exception as e:
        print("Impossible de choisir une connexion")
        return -1
    for connexionIndex in range(len(neurone.inputs)):
        if randomConnexion == connexionIndex:
            return randomConnexion

# -------------------- CREATION INDIVIDU -------------------- #

def neuroneGenerator(label, layerPrecedent):
    """génère de manière aléatoire un Neurone

    Args:
        label (string): label du neurone
        layerPrecedent (Layer): Layer avec lequel le Neurone doit faire ses connexions

    Returns:
        Neurone: Neurone créé
    """
    bias = round(random.uniform(-10, 10), 2)
    inputs = []
    listeNeuronesLayerPrecedent = layerPrecedent.neurones
    for neurone in choisirDansListeSansRemise(listeNeuronesLayerPrecedent):
        weight = round(random.uniform(0, 10), 2)
        inputs.append([neurone, weight])
    return Neurone(label, bias, inputs)