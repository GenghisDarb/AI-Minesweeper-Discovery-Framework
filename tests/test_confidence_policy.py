import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.solver import RiskAssessor
from ai_minesweeper.cell import Cell, State


def test_policy_choose_move():
    board = Board(
        grid=[
            [Cell(state=State.HIDDEN), Cell(state=State.HIDDEN)],
            [Cell(state=State.HIDDEN), Cell(is_mine=True)],
        ]
    )
    confidence = BetaConfidence()
    policy = ConfidencePolicy(RiskAssessor, confidence)

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
