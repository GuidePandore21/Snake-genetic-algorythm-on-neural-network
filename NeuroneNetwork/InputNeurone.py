from NeuroneNetwork.Neurone import Neurone
class InputNeurone(Neurone):
    def __init__(self, label, inputData) -> None:
        """Constructeur de la classe Neurone

        Args:
            bias (float): valeur du bias du Neurone
            inputDatas (float): liste des données d'entrées
        """
        self.label = label
        self.inputData = inputData

    def forwardPropagation(self):
        """retourne la valeur du calcul de la forward propagation avec les inputs du Neurone et le bias
        Fonction : ∑ xi

        Returns:
            float: valeur du calcul de la forward propagation
        """
        self.output = self.inputData
        return self.output