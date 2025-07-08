from enum import Enum, auto
from dataclasses import dataclass
from typing import Union


class State(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    TRUE = REVEALED  # legacy alias for old tests
    FLAGGED = auto()


@dataclass
class Cell:
    state: State = State.HIDDEN
    description: str = ""  # Human-readable hypothesis description
    evidence: str | None = None  # Optional field for supporting data or source
    adjacent_mines: int = 0  # Number of false hypotheses among neighbors
    is_mine: bool = False  # Indicates a false hypothesis (mine/contradiction)
    row: int = -1  # Row position of the cell
    col: int = -1  # Column position of the cell
    adjacent_mine_weight: float = 0.0  # Weight of adjacent mines
    clue: int | None = None  # Numeric clue shown to user
    z: int | None = None  # Atomic number
    n: int | None = None  # Neutron number
    confidence: float = 0.0  # Solver's confidence level for this cell
    neighbors: list["Cell"] = None  # List of neighboring cells
    symbol: str = ""  # Chemical symbol for periodic table cells
    group: int | None = None  # Group number for periodic table cells
    period: int | None = None  # Period number for periodic table cells

    def __repr__(self) -> str:
        """
        Returns a string representation of the Cell object.

        :return: A string describing the cell's state, mine status, position, clue, and confidence.
        """
        return f"Cell(state={self.state}, is_mine={self.is_mine}, row={self.row}, col={self.col}, clue={self.clue}, confidence={self.confidence:.2f})"

    @staticmethod
    def from_token(token: Union[str, "Cell"]) -> "Cell":
        """
        Creates a Cell object from a token.

        :param token: A string or Cell object representing the cell's state.
        :return: A Cell object initialized based on the token.
        """
        if isinstance(token, Cell):
            return token
        token = str(token).strip().upper()
        if token in ["HIDDEN", "."]:
            return Cell(state=State.HIDDEN)
        elif token in ["MINE", "*", "FALSE"] or token.startswith("EKA"):
            return Cell(is_mine=True)
        elif token.isdigit() and int(token) > 100:
            return Cell(is_mine=True)
        cell = Cell()
        cell.confidence = 0.0  # Default confidence level
        return cell
