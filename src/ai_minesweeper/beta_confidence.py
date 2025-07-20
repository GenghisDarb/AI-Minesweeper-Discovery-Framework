import logging

class BetaConfidence:
    def __init__(self):
        self.alpha = 1.0
        self.beta = 1.0
        self.logger = logging.getLogger(__name__)
        self.threshold = None  # Initialize threshold with None

    def update(self, predicted_probability: float = None, revealed_is_mine: bool = None, success: bool = None):
        """
        Update confidence values based on prediction accuracy.

        :param predicted_probability: The predicted probability of the cell being a mine.
        :param revealed_is_mine: Whether the revealed cell is actually a mine.
        :param success: Whether the prediction was successful (True for success, False for failure).
        """
        self.logger.debug(f"Update called with: predicted_probability={predicted_probability}, revealed_is_mine={revealed_is_mine}, success={success}")
        self.logger.debug(f"Before update: alpha={self.alpha}, beta={self.beta}")

        if success is not None:
            if success:
                self.alpha += 1
            else:
                self.beta += 1
        elif predicted_probability is not None and revealed_is_mine is not None:
            if not (0 <= predicted_probability <= 1):
                self.logger.error("Invalid predicted_probability value.")
                raise ValueError("predicted_probability must be between 0 and 1.")
            if revealed_is_mine:
                self.alpha += predicted_probability
                self.beta += (1 - predicted_probability)
            else:
                self.alpha += (1 - predicted_probability)
                self.beta += predicted_probability
        else:
            self.logger.error("Invalid input combination for update.")
            raise ValueError("Either `success` or both `predicted_probability` and `revealed_is_mine` must be provided.")

        self.logger.debug(f"After update: alpha={self.alpha}, beta={self.beta}")

    def mean(self):
        """Calculate the mean of the Beta distribution."""
        if self.alpha + self.beta == 0:
            self.logger.warning("Alpha and Beta sum to zero, returning mean as 0.")
            return 0
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, threshold: float):
        """Set a confidence threshold."""
        if not (0 <= threshold <= 1):
            self.logger.error("Invalid threshold value.")
            raise ValueError("Threshold must be between 0 and 1.")
        self.threshold = threshold
        self.logger.info(f"Threshold set to: {self.threshold}")

    def get_threshold(self):
        """Get the current confidence threshold."""
        if self.threshold is None:
            self.logger.warning("Threshold is not set.")
        return self.threshold
