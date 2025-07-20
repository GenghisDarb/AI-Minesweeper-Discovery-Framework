from .confidence import BetaConfidence
from ai_minesweeper.board import Board


class ConfidencePolicy:
    """
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(self, base_solver, confidence: BetaConfidence):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param confidence: BetaConfidence instance for tracking.
        """
        self.base_solver = base_solver()
        self.confidence = confidence

    def choose_move(self, board_state: Board):
        """
        Select the next move based on confidence-adjusted risk threshold.

        :param board_state: Current state of the Minesweeper board.
        :return: The chosen Cell object.
        """
        from ai_minesweeper.cell import Cell
        
        tau = self.confidence.get_threshold()
        prob_map = self.base_solver.estimate(board_state)

        if not prob_map:
            # Fallback: no probability info – choose the first hidden, unflagged cell
            for r in range(board_state.n_rows):
                for c in range(board_state.n_cols):
                    cell = board_state.grid[r][c]
                    if cell.is_hidden() and not cell.is_flagged():
                        return cell
            raise RuntimeError("No valid moves remaining.")

        # Λ-ladder curve (Observer-State §2.3):
        # early confidence moves the threshold quickly; high confidence tapers.
        tau_min, tau_max = 0.05, 0.25
        tau = tau_min + (tau_max - tau_min) * (1 - self.confidence.mean()) ** 2

        print(f"Using Λ-ladder threshold: {tau}")

        # Select the move with the lowest probability below the threshold
        for cell, prob in prob_map.items():
            if prob < tau:
                return cell

        # Fallback: If no probabilities are below the threshold, pick the lowest
        return min(prob_map, key=prob_map.get)

        # ── guaranteed-safe fallback ──
        for r in range(board_state.n_rows):
            for c in range(board_state.n_cols):
                cell = board_state[r, c]
                if cell.is_hidden() and not cell.is_flagged():
                    return cell

        # No moves left – board solved or invalid
        raise RuntimeError("No valid moves remaining on the board.")
        # safe_cells = [cell for cell, prob in prob_map.items() if prob <= tau]
        confidence = self.confidence.mean()
        
        result = None
        if confidence > 0.8:
            # High confidence: exploit
            if hasattr(self.base_solver, 'choose_safest_move'):
                result = self.base_solver.choose_safest_move(board_state)
            else:
                result = self.base_solver.choose_move(board_state)
        elif confidence < 0.5:
            # Low confidence: explore
            if hasattr(self.base_solver, 'choose_information_rich_move'):
                result = self.base_solver.choose_information_rich_move(board_state)
            else:
                result = self.base_solver.choose_move(board_state)
        else:
            # Moderate confidence: default behavior
            result = self.base_solver.choose_move(board_state)
        
        # Type validation: ensure we return a Cell object
        if result is None:
            return None
        
        if isinstance(result, tuple) and len(result) == 2:
            # Convert tuple (row, col) to Cell object
            row, col = result
            if (0 <= row < board_state.n_rows and 
                0 <= col < board_state.n_cols):
                cell = board_state.grid[row][col]
                if cell.row is None:
                    cell.row = row
                if cell.col is None:
                    cell.col = col
                return cell
            return None
        elif isinstance(result, Cell):
            return result
        else:
            # Unexpected return type, log and return None
            print(f"Warning: base_solver returned unexpected type {type(result)}: {result}")
            return None
