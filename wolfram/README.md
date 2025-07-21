# χ-Phase AI Minesweeper – Wolfram Batch Runner

This batch generates recursion-related constants and visuals used in:

- The Streamlit frontend
- The backend solver tuning (τ-mapping, χ-phase tracking)
- The CI evidence badge pipeline

## Included Scripts

- `chi_precision.wls`: log(φ) to 50-digit precision
- `torus_brot_scaling.wls`: fractal field & FFT
- `prime_residue_scan.wls`: mod-14 S-statistic
- `confidence_osc_fit.wls`: fit damped χ oscillation curve
- `run_all.wls`: master batch executor

## Usage

To run locally:

```bash
wolfram -script wolfram/run_all.wls
```

This updates:

- `/data/*.txt, *.json, *.csv`
- `/reports/*.csv`
- `/figures/*.png`
