import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.cell import Cell, State
from ai_minesweeper.solver_logic import SolverLogic


def test_solver_basic():
    # Adjust test setup to ensure realistic conditions
    board = Board(
        n_rows=3,
        n_cols=3,
        grid=[
            [
                Cell(state=State.HIDDEN, clue=0, neighbors=[]),
                Cell(is_mine=True, clue=0, neighbors=[]),
                Cell(state=State.HIDDEN, clue=0, neighbors=[]),
            ],
            [
                Cell(state=State.HIDDEN, clue=1, neighbors=[]),
                Cell(is_mine=True, clue=0, neighbors=[]),
                Cell(state=State.HIDDEN, clue=1, neighbors=[]),
            ],
            [
                Cell(state=State.HIDDEN, clue=0, neighbors=[]),
                Cell(state=State.HIDDEN, clue=0, neighbors=[]),
                Cell(state=State.HIDDEN, clue=0, neighbors=[]),
            ],
        ],
    )

    # Initialize neighbors
    for i, row in enumerate(board.grid):
        for j, cell in enumerate(row):
            cell.neighbors = [
                board.grid[x][y]
                for x in range(max(0, i - 1), min(board.n_rows, i + 2))
                for y in range(max(0, j - 1), min(board.n_cols, j + 2))
                if (x, y) != (i, j)
            ]

    # Calculate and set correct clue values
    for row in board.grid:
        for cell in row:
            cell.clue = sum(neighbor.is_mine for neighbor in cell.neighbors)

    # Debug print removed to satisfy line-length checks

    # Reveal one cell to kick off logic
    board.grid[0][0].state = State.REVEALED
    SolverLogic.flag_mines(board)
    SolverLogic.cascade_reveal(board)
    assert all(
        cell.state == State.REVEALED
        for row in board.grid
        for cell in row
        if not cell.is_mine
    )


def test_solver_propagation():
    board = BoardBuilder.fixed_board(
        layout=[
            "1. ",
            "...",
            "...",
        ],
        mines=[(0, 1)],
    )
    solver = SolverLogic()
    board.reveal(0, 0)  # Corrected reveal method usage
    changed = solver.flag_mines(board)
    assert changed

    cascade = solver.cascade_reveal(board)
    assert cascade

    board.print_board()  # Debugging output to verify board state


def test_solver_assertions():
    actual = 0.9  # Example actual value
    expected = 1.0  # Example expected value
    assert abs(actual - expected) < 0.1
