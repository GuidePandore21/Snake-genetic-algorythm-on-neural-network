class Network:
    def __init__(self, layers) -> None:
        """Constructeur de la classe Network

        Args:
            layers (Layer): liste des Layer du Network
        """
        self.layers = layers
        self.fitness = 0