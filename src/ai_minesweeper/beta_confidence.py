class BetaConfidence:
    def __init__(self):
        self.alpha = 0.0
        self.beta = 0.0

    def update(self, predicted_probability: float, revealed_is_mine: bool):
        """
        Update confidence values based on prediction accuracy.

        :param predicted_probability: The predicted probability of the cell being a mine.
        :param revealed_is_mine: Whether the revealed cell is actually a mine.
        """
        if revealed_is_mine:
            self.alpha += predicted_probability
        else:
            self.beta += predicted_probability
