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

    def forwardPropagation(self):
        """retourne la valeur du calcul de la forward propagation avec les inputs du Neurone et le bias
        Fonction : ∑ wi * xi + biais

        Returns:
            float: valeur du calcul de la forward propagation
        """
        calcul = self.bias
        for input in self.inputs:
            calcul += input[0].output * input[1]
        self.output = self.activation(calcul)
        return self.output