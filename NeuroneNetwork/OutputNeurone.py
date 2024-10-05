from NeuroneNetwork.Neurone import Neurone
class OutputNeurone(Neurone):
    def __init__(self, label, bias, inputs, valeurOutput) -> None:
        """Constructeur de la classe Neurone

        Args:
            bias (float): valeur du bias du Neurone
            inputs (Neurone, float): liste de liste du Neurone précédent et de son poids : [NeuronePrécédent, weight]
        """
        self.label = label
        self.bias = bias
        self.inputs = inputs
        self.valeurOutput = valeurOutput
        self.output = 0