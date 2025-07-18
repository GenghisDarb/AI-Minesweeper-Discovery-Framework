class BetaConfidence:
    """
    Tracks confidence in false-hypothesis predictions using a Beta distribution.

    Attributes:
        alpha (float): Success count parameter of the Beta distribution, representing correct predictions.
        beta (float): Failure count parameter of the Beta distribution, representing incorrect predictions.
        _tau (float): Risk threshold, representing the probability of encountering a false hypothesis.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0, tau: float = 0.10):
        """
        Initialize the BetaConfidence object with parameters for the Beta distribution.

        Args:
            alpha (float): Initial success count parameter of the Beta distribution.
            beta (float): Initial failure count parameter of the Beta distribution.
            tau (float): Initial risk threshold, representing the probability of encountering a false hypothesis.
        """
        self.alpha = alpha
        self.beta = beta
        self._tau = tau  # initial risk threshold

    def get_threshold(self) -> float:
        """
        Return the current risk threshold τ, representing the probability of encountering a false hypothesis.
        """
        return self._tau

    def set_threshold(self, tau: float) -> None:
        """
        Set the risk threshold τ, ensuring it remains within the range [0.01, 0.49].

        Args:
            tau (float): The desired risk threshold.
        """
        self._tau = max(0.01, min(0.99, tau))  # allow high manual τ for tests

    def update(self, success: bool, count: int = 1) -> None:
        """
        Update the Beta distribution based on prediction success or failure.

        Args:
            success (bool): True if the prediction was correct, False otherwise.
            count (int): The number of successes or failures to update the distribution by.
        """
        if success:
            self.alpha += count
        else:
            self.beta += count

    def mean(self) -> float:
        """
        Calculate the mean of the Beta distribution.

        Returns:
            float: The mean value of the Beta distribution.
        """
        return self.alpha / (self.alpha + self.beta)

    def variance(self) -> float:
        """
        Calculate the variance of the Beta distribution.

        Returns:
            float: The variance of the Beta distribution.
        """
        total = self.alpha + self.beta
        return (self.alpha * self.beta) / (total**2 * (total + 1))

    def choose_move(self, board) -> tuple[int, int] | None:
        """
        Select the next cell to probe based on confidence and risk assessment.
        """
        prob_map = self.assessor.estimate(board)  # keys are Cell objects
        tau = self.confidence.get_threshold()
        safe = [cell for cell, p in prob_map.items() if p <= tau]
        pick = (
            min(safe, key=lambda cell: (prob_map[cell], cell.row, cell.col))
            if safe
            else None
        )
        if pick is None:  # Fallback logic
            for r in range(board.n_rows):
                for c in range(board.n_cols):
                    if board[r, c].is_hidden() and not board[r, c].is_flagged():
                        return (r, c)
        return pick
