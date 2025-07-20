from typing import Union, Optional
from ai_minesweeper.board import Cell
from ai_minesweeper.cell import State

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
        self._threshold: Optional[float] = None

    def update(self, prob_pred: float, revealed_is_mine: bool) -> None:
        """Update confidence based on a move’s predicted probability and the actual outcome."""
        if not (0 <= prob_pred <= 1):
            raise ValueError("Probability must be between 0 and 1.")
            
        predicted_mine = prob_pred >= 0.5
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
        """Set a confidence threshold value."""
        if 0 <= tau <= 1:
            self._threshold = tau
        else:
            raise ValueError("Threshold must be between 0 and 1.")

    def get_threshold(self) -> Optional[float]:
        """Get the current confidence threshold value."""
        return self._threshold

    def choose_move(self, board) -> Union[Cell, None]:
        """
        Select the next cell to probe based on confidence and risk assessment.

        :param board: The current Minesweeper board.
        :return: The chosen Cell object or None if no valid move is found.
        """
        hidden_cells = [(r, c) for r in range(board.n_rows) for c in range(board.n_cols) if board.grid[r][c].state == State.HIDDEN]
        if not hidden_cells:
            return None

        # Use confidence threshold to filter candidates
        tau = self.get_threshold() or 0.5  # Default threshold if not set
        prob_map = {cell: 0.5 for cell in hidden_cells}  # Placeholder for actual probabilities

        # Find the safest move below the threshold
        safe_candidates = [cell for cell in hidden_cells if prob_map[cell] <= tau]
        if safe_candidates:
            r, c = min(safe_candidates, key=lambda cell: prob_map[cell])
        else:
            # Fallback to the least risky cell
            r, c = min(hidden_cells, key=lambda cell: prob_map[cell])

        return board.grid[r][c]
