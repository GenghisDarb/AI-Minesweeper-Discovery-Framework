import os
from pathlib import Path

from ai_minesweeper.domain.nuclear_isotopes import NuclearIsotopeAdapter

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "examples"
PERIODIC_PATH = DATA_DIR / "periodic_table" / "elements.csv"


class DomainLoader:
    @staticmethod
    def load(domain_name, csv_path=None):
        """
        Load a domain-specific Minesweeper board.
        :param domain_name: Name of the domain.
        :param csv_path: Path to the CSV file (optional).
        """
        if domain_name == "periodic-table-v2":
            path = os.path.join(DATA_DIR, "periodic_table", "isotopes.csv")
            if not os.path.exists(path):
                raise FileNotFoundError(f"Expected data file not found: {path}")
            adapter = NuclearIsotopeAdapter()
            return adapter.build_board(path)

        raise ValueError(f"Unknown domain: {domain_name}")
