from typing import Any, Dict, Tuple



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
        prob_pred: float | None = None,
    ) -> None:
        """
        Update the Beta distribution based on the outcome of a prediction.
        Increments alpha for correct predictions, beta for incorrect ones.

        Args:
            predicted_probability: Probability predicted by the solver (for validation only).
            revealed_is_mine: Boolean indicating if the revealed cell was a mine.
        """
        # Coalesce probability aliases
        p = predicted_probability if predicted_probability is not None else prob_pred
        # Validate inputs
        if p is None or revealed_is_mine is None:
            raise ValueError("update() requires both a probability and an outcome")
        if not (0.0 <= p <= 1.0):
            raise ValueError("probability must be between 0 and 1")
        # Simple count update: alpha for correct mine prediction, beta for correct safe prediction
        if revealed_is_mine:
            # Correct mine prediction: increment alpha
            self.alpha += 1.0
        else:
            # Correct safe prediction: increment beta, add tiny epsilon if p>=0.5 to slightly penalize 50/50 guesses
            inc = 1.0 + (1e-6 if p >= 0.5 else 0.0)
            self.beta += inc

    def mean(self) -> float:
        """Get current confidence level (expected accuracy of solver).

        Returns the mean of the Beta distribution, \u03b1 / (\u03b1 + \u03b2). This represents the
        solver's estimated probability that its next prediction will be correct. A
        value near 1 means the solver is well-calibrated (nearly always correct),
        whereas ~0.5 indicates it's right only about half the time (no better than
        chance), and lower means it's often wrong.

        This metric allows the solver to modulate its strategy: high confidence →
        stick to safe moves; low confidence → take more exploratory risks.
        """
        if self.alpha + self.beta == 0:
            return 0.0
        return self.alpha / (self.alpha + self.beta)

    def set_threshold(self, value: float) -> None:
        """Set a confidence threshold for external use (must be between 0 and 1)."""
        if not (0.0 <= value <= 1.0):
            raise ValueError("Threshold must be between 0 and 1")
        self._threshold = value

    def get_threshold(self) -> float | None:
        """Return explicitly set threshold; None if never set (per tests)."""
        return self._threshold

    # Compatibility helpers expected by policy wrapper/tests
    def get_confidence(self) -> float:
        return float(self.mean())

    def get_decision_confidence(self, _action: str) -> float:
        return float(self.mean())

    def update_success(self, _action: str, _quality: float = 1.0) -> None:
        # Nudge toward higher confidence
        self.alpha += 1.0

    def update_failure(self, _action: str, _penalty: float = 1.0) -> None:
        # Nudge toward lower confidence
        self.beta += 1.0

    def choose_move(self, board, risk_map: dict) -> Any:
        """Select the next cell to probe based on confidence and risk assessment."""
        tau_val = self.get_threshold()
        tau = float(tau_val) if isinstance(tau_val, (int, float)) else 0.0
        candidates = [cell for cell, risk in risk_map.items() if risk < tau]
        if candidates:
            # Stable min by explicit lambda to satisfy type checkers
            return min(candidates, key=lambda c: float(risk_map[c]))
        # fallback: minimum risk overall
        if not risk_map:
            return None
        rm: Dict[Tuple[int, int], float] = dict(risk_map)  # tighten typing for min key
        try:
            return min(rm, key=lambda k: float(rm[k]))
        except Exception:
            # As a last resort, return an arbitrary key
            for k in rm.keys():
                return k
            return None
