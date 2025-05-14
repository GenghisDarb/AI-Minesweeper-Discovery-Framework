from pathlib import Path
from .board import Board


class BoardBuilder:
    """Factory for Board objects."""

    @staticmethod
    def from_csv(path: str | Path) -> Board:
        """Return a Board parsed from a CSV of `*` (mine) and `.` (empty).

        Placeholder: not implemented yet.
        """
        raise NotImplementedError
