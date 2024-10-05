class Layer:
    def __init__(self, label, neurones) -> None:
        """Constructeur de la classe Layer

        Args:
            neurones (Neurone): liste de Neurone du Layer
        """
        self.label = label
        self.neurones = neurones