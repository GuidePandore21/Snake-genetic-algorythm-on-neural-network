from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone
# from AlgorithmeGenetique import inputLayerGenerator

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

def saveNetwork(Network, cheminFichier):
    """Sauvegarde dans un fichier txt un Network

    Args:
        Network (Network): Network à sauvegarder
        cheminFichier (String): chemin du fichier (chemin relatif) ne pas oublier d'ajouter l'extension .txt
    """
    with open(cheminFichier, "w") as fichier:
        fichier.write(str(0) + "\n")
        fichier.write(str(len(Network.layers)) + "\n")
        
        for i in range(1, len(Network.layers)):
            fichier.write(Network.layers[i].label + "\n")
            fichier.write(str(len(Network.layers[i].neurones)) + "\n")
            
            for j in range(len(Network.layers[i].neurones)):
                fichier.write(Network.layers[i].neurones[j].label + "\n")
                if i != 0:
                    fichier.write(str(Network.layers[i].neurones[j].bias) + "\n")
                    fichier.write(str(len(Network.layers[i].neurones[j].inputs)) + "\n")
                    for k in range(len(Network.layers[i].neurones[j].inputs)):
                        fichier.write(Network.layers[i].neurones[j].inputs[k][0].label + " " + str(Network.layers[i].neurones[j].inputs[k][1]) + "\n")

def loadNetwork(cheminFichier, INPUTS, OUTPUTS):
    """Créer / Charge un Network à partir d'un txt

    Args:
        cheminFichier (string): chemin du fichier txt
        INPUTS ([int]): liste des inputs du Network
        OUTPUTS ([float]): liste des outputs du Network

    Returns:
        Network: retourne le Network créer / charger
    """
    curseur = 0
    with open(cheminFichier, "r") as fichier:
        tempLignes = fichier.readlines()
        lignes = []
        for ligne in tempLignes:
            lignes.append(ligne.replace("\n", ""))
            
        neurones = []
        for i in range(len(INPUTS)):
            label = "InputNeurone" + str(i + 1)
            neurones.append(InputNeurone(label, INPUTS[i]))
            
        listeLayer = []
        listeLayer.append(Layer("InputLayer", neurones))
        
        fitness = lignes[curseur]
        curseur += 1
        nbLayer = int(lignes[curseur])
        for l in range(nbLayer - 1): # Layers
            curseur += 1
            labelLayer = lignes[curseur]
            curseur += 1
            listeNeurones = []
            nbNeurone = int(lignes[curseur])
            for _ in range(nbNeurone): # Neurones
                curseur += 1
                labelNeurone = lignes[curseur]
                curseur += 1
                biasNeurone = float(lignes[curseur])
                curseur += 1
                inputs = []
                for i in range(int(lignes[curseur])): # Inputs
                    curseur += 1
                    input = lignes[curseur].split(" ")
                    for neurone in listeLayer[len(listeLayer) - 1].neurones:
                        if neurone.label == input[0]:
                            inputs.append([neurone, float(input[1])])
                            break
                if l == nbLayer - 2:
                    neurone = OutputNeurone(labelNeurone, biasNeurone, inputs, OUTPUTS)
                else:
                    neurone = Neurone(labelNeurone, biasNeurone, inputs)
                listeNeurones.append(neurone)
            layer = Layer(labelLayer, listeNeurones)
            listeLayer.append(layer)
            network = Network(listeLayer)
            network.fitness = fitness
        return network