import random 
import matplotlib.pyplot as plt
from configAlgorithmeGenetique import *
from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone
from SaveAndLoadSnake import *
import copy
import gc
import os

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

def suppressionContenuDossier(dossier):
    for fichier in os.listdir(dossier):
        chemin = os.path.join(dossier, fichier)
        try:
            if os.path.isfile(chemin):
                os.unlink(chemin)
        except Exception as e:
            print(e)

def chargerTousLesFichiersDUnDossier(dossier):
    listeFichier = []
    for fichier in os.listdir(dossier):
        listeFichier.append(loadNetwork(dossier + "/" + fichier))
    return listeFichier

def supprimerProprementNetwork(network):
    for layer in network.layers:
        for neuron in layer.neurones:
            del neuron
        del layer
    del network
    
def supprimerProprementPopulation(population):
    for individu in population:
        supprimerProprementNetwork(individu)
    del population
    gc.collect()
    
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
        
def randomPoidsLoiNormale(mu=0, sigma=6):
    """Génère un poids avec une distribution normale"""
    return round(random.gauss(mu, sigma), 15)

def randomBiasLoiNormale(mu=0, sigma=20):
    """Génère un biais avec une distribution normale"""
    return round(random.gauss(mu, sigma), 15)


# -------------------- CREATION INDIVIDU -------------------- #

def neuroneGenerator(label, layerPrecedent):
    """génère de manière aléatoire un Neurone

    Args:
        label (string): label du neurone
        layerPrecedent (Layer): Layer avec lequel le Neurone doit faire ses connexions

    Returns:
        Neurone: Neurone créé
    """
    bias = randomBiasLoiNormale()
    inputs = []
    listeNeuronesLayerPrecedent = layerPrecedent.neurones
    for neurone in choisirDansListeSansRemise(listeNeuronesLayerPrecedent):
        weight = randomPoidsLoiNormale()
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
        bias = randomBiasLoiNormale()
        inputs = []
        listeNeuronesLayerPrecedent = layerPrecedent.neurones
        for neurone in choisirDansListeSansRemise(listeNeuronesLayerPrecedent):
            weight = randomPoidsLoiNormale()
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
            weight = randomPoidsLoiNormale()
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
    
    try:
        randomSeparationIndividu1 = random.randint(1, len(individu1.layers) - 2)
    except Exception as e:
        randomSeparationIndividu1 = 1
    try:
        randomSeparationIndividu2 = random.randint(1, len(individu2.layers) - 2)
    except Exception as e:
        randomSeparationIndividu2 = 1
    
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
    for layer in child2.layers:
        layer.renameNeurones()
    
    for i in range(1, len(child2.layers)):
        createLayerConnexion(child2.layers[i], child2.layers[i - 1])
    
    return child1, child2

def croisementPondere(individu1, individu2):
    """Croisement en mélangeant les poids des parents au lieu de couper les couches"""
    
    enfant = copy.deepcopy(individu1)

    for layer1, layer2, layerEnfant in zip(individu1.layers, individu2.layers, enfant.layers):
        if layer1.label == "InputLayer" or layer1.label == "OutputLayer":
            continue
        for neurone1, neurone2, neuroneEnfant in zip(layer1.neurones, layer2.neurones, layerEnfant.neurones):
            alpha = random.uniform(0, 1)  # Facteur de mélange

            # Assurer que les deux neurones ont le même nombre d'inputs
            taille_min = min(len(neurone1.inputs), len(neurone2.inputs))
            
            for i in range(taille_min):
                poids1 = neurone1.inputs[i][1]
                poids2 = neurone2.inputs[i][1]
                
                # Nouveau poids = mix des parents
                neuroneEnfant.inputs[i][1] = alpha * poids1 + (1 - alpha) * poids2

    return enfant

# -------------------- MUTATIONS -------------------- #

