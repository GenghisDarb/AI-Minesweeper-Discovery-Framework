from ai_minesweeper.board import State


class PeriodicTableDomain:
    @staticmethod
    def is_mine(cell):
        return cell.state == State.MINE