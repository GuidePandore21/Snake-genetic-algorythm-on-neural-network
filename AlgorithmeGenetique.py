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

def inputLayerGenerator(inputs):
    """Génère un input layer et le retourne

    Args:
        inputs (float): valeur d'input du Network

    Returns:
        Layer: inputLayer du Network
    """
    neurones = []
    for i in range(len(inputs)):
        label = "InputNeurone" + str(i + 1)
        neurones.append(InputNeurone(label, inputs[i]))
    return Layer("InputLayer", neurones)

def hiddenLayerGenerator(layerPrecedent, numeroLayer):
    """Génère un Hidden Layer et le retourne

    Args:
        layerPrecedent (Layer): Layer précédent sert pour les connexions
        numeroLayer (int): numéro du HiddenLayer

    Returns:
        Layer: HiddenLayer du Network
    """
    neurones = []
    nbNeurones = random.randint(1, NB_MAX_NEURONES_PAR_LAYER + 1)
    for i in range(nbNeurones):
        label = "HiddenLayer" + str(numeroLayer) + "Neurone" + str(i + 1)
        neurones.append(neuroneGenerator(label, layerPrecedent))
    return Layer("HiddenLayer" + str(numeroLayer) , neurones)

def outputLayerGenerator(layerPrecedent, outputs):
    """Génère un OutputLayer et le retourne

    Args:
        layerPrecedent (Layer): Layer précédent sert pour les connexions
        outputs (string): valeurs d'output du Network

    Returns:
        Layer: outputLayer du Network
    """
    neurones = []
    for i in range(len(outputs)):
        label = "OutputNeurone" + str(i + 1)
        bias = round(random.uniform(-10, 10), 2)
        inputs = []
        listeNeuronesLayerPrecedent = layerPrecedent.neurones
        for neurone in choisirDansListeSansRemise(listeNeuronesLayerPrecedent):
            weight = round(random.uniform(0, 10), 2)
            inputs.append([neurone, weight])
        neurones.append(OutputNeurone(label, bias, inputs, outputs[i]))
    return Layer("OutputLayer", neurones)

def networkGenerator(inputs, outputs):
    """Génère un Network et le retourne

    Args:
        inputs (float): valeur d'input du Network
        outputs (string): valeurs d'output du Network

    Returns:
        Network: Network généré
    """
    layers = [inputLayerGenerator(inputs)]
    
    nbHiddenLayer = random.randint(1, NB_MAX_LAYER_PAR_NETWORK + 1)
    for i in range(nbHiddenLayer):
        layers.append(hiddenLayerGenerator(layers[len(layers) - 1], i + 1))
    
    layers.append(outputLayerGenerator(layers[len(layers) - 1], outputs))
    
    return Network(layers)

def createLayerConnexion(layer, layerPrecedent):
    """Génère les connexions entres les neurones de deux layer et retourne le layer

    Args:
        layer (Layer): layer à connecter
        layerPrecedent (Layer): layer cible

    Returns:
        Layer: Layer connecté au Layer cible
    """
    for neurone in layer.neurones:
        inputs = []
        for neuroneCible in choisirDansListeSansRemise(layerPrecedent.neurones):
            weight = round(random.uniform(0, 10), 2)
            inputs.append([neuroneCible, weight])
        neurone.inputs = inputs
    return layer

# -------------------- CROISEMENT -------------------- #