def trouverConnexionsInfluentes(network, seuil=0.5):
    """Retourne les connexions influentes (poids élevés)"""
    connexions = []

    for layer in network.layers:
        if layer.label in ["InputLayer", "OutputLayer"]:
            continue
        for neurone in layer.neurones:
            for connexion in neurone.inputs:
                poids = connexion[1]
                if abs(poids) > seuil:
                    connexions.append((neurone, connexion))
                    
    return connexions

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
            try:
                listeNeuronesNonConnexes = trouverElementsNonConnexes(network.layers[layer].neurones[randomNeurone].inputs[0], network.layers[layer - 1].neurones)
                randomNeuroneNonConnexes = random.randint(0, len(listeNeuronesNonConnexes) - 1)
            except Exception as e:
                print("Impossible d'ajouter une connexion")
                return -1
            weight = randomPoidsLoiNormale()
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
                weight = randomPoidsLoiNormale()
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

def mutationModificationNeuroneBias(network, sigma_perturbation=5):
    """Ajoute une perturbation gaussienne douce au biais d’un neurone, hors InputLayer"""
    hiddenOrOutputLayers = [layer for layer in network.layers if layer.label != "InputLayer"]
    layer = random.choice(hiddenOrOutputLayers)
    neurone = chooseRandomNeurone(layer)[0]

    perturbation = random.gauss(0, sigma_perturbation)
    neurone.bias = round(neurone.bias + perturbation, 15)

def mutationModificationConnexionPoids(network, sigma_perturbation=1):
    """Modifie en priorité une connexion influente en ajoutant une perturbation gaussienne"""
    
    connexions_influentes = trouverConnexionsInfluentes(network, seuil=0.5)  # seuil ajustable

    if connexions_influentes:
        # Tirage aléatoire dans les connexions influentes
        neurone, connexion = random.choice(connexions_influentes)
        perturbation = random.gauss(0, sigma_perturbation)
        connexion[1] = round(connexion[1] + perturbation, 15)
    else:
        # Fallback : mutation aléatoire (sans InputLayer)
        hiddenOrOutputLayers = [layer for layer in network.layers if layer.label != "InputLayer"]
        layer = random.choice(hiddenOrOutputLayers)
        neurone = chooseRandomNeurone(layer)[0]
        index = chooseRandomConnexion(neurone)
        if index != -1:
            perturbation = random.gauss(0, sigma_perturbation)
            neurone.inputs[index][1] = round(neurone.inputs[index][1] + perturbation, 15)

# -------------------- MUTATIONS SWAP (LAYER, NEURONE, CONNEXION) -------------------- #

def mutationSwapNeuroneBias(network):
    """intervertit le bias de deux Neurone de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel se fait le swap
    """
    neuroneBiasToSwap1Layer = chooseRandomAllLayer(network)[0]
    neuroneBiasToSwap1Neurone = chooseRandomNeurone(neuroneBiasToSwap1Layer)[0]
    neuroneBiasToSwap2Layer = chooseRandomAllLayer(network)[0]
    neuroneBiasToSwap2Neurone = chooseRandomNeurone(neuroneBiasToSwap2Layer)[0]
    
    temp = neuroneBiasToSwap1Neurone.bias
    neuroneBiasToSwap1Neurone.bias = neuroneBiasToSwap2Neurone.bias
    neuroneBiasToSwap2Neurone.bias = temp

def mutationSwapConnexion(network):
    """intervertit deux connexions de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel le swap se fait

    Returns:
        int: return -1 en cas d'impossibilité d'effectuer le swap
    """
    connexionToSwapLayer = chooseRandomLayer(network)[0]
    connexionToSwap1Neurone = chooseRandomNeurone(connexionToSwapLayer)[0]
    connexionToSwap1 = chooseRandomConnexion(connexionToSwap1Neurone)
    connexionToSwap2Neurone = chooseRandomNeurone(connexionToSwapLayer)[0]
    connexionToSwap2 = chooseRandomConnexion(connexionToSwap2Neurone)
    
    for connexion in connexionToSwap1Neurone.inputs:
        if connexion[0] == connexionToSwap2Neurone.inputs[connexionToSwap2][0]:
            return -1
        
    for connexion in connexionToSwap2Neurone.inputs:
        if connexion[0] == connexionToSwap1Neurone.inputs[connexionToSwap1][0]:
            return -1
    
    if connexionToSwap1Neurone == connexionToSwap2Neurone or connexionToSwap1 == -1 or connexionToSwap2 == -1:
        return -1
    else:
        temp = connexionToSwap1Neurone.inputs[connexionToSwap1]
        connexionToSwap1Neurone.inputs[connexionToSwap1] = connexionToSwap2Neurone.inputs[connexionToSwap2]
        connexionToSwap2Neurone.inputs[connexionToSwap2] = temp

