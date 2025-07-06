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

    @staticmethod
    def from_token(token: Union[str, "Cell"]) -> "Cell":
        if isinstance(token, Cell):
            return token
        token = str(token).strip().upper()
        if token in ["HIDDEN", "."]:
            return Cell(state=State.HIDDEN)
        elif token in ["MINE", "*", "FALSE"] or token.startswith("EKA"):
            return Cell(is_mine=True)
        elif token.isdigit() and int(token) > 100:
            return Cell(is_mine=True)
        return Cell()

    def __repr__(self):
        return f"Cell(state={self.state}, is_mine={self.is_mine}, row={self.row}, col={self.col}, clue={self.clue})"
