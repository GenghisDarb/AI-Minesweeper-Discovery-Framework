from enum import Enum
from dataclasses import dataclass
from typing import Union, Optional, List


class State(Enum):
    HIDDEN = "hidden"
    MINE = "mine"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    FALSE = FLAGGED  # Alias for legacy support
    TRUE = REVEALED  # Alias for revealed safe cells

    def __str__(self):
        return self.value


# print(f"[DEBUG] State.HIDDEN id during import: {id(State.HIDDEN)}")
# print(f"[DEBUG] State.HIDDEN id = {id(State.HIDDEN)} in module cell")


@dataclass
class Cell:
    state: State = State.HIDDEN
    description: str = ""  # Human-readable hypothesis description
    evidence: str | None = None  # Optional field for supporting data or source
    adjacent_false_hypotheses: int = 0  # Number of false hypotheses among neighbors
    is_false_hypothesis: bool = False  # Indicates a false hypothesis (contradiction)
    is_mine: bool = False  # Indicates if the cell is a mine
    adjacent_mines: int = 0  # Number of mines among neighbors
    row: int = -1  # Row position of the cell
    col: int = -1  # Column position of the cell
    adjacent_false_hypothesis_weight: float = 0.0  # Weight of adjacent false hypotheses
    clue: int | None = None  # Numeric clue shown to user
    z: int | None = None  # Atomic number
    n: int | None = None  # Neutron number
    confidence: float = 0.0  # Solver's confidence level for this cell
    neighbors: Optional[List["Cell"]] = None  # List of neighboring cells
    symbol: str = ""  # Chemical symbol for periodic table cells
    group: int | None = None  # Group number for periodic table cells
    period: int | None = None  # Period number for periodic table cells

    def __post_init__(self):
        pass
        # print(
        #     f"[DEBUG] Cell initialized with state: {self.state}, State id: {id(self.state)}, Expected State.HIDDEN id: {id(State.HIDDEN)}"
        # )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Cell object.

        :return: A string describing the cell's state, false hypothesis status, position, clue, and confidence.
        """
        return f"Cell(state={self.state}, is_false_hypothesis={self.is_false_hypothesis}, row={self.row}, col={self.col}, clue={self.clue}, confidence={self.confidence:.2f})"

    @staticmethod
    def from_token(token: Union[str, "Cell", None]) -> "Cell":
        """
        Creates a Cell object from a token.

        :param token: A string, Cell object, or None representing the cell's state.
        :return: A Cell object initialized based on the token.
        """
        if isinstance(token, Cell):
            return token
        try:
            token = str(token).strip().upper() if token is not None else ""
        except Exception:
            token = ""

        cell = Cell()
        cell.symbol = token  # Set the symbol attribute for all tokens
        if token in ["HIDDEN", ".", "1"]:
            cell.state = State.HIDDEN
        elif token in ["MINE", "*", "X"]:
            cell.state = State.MINE
        elif token.isdigit() and 0 <= int(token) <= 8:
            cell.state = State.REVEALED
            cell.clue = int(token)
        else:
            cell.confidence = 0.0  # Default confidence level
        return cell

    def __hash__(self):
        """
        Make the Cell class hashable by using its row and column as unique identifiers.
        """
        return hash((self.row, self.col))

    def __eq__(self, other):
        """
        Ensure equality comparison is based on row and column.
        """
        return (
            isinstance(other, Cell) and self.row == other.row and self.col == other.col
        )

    def is_hidden(self) -> bool:
        """Check if the cell is in the hidden state."""
        return self.state and getattr(self.state, "value", None) == State.HIDDEN.value

    def is_flagged(self) -> bool:
        return self.state == State.FLAGGED
