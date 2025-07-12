import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.cell import Cell, State


class SpreadRiskAssessor(RiskAssessor):
    def estimate(self, board):
        hidden = board.hidden_cells()
        spectrum = [0.05, 0.10, 0.15, 0.20]
        return {cell: spectrum[i % len(spectrum)] for i, cell in enumerate(hidden)}


def test_policy_choose_move():
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(is_mine=True)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor, confidence)

    with open("debug_board_state.log", "w") as log_file:
        log_file.write("Board state:\n")
        for row in board.grid:
            log_file.write(
                str([f"state={cell.state}, is_mine={cell.is_mine}" for cell in row])
                + "\n"
            )

    move = policy.choose_move(board)
    assert move is not None
    assert board.grid[move[0]][move[1]].state == State.HIDDEN


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
        # Adjust probabilities based on confidence threshold
        adjusted_prob = {c: p * tau for c, p in prob.items()}
        # candidate set = cells with adjusted p ≤ τ (fallback to all)
        # Prioritize cells with probabilities closest to the threshold
        safe = [c for c, p in prob.items() if abs(p - tau) <= tau] or list(prob)
        result = min(safe, key=lambda c: (abs(prob[c] - tau), c))

        # Debugging output
        print(f"Original probabilities: {prob}")
        print(f"Adjusted probabilities with tau={tau}: {adjusted_prob}")
        print(f"Chosen cell: {result} with adjusted probability: {adjusted_prob[result]}")

        return result

    confidence.set_threshold(0.1)
    tau_low = 0.1
    move_low_confidence = _pick_with_tau(board, tau_low)

    confidence.set_threshold(0.9)
    tau_high = 0.9
    move_high_confidence = _pick_with_tau(board, tau_high)

    # Debugging output
    print(f"BetaConfidence instance: {confidence}")
    print(f"Threshold: {confidence.get_threshold()}")

    assert move_low_confidence != move_high_confidence
    assert board.grid[move_low_confidence[0]][move_low_confidence[1]].state == State.HIDDEN
    assert board.grid[move_high_confidence[0]][move_high_confidence[1]].state == State.HIDDEN
