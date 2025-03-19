from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone
import json

def saveNetwork(network, filename):
    """Sauvegarde le réseau de neurones dans un fichier JSON."""
    data = {
        "fitness": network.fitness,
        "layers": [
            {
                "label": layer.label,
                "neurones": [
                    {
                        "label": neurone.label,
                        "bias": neurone.bias if hasattr(neurone, 'bias') else None,
                        "inputs": [
                            {"neurone": inp[0].label, "weight": inp[1]} for inp in neurone.inputs
                        ] if hasattr(neurone, 'inputs') else [],
                        "valeurOutput": getattr(neurone, "valeurOutput", None),
                        "inputData": getattr(neurone, "inputData", None)
                    }
                    for neurone in layer.neurones
                ]
            }
            for layer in network.layers
        ]
    }
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    # print(f"Réseau de neurones sauvegardé dans {filename}.")

def loadNetwork(filename):
    """Charge un réseau de neurones à partir d'un fichier JSON."""
    with open(filename, "r") as file:
        data = json.load(file)

    layers = []
    neurone_dict = {}

    # Création des neurones sans leurs inputs
    for layer_data in data["layers"]:
        neurones = []
        for neurone_data in layer_data["neurones"]:
            if "inputData" in neurone_data and neurone_data["inputData"] is not None:
                neurone = InputNeurone(neurone_data["label"], neurone_data["inputData"])
            elif "valeurOutput" in neurone_data and neurone_data["valeurOutput"] is not None:
                neurone = OutputNeurone(neurone_data["label"], neurone_data["bias"], [], neurone_data["valeurOutput"])
            else:
                neurone = Neurone(neurone_data["label"], neurone_data["bias"], [])
            neurones.append(neurone)
            neurone_dict[neurone.label] = neurone
        layers.append(Layer(layer_data["label"], neurones))

    # Ajout des connexions entre neurones
    for layer_data, layer in zip(data["layers"], layers):
        for neurone_data, neurone in zip(layer_data["neurones"], layer.neurones):
            if "inputs" in neurone_data:
                for inp in neurone_data["inputs"]:
                    neurone.inputs.append((neurone_dict[inp["neurone"]], inp["weight"]))

    # Création du réseau de neurones final
    network = Network(layers)
    network.fitness = data["fitness"]
    
    # print(f"Réseau de neurones chargé depuis {filename}.")
    return network
