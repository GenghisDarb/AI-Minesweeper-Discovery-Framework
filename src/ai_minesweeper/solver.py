class ConstraintSolver:
        def solve(self, board):
        click_engine = ClickEngine(board)
        for _ in range(10):
            r, c = click_engine.next_click()
            board.reveal(r, c)

