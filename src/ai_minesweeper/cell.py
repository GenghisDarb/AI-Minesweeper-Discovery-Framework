from enum import Enum, auto
from dataclasses import dataclass

class State(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    TRUE = REVEALED        # legacy alias for old tests
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
