class PeriodicTableDomain:
    @staticmethod
    def is_mine(cell):
        return cell.state == State.MINE  # or match on symbol, etc.