from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


def test_solver_move_sequence_deterministic():
    board = BoardBuilder.fixed_board(
        layout=[
            "...",
            "...",
            "...",
        ],
        mines=[(0, 1)],
    )
    solver = ConstraintSolver()
    # Drive a few steps deterministically using choose_move
    seq1 = []
    b1 = board
    for _ in range(5):
        mv = solver.choose_move(b1)
        if mv is None:
            break
        seq1.append(mv)
        # apply without peeking
        r, c = mv
        b1.reveal((r, c), flood=True)

    # Rebuild the same board and repeat
    board2 = BoardBuilder.fixed_board(
        layout=[
            "...",
            "...",
            "...",
        ],
        mines=[(0, 1)],
    )
    solver2 = ConstraintSolver()
    seq2 = []
    b2 = board2
    for _ in range(5):
        mv = solver2.choose_move(b2)
        if mv is None:
            break
        seq2.append(mv)
        r, c = mv
        b2.reveal((r, c), flood=True)

    assert seq1 == seq2
