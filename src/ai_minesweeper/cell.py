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
    is_mine: bool = False
    adjacent_mines: int = 0
