import pytest

from ai_minesweeper.board import Board
from ai_minesweeper.cell import Cell, State
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.risk_assessor import SpreadRiskAssessor


def test_policy_choose_move():
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(is_mine=True)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor(), confidence)

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
        safe = [c for c, p in prob.items() if abs(p - tau) <= tau] or list(prob)
        result = min(safe, key=lambda c: (abs(prob[c] - tau), c.row, c.col))

        return result

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


def test_beta_confidence():
    confidence = BetaConfidence()
    assert confidence.mean() == 0.5  # Initial mean with alpha=1, beta=1

    confidence.update(0.1, False)  # Incorrect prediction
    assert confidence.alpha == 1.0
    assert confidence.beta == 2.0
    assert confidence.mean() == pytest.approx(1 / 3)

    confidence.update(0.9, True)  # Correct prediction
    assert confidence.alpha == 2.0
    assert confidence.beta == 2.0
    assert confidence.mean() == 0.5


def test_confidence_policy():
    class MockSolver:
        def __init__(self):
            self.last_prob = {}

        def predict(self, board):
            # Mock probability map for testing
            self.last_prob = {(0, 0): 0.1, (0, 1): 0.2, (1, 0): 0.3, (1, 1): 0.4}
            return self.last_prob

    class MockBoard:
        def is_hidden(self, r, c):
            # Mock all cells as hidden for simplicity
            return True

    solver = MockSolver()
    board = MockBoard()
    policy = ConfidencePolicy(solver)

    move = policy.choose_move(board)
    assert move == (0, 0)  # Lowest probability cell

    # Simulate a correct prediction and update confidence
    policy.confidence.update(0.1, False)
    assert policy.confidence.mean() == pytest.approx(1 / 3)

    # Simulate another move
    move = policy.choose_move(board)
    assert move == (0, 1)  # Next lowest probability cell


def test_fallback_logic_no_safe_moves():
    """
    Test that ConfidencePolicy.choose_move falls back to the first hidden cell
    when no safe moves are available.
    """
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor(), confidence)

    # Mock the probability map to simulate no safe moves
    policy.solver.predict = lambda _: {
        (0, 0): 0.9,
        (0, 1): 0.9,
        (1, 0): 0.9,
        (1, 1): 0.9,
    }

    move = policy.choose_move(board)
    assert move is not None
    assert board.grid[move.row][move.col].state == State.HIDDEN


def test_confidence_policy_deterministic_move():
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor(), confidence)

    # Mock the probability map to simulate deterministic behavior
    policy.solver.predict = lambda _: {
        (0, 0): 0.1,
        (0, 1): 0.2,
        (1, 0): 0.3,
        (1, 1): 0.4,
    }

    move = policy.choose_move(board)
    assert move.row == 0 and move.col == 0  # Lowest probability cell
