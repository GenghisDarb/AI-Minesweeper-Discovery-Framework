# Meta-Cell Guide

Learn how to use the Meta-Cell Confidence Module to enhance solver stability.

## Features
- Adaptive risk tolerance.
- Real-time confidence visualization.

## Usage
Enable the Meta-Cell module in the Streamlit sidebar.

# Meta-Cell Usage

The Meta-Cell Confidence Module dynamically adjusts the hypothesis solver's risk tolerance based on prediction accuracy. This module ensures a balanced strategy between exploration and exploitation.

## CLI Usage
To activate the Meta-Cell Confidence Module in CLI mode, wrap the base solver with `ConfidencePolicy` and use `BetaConfidence` for tracking.

```python
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

confidence = BetaConfidence()
policy = ConfidencePolicy(base_solver=RiskAssessor, confidence=confidence)
move = policy.choose_move(board)
```

## Streamlit Mode
In Streamlit mode, the confidence level is dynamically displayed, including metrics and progress bars, providing real-time feedback on solver calibration.
