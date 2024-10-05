class Neurone:
    def __init__(self, label, bias, inputs) -> None:
        """Constructeur de la classe Neurone

        Args:
            bias (float): valeur du bias du Neurone
            inputs (Neurone, float): liste de liste du Neurone précédent et de son poids : [NeuronePrécédent, weight]
        """
        self.label = label
        self.bias = bias
        self.inputs = inputs
        self.output = 0

    def representation(self):
        """retourne une liste contenant le bias et la liste des Input du Neurone

        Returns:
            float: liste contenant le bias et la liste des Input du Neurone
        """
        return self