"""
Meta-cell confidence module for χ-recursive decision making.

This package adds a controller-layer feedback loop to the Minesweeper AI, enabling
the solver to self-calibrate its confidence. Inspired by TORUS Theory’s recursion
closure and the “ghost rider” bicycle effect, the module introduces a meta-cell that
tracks prediction accuracy and adjusts the solver's risk policy dynamically.
"""

from .policy_wrapper import ConfidencePolicy
from .beta_confidence import BetaConfidence

__all__ = ["ConfidencePolicy", "BetaConfidence"]
