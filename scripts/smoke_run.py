from ai_minesweeper.board_builder import BoardBuilder


def run():
    board = BoardBuilder.random_board(rows=12, cols=12, mines=20)
    # center reveal
    board.reveal((board.n_rows // 2, board.n_cols // 2), flood=True)
    steps = 0
    flagged = 0
    while steps < 200 and board.has_unresolved_cells():
        mv = board.solve_next()
        if mv is None:
            break
        steps += 1
        # count flagged mines
        flagged = sum(1 for row in board.grid for cell in row if cell.is_mine and str(getattr(cell, 'state', '')) == 'State.FLAGGED')
    print({'steps': steps, 'flaggedTrue': flagged})


if __name__ == '__main__':
    run()