def mutationSwapNeurone(network):
    """intervertit deux Neurone de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel se fait le swap

    Returns:
        _type_: return -1 en cas d'impossibilité de faire le swap
    """
    neuroneToSwap1Layer, neuroneToSwap1LayerIndex = chooseRandomHiddenLayer(network)
    neuroneToSwap1, neuroneToSwap1Index  = chooseRandomNeurone(neuroneToSwap1Layer)
    neuroneToSwap2Layer, neuroneToSwap2LayerIndex = chooseRandomHiddenLayer(network)
    neuroneToSwap2, neuroneToSwap2Index = chooseRandomNeurone(neuroneToSwap2Layer)
    
    if neuroneToSwap1Layer == neuroneToSwap2Layer:
        return -1
    
    tempBias = neuroneToSwap1.bias
    neuroneToSwap1 = neuroneGenerator(neuroneToSwap1.label, network.layers[neuroneToSwap1LayerIndex - 1])
    neuroneToSwap1.bias = neuroneToSwap2.bias
    neuroneToSwap2 = neuroneGenerator(neuroneToSwap2.label, network.layers[neuroneToSwap2LayerIndex - 1])
    neuroneToSwap2.bias = tempBias
    
    network.layers[neuroneToSwap1LayerIndex].neurones[neuroneToSwap1Index] = neuroneToSwap1
    network.layers[neuroneToSwap2LayerIndex].neurones[neuroneToSwap2Index] = neuroneToSwap2

def mutationSwapLayer(network):
    """intervertit deux HiddenLayer de manière aléatoire dans le Network

    Args:
        network (Network): Network dans lequel le swap se fait

    Returns:
        int: return -1 en cas d'impossibilité de faire le swap
    """
    layerToSwap1, layerToSwap1Index = chooseRandomHiddenLayer(network)
    layerToSwap2, layerToSwap2Index = chooseRandomHiddenLayer(network)
    
    # solution temporaire pour outputlayer -> pb creation Neurone à la place OutPutNeurone
    if layerToSwap1 == layerToSwap2 or network.layers[layerToSwap1Index + 1].label == "OutputLayer" or network.layers[layerToSwap2Index + 1].label == "OutputLayer":
        return -1
    
    if layerToSwap1Index > layerToSwap2Index:
        temp = layerToSwap1
        layerToSwap1 = layerToSwap2
        layerToSwap2 = temp
        
        temp = layerToSwap1Index
        layerToSwap1Index = layerToSwap2Index
        layerToSwap2Index = temp

    tempNeurones1 = network.layers[layerToSwap1Index].neurones
    
    neuronesLayer1 = []
    for neurone in layerToSwap2.neurones:
        tempBias = neurone.bias
        newNeurone = neuroneGenerator(neurone.label, network.layers[layerToSwap1Index - 1])
        newNeurone.bias = tempBias
        neuronesLayer1.append(newNeurone)
    
    network.layers[layerToSwap1Index].neurones = neuronesLayer1
    network.layers[layerToSwap1Index].renameNeurones()
    
    neuronesLayer2 = []
    for neurone in tempNeurones1:
        tempBias = neurone.bias
        newNeurone = neuroneGenerator(neurone.label, network.layers[layerToSwap2Index - 1])
        newNeurone.bias = tempBias
        neuronesLayer2.append(newNeurone)
        
    network.layers[layerToSwap2Index].neurones = neuronesLayer2
    network.layers[layerToSwap2Index].renameNeurones()
    
    if layerToSwap1Index + 1 != layerToSwap2Index:
        neuronesLayer3 = []
        for neurone in network.layers[layerToSwap1Index + 1].neurones:
            tempBias = neurone.bias
            newNeurone = neuroneGenerator(neurone.label, network.layers[layerToSwap1Index])
            newNeurone.bias = tempBias
            neuronesLayer3.append(newNeurone)
        network.layers[layerToSwap1Index + 1].neurones = neuronesLayer3
    
    if layerToSwap2Index + 1 != layerToSwap1Index:
        neuronesLayer4 = []
        for neurone in network.layers[layerToSwap2Index + 1].neurones:
            tempBias = neurone.bias
            newNeurone = neuroneGenerator(neurone.label, network.layers[layerToSwap2Index])
            newNeurone.bias = tempBias
            neuronesLayer4.append(newNeurone)
        network.layers[layerToSwap2Index + 1].neurones = neuronesLayer4

