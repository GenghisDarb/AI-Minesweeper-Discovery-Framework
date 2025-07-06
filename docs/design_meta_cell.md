# Meta-Cell Confidence Module

## Overview
The Meta-Cell Confidence Module introduces a feedback loop to dynamically adjust the solver's risk tolerance based on its prediction accuracy. Inspired by TORUS Theory's controller dimension, this module ensures the solver maintains a balanced strategy between exploration and exploitation.

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
