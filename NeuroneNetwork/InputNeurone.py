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