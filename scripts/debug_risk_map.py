from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor, SpreadRiskAssessor


def print_risk_maps():
    board = BoardBuilder.random_board(rows=2, cols=2, mines=1)
    print("Board:")
    for row in board.grid:
        print([f"({cell.row},{cell.col}) {cell.state.name}" for cell in row])
    ra = RiskAssessor()
    sra = SpreadRiskAssessor()
    risk_map = ra.estimate(board)
    spread_map = sra.get_probabilities(board)
    print("\nRiskAssessor.estimate:")
    for k, v in risk_map.items():
        print(f"  {k}: {v} ({type(v)})")
    print("\nSpreadRiskAssessor.get_probabilities:")
    for k, v in spread_map.items():
        print(f"  {k}: {v} ({type(v)})")

if __name__ == "__main__":
    print_risk_maps()