# -------------------- MUTATIONS SUPPRESSION (LAYER, NEURONE, CONNEXION) -------------------- #

def mutationSuppressionConnexion(network):
    """supprime de manière aléatoire une connexion dans le Network

    Args:
        network (Network): Network dans lequel la suppression se fait
    """
    connexionToDeleteLayer = chooseRandomLayer(network)[0]
    connexionToDeleteNeurone = chooseRandomNeurone(connexionToDeleteLayer)[0]
    connexionToDelete = chooseRandomConnexion(connexionToDeleteNeurone)
    try:
        connexionToDeleteNeurone.inputs.pop(connexionToDelete)
    except Exception as e:
        print("Impossible de supprimer une connexion")

def mutationSuppressionNeurone(network):
    """supprime de manière aléatoire un Neurone dans le Network

    Args:
        network (Network): Network dans lequel le suppression se fait
    """
    neuroneToDeleteLayer, neuroneToDeleteLayerIndex = chooseRandomHiddenLayer(network)
    neuroneToDeleteNeurone, neuroneToDeleteNeuroneIndex = chooseRandomNeurone(neuroneToDeleteLayer)
    
    if len(neuroneToDeleteLayer.neurones) <= 1:
        return -1
    
    for neurone in network.layers[neuroneToDeleteLayerIndex + 1].neurones:
        for i in range(len(neurone.inputs)):
            if neurone.inputs[i][0] == neuroneToDeleteNeurone:
                neurone.inputs.pop(i)
                break
                
    neuroneToDeleteLayer.neurones.pop(neuroneToDeleteNeuroneIndex)

def mutationSuppressionLayer(network):
    """supprime de manière aléatoire un HiddenLayer dans le Network

    Args:
        network (Network): Network dans lequel la suppression se fait
    """
    layerToDeleteIndex = chooseRandomHiddenLayer(network)[1]
    for neurone in network.layers[layerToDeleteIndex + 1].neurones:
        inputs = []
        listeNeuronesLayerPrecedent = network.layers[layerToDeleteIndex - 1].neurones
        for neuroneCible in choisirDansListeSansRemise(listeNeuronesLayerPrecedent):
            weight = randomPoidsLoiNormale()
            inputs.append([neuroneCible, weight])
        neurone.inputs = inputs
    
    network.layers.pop(layerToDeleteIndex)
    
    network.renameLayers()
    for layer in network.layers:
        layer.renameNeurones

mutations = [
    mutationCreationConnexion,
    # mutationCreationNeurone,
    # mutationCreationLayer, 
    mutationModificationConnexionPoids,
    mutationModificationNeuroneBias,
    # mutationSwapConnexion,
    # mutationSwapNeurone,
    # mutationSwapLayer,
    mutationSuppressionConnexion,
    # mutationSuppressionNeurone,
    # mutationSuppressionLayer
]

# -------------------- SELECTIONS MEILLEUR INDIVIDU -------------------- #

def selectionParRang(population):
    population = list(reversed(population))
    elite = []
    
    if len(population) < int(NB_INDIVIDU * ELITE_RATIO_RANG + 1):
        nbIndividu = len(population)
    else:
        nbIndividu = int(NB_INDIVIDU * ELITE_RATIO_RANG + 1)
        
    if len(population) > 1:
        for i in range(0, nbIndividu):
            elite.append(copy.deepcopy(population[i]))
    
    return elite

