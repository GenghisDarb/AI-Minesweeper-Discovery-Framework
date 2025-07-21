from typing import Optional, Union

from ai_minesweeper.board import Cell


class BetaConfidence:
    """Bayesian confidence tracker for Minesweeper solver predictions.

    Maintains a Beta(α, β) distribution representing the solver’s calibration. After
    each move, update α (confidence in solver when correct) or β (when wrong) to
    adjust the estimated accuracy. This meta-level state is analogous to TORUS’s
    controller dimension operator that compensates a ~25.7° phase gap to
    achieve perfect 13→0 closure. In our context, it “closes the loop”
    between predicted probabilities and actual outcomes.

    The Beta distribution’s mean (α/(α+β)) serves as the solver’s current confidence
    level (0 = totally uncalibrated, 1 = perfectly calibrated). A high mean indicates
    the solver’s predictions have been accurate, whereas a low mean signals
    systematic errors, prompting more exploratory moves.
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        """Initialize with a prior Beta(α, β). Defaults to an uninformative prior (1,1)."""
        self.alpha: float = alpha
        self.beta: float = beta

    def update(
        self,
        prob_pred: float | None = None,
        revealed_is_mine: bool | None = None,
        *,
        predicted_probability: float | None = None,
        success: bool | None = None,
    ):
        if success is not None:  # legacy quick path
            if success:
                self.alpha += 1.0
            else:
                self.beta += 1.0
        else:
            p = prob_pred if prob_pred is not None else predicted_probability
            if p is None or revealed_is_mine is None:
                raise ValueError("Both probability and outcome must be provided.")
            predicted_mine = p >= 0.5
            actual_mine = revealed_is_mine
            if predicted_mine == actual_mine:
                self.alpha += 1.0
            else:
                self.beta += 1.0

    def mean(self) -> float:
        """Get current confidence level (expected accuracy of solver).

        Returns the mean of the Beta distribution, α / (α + β). This represents the
        solver’s estimated probability that its next prediction will be correct. A
        value near 1 means the solver is well-calibrated (nearly always correct),
        whereas ~0.5 indicates it’s right only about half the time (no better than
        chance), and lower means it’s often wrong.

        This metric allows the solver to modulate its strategy: high confidence →
        stick to safe moves; low confidence → take more exploratory risks.
        """
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, tau: float) -> None:
        """Set a confidence threshold for external use."""
        if not (0.0 <= tau <= 1.0):
            raise ValueError("Threshold must be between 0 and 1.")
        self.tau = tau

    def get_threshold(self) -> Optional[float]:
        """Get the current confidence threshold."""
        return getattr(self, "tau", None)

    def choose_move(self, board) -> Union[Cell, None]:
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
                    cell = board.grid[r][c]
                    if cell.is_hidden() and not cell.is_flagged():
                        if cell.row == -1:
                            cell.row = r
                        if cell.col == -1:
                            cell.col = c
                        return cell
        return pick
