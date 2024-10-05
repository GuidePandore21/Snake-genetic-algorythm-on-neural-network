class Layer:
    def __init__(self, label, neurones) -> None:
        """Constructeur de la classe Layer

        Args:
            neurones (Neurone): liste de Neurone du Layer
        """
        self.label = label
        self.neurones = neurones
    
    def representation(self):
        """retourne une liste contenant la liste des Neurone du Layer

        Returns:
            float: une liste contenant la liste des Neurone du Layer
        """
        layer = []
        for neurone in self.neurones:
            layer.append(neurone.representation())
        return layer
    
    def renameNeurones(self):
        for i in range(len(self.neurones)):
            self.neurones[i].label = self.label + "Neurone" + str(i + 1)