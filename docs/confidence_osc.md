# Confidence Oscillation

Confidence oscillation relates BetaConfidence dynamics to the χ-cycle and the controller dimension. Oscillations around χ=1/√2 reflect calibration dynamics.

## Overview
The BetaConfidence component tracks solver calibration, ensuring dynamic risk modulation. Confidence oscillations align with the χ-cycle, demonstrating periodic adjustments in solver behavior.

## Visualization
Confidence oscillations are visualized in the Streamlit app, providing real-time feedback on solver calibration.

The chart below demonstrates the τ effect, where τ represents the decay constant of the oscillation, indicating how quickly the confidence stabilizes over time.

![Confidence Fit](figures/confidence_fit.png)

Parameters:
- Amplitude: Initial confidence level.
- Decay rate (τ): Rate at which confidence stabilizes.
- Period: Time between oscillation peaks.

The τ parameter controls how exploratory the confidence policy becomes. Higher τ spreads probability mass and encourages more exploratory selections.

The τ effect is critical for understanding solver calibration and risk tolerance adjustments in dynamic environments.
