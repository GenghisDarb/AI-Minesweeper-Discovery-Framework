# Meta-Cell Confidence Module

## Overview
The Meta-Cell Confidence Module introduces a feedback loop to dynamically adjust the solver's risk tolerance based on its prediction accuracy. Inspired by TORUS Theory's controller dimension, this module ensures the solver maintains a balanced strategy between exploration and exploitation.

## Rationale
The Meta-Cell Confidence Module dynamically adjusts risk tolerance based on solver accuracy. Using a Beta distribution, it tracks success rates and tunes the solver's behavior.

## BetaConfidence Class
Tracks solver confidence using a Beta distribution. Updates confidence based on prediction accuracy using the Brier score.

## ConfidencePolicy Class
Wraps the base solver to adjust move selection based on confidence. Implements a risk threshold that varies with confidence level.

## Visualization
Displays confidence in GUI (Streamlit) or CLI mode, providing real-time feedback on solver calibration.

## Expected Outcomes
Confidence oscillates over time, reflecting the solver's self-correcting mechanism. This aligns with TORUS Theory's χ-cycle structure.

## Usage
To enable the confidence module, wrap the base solver with ConfidencePolicy and use BetaConfidence for tracking.

Wrap your solver with `ConfidencePolicy`:
```python
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

confidence = BetaConfidence()
policy = ConfidencePolicy(base_solver=RiskAssessor, confidence=confidence)
move = policy.choose_move(board)
```

See the `confidence_oscillation_demo.ipynb` notebook for a practical demonstration.

# Meta-Cell Confidence Design

## Overview
The meta-cell confidence module tracks the accuracy of mine-probability predictions and adjusts the solver's risk threshold dynamically. This is inspired by the TORUS "controller dimension" concept, which harmonizes observer-state interactions.

## Key Concepts
- **Beta Confidence**: A Beta distribution is used to model prediction confidence.
- **Confidence Policy**: Modulates exploration vs. exploitation based on confidence.
- **χ-Cycle**: The confidence oscillation period aligns with the χ-cycle (~14 moves).

## References
- TORUS Theory and Bicycle Self-Stability §3, §4
- Unified Glossary – entries "χ-cycle", "Controller Dimension".