def selectionParAdaptation(population):
    """Sélectionne les individus selon une Roulette Wheel Selection, même avec des fitness négatives."""
    
    min_fitness = min(individu.fitness for individu in population)
    if len(population) < int(NB_INDIVIDU * ELITE_RATIO_ADAPTATION + 1):
        nbSelectionnes = len(population)
    else:
        nbSelectionnes = int(NB_INDIVIDU * ELITE_RATIO_ADAPTATION + 1)

    # Décaler les fitness pour qu'elles soient toutes positives
    if min_fitness < 0:
        decalage = abs(min_fitness) + 1  # Décalage pour rendre toutes les valeurs ≥ 1
    else:
        decalage = 0  # Pas besoin de décalage si toutes sont positives

    fitness_ajustees = [(individu.fitness + decalage) for individu in population]
    total_fitness = sum(fitness_ajustees)

    if total_fitness == 0:
        return random.sample(population, nbSelectionnes)

    probabilites = [fitness / total_fitness for fitness in fitness_ajustees]
    cumulees = [sum(probabilites[:i+1]) for i in range(len(probabilites))]

    selectionnes = []
    for _ in range(nbSelectionnes):
        r = random.random()  # Nombre aléatoire entre 0 et 1
        for i, seuil in enumerate(cumulees):
            if r <= seuil:
                selectionnes.append(copy.deepcopy(population[i]))
                break  # Sortir dès qu'on trouve l'individu correspondant

    return selectionnes



def selectionUniforme(population):
    """Choisit de manière aléatoire des Network à dupliquer pour la prochaine génération

    Args:
        population (Network): génération précédente

    Returns:
        [Network] : liste d'individu pour la prochaine génération
    """
    liste = population
    random.shuffle(liste)
    selectionnes = []
    
    nbSelectionnes = int(NB_INDIVIDU * ELITE * ELITE_RATIO_UNIFORME / 2)
    if nbSelectionnes < 1:
        nbSelectionnes = 1
    
    if nbSelectionnes % 2 == 1:
        nbSelectionnes -= 1

    for i in range(int(nbSelectionnes - 1)):
        selectionnes.append(liste[i])
    
    newGen = []
    for i in range(0, len(selectionnes) - 1, 2):
        children = croisement(selectionnes[i], selectionnes[i + 1])
        newGen.append(copy.deepcopy(children[0]))
        newGen.append(copy.deepcopy(children[1]))
    
    random.shuffle(newGen)
    for i in range(len(newGen)):
        chanceMutation = random.randint(0, 100)
        if chanceMutation < 100 * MUTATION:
            randomMutation = random.randint(0, len(mutations) - 1)
            print("Mutation : ", mutations[randomMutation])
            mutations[randomMutation](newGen[i])
            
    return newGen

def reproductionMeilleur(population):
    """Reproduction des individu ayant un fitness élevé

    Args:
        population (Network): génération précédente

    Returns:
        [Network] : liste d'individu pour la prochaine génération
    """

    population = chargerTousLesFichiersDUnDossier("oldGen")
    population = list(reversed(population))
    
    if len(population) < int(NB_INDIVIDU * NB_REPRODUCTION_MEILLEUR / 2):
        nbSelectionnes = len(population)
    else:
        nbSelectionnes = int(NB_INDIVIDU * NB_REPRODUCTION_MEILLEUR / 2)
    
    newGen = []
    for i in range(nbSelectionnes):
        child = croisementPondere(population[i], population[-i - 1])
        newGen.append(copy.deepcopy(child))

    random.shuffle(newGen)
    for i in range(len(newGen)):
        chanceMutation = random.randint(0, 100)
        if chanceMutation < 100 * MUTATION:
            randomMutation = random.randint(0, len(mutations) - 1)
            print("Mutation : ", mutations[randomMutation])
            mutations[randomMutation](newGen[i])

    return newGen

def reproductionAleatoire(population):
    population = chargerTousLesFichiersDUnDossier("oldGen")
    random.shuffle(population)
    
    if len(population) < int(NB_INDIVIDU * NB_REPRODUCTION_MEILLEUR / 2):
        nbSelectionnes = len(population)
    else:
        nbSelectionnes = int(NB_INDIVIDU * NB_REPRODUCTION_MEILLEUR / 2)
    
    newGen = []
    for i in range(nbSelectionnes):
        child = croisementPondere(population[i], population[-i - 1])
        newGen.append(copy.deepcopy(child))

    random.shuffle(newGen)
    for i in range(len(newGen)):
        chanceMutation = random.randint(0, 100)
        if chanceMutation < 100 * MUTATION:
            randomMutation = random.randint(0, len(mutations) - 1)
            print("Mutation : ", mutations[randomMutation])
            mutations[randomMutation](newGen[i])

    return newGen

