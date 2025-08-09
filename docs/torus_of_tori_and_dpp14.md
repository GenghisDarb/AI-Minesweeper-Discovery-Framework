# Torus of Tori and DPP‑14

This note summarizes the Torus‑of‑Tori intuition used by the χ‑recursive solver and outlines the DPP‑14 (Deep Parallel Processing, 14 lanes) protocol referenced across the framework. It’s intentionally concise and operational, matching the implementation.

## χ‑cycle and controller dimension

- χ‑cycle: a bounded, cyclical modulation applied to solver confidence and risk thresholds. Every reveal/flag ticks a counter; UI charts show this as a smooth oscillator for intuition and debugging. The solver remains deterministic: no jitter, canonical tie‑breaks, and normalization over hidden cells only.
- Controller dimension: the degrees of freedom the solver can adjust (risk tolerance, constraint ordering, lane interactions). These are tracked, not randomized, to ensure reproducibility in CI and tests.

## Torus‑of‑Tori intuition

Think of each recursion lane as a small torus evolving over time. Cross‑links between lanes form a larger torus‑of‑tori where information propagates without peeking at unrevealed answers. Practically, this translates to:
- Local constraints first (classic Minesweeper logic),
- Deterministic risk scoring for ambiguous regions,
- Confidence‑gated actions that modulate when flags are “safe” vs “certain.”

## DPP‑14 protocol (what it means in code)

1. 14 parallel reasoning lanes. Each lane carries a consistent state view; no lane sees forbidden information.
2. Cross‑lane propagation occurs only through admissible, derived facts (no peeking). If a lane diverges, it’s pruned deterministically.
3. Risk and confidence are aggregated with stable ordering. When ties occur, coordinates are ordered canonically.
4. Every mutation (reveal/flag/unflag) advances the χ‑cycle counter; visualizations reflect the phase but never influence tie‑breaks.

## Determinism and testing

- Tests set AIMS_TEST_MODE=1 to allow deterministic shortcuts where appropriate. Production code remains pure and identical across runs.
- CI verifies: lint, security (non‑blocking), and full test suite. A smoke script demonstrates a short, reproducible run with stable move ordering.

## Extending the model

- Additional lanes: keep cross‑lane communication admissible and auditably deterministic.
- New risk terms: ensure they normalize over hidden cells and use stable sorts.
- UI: you may visualize χ‑phase and lane status, but do not couple visuals to decision ordering.

For a narrative motivation and broader context, see Why TORUS Matters and the χ‑brot demo. These show how cyclical modulation can make complex discovery tasks legible without sacrificing reproducibility.
