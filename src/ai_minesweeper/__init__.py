"""
AI Minesweeper Discovery Framework

A χ-recursive minesweeper AI with TORUS theory integration and meta-cell confidence.
Version 1.1.0
"""

__version__ = "1.1.0"
__author__ = "AI Minesweeper Discovery Framework Team"

from .board import Board, CellState
from .constraint_solver import ConstraintSolver
from .board_builder import BoardBuilder
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
from .meta_cell_confidence.beta_confidence import BetaConfidence
from .meta_cell_confidence.confidence import BetaConfidence as LegacyBetaConfidence
from .risk_assessor import RiskAssessor

# Optionally include SpreadRiskAssessor if present
try:
    from .risk_assessor import SpreadRiskAssessor
except ImportError:
    SpreadRiskAssessor = None

__all__ = [
    "Board",
    "BoardBuilder",
    "RiskAssessor",
    "ConstraintSolver",
    "ConfidencePolicy",
    "BetaConfidence",
    "LegacyBetaConfidence",
    "__version__",
    "CellState"
]
# Add SpreadRiskAssessor if available
if SpreadRiskAssessor:
    __all__.append("SpreadRiskAssessor")
