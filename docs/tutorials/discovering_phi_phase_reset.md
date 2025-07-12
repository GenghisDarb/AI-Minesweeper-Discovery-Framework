# Discovering φ-Phase Reset

This tutorial explains how to use the Phase-Lock Minesweeper module to detect φ-phase resets in time-series data.

## Steps

1. Configure the sampling rate and target frequency in `phase_lock_phi_config.yaml`.
2. Use the `evaluate_cell` function to extract 14-cycle segments.
3. Apply the Hilbert transform and compute Δφ.
4. Run the Rayleigh test to check for resets.

## Example

Refer to the notebook `PhaseLockMinesweeper.ipynb` for a demonstration.
