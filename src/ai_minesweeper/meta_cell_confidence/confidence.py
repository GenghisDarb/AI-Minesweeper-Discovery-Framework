class BetaConfidence:
    """
    Tracks solver confidence using a Beta distribution.
    Inspired by TORUS Theory's controller dimension for recursive self-correction.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        """
        Initialize Beta distribution parameters.
        :param alpha: Success pseudo-counts (default 1.0).
        :param beta: Failure pseudo-counts (default 1.0).
        """
        self.alpha = alpha
        self.beta = beta
        self.threshold = None  # Initialize threshold attribute

    def update(self, prediction: float, outcome: bool):
        """Update alpha and beta based on the prediction and outcome."""
        if outcome:
            self.alpha += prediction
        else:
            self.beta += 1 - prediction

    def mean(self) -> float:
        """
        Calculate the mean of the Beta distribution.
        :return: Confidence level (alpha / (alpha + beta)).
        """
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, threshold: float):
        """Set a confidence threshold for decision-making."""
        self.threshold = threshold

    def get_threshold(self) -> float:
        """Retrieve the current confidence threshold."""
        return self.threshold