def croisement(individu1, individu2):
    """génère deux fils de deux individus en croisant leurs parties
        individu1 = AB
        individu2 = CD
        child1 = AD
        child2 = CB

    Args:
        individu1 (Network): premier parent
        individu2 (Network): deuxième parent

    Returns:
        Network: retourne les deux fils des deux individus (AD) (CB)
    """
    layersChild1 = []
    layersChild2 = []
    
    randomSeparationIndividu1 = random.randint(1, len(individu1.layers) - 2)
    randomSeparationIndividu2 = random.randint(1, len(individu2.layers) - 2)
    
    for i in range(0, randomSeparationIndividu1):
        layersChild1.append(individu1.layers[i])
    for i in range(randomSeparationIndividu2, len(individu2.layers)):
        layersChild1.append(individu2.layers[i])

    child1 = Network(layersChild1)
    child1.renameLayers()
    for layer in child1.layers:
        layer.renameNeurones()
    
    for i in range(1, len(child1.layers)):
        createLayerConnexion(child1.layers[i], child1.layers[i - 1])
        
    for i in range(0, randomSeparationIndividu2):
        layersChild2.append(individu2.layers[i])
    for i in range(randomSeparationIndividu1, len(individu1.layers)):
        layersChild2.append(individu1.layers[i])

    child2 = Network(layersChild2)
    child2.renameLayers()
    for layer in child1.layers:
        layer.renameNeurones()
    
    for i in range(1, len(child2.layers)):
        createLayerConnexion(child2.layers[i], child2.layers[i - 1])
    
    return child1, child2

# -------------------- MUTATIONS CREATION (LAYER, NEURONE, CONNEXION) -------------------- #

def mutationCreationConnexion(network):
    """créer une connexion de manière aléatoire dans un Network

    Args:
        network (Network): Network dans lequel la création se fait

    Returns:
        int: retourne -1 si ne peut pas créer la connexion
    """
    randomLayer = random.randint(1, len(network.layers) - 1)
    for layer in range(len(network.layers)):
        if randomLayer == layer:
            randomNeurone = random.randint(0, len(network.layers[layer].neurones) - 1)
            listeNeuronesNonConnexes = trouverElementsNonConnexes(network.layers[layer].neurones[randomNeurone].inputs[0], network.layers[layer - 1].neurones)
            try:
                randomNeuroneNonConnexes = random.randint(0, len(listeNeuronesNonConnexes) - 1)
            except Exception as e:
                print("Impossible d'ajouter une connexion")
                return -1
            weight = round(random.uniform(0, 10), 2)
            network.layers[layer].neurones[randomNeurone].inputs.append([listeNeuronesNonConnexes[randomNeuroneNonConnexes], weight])

def mutationCreationNeurone(network):
    """créer un Neurone de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel la création se fait
    """
    randomLayer = random.randint(1, len(network.layers) - 2)
    for layer in range(len(network.layers)):
        if randomLayer == layer:
            label = "HiddenLayer" + str(layer + 1) + "Neurone" + str(network.layers[layer].neurones)
            network.layers[layer].neurones.append(neuroneGenerator(label, network.layers[layer - 1]))
            listeNeuroneAConnecter = choisirDansListeSansRemise(network.layers[layer + 1].neurones)
            for neurone in listeNeuroneAConnecter:
                weight = round(random.uniform(0, 10), 2)
                neurone.inputs.append([network.layers[layer].neurones[len(network.layers[layer].neurones) - 1], weight])

def mutationCreationLayer(network):
    """créer un Layer de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel la création se fait
    """
    randomLayer = random.randint(1, len(network.layers) - 1)
    layer = hiddenLayerGenerator(network.layers[randomLayer - 1], randomLayer)
    renameLayerNetworkDecalage(network, randomLayer)
    insererNouveauLayer(network, randomLayer, layer)
    remplacerConnexion(network.layers[randomLayer + 1], layer)

# -------------------- MUTATIONS MODIFICATION (NEURONE BIAS, CONNEXION POIDS) -------------------- #

def mutationModificationNeuroneBias(network):
    """modifie de manière aléatoire la valeur du bias d'un Neurone dans le Network

    Args:
        network (Network): Network dans lequel la modification se fait
    """
    neuroneBiasToModifyLayer = chooseRandomAllLayer(network)
    neuroneBiasToModifyNeurone = chooseRandomNeurone(neuroneBiasToModifyLayer[0])
    neuroneBiasToModifyNeurone[0].bias = round(random.uniform(-10, 10), 2)