def reproductionMeilleurMoinsBon(population):
    """Reproduction des individu ayant un fitness moindre

    Args:
        population (Network): génération précédente

    Returns:
        [Network] : liste d'individu pour la prochaine génération
    """
    
    newGen = []
    for i in range(int(NB_INDIVIDU * NB_REPRODUCTION_BON_PAS_BON / 2)):
        child = croisementPondere(population[i], population[- i - 1])
        newGen.append(copy.deepcopy(child))
    
    random.shuffle(newGen)
    for i in range(len(newGen)):
        chanceMutation = random.randint(0, 100)
        if chanceMutation < 100 * MUTATION:
            randomMutation = random.randint(0, len(mutations) - 1)
            print("Mutation : ", mutations[randomMutation])
            mutations[randomMutation](newGen[i])
    
    return newGen

# -------------------- CREATION GENERATION -------------------- #

def initGeneration(INPUTS, OUTPUTS):
    """créer une 1ère génération de Network d'une quantité régie par la Variable Globale POPULATION

    Args:
        INPUTS (_type_): données input du Network
        OUTPUTS (_type_): données output du Network

    Returns:
        [Network]: population (liste Network)
    """
    generation = []
    for i in range(NB_INDIVIDU):
        generation.append(networkGenerator(INPUTS, OUTPUTS))
    return generation

def nouvelleGeneration(populationPrecedente, INPUTS, OUTPUTS):
    """Génère la prochaine génération d'individu

    Args:
        populationPrecedente ([Network]): génération précédente
        INPUTS ([tout]): liste des inputs du Network
        OUTPUTS ([tout]): liste des outputs du Network

    Returns:
        [Network]: Nouvelle génération
    """    
    populationPrecedente = chargerTousLesFichiersDUnDossier("oldGen")
    populationPrecedenteTrie = triRapide(populationPrecedente)
    
    tempGen = []
    newGen = []
    tempGen += selectionParRang(populationPrecedenteTrie)
    tempGen += selectionParAdaptation(populationPrecedenteTrie)
    # tempGen += selectionUniforme(populationPrecedenteTrie)
    tempGen += reproductionMeilleur(populationPrecedenteTrie)
    tempGen += reproductionAleatoire(populationPrecedenteTrie)
    # tempGen += reproductionMeilleurMoinsBon(populationPrecedenteTrie)
    
    for i in range(len(tempGen)):
        saveNetwork(tempGen[i], "newGen/" + str(i + 1) + ".json")
    
    newGen = chargerTousLesFichiersDUnDossier("newGen")
    
    while len(newGen) != NB_INDIVIDU:
        newGen.append(networkGenerator(INPUTS, OUTPUTS))
    
    # random.shuffle(newGen)
    
    suppressionContenuDossier("oldGen")
    suppressionContenuDossier("newGen")
    
    return newGen

# -------------------- ANALYSE -------------------- #
def moyenneFitnessPopulation(population):
    """Calcul et retourne la moyenne des score de fitness d'une population

    Args:
        population ([Network]): population cible

    Returns:
        float: moyenne des fitness
    """
    somme = 0
    for individu in population:
        somme += individu.fitness
    return somme / NB_INDIVIDU

def maxFitnessPopulation(population):
    """retourne la valeur maximale de la fitness des Network de la population

    Args:
        population ([Network]): population cible

    Returns:
        float: fitness max
    """
    listeTriee = triRapide(population)
    return listeTriee[-1].fitness

def afficherMoyenneFitnessGenerations(data):
    """génère un graphe de toutes les moyennes de fitness par génération

    Args:
        data ([float]): liste des moyennes de fitness
    """
    somme = 0
    for moyenne in data:
        somme += moyenne
    
    print("Moyenne Fitness : ", somme / NB_GENERATION)
    
    plt.plot(range(1, NB_GENERATION + 1), data, linestyle='-')
    plt.title('Moyenne de Fitness par Génération')
    plt.xlabel('Génération')
    plt.ylabel('Fitness Moyenne')
    plt.grid(True)
    plt.show()

def afficherMaxFitnessGenerations(data):
    """génère un graphe de toutes les valeurs maximales de fitness par génération

    Args:
        data ([float]): liste des valeurs maximales de fitness
    """

    plt.plot(range(1, NB_GENERATION + 1), data, linestyle='-')
    plt.title('Max de Fitness par Génération')
    plt.xlabel('Génération')
    plt.ylabel('Fitness Max')
    plt.grid(True)
    plt.show()