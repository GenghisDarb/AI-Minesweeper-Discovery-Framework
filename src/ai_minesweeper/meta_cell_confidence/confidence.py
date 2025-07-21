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

    def __init__(self, alpha: float = 1.0, beta: float = 1.0) -> None:
        """Initialize with a prior Beta(α, β). Defaults to an uninformative prior (1,1)."""
        self.alpha: float = alpha
        self.beta: float = beta
        self._threshold: float | None = None  # allow override

    def update(
        self,
        predicted_probability: float | None = None,
        revealed_is_mine: bool | None = None,
    ) -> None:
        """
        Update the Beta distribution given a predicted probability and outcome.
        If both args are provided, use a Brier-score style update; otherwise fall back to simple counts.
        """
        if predicted_probability is not None and revealed_is_mine is not None:
            # Brier error: 1−p for a mine, p for a safe cell
            error = (1.0 - predicted_probability) if revealed_is_mine else predicted_probability
            self.alpha += (1.0 - error)
            self.beta += error
        elif revealed_is_mine is not None:
            # no prob provided, treat as 0.5 baseline
            if revealed_is_mine:
                self.beta += 1
            else:
                self.alpha += 1

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

    def set_threshold(self, value: float) -> None:
        """Set a confidence threshold for external use."""
        self._threshold = value

    def get_threshold(self) -> float:
        """Get the current confidence threshold."""
        if self._threshold is not None:
            return self._threshold
        return 0.05 + self.mean() * (0.25 - 0.05)

    def choose_move(self, board, risk_map: dict[Cell, float]) -> Cell:
        """
        Select the next cell to probe based on confidence and risk assessment.
        """
        tau = self.get_threshold()
        candidates = [cell for cell, risk in risk_map.items() if risk < tau]
        if candidates:
            return min(candidates, key=lambda c: risk_map[c])
        # fallback: return the minimum risk cell
        return min(risk_map, key=risk_map.get)
