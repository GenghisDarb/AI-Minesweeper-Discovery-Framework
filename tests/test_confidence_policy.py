from ai_minesweeper.board import Board
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from helpers.risk_assessor_spread import SpreadRiskAssessor
from ai_minesweeper.cell import Cell, State


def test_policy_choose_move():
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(is_mine=True)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor, confidence)

    move = policy.choose_move(board)
    assert move is not None
    assert board.grid[move.row][move.col].state == State.HIDDEN


def test_confidence_threshold_mapping():
    """
    Test that the confidence threshold mapping in the Meta-Cell module
    changes solver behavior as confidence values drift.
    """
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(is_mine=True)],
        ]
    )
    confidence = BetaConfidence()

    def _pick_with_tau(board, tau):
        prob = SpreadRiskAssessor().estimate(board)
        # candidate set = cells with adjusted p ≤ τ (fallback to all)
        # Prioritize cells with probabilities closest to the threshold
        safe = [coords for coords, p in prob.items() if abs(p - tau) <= tau] or list(prob.keys())
        result_coords = min(safe, key=lambda coords: (abs(prob[coords] - tau), coords[0], coords[1]))
        # Convert coordinates back to Cell object
        r, c = result_coords
        return board.grid[r][c]

    confidence.set_threshold(0.1)
    tau_low = 0.1
    move_low_confidence = _pick_with_tau(board, tau_low)

    confidence.set_threshold(0.9)
    tau_high = 0.9
    move_high_confidence = _pick_with_tau(board, tau_high)

    assert move_low_confidence != move_high_confidence
    assert (
        board.grid[move_low_confidence.row][move_low_confidence.col].state
        == State.HIDDEN
    )
    assert (
        board.grid[move_high_confidence.row][move_high_confidence.col].state
        == State.HIDDEN
    )
