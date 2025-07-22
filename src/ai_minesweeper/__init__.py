"""
AI Minesweeper Discovery Framework

A χ-recursive minesweeper AI with TORUS theory integration and meta-cell confidence.
Version 1.1.0
"""

__version__ = "1.1.0"
__author__ = "AI Minesweeper Discovery Framework Team"

from .board import Board
from .constraint_solver import ConstraintSolver
from .board_builder import BoardBuilder
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
from .risk_assessor import RiskAssessor

__all__ = [
    "Board",
    "BoardBuilder",
    "RiskAssessor", 
    "ConstraintSolver",
    "__version__"
]
