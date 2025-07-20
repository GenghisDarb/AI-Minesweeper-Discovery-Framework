# Meta-Cell Confidence Module

## Overview
The Meta-Cell Confidence Module introduces a feedback loop to dynamically adjust the hypothesis solver's risk tolerance based on its prediction accuracy. Inspired by TORUS Theory's controller dimension, this module ensures the solver maintains a balanced strategy between exploration and exploitation.

## Rationale
The Meta-Cell Confidence Module dynamically adjusts risk tolerance based on solver accuracy. Using a Beta distribution, it tracks success rates and tunes the solver's behavior.

## BetaConfidence Class
Tracks solver confidence using a Beta distribution. Updates confidence based on prediction accuracy using the Brier score.

## ConfidencePolicy Class
Wraps the base solver to adjust move selection based on confidence. Implements a risk threshold that varies with confidence level.

## Visualization
Displays confidence in GUI (Streamlit) or CLI mode, providing real-time feedback on solver calibration.

## Expected Outcomes
Confidence oscillates over time, reflecting the solver's self-correcting mechanism. This aligns with TORUS Theory's \\chi-cycle structure.

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

## Motivation and Theoretical Inspiration

**TORUS Controller Dimension:** In TORUS Theory, when a system evolves through 14 recursive layers (0D through 13D), an exact closure is not achieved without an extra adjustment; there’s a fixed phase gap of 360°/14 in the cycle. TORUS introduces a controller operator $R_{\text{control}}$ to address this, which is applied at the end of the 13D layer to perfectly "stitch" the cycle closed. This operator doesn’t add new physics; it’s a structural, zero-trace transform that compensates the residual error, aligning the end state with the beginning. 

*In our Minesweeper analogy*, after a sequence of moves (an analog of a full recursion cycle), the solver may have accumulated a calibration error — its internal probability estimates might not align with reality. The **BetaConfidence** component plays the role of $R_{\text{control}}$: it updates the solver’s state to account for that error, ensuring the next cycle of moves starts with a corrected perspective. In essence, the meta-cell provides the “twist” that closes the loop of perception and action for the solver, just as $R_{\text{control}}$ provides the final twist to close TORUS’s 14-layer loop.

**Ghost-Loop Bicycle Analogy:** A riderless bicycle can balance itself only within a narrow speed range, a long-puzzling fact explained by a hidden feedback: the spinning front wheel and the geometry form a **toroidal feedback loop** that self-corrects the bike’s lean. TORUS modeling showed that the wheel’s gyroscopic effect and the ground contact act like two coupled tori that resonate and stabilize the bike when conditions are right (closing the loop in a 14-layer toroidal lattice). The “ghost rider” (no human input) stays up because the system itself provides a corrective torque via this closed flux loop. 

*Our meta-cell is analogous to this ghost torque loop.* The solver by itself (like a classical bike model) has no way to adjust if its predictions are systematically off. By adding the meta-cell, we introduce a **feedback torque** in the form of dynamic policy adjustments: when the solver’s confidence drops, the meta-cell pushes it to explore new areas (a corrective action); when confidence is high, it allows the solver to coast with minimal risk. This feedback ensures stability in performance in much the same way the toroidal loop stabilizes the bicycle. It’s an emergent, second-order effect not present in the base solver, but crucial for self-stability.

## Implementation Details

**BetaConfidence – Calibration Tracker:** We maintain a Beta distribution $Beta(\alpha, \beta)$ that represents the solver’s belief about its own accuracy. Initially $(\alpha=1, \beta=1)$ implies no prior bias. After each move:
- If the solver’s prediction for that move was **correct** (e.g., it expected a safe cell and it was safe, or expected a mine and a mine was there), we update $\alpha \leftarrow \alpha + 1$.
- If the prediction was **wrong**, $\beta \leftarrow \beta + 1$.  
This update rule is a simplified Bayesian calibration: essentially treating each move as a Bernoulli trial of the solver’s prediction skill. The Beta mean $m = \frac{\alpha}{\alpha+\beta}$ is the solver’s running accuracy estimate. Notably, if the solver is overconfident (making mistakes because it underestimates uncertainties), $m$ will drop below 0.5, which serves as an internal alert that the inference engine is miscalibrated.

Over many moves, $\alpha$ and $\beta$ grow, and the confidence metric becomes more stable. A well-tuned solver will see $\alpha$ increase faster than $\beta$, pushing $m$ toward 1 (but never reaching it if occasional surprises occur). An erratic solver will have $m$ hover low, prompting persistent exploration.

**ConfidencePolicy – Dynamic Risk Modulation:** The policy uses the BetaConfidence $m$ to set a risk threshold $\tau$. We define a mapping $\tau = 0.25 - 0.20 \cdot m$, which yields $\tau = 0.25$ when $m = 0$ and $\tau = 0.05$ when $m = 1$. (Any monotonic function would do; this linear mapping is simple and covers the specified range 5%–25%.) Before each move, the solver requests a probability for each unopened cell (the chance that cell hides a mine). The ConfidencePolicy then:

1. Calculates the current $\tau$.  
2. Finds all cells with predicted mine probability $p \le \tau$. These are “safe enough” to click given the current confidence.  
3. If there is at least one such cell, it chooses the one with the lowest $p$ (maximally safe). If *no* cell falls below $\tau$ (meaning the solver is very confident but all moves look dangerous, or the solver is forced to guess), the policy defaults to the least risky cell available (the minimum $p$ overall).

This mechanism ensures a couple of behaviors:
- **High Confidence (m near 1):** $\tau$ is very low, so the solver will refuse to click anything that isn’t almost certain to be safe. It will only proceed if it finds an extremely low-probability cell. In practical terms, if the solver is doing well, it becomes very selective, avoiding any move that looks even slightly risky. This greediness maximizes the chance of winning when the solver “believes” it’s on the right track.
- **Low Confidence (m drops):** $\tau$ increases, meaning the solver is willing to click cells that have a higher probability of being mines. This might seem counter-intuitive (why click risky cells?), but it’s a form of **exploration**. A low confidence implies the solver’s model might be wrong or incomplete, so taking a calculated risk can reveal new information and potentially break it out of a situation where it’s stuck or repeatedly wrong. Essentially, the solver becomes curious and experimentally probes the board when it doubts itself.

## References
- TORUS Theory and Bicycle Self-Stability §3, §4
- Unified Glossary – entries "χ-cycle", "Controller Dimension".
