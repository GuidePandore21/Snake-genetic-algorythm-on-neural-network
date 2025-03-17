from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone
import json

def compareNetworks(network1, network2):
    """Compare deux réseaux de neurones et retourne s'ils sont identiques."""
    
    # Vérifier le nombre de couches
    if len(network1.layers) != len(network2.layers):
        print("❌ Nombre de couches différent")
        return False

    for layer1, layer2 in zip(network1.layers, network2.layers):
        # Vérifier le label du layer
        if layer1.label != layer2.label:
            print(f"❌ Label de couche différent : {layer1.label} ≠ {layer2.label}")
            return False
        
        # Vérifier le nombre de neurones par couche
        if len(layer1.neurones) != len(layer2.neurones):
            print(f"❌ Nombre de neurones dans {layer1.label} différent")
            return False

        for neurone1, neurone2 in zip(layer1.neurones, layer2.neurones):
            # Vérifier le label des neurones
            if neurone1.label != neurone2.label:
                print(f"❌ Label de neurone différent : {neurone1.label} ≠ {neurone2.label}")
                return False

            # Si c'est un InputNeurone, comparer inputData
            if isinstance(neurone1, InputNeurone) and isinstance(neurone2, InputNeurone):
                if neurone1.inputData != neurone2.inputData:
                    print(f"❌ inputData différent dans {neurone1.label} : {neurone1.inputData} ≠ {neurone2.inputData}")
                    return False
                continue  # Pas besoin de vérifier bias et inputs

            # Vérifier le biais des neurones (en arrondissant pour éviter les erreurs d'arrondi)
            if round(neurone1.bias, 15) != round(neurone2.bias, 15):
                print(f"❌ Biais différent dans {neurone1.label} : {neurone1.bias} ≠ {neurone2.bias}")
                return False

            # Vérifier le nombre d'entrées (connexions)
            if len(neurone1.inputs) != len(neurone2.inputs):
                print(f"❌ Nombre d'entrées différent dans {neurone1.label}")
                return False

            # Vérifier les connexions (même neurone cible et même poids)
            inputs1 = sorted([(inp[0].label, round(inp[1], 15)) for inp in neurone1.inputs])
            inputs2 = sorted([(inp[0].label, round(inp[1], 15)) for inp in neurone2.inputs])

            if inputs1 != inputs2:
                print(f"❌ Connexions différentes dans {neurone1.label}")
                return False

    print("✅ Les deux réseaux sont identiques !")
    return True



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
    print(f"Réseau de neurones sauvegardé dans {filename}.")

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
    
    print(f"Réseau de neurones chargé depuis {filename}.")
    return network
