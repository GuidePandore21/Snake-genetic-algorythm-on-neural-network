from NeuroneNetwork.Network import Network
from NeuroneNetwork.Layer import Layer
from NeuroneNetwork.Neurone import Neurone
from NeuroneNetwork.InputNeurone import InputNeurone
from NeuroneNetwork.OutputNeurone import OutputNeurone

def saveNetwork(Network, cheminFichier):
    """Sauvegarde dans un fichier txt un Network

    Args:
        Network (Network): Network à sauvegarder
        cheminFichier (String): chemin du fichier (chemin relatif) ne pas oublier d'ajouter l'extension .txt
    """
    with open(cheminFichier, "w") as fichier:
        fichier.write(str(0) + "\n")
        fichier.write(str(len(Network.layers)) + "\n")
        
        for i in range(len(Network.layers)):
            fichier.write(Network.layers[i].label + "\n")
            fichier.write(str(len(Network.layers[i].neurones)) + "\n")
            
            for j in range(len(Network.layers[i].neurones)):
                fichier.write(Network.layers[i].neurones[j].label + "\n")
                if i != 0:
                    fichier.write(str(Network.layers[i].neurones[j].bias) + "\n")
                    for k in range(len(Network.layers[i].neurones[j].inputs)):
                        fichier.write(Network.layers[i].neurones[j].inputs[k][0].label + " " + str(Network.layers[i].neurones[j].inputs[k][1]) + "\n")
