class BetaConfidence:
    """
    Tracks confidence in mine-probability predictions using a Beta distribution.

    Attributes:
        alpha (float): Success count parameter of the Beta distribution.
        beta (float): Failure count parameter of the Beta distribution.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        self.alpha = alpha
        self.beta = beta

    def update(self, prob_pred: float, revealed_is_mine: bool):
        """
        Updates the Beta distribution based on the prediction and actual outcome.

        Args:
            prob_pred (float): Predicted probability of a mine.
            revealed_is_mine (bool): Whether the revealed cell is a mine.
        """
        actual = 1.0 if revealed_is_mine else 0.0
        error = (prob_pred - actual) ** 2
        self.alpha += 1 - error
        self.beta += error

    def mean(self) -> float:
        """
        Returns the mean of the Beta distribution.

        Returns:
            float: The mean confidence value.
        """
        return self.alpha / (self.alpha + self.beta)
