"""
AI Minesweeper Discovery Framework

A χ-recursive minesweeper AI with TORUS theory integration and meta-cell confidence.
Version 1.1.0
"""

__version__ = "1.1.0"
__author__ = "AI Minesweeper Discovery Framework Team"

from .board import Board
from .risk_assessor import RiskAssessor
from .constraint_solver import ConstraintSolver

__all__ = [
    "Board",
    "RiskAssessor", 
    "ConstraintSolver",
    "__version__"
]