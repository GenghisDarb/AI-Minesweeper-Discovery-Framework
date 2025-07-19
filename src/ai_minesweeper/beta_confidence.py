class BetaConfidence:
    def __init__(self):
        self.alpha = 1.0
        self.beta = 1.0

    def update(self, predicted_probability: float, revealed_is_mine: bool):
        """
        Update confidence values based on prediction accuracy.

        :param predicted_probability: The predicted probability of the cell being a mine.
        :param revealed_is_mine: Whether the revealed cell is actually a mine.
        """
        if revealed_is_mine:
            self.alpha += predicted_probability
            self.beta += (1 - predicted_probability)
        else:
            self.alpha += (1 - predicted_probability)
            self.beta += predicted_probability

    def mean(self):
        """Calculate the mean of the Beta distribution."""
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, threshold: float):
        """Set a confidence threshold."""
        self.threshold = threshold

    def get_threshold(self):
        """Get the current confidence threshold."""
        return self.threshold
