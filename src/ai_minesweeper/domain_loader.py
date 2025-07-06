from ai_minesweeper.domain.nuclear_isotopes import NuclearIsotopeAdapter

class DomainLoader:
    @staticmethod
    def load(domain_name, csv_path=None):
        """
        Load a domain-specific Minesweeper board.
        :param domain_name: Name of the domain.
        :param csv_path: Path to the CSV file (optional).
        """
        if domain_name == "periodic-table-v2":
            adapter = NuclearIsotopeAdapter()
            return adapter.build_board(csv_path)

        raise ValueError(f"Unknown domain: {domain_name}")
