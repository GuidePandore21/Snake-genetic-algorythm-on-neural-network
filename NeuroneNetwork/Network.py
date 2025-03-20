import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Network:
    def __init__(self, layers) -> None:
        """Constructeur de la classe Network

        Args:
            layers (Layer): liste des Layer du Network
        """
        self.layers = layers
        self.fitness = 0
    
    def deplacement(self, x, y, distance_sf):
        """Mise à jour des valeurs des InputNeurones pour le déplacement du Snake

        Args:
            x (int): position en x du Snake
            y (int): position en y du Snake
            distance_sf (int): distance manhattan du Snake par rapport à la pomme
        """
        self.layers[0].neurones[0].inputData = x
        self.layers[0].neurones[1].inputData = y
        self.layers[0].neurones[4].inputData = distance_sf
    
    def mangerPomme(self, foodx, foody, fitness):
        """ajoute une valeurs fitness au score du Network et modifie les valeurs d'InputNeurones pour qu'elles correspondent à la nouvelle position de la pomme

        Args:
            foodx (_type_): position en x de la pomme
            foody (_type_): position en y de la pomme
            fitness (_type_): valeur à ajouter au score
        """
        self.fitness += fitness
        self.layers[0].neurones[2].inputData = foodx
        self.layers[0].neurones[3].inputData = foody

    def softmax(self, x):
        """Applique la fonction Softmax à une liste de valeurs."""
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)

    def outputNetwork(self):
        """Retourne la valeur de sortie du Network avec Softmax.

        Returns:
            string: valeur de sortie choisie
        """
        outputs = []
        
        for layer in self.layers:
            for neurone in layer.neurones:
                if layer.label == "OutputLayer":
                    outputs.append(neurone.forwardPropagation())
                else:
                    neurone.forwardPropagation()

        # Appliquer Softmax sur les valeurs de sortie
        outputs = self.softmax(outputs)

        # Sélectionner l'index avec la probabilité la plus élevée
        indexMax = np.argmax(outputs)
        
        return self.layers[-1].neurones[indexMax].valeurOutput

    
    def printOutputNetwork(self):
        """Affiche toutes les valeurs de sortie possible du Network
        """
        for layer in self.layers:
            for neurone in layer.neurones:
                print(neurone.label, ": Valeur Output :", neurone.output)

    def renameLayers(self):
        """Rename les layers (utile entre deux génération pour les modifications des Network)
        """
        self.layers[0].label = "InputLayer"
        self.layers[len(self.layers) - 1].label = "OutputLayer"
        for i in range(1, len(self.layers) - 1):
            self.layers[i].label = "HiddenLayer" + str(i)
    
    def representation(self):
        """retourne un dictionnaire contenant la liste des Layer du Neurone

        Returns:
            Layer: dictionnaire contenant la liste des Layer du Neurone
        """
        network = {}
        for layer in self.layers:
            network[layer.label] = layer.representation()
        return network
    
    def drawNeuroneNetwork(self):
        """Dessine sous forme d'un graphe le Network en paramètre
        """
        G = nx.Graph()
        
        for layer in self.representation():
            for neurone in self.representation()[layer]:
                G.add_node(neurone.label)
                
        for layer in self.representation():
            if layer != "InputLayer":
                for neurone in self.representation()[layer]:
                    for input in neurone.inputs:
                        G.add_edge(input[0].label, neurone.label, weight = input[1])
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        pos = {}
        y = 0
        compteur = 0
        for layer in self.representation():
            x = compteur * 2
            for neurone in self.representation()[layer]:
                pos[neurone.label] = (x, y)
                y -= 1
            y = 0
            compteur += 1
        
        nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue', font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Réseau de Neurones")
        plt.show()
        
    def miseAJourInputValue(self, INPUTS):
        """Mise à jour des valeurs des InputNeurones

        Args:
            INPUTS (list): liste des valeurs à mettre à jour
        """
        for i in range(len(INPUTS)):
            self.layers[0].neurones[i].inputData = INPUTS[i]