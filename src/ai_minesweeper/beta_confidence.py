class BetaConfidence:
    def __init__(self):
        self.alpha = 1.0
        self.beta = 1.0

    def update(self, predicted_probability: float = None, revealed_is_mine: bool = None, success: bool = None):
        """
        Update confidence values based on prediction accuracy.

        :param predicted_probability: The predicted probability of the cell being a mine.
        :param revealed_is_mine: Whether the revealed cell is actually a mine.
        :param success: Whether the prediction was successful (True for success, False for failure).
        """
        print(f"Update called with: predicted_probability={predicted_probability}, revealed_is_mine={revealed_is_mine}, success={success}")
        print(f"Before update: alpha={self.alpha}, beta={self.beta}")
        if success is not None:
            if success:
                self.alpha += 1
            else:
                self.beta += 1
        elif predicted_probability is not None and revealed_is_mine is not None:
            if revealed_is_mine:
                self.alpha += predicted_probability
                self.beta += (1 - predicted_probability)
            else:
                self.alpha += (1 - predicted_probability)
                self.beta += (predicted_probability)  # Remove epsilon adjustment
        else:
            raise ValueError("Either `success` or both `predicted_probability` and `revealed_is_mine` must be provided.")
        print(f"After update: alpha={self.alpha}, beta={self.beta}")

    def mean(self):
        """Calculate the mean of the Beta distribution."""
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, threshold: float):
        """Set a confidence threshold."""
        self.threshold = threshold

    def get_threshold(self):
        """Get the current confidence threshold."""
        return self.threshold
