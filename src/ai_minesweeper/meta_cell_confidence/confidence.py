class BetaConfidence:
    """
    Tracks confidence in mine-probability predictions using a Beta distribution.

    Attributes:
        alpha (float): Success count parameter of the Beta distribution.
        beta (float): Failure count parameter of the Beta distribution.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0, tau: float = 0.10):
        self.alpha = alpha
        self.beta = beta
        self._tau = tau            # initial risk threshold

    def get_threshold(self) -> float:
        """Return current risk threshold τ = β / (α+β)."""
        return self._tau

    def set_threshold(self, tau: float) -> None:
        """Force risk threshold into [0.01, 0.49]."""
        self._tau = max(0.01, min(0.99, tau))  # allow high manual τ for tests

    def update(self, prob_pred: float, revealed_is_mine: bool) -> None:
        """
        Bayesian calibration:
        • actual = 1 if mine, 0 otherwise
        • Brier error = (pred-actual)^2
        • α accumulates correct predictions, β accumulates errors
        τ (risk threshold) tracks empirical failure rate.
        """
        actual = 1.0 if revealed_is_mine else 0.0
        if revealed_is_mine:
            self.alpha += 0.5
        else:
            self.beta += 0.5
        self.alpha, self.beta = max(self.alpha, 1e-3), max(self.beta, 1e-3)
        total = self.alpha + self.beta
        self._tau = self.beta / total

    def mean(self) -> float:
        """
        Returns the mean of the Beta distribution.

        Returns:
            float: The mean confidence value.
        """
        return self.alpha / (self.alpha + self.beta)

    def choose_move(self, board):
        """
        Select the next cell to probe based on confidence and risk assessment.
        """
        prob_map = self.assessor.estimate(board)  # keys are Cell objects
        tau = self.confidence.get_threshold()
        safe = [cell for cell, p in prob_map.items() if p <= tau]
        pick = min(
            safe,
            key=lambda cell: (prob_map[cell], cell.row, cell.col)
        ) if safe else None
        return pick